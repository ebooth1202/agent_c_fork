"""JSONNavigator - Business logic for navigating and querying JSON files."""

import json
import yaml
from typing import Any, Dict, List, Optional, Union
from jsonpath_ng import parse as jsonpath_parse
from jsonpath_ng.exceptions import JSONPathError


class JSONNavigator:
    """A tool to navigate and query JSON files with depth control."""

    def __init__(self, workspace):
        self.workspace = workspace
        self.logger = workspace.logger

    def _load_json_file(self, file_path: str) -> tuple[Optional[Dict], Optional[str]]:
        """
        Load a JSON file from the workspace.

        Args:
            file_path: Path to the JSON file relative to workspace root

        Returns:
            Tuple of (data, error_message). If successful, data is populated and error is None.
        """
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

    def _get_type_info(self, value: Any) -> str:
        """Get a human-readable type description for a value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return f"array[{len(value)}]"
        elif isinstance(value, dict):
            return f"object[{len(value)} keys]"
        else:
            return type(value).__name__

    def _get_structure_info(
        self,
        data: Any,
        current_path: str,
        current_depth: int,
        max_depth: int,
        sample_count: int
    ) -> Dict[str, Any]:
        """
        Recursively extract structure information from JSON data.

        Args:
            data: Current data node
            current_path: JSONPath to current node
            current_depth: Current depth level
            max_depth: Maximum depth to traverse
            sample_count: Number of samples to collect at each level

        Returns:
            Dictionary containing structure information
        """
        structure = {
            'path': current_path,
            'type': self._get_type_info(data),
            'depth': current_depth
        }

        # Stop if we've reached max depth
        if current_depth >= max_depth:
            return structure

        if isinstance(data, dict):
            structure['keys'] = list(data.keys())
            structure['key_count'] = len(data.keys())
            structure['children'] = {}

            # Sample some child structures
            for i, (key, value) in enumerate(data.items()):
                if i >= sample_count:
                    break
                child_path = f"{current_path}.{key}" if current_path else f"$.{key}"
                structure['children'][key] = self._get_structure_info(
                    value, child_path, current_depth + 1, max_depth, sample_count
                )

        elif isinstance(data, list):
            structure['length'] = len(data)
            structure['children'] = []

            # Sample some array elements
            for i in range(min(sample_count, len(data))):
                child_path = f"{current_path}[{i}]"
                structure['children'].append(self._get_structure_info(
                    data[i], child_path, current_depth + 1, max_depth, sample_count
                ))

        return structure

    async def get_structure(
        self,
        file_path: str,
        max_depth: int = 3,
        sample_count: int = 5
    ) -> str:
        """
        Get a structural overview of the JSON file.

        Args:
            file_path: Path to the JSON file relative to workspace root
            max_depth: Maximum depth to traverse in the JSON structure
            sample_count: Number of sample elements to include at each level

        Returns:
            JSON string with structure information
        """
        data, error = self._load_json_file(file_path)
        if error:
            return json.dumps({'error': error})

        try:
            structure = self._get_structure_info(data, '$', 0, max_depth, sample_count)

            return json.dumps({
                'success': True,
                'structure': structure
            }, indent=2)

        except Exception as e:
            error_msg = f'Error analyzing JSON structure: {str(e)}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})

    async def jsonpath_query(
        self,
        file_path: str,
        jsonpath: str,
        limit: int = 10
    ) -> str:
        """
        Execute a JSONPath query on the JSON file.

        Args:
            file_path: Path to the JSON file relative to workspace root
            jsonpath: JSONPath query to execute
            limit: Maximum number of results to return

        Returns:
            JSON string with query results
        """
        data, error = self._load_json_file(file_path)
        if error:
            return json.dumps({'error': error})

        try:
            # Parse and execute the JSONPath query
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(data)

            # Limit results
            matches = matches[:limit]

            # Extract values from matches
            results = [match.value for match in matches]

            # Convert results to YAML for better readability
            results_yaml = yaml.dump(results, default_flow_style=False, sort_keys=False, allow_unicode=True)

            response = {
                'success': True,
                'query': jsonpath,
                'count': len(matches),
                'results_yaml': results_yaml
            }

            return json.dumps(response, indent=2)

        except JSONPathError as e:
            error_msg = f'Invalid JSONPath expression: {str(e)}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})
        except Exception as e:
            error_msg = f'Error executing JSONPath query: {str(e)}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})

    def _extract_with_depth(
        self,
        data: Any,
        current_depth: int,
        max_depth: Optional[int]
    ) -> Any:
        """
        Extract data with depth limiting.

        Args:
            data: Current data node
            current_depth: Current depth level
            max_depth: Maximum depth to include (None = unlimited)

        Returns:
            Data limited to specified depth
        """
        # If max_depth is None, return everything
        if max_depth is None:
            return data

        # If we've reached the depth limit, return a summary instead of the data
        if current_depth >= max_depth:
            if isinstance(data, dict):
                return f"<object with {len(data)} keys>"
            elif isinstance(data, list):
                return f"<array with {len(data)} items>"
            else:
                return data

        # Recursively process children
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                result[key] = self._extract_with_depth(value, current_depth + 1, max_depth)
            return result
        elif isinstance(data, list):
            return [
                self._extract_with_depth(item, current_depth + 1, max_depth)
                for item in data
            ]
        else:
            return data

    async def extract_subtree(
        self,
        file_path: str,
        jsonpath: str,
        max_depth: Optional[int] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Extract a subtree from the JSON file with depth control.

        Args:
            file_path: Path to the JSON file relative to workspace root
            jsonpath: JSONPath to the root of the subtree to extract
            max_depth: Maximum depth to include (None = unlimited, 0 = just the node, 1 = node + children, etc.)
            output_path: Optional path to save the extracted subtree

        Returns:
            JSON string with the extracted subtree or status message
        """
        data, error = self._load_json_file(file_path)
        if error:
            return json.dumps({'error': error})

        try:
            # Parse and execute the JSONPath query
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(data)

            if not matches:
                return json.dumps({'error': f'No element matches JSONPath: {jsonpath}'})

            # Get the first matching element
            subtree_data = matches[0].value

            # Apply depth limiting
            limited_data = self._extract_with_depth(subtree_data, 0, max_depth)

            # Convert to YAML for better readability
            result_str = yaml.dump(limited_data, default_flow_style=False, sort_keys=False, allow_unicode=True)

            # Write to output file if specified
            if output_path:
                full_output_path = self.workspace.full_path(output_path)
                if not full_output_path:
                    return json.dumps({'error': f'Invalid output path: {output_path}'})

                with open(full_output_path, 'w', encoding='utf-8') as f:
                    f.write(result_str)

                return json.dumps({
                    'success': True,
                    'message': f'Subtree extracted to {output_path} as YAML',
                    'size': len(result_str),
                    'depth_limit': max_depth if max_depth is not None else 'unlimited'
                }, indent=2)
            else:
                # Return the subtree if no output path is specified
                return json.dumps({
                    'success': True,
                    'format': 'yaml',
                    'depth_limit': max_depth if max_depth is not None else 'unlimited',
                    'subtree': result_str
                }, indent=2)

        except JSONPathError as e:
            error_msg = f'Invalid JSONPath expression: {str(e)}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})
        except Exception as e:
            error_msg = f'Error extracting subtree: {str(e)}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})

    async def get_value(
        self,
        file_path: str,
        jsonpath: str
    ) -> str:
        """
        Get a simple value at a specific JSONPath.

        Args:
            file_path: Path to the JSON file relative to workspace root
            jsonpath: JSONPath to the value

        Returns:
            JSON string with the value
        """
        data, error = self._load_json_file(file_path)
        if error:
            return json.dumps({'error': error})

        try:
            # Parse and execute the JSONPath query
            jsonpath_expr = jsonpath_parse(jsonpath)
            matches = jsonpath_expr.find(data)

            if not matches:
                return json.dumps({'error': f'No value found at JSONPath: {jsonpath}'})

            # Get the first match
            value = matches[0].value

            return json.dumps({
                'success': True,
                'path': jsonpath,
                'value': value,
                'type': self._get_type_info(value)
            }, indent=2)

        except JSONPathError as e:
            error_msg = f'Invalid JSONPath expression: {str(e)}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})
        except Exception as e:
            error_msg = f'Error getting value: {str(e)}'
            self.logger.error(error_msg)
            return json.dumps({'error': error_msg})
