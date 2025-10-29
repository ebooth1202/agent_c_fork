"""JSONEditor - Business logic for editing JSON files with preview and backup capabilities."""

import yaml
import shutil
import json
import copy
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from jsonpath_ng import parse as jsonpath_parse
from jsonpath_ng.exceptions import JSONPathError


class JSONEditor:
    """A tool to modify JSON files with preview, backup, and validation capabilities."""

    def __init__(self, workspace):
        self.workspace = workspace
        self.logger = workspace.logger

    def _create_result(self, success: bool, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Create a standardized result dictionary for YAML serialization.

        Args:
            success: Whether the operation succeeded
            operation: Name of the operation performed
            **kwargs: Additional result data

        Returns:
            Standardized result dictionary
        """
        result = {
            'success': success,
            'operation': operation,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        result.update(kwargs)
        return result

    def _load_json_file(self, file_path: str) -> tuple[Optional[Dict], Optional[str]]:
        """Load a JSON file from the workspace."""
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return None, f'Invalid file path: {file_path}'

            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return data, None

        except json.JSONDecodeError as e:
            error_msg = f'Invalid JSON in file: {str(e)}'
            self.logger.error(error_msg)
            return None, error_msg
        except Exception as e:
            error_msg = f'Error loading JSON file: {str(e)}'
            self.logger.error(error_msg)
            return None, error_msg

    def _save_json_file(self, file_path: str, data: Any) -> Optional[str]:
        """Save data to a JSON file."""
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return f'Invalid file path: {file_path}'

            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return None

        except Exception as e:
            error_msg = f'Error saving JSON file: {str(e)}'
            self.logger.error(error_msg)
            return error_msg

    def _find_parent_and_key(self, data: Any, jsonpath: str) -> tuple[Optional[Any], Optional[Union[str, int]], Optional[str]]:
        """Find the parent container and key/index for a given JSONPath."""
        try:
            # Parse the JSONPath
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(data)

            if not matches:
                return None, None, 'No element found at JSONPath'

            match = matches[0]
            
            # Get the path components to find parent
            # This is a bit tricky - we need to navigate to the parent
            # For now, we'll use a simpler approach: parse the path string
            path_str = str(match.full_path)
            
            # Handle array access like [0]
            if '[' in path_str:
                # Extract parent path and index
                parent_path = path_str[:path_str.rfind('[')]
                index_str = path_str[path_str.rfind('[')+1:path_str.rfind(']')]
                try:
                    index = int(index_str)
                except ValueError:
                    index = index_str  # It's a key, not an index
                
                if parent_path:
                    parent_expr = jsonpath_parse(parent_path)
                    parent_matches = parent_expr.find(data)
                    if parent_matches:
                        return parent_matches[0].value, index, None
                else:
                    # Root is the parent
                    return data, index, None
            
            # Handle object key access like .key
            if '.' in path_str:
                parts = path_str.split('.')
                key = parts[-1]
                if len(parts) > 1:
                    parent_path = '.'.join(parts[:-1])
                    parent_expr = jsonpath_parse(parent_path)
                    parent_matches = parent_expr.find(data)
                    if parent_matches:
                        return parent_matches[0].value, key, None
                else:
                    return data, key, None

            return None, None, 'Unable to determine parent and key'

        except JSONPathError as e:
            return None, None, f'Invalid JSONPath: {str(e)}'
        except Exception as e:
            return None, None, f'Error finding parent: {str(e)}'

    async def create_backup(self, file_path: str) -> str:
        """Create a timestamped backup of a JSON file."""
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'create_backup', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Check if file exists
            path_obj = Path(full_path)
            if not path_obj.exists():
                return yaml.dump(
                    self._create_result(False, 'create_backup', error=f'File not found: {file_path}'),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Create backup with timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_path = path_obj.parent / f"{path_obj.stem}_backup_{timestamp}{path_obj.suffix}"

            shutil.copy2(full_path, backup_path)

            return yaml.dump(
                self._create_result(
                    True,
                    'create_backup',
                    message='Backup created successfully',
                    original_file=file_path,
                    backup_file=str(backup_path),
                    backup_size=backup_path.stat().st_size
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except Exception as e:
            error_msg = f'Error creating backup: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'create_backup', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

    async def validate_json(self, file_path: str) -> str:
        """Validate that a JSON file is valid and well-formed."""
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'validate_json', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Attempt to parse the JSON file
            data, error = self._load_json_file(file_path)
            if error:
                return yaml.dump(
                    self._create_result(
                        False,
                        'validate_json',
                        message='JSON is not valid',
                        error=error
                    ),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Analyze the structure
            def count_items(obj, depth=0, max_depth=5):
                if depth > max_depth:
                    return {'truncated': True}
                
                if isinstance(obj, dict):
                    return {
                        'type': 'object',
                        'key_count': len(obj),
                        'nested': depth > 0
                    }
                elif isinstance(obj, list):
                    return {
                        'type': 'array',
                        'length': len(obj),
                        'nested': depth > 0
                    }
                else:
                    return {'type': type(obj).__name__}

            structure_info = count_items(data)

            return yaml.dump(
                self._create_result(
                    True,
                    'validate_json',
                    message='JSON is valid and well-formed',
                    file_path=file_path,
                    root_type=structure_info.get('type'),
                    details=structure_info
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except Exception as e:
            error_msg = f'Error validating JSON: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'validate_json', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

    async def set_value(
            self,
            file_path: str,
            jsonpath: str,
            value: Any,
            preview: bool = False
    ) -> str:
        """Set or update a value at a specific JSONPath."""
        try:
            data, error = self._load_json_file(file_path)
            if error:
                return yaml.dump(
                    self._create_result(False, 'set_value', error=error),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Make a deep copy for preview or modification
            modified_data = copy.deepcopy(data)

            # Parse JSONPath and find matches
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(modified_data)

            if not matches:
                return yaml.dump(
                    self._create_result(
                        False,
                        'set_value',
                        error=f'No element found at JSONPath: {jsonpath}'
                    ),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            values_set = 0
            old_values = []

            # Update each match
            for match in matches:
                old_value = match.value
                old_values.append({
                    'path': str(match.full_path),
                    'old_value': old_value,
                    'new_value': value
                })

                # Use JSONPath's update method
                jsonpath_expr.update(modified_data, value)
                values_set += 1

            # Save changes if not in preview mode
            if not preview:
                error = self._save_json_file(file_path, modified_data)
                if error:
                    return yaml.dump(
                        self._create_result(False, 'set_value', error=error),
                        default_flow_style=False, sort_keys=False, allow_unicode=True
                    )

            return yaml.dump(
                self._create_result(
                    True,
                    'set_value',
                    message=f'{"Would set" if preview else "Set"} {values_set} value(s)',
                    file_path=file_path,
                    jsonpath=jsonpath,
                    new_value=value,
                    values_set=values_set,
                    preview_mode=preview,
                    changes=old_values if values_set <= 5 else f'{values_set} values changed'
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except JSONPathError as e:
            return yaml.dump(
                self._create_result(False, 'set_value', error=f'Invalid JSONPath: {str(e)}'),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )
        except Exception as e:
            error_msg = f'Error setting value: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'set_value', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

    async def add_to_object(
            self,
            file_path: str,
            jsonpath: str,
            key: str,
            value: Any,
            preview: bool = False
    ) -> str:
        """Add a new key-value pair to an object at the specified JSONPath."""
        try:
            data, error = self._load_json_file(file_path)
            if error:
                return yaml.dump(
                    self._create_result(False, 'add_to_object', error=error),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Make a deep copy
            modified_data = copy.deepcopy(data)

            # Parse JSONPath and find matches
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(modified_data)

            if not matches:
                return yaml.dump(
                    self._create_result(
                        False,
                        'add_to_object',
                        error=f'No element found at JSONPath: {jsonpath}'
                    ),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            keys_added = 0
            additions = []

            for match in matches:
                target = match.value

                if not isinstance(target, dict):
                    continue

                # Check if key already exists
                key_existed = key in target
                old_value = target.get(key) if key_existed else None

                additions.append({
                    'path': str(match.full_path),
                    'key': key,
                    'value': value,
                    'action': 'updated' if key_existed else 'added',
                    'old_value': old_value if key_existed else None
                })

                target[key] = value
                keys_added += 1

            # Save changes if not in preview mode
            if not preview and keys_added > 0:
                error = self._save_json_file(file_path, modified_data)
                if error:
                    return yaml.dump(
                        self._create_result(False, 'add_to_object', error=error),
                        default_flow_style=False, sort_keys=False, allow_unicode=True
                    )

            return yaml.dump(
                self._create_result(
                    True,
                    'add_to_object',
                    message=f'{"Would add" if preview else "Added"} key to {keys_added} object(s)',
                    file_path=file_path,
                    jsonpath=jsonpath,
                    key=key,
                    value=value,
                    keys_added=keys_added,
                    preview_mode=preview,
                    details=additions if keys_added <= 5 else f'{keys_added} objects modified'
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except JSONPathError as e:
            return yaml.dump(
                self._create_result(False, 'add_to_object', error=f'Invalid JSONPath: {str(e)}'),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )
        except Exception as e:
            error_msg = f'Error adding to object: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'add_to_object', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

    async def remove_key(
            self,
            file_path: str,
            jsonpath: str,
            key: str,
            preview: bool = False
    ) -> str:
        """Remove a key from an object at the specified JSONPath."""
        try:
            data, error = self._load_json_file(file_path)
            if error:
                return yaml.dump(
                    self._create_result(False, 'remove_key', error=error),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Make a deep copy
            modified_data = copy.deepcopy(data)

            # Parse JSONPath and find matches
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(modified_data)

            if not matches:
                return yaml.dump(
                    self._create_result(
                        False,
                        'remove_key',
                        error=f'No element found at JSONPath: {jsonpath}'
                    ),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            keys_removed = 0
            removals = []

            for match in matches:
                target = match.value

                if not isinstance(target, dict):
                    continue

                if key in target:
                    old_value = target[key]
                    removals.append({
                        'path': str(match.full_path),
                        'key': key,
                        'old_value': old_value
                    })

                    del target[key]
                    keys_removed += 1

            # Save changes if not in preview mode
            if not preview and keys_removed > 0:
                error = self._save_json_file(file_path, modified_data)
                if error:
                    return yaml.dump(
                        self._create_result(False, 'remove_key', error=error),
                        default_flow_style=False, sort_keys=False, allow_unicode=True
                    )

            return yaml.dump(
                self._create_result(
                    True,
                    'remove_key',
                    message=f'{"Would remove" if preview else "Removed"} key from {keys_removed} object(s)',
                    file_path=file_path,
                    jsonpath=jsonpath,
                    key=key,
                    keys_removed=keys_removed,
                    preview_mode=preview,
                    details=removals if keys_removed <= 5 else f'{keys_removed} objects modified'
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except JSONPathError as e:
            return yaml.dump(
                self._create_result(False, 'remove_key', error=f'Invalid JSONPath: {str(e)}'),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )
        except Exception as e:
            error_msg = f'Error removing key: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'remove_key', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

    async def append_to_array(
            self,
            file_path: str,
            jsonpath: str,
            value: Any,
            preview: bool = False
    ) -> str:
        """Append a value to an array at the specified JSONPath."""
        try:
            data, error = self._load_json_file(file_path)
            if error:
                return yaml.dump(
                    self._create_result(False, 'append_to_array', error=error),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Make a deep copy
            modified_data = copy.deepcopy(data)

            # Parse JSONPath and find matches
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(modified_data)

            if not matches:
                return yaml.dump(
                    self._create_result(
                        False,
                        'append_to_array',
                        error=f'No element found at JSONPath: {jsonpath}'
                    ),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            items_appended = 0
            appends = []

            for match in matches:
                target = match.value

                if not isinstance(target, list):
                    continue

                old_length = len(target)
                appends.append({
                    'path': str(match.full_path),
                    'value': value,
                    'old_length': old_length,
                    'new_length': old_length + 1
                })

                target.append(value)
                items_appended += 1

            # Save changes if not in preview mode
            if not preview and items_appended > 0:
                error = self._save_json_file(file_path, modified_data)
                if error:
                    return yaml.dump(
                        self._create_result(False, 'append_to_array', error=error),
                        default_flow_style=False, sort_keys=False, allow_unicode=True
                    )

            return yaml.dump(
                self._create_result(
                    True,
                    'append_to_array',
                    message=f'{"Would append" if preview else "Appended"} to {items_appended} array(s)',
                    file_path=file_path,
                    jsonpath=jsonpath,
                    value=value,
                    items_appended=items_appended,
                    preview_mode=preview,
                    details=appends if items_appended <= 5 else f'{items_appended} arrays modified'
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except JSONPathError as e:
            return yaml.dump(
                self._create_result(False, 'append_to_array', error=f'Invalid JSONPath: {str(e)}'),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )
        except Exception as e:
            error_msg = f'Error appending to array: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'append_to_array', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

    async def insert_into_array(
            self,
            file_path: str,
            jsonpath: str,
            index: int,
            value: Any,
            preview: bool = False
    ) -> str:
        """Insert a value at a specific index in an array at the specified JSONPath."""
        try:
            data, error = self._load_json_file(file_path)
            if error:
                return yaml.dump(
                    self._create_result(False, 'insert_into_array', error=error),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Make a deep copy
            modified_data = copy.deepcopy(data)

            # Parse JSONPath and find matches
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(modified_data)

            if not matches:
                return yaml.dump(
                    self._create_result(
                        False,
                        'insert_into_array',
                        error=f'No element found at JSONPath: {jsonpath}'
                    ),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            items_inserted = 0
            inserts = []

            for match in matches:
                target = match.value

                if not isinstance(target, list):
                    continue

                # Handle negative indices
                actual_index = index if index >= 0 else len(target) + index + 1
                
                if actual_index < 0 or actual_index > len(target):
                    continue

                old_length = len(target)
                inserts.append({
                    'path': str(match.full_path),
                    'index': index,
                    'value': value,
                    'old_length': old_length,
                    'new_length': old_length + 1
                })

                target.insert(actual_index, value)
                items_inserted += 1

            # Save changes if not in preview mode
            if not preview and items_inserted > 0:
                error = self._save_json_file(file_path, modified_data)
                if error:
                    return yaml.dump(
                        self._create_result(False, 'insert_into_array', error=error),
                        default_flow_style=False, sort_keys=False, allow_unicode=True
                    )

            return yaml.dump(
                self._create_result(
                    True,
                    'insert_into_array',
                    message=f'{"Would insert" if preview else "Inserted"} into {items_inserted} array(s)',
                    file_path=file_path,
                    jsonpath=jsonpath,
                    index=index,
                    value=value,
                    items_inserted=items_inserted,
                    preview_mode=preview,
                    details=inserts if items_inserted <= 5 else f'{items_inserted} arrays modified'
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except JSONPathError as e:
            return yaml.dump(
                self._create_result(False, 'insert_into_array', error=f'Invalid JSONPath: {str(e)}'),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )
        except Exception as e:
            error_msg = f'Error inserting into array: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'insert_into_array', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

    async def remove_from_array(
            self,
            file_path: str,
            jsonpath: str,
            index: int,
            preview: bool = False
    ) -> str:
        """Remove an item at a specific index from an array at the specified JSONPath."""
        try:
            data, error = self._load_json_file(file_path)
            if error:
                return yaml.dump(
                    self._create_result(False, 'remove_from_array', error=error),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            # Make a deep copy
            modified_data = copy.deepcopy(data)

            # Parse JSONPath and find matches
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(modified_data)

            if not matches:
                return yaml.dump(
                    self._create_result(
                        False,
                        'remove_from_array',
                        error=f'No element found at JSONPath: {jsonpath}'
                    ),
                    default_flow_style=False, sort_keys=False, allow_unicode=True
                )

            items_removed = 0
            removals = []

            for match in matches:
                target = match.value

                if not isinstance(target, list):
                    continue

                # Handle negative indices
                actual_index = index if index >= 0 else len(target) + index
                
                if actual_index < 0 or actual_index >= len(target):
                    continue

                old_value = target[actual_index]
                old_length = len(target)
                removals.append({
                    'path': str(match.full_path),
                    'index': index,
                    'old_value': old_value,
                    'old_length': old_length,
                    'new_length': old_length - 1
                })

                del target[actual_index]
                items_removed += 1

            # Save changes if not in preview mode
            if not preview and items_removed > 0:
                error = self._save_json_file(file_path, modified_data)
                if error:
                    return yaml.dump(
                        self._create_result(False, 'remove_from_array', error=error),
                        default_flow_style=False, sort_keys=False, allow_unicode=True
                    )

            return yaml.dump(
                self._create_result(
                    True,
                    'remove_from_array',
                    message=f'{"Would remove" if preview else "Removed"} from {items_removed} array(s)',
                    file_path=file_path,
                    jsonpath=jsonpath,
                    index=index,
                    items_removed=items_removed,
                    preview_mode=preview,
                    details=removals if items_removed <= 5 else f'{items_removed} arrays modified'
                ),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )

        except JSONPathError as e:
            return yaml.dump(
                self._create_result(False, 'remove_from_array', error=f'Invalid JSONPath: {str(e)}'),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )
        except Exception as e:
            error_msg = f'Error removing from array: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'remove_from_array', error=error_msg),
                default_flow_style=False, sort_keys=False, allow_unicode=True
            )
        