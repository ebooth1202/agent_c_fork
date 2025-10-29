import yaml
import shutil
from lxml import etree
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime


class XMLEditor:
    """A tool to modify XML files with preview, backup, and validation capabilities"""

    def __init__(self, workspace):
        self.workspace = workspace
        self.logger = workspace.logger
        self._preview_mode = False
        self._changes_log = []

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

    def _log_change(self, change_type: str, xpath: str, details: Dict[str, Any]):
        """Log a change for preview/rollback purposes"""
        self._changes_log.append({
            'type': change_type,
            'xpath': xpath,
            'details': details,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })

    async def create_backup(self, file_path: str) -> str:
        """
        Create a backup of the XML file before making modifications.

        Args:
            file_path: Path to the XML file relative to workspace root

        Returns:
            YAML string with backup information
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'create_backup', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Check if file exists
            path_obj = Path(full_path)
            if not path_obj.exists():
                return yaml.dump(
                    self._create_result(False, 'create_backup', error=f'File not found: {file_path}'),
                    default_flow_style=False, sort_keys=False
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
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error creating backup: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'create_backup', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def validate_xml(self, file_path: str) -> str:
        """
        Validate that an XML file is well-formed.

        Args:
            file_path: Path to the XML file relative to workspace root

        Returns:
            YAML string with validation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'validate_xml', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Attempt to parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Count elements and attributes
            element_count = len(list(root.iter()))
            attr_count = sum(len(elem.attrib) for elem in root.iter())

            return yaml.dump(
                self._create_result(
                    True,
                    'validate_xml',
                    message='XML is well-formed and valid',
                    file_path=file_path,
                    root_tag=root.tag,
                    element_count=element_count,
                    attribute_count=attr_count,
                    has_namespaces=len(root.nsmap) > 0,
                    namespaces=dict(root.nsmap) if root.nsmap else None
                ),
                default_flow_style=False, sort_keys=False
            )

        except etree.XMLSyntaxError as e:
            return yaml.dump(
                self._create_result(
                    False,
                    'validate_xml',
                    message='XML is not well-formed',
                    error=str(e),
                    line=e.lineno if hasattr(e, 'lineno') else None
                ),
                default_flow_style=False, sort_keys=False
            )
        except Exception as e:
            error_msg = f'Error validating XML: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'validate_xml', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def add_element(
            self,
            file_path: str,
            parent_xpath: str,
            element_name: str,
            attributes: Optional[Dict[str, str]] = None,
            text: Optional[str] = None,
            namespace: Optional[str] = None,
            preview: bool = False
    ) -> str:
        """
        Add a new element to the XML file.

        Args:
            file_path: Path to the XML file relative to workspace root
            parent_xpath: XPath to the parent element where new element will be added
            element_name: Name/tag of the new element
            attributes: Optional dictionary of attributes for the new element
            text: Optional text content for the new element
            namespace: Optional namespace URI for the new element
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'add_element', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find parent element(s)
            parents = root.xpath(parent_xpath)

            if not parents:
                return yaml.dump(
                    self._create_result(
                        False,
                        'add_element',
                        error=f'No parent element found matching XPath: {parent_xpath}'
                    ),
                    default_flow_style=False, sort_keys=False
                )

            elements_added = 0
            parent_details = []

            for parent in parents:
                if not isinstance(parent, etree._Element):
                    continue

                # Create new element with optional namespace
                if namespace:
                    new_element = etree.Element(f"{{{namespace}}}{element_name}")
                else:
                    new_element = etree.Element(element_name)

                # Add attributes if provided
                if attributes:
                    for key, value in attributes.items():
                        new_element.set(key, str(value))

                # Add text content if provided
                if text:
                    new_element.text = text

                if not preview:
                    parent.append(new_element)

                elements_added += 1
                parent_details.append({
                    'parent_tag': parent.tag,
                    'parent_path': tree.getpath(parent),
                    'new_element': element_name
                })

            # Save changes if not in preview mode
            if not preview and elements_added > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            result = self._create_result(
                True,
                'add_element',
                message=f'{"Would add" if preview else "Added"} {elements_added} element(s)',
                file_path=file_path,
                parent_xpath=parent_xpath,
                element_name=element_name,
                elements_added=elements_added,
                preview_mode=preview,
                details=parent_details if elements_added <= 5 else f'{elements_added} parents affected'
            )

            if attributes:
                result['attributes'] = attributes
            if text:
                result['text_content'] = text
            if namespace:
                result['namespace'] = namespace

            return yaml.dump(result, default_flow_style=False, sort_keys=False)

        except Exception as e:
            error_msg = f'Error adding element: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'add_element', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def remove_element(self, file_path: str, xpath: str, preview: bool = False) -> str:
        """
        Remove element(s) from the XML file.

        Args:
            file_path: Path to the XML file relative to workspace root
            xpath: XPath to the element(s) to remove
            preview: If True, show what would be removed without actually removing

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'remove_element', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find elements to remove
            elements = root.xpath(xpath)

            if not elements:
                return yaml.dump(
                    self._create_result(
                        False,
                        'remove_element',
                        message='No elements found matching XPath',
                        xpath=xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            elements_removed = 0
            removed_details = []

            for elem in elements:
                if not isinstance(elem, etree._Element):
                    continue

                parent = elem.getparent()
                if parent is not None:
                    removed_details.append({
                        'tag': elem.tag,
                        'path': tree.getpath(elem),
                        'attributes': dict(elem.attrib) if elem.attrib else None,
                        'had_children': len(elem) > 0
                    })

                    if not preview:
                        parent.remove(elem)

                    elements_removed += 1

            # Save changes if not in preview mode
            if not preview and elements_removed > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            return yaml.dump(
                self._create_result(
                    True,
                    'remove_element',
                    message=f'{"Would remove" if preview else "Removed"} {elements_removed} element(s)',
                    file_path=file_path,
                    xpath=xpath,
                    elements_removed=elements_removed,
                    preview_mode=preview,
                    details=removed_details if elements_removed <= 5 else f'{elements_removed} elements affected'
                ),
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error removing element: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'remove_element', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def replace_element(
            self,
            file_path: str,
            xpath: str,
            new_element_name: str,
            attributes: Optional[Dict[str, str]] = None,
            text: Optional[str] = None,
            preserve_children: bool = True,
            namespace: Optional[str] = None,
            preview: bool = False
    ) -> str:
        """
        Replace existing element(s) with new element(s).

        Args:
            file_path: Path to the XML file relative to workspace root
            xpath: XPath to the element(s) to replace
            new_element_name: Name/tag of the replacement element
            attributes: Optional dictionary of attributes for the new element
            text: Optional text content for the new element
            preserve_children: If True, copy children from old element to new element
            namespace: Optional namespace URI for the new element
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'replace_element', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find elements to replace
            elements = root.xpath(xpath)

            if not elements:
                return yaml.dump(
                    self._create_result(
                        False,
                        'replace_element',
                        message='No elements found matching XPath',
                        xpath=xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            elements_replaced = 0
            replacement_details = []

            for elem in elements:
                if not isinstance(elem, etree._Element):
                    continue

                parent = elem.getparent()
                if parent is None:
                    continue

                # Create new element with optional namespace
                if namespace:
                    new_elem = etree.Element(f"{{{namespace}}}{new_element_name}")
                else:
                    new_elem = etree.Element(new_element_name)

                # Add attributes if provided
                if attributes:
                    for key, value in attributes.items():
                        new_elem.set(key, str(value))

                # Add text content if provided
                if text:
                    new_elem.text = text

                # Preserve children if requested
                if preserve_children:
                    for child in elem:
                        new_elem.append(child)

                replacement_details.append({
                    'old_tag': elem.tag,
                    'new_tag': new_element_name,
                    'path': tree.getpath(elem),
                    'children_preserved': preserve_children and len(elem) > 0,
                    'child_count': len(elem) if preserve_children else 0
                })

                if not preview:
                    # Replace element
                    parent.replace(elem, new_elem)

                elements_replaced += 1

            # Save changes if not in preview mode
            if not preview and elements_replaced > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            result = self._create_result(
                True,
                'replace_element',
                message=f'{"Would replace" if preview else "Replaced"} {elements_replaced} element(s)',
                file_path=file_path,
                xpath=xpath,
                new_element_name=new_element_name,
                elements_replaced=elements_replaced,
                preview_mode=preview,
                preserve_children=preserve_children,
                details=replacement_details if elements_replaced <= 5 else f'{elements_replaced} elements affected'
            )

            if attributes:
                result['attributes'] = attributes
            if text:
                result['text_content'] = text
            if namespace:
                result['namespace'] = namespace

            return yaml.dump(result, default_flow_style=False, sort_keys=False)

        except Exception as e:
            error_msg = f'Error replacing element: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'replace_element', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def insert_at_position(
            self,
            file_path: str,
            reference_xpath: str,
            element_name: str,
            position: str = 'after',
            attributes: Optional[Dict[str, str]] = None,
            text: Optional[str] = None,
            namespace: Optional[str] = None,
            preview: bool = False
    ) -> str:
        """
        Insert a new element before or after a reference element.

        Args:
            file_path: Path to the XML file relative to workspace root
            reference_xpath: XPath to the reference element
            element_name: Name/tag of the new element
            position: Where to insert - 'before' or 'after' (default: 'after')
            attributes: Optional dictionary of attributes for the new element
            text: Optional text content for the new element
            namespace: Optional namespace URI for the new element
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'insert_at_position', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            if position not in ['before', 'after']:
                return yaml.dump(
                    self._create_result(
                        False,
                        'insert_at_position',
                        error=f'Invalid position: {position}. Must be "before" or "after"'
                    ),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find reference element(s)
            references = root.xpath(reference_xpath)

            if not references:
                return yaml.dump(
                    self._create_result(
                        False,
                        'insert_at_position',
                        message='No reference element found matching XPath',
                        xpath=reference_xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            elements_inserted = 0
            insertion_details = []

            for ref_elem in references:
                if not isinstance(ref_elem, etree._Element):
                    continue

                parent = ref_elem.getparent()
                if parent is None:
                    continue

                # Create new element with optional namespace
                if namespace:
                    new_element = etree.Element(f"{{{namespace}}}{element_name}")
                else:
                    new_element = etree.Element(element_name)

                # Add attributes if provided
                if attributes:
                    for key, value in attributes.items():
                        new_element.set(key, str(value))

                # Add text content if provided
                if text:
                    new_element.text = text

                insertion_details.append({
                    'reference_tag': ref_elem.tag,
                    'reference_path': tree.getpath(ref_elem),
                    'new_element': element_name,
                    'position': position
                })

                if not preview:
                    # Get index of reference element
                    ref_index = list(parent).index(ref_elem)

                    if position == 'after':
                        parent.insert(ref_index + 1, new_element)
                    else:  # before
                        parent.insert(ref_index, new_element)

                elements_inserted += 1

            # Save changes if not in preview mode
            if not preview and elements_inserted > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            result = self._create_result(
                True,
                'insert_at_position',
                message=f'{"Would insert" if preview else "Inserted"} {elements_inserted} element(s) {position} reference',
                file_path=file_path,
                reference_xpath=reference_xpath,
                element_name=element_name,
                position=position,
                elements_inserted=elements_inserted,
                preview_mode=preview,
                details=insertion_details if elements_inserted <= 5 else f'{elements_inserted} insertions made'
            )

            if attributes:
                result['attributes'] = attributes
            if text:
                result['text_content'] = text
            if namespace:
                result['namespace'] = namespace

            return yaml.dump(result, default_flow_style=False, sort_keys=False)

        except Exception as e:
            error_msg = f'Error inserting element: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'insert_at_position', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def set_attribute(
            self,
            file_path: str,
            xpath: str,
            attribute_name: str,
            attribute_value: str,
            namespace: Optional[str] = None,
            preview: bool = False
    ) -> str:
        """
        Set or update an attribute on element(s).

        Args:
            file_path: Path to the XML file relative to workspace root
            xpath: XPath to the element(s) to modify
            attribute_name: Name of the attribute to set
            attribute_value: Value to set for the attribute
            namespace: Optional namespace URI for the attribute
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'set_attribute', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find elements
            elements = root.xpath(xpath)

            if not elements:
                return yaml.dump(
                    self._create_result(
                        False,
                        'set_attribute',
                        message='No elements found matching XPath',
                        xpath=xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            attributes_set = 0
            attribute_details = []

            for elem in elements:
                if not isinstance(elem, etree._Element):
                    continue

                # Check if attribute already exists
                if namespace:
                    attr_key = f"{{{namespace}}}{attribute_name}"
                else:
                    attr_key = attribute_name

                old_value = elem.get(attr_key)

                attribute_details.append({
                    'element_tag': elem.tag,
                    'element_path': tree.getpath(elem),
                    'attribute_name': attribute_name,
                    'old_value': old_value,
                    'new_value': attribute_value,
                    'action': 'updated' if old_value else 'added'
                })

                if not preview:
                    elem.set(attr_key, str(attribute_value))

                attributes_set += 1

            # Save changes if not in preview mode
            if not preview and attributes_set > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            result = self._create_result(
                True,
                'set_attribute',
                message=f'{"Would set" if preview else "Set"} attribute on {attributes_set} element(s)',
                file_path=file_path,
                xpath=xpath,
                attribute_name=attribute_name,
                attribute_value=attribute_value,
                attributes_set=attributes_set,
                preview_mode=preview,
                details=attribute_details if attributes_set <= 5 else f'{attributes_set} elements affected'
            )

            if namespace:
                result['namespace'] = namespace

            return yaml.dump(result, default_flow_style=False, sort_keys=False)

        except Exception as e:
            error_msg = f'Error setting attribute: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'set_attribute', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def remove_attribute(
            self,
            file_path: str,
            xpath: str,
            attribute_name: str,
            namespace: Optional[str] = None,
            preview: bool = False
    ) -> str:
        """
        Remove an attribute from element(s).

        Args:
            file_path: Path to the XML file relative to workspace root
            xpath: XPath to the element(s) to modify
            attribute_name: Name of the attribute to remove
            namespace: Optional namespace URI for the attribute
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'remove_attribute', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find elements
            elements = root.xpath(xpath)

            if not elements:
                return yaml.dump(
                    self._create_result(
                        False,
                        'remove_attribute',
                        message='No elements found matching XPath',
                        xpath=xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            attributes_removed = 0
            removal_details = []

            for elem in elements:
                if not isinstance(elem, etree._Element):
                    continue

                # Construct attribute key with optional namespace
                if namespace:
                    attr_key = f"{{{namespace}}}{attribute_name}"
                else:
                    attr_key = attribute_name

                # Check if attribute exists
                old_value = elem.get(attr_key)

                if old_value is not None:
                    removal_details.append({
                        'element_tag': elem.tag,
                        'element_path': tree.getpath(elem),
                        'attribute_name': attribute_name,
                        'old_value': old_value
                    })

                    if not preview:
                        del elem.attrib[attr_key]

                    attributes_removed += 1

            # Save changes if not in preview mode
            if not preview and attributes_removed > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            return yaml.dump(
                self._create_result(
                    True,
                    'remove_attribute',
                    message=f'{"Would remove" if preview else "Removed"} attribute from {attributes_removed} element(s)',
                    file_path=file_path,
                    xpath=xpath,
                    attribute_name=attribute_name,
                    attributes_removed=attributes_removed,
                    preview_mode=preview,
                    details=removal_details if attributes_removed <= 5 else f'{attributes_removed} elements affected'
                ),
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error removing attribute: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'remove_attribute', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def set_text(
            self,
            file_path: str,
            xpath: str,
            text_content: str,
            append: bool = False,
            preview: bool = False
    ) -> str:
        """
        Set or append text content to element(s).

        Args:
            file_path: Path to the XML file relative to workspace root
            xpath: XPath to the element(s) to modify
            text_content: Text content to set or append
            append: If True, append to existing text; if False, replace text
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'set_text', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find elements
            elements = root.xpath(xpath)

            if not elements:
                return yaml.dump(
                    self._create_result(
                        False,
                        'set_text',
                        message='No elements found matching XPath',
                        xpath=xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            text_modified = 0
            text_details = []

            for elem in elements:
                if not isinstance(elem, etree._Element):
                    continue

                old_text = elem.text or ''

                if append:
                    new_text = old_text + text_content
                else:
                    new_text = text_content

                text_details.append({
                    'element_tag': elem.tag,
                    'element_path': tree.getpath(elem),
                    'old_text': old_text if old_text else None,
                    'new_text': new_text,
                    'action': 'appended' if append else 'replaced'
                })

                if not preview:
                    elem.text = new_text

                text_modified += 1

            # Save changes if not in preview mode
            if not preview and text_modified > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            return yaml.dump(
                self._create_result(
                    True,
                    'set_text',
                    message=f'{"Would modify" if preview else "Modified"} text content on {text_modified} element(s)',
                    file_path=file_path,
                    xpath=xpath,
                    text_content=text_content,
                    text_modified=text_modified,
                    append_mode=append,
                    preview_mode=preview,
                    details=text_details if text_modified <= 5 else f'{text_modified} elements affected'
                ),
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error setting text: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'set_text', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def add_namespace(
            self,
            file_path: str,
            prefix: str,
            uri: str,
            preview: bool = False
    ) -> str:
        """
        Add a namespace declaration to the root element.

        Args:
            file_path: Path to the XML file relative to workspace root
            prefix: Namespace prefix (use empty string for default namespace)
            uri: Namespace URI
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'add_namespace', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Get current namespaces
            current_nsmap = dict(root.nsmap) if root.nsmap else {}

            # Check if namespace already exists
            namespace_key = prefix if prefix else None
            already_exists = namespace_key in current_nsmap

            if not preview:
                # To add a namespace, we need to recreate the root with the new namespace
                new_nsmap = dict(current_nsmap)
                new_nsmap[namespace_key] = uri

                # Create new root with updated nsmap
                new_root = etree.Element(root.tag, nsmap=new_nsmap, attrib=root.attrib)
                new_root.text = root.text
                new_root.tail = root.tail

                # Copy all children
                for child in root:
                    new_root.append(child)

                # Create new tree and write
                new_tree = etree.ElementTree(new_root)
                new_tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            return yaml.dump(
                self._create_result(
                    True,
                    'add_namespace',
                    message=f'{"Would add" if preview else "Added"} namespace {"(already existed)" if already_exists else ""}',
                    file_path=file_path,
                    prefix=prefix if prefix else '(default)',
                    uri=uri,
                    already_existed=already_exists,
                    preview_mode=preview,
                    current_namespaces=current_nsmap
                ),
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error adding namespace: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'add_namespace', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def set_namespace(
            self,
            file_path: str,
            xpath: str,
            namespace_uri: str,
            preview: bool = False
    ) -> str:
        """
        Set the namespace of existing element(s).

        Args:
            file_path: Path to the XML file relative to workspace root
            xpath: XPath to the element(s) to modify
            namespace_uri: Namespace URI to apply to the element
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'set_namespace', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find elements
            elements = root.xpath(xpath)

            if not elements:
                return yaml.dump(
                    self._create_result(
                        False,
                        'set_namespace',
                        message='No elements found matching XPath',
                        xpath=xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            namespaces_set = 0
            namespace_details = []

            for elem in elements:
                if not isinstance(elem, etree._Element):
                    continue

                # Get current namespace
                old_namespace = elem.nsmap.get(elem.prefix) if hasattr(elem, 'nsmap') and elem.nsmap else None
                local_tag = etree.QName(elem).localname

                namespace_details.append({
                    'element_tag': elem.tag,
                    'local_name': local_tag,
                    'old_namespace': old_namespace,
                    'new_namespace': namespace_uri,
                    'element_path': tree.getpath(elem)
                })

                if not preview:
                    # Change element namespace by recreating it
                    new_elem = etree.Element(f"{{{namespace_uri}}}{local_tag}",
                                             attrib=elem.attrib,
                                             nsmap=elem.nsmap)
                    new_elem.text = elem.text
                    new_elem.tail = elem.tail

                    # Copy children
                    for child in elem:
                        new_elem.append(child)

                    # Replace in parent
                    parent = elem.getparent()
                    if parent is not None:
                        parent.replace(elem, new_elem)

                namespaces_set += 1

            # Save changes if not in preview mode
            if not preview and namespaces_set > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            return yaml.dump(
                self._create_result(
                    True,
                    'set_namespace',
                    message=f'{"Would set" if preview else "Set"} namespace on {namespaces_set} element(s)',
                    file_path=file_path,
                    xpath=xpath,
                    namespace_uri=namespace_uri,
                    namespaces_set=namespaces_set,
                    preview_mode=preview,
                    details=namespace_details if namespaces_set <= 5 else f'{namespaces_set} elements affected'
                ),
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error setting namespace: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'set_namespace', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def add_comment(
            self,
            file_path: str,
            parent_xpath: str,
            comment_text: str,
            position: str = 'append',
            preview: bool = False
    ) -> str:
        """
        Add a comment to the XML file.

        Args:
            file_path: Path to the XML file relative to workspace root
            parent_xpath: XPath to the parent element where comment will be added
            comment_text: Text content of the comment
            position: Where to add - 'append', 'prepend', or 'before' (default: 'append')
            preview: If True, show changes without applying them

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'add_comment', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            if position not in ['append', 'prepend', 'before']:
                return yaml.dump(
                    self._create_result(
                        False,
                        'add_comment',
                        error=f'Invalid position: {position}. Must be "append", "prepend", or "before"'
                    ),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find parent element(s)
            parents = root.xpath(parent_xpath)

            if not parents:
                return yaml.dump(
                    self._create_result(
                        False,
                        'add_comment',
                        message='No parent element found matching XPath',
                        xpath=parent_xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            comments_added = 0
            comment_details = []

            for parent in parents:
                if position == 'before':
                    # Add comment before the element
                    if not isinstance(parent, etree._Element):
                        continue

                    parent_elem = parent.getparent()
                    if parent_elem is None:
                        continue

                    comment = etree.Comment(comment_text)

                    comment_details.append({
                        'parent_tag': parent.tag,
                        'parent_path': tree.getpath(parent),
                        'position': 'before element'
                    })

                    if not preview:
                        parent_index = list(parent_elem).index(parent)
                        parent_elem.insert(parent_index, comment)

                    comments_added += 1
                else:
                    # Add comment inside the element
                    if not isinstance(parent, etree._Element):
                        continue

                    comment = etree.Comment(comment_text)

                    comment_details.append({
                        'parent_tag': parent.tag,
                        'parent_path': tree.getpath(parent),
                        'position': position
                    })

                    if not preview:
                        if position == 'prepend':
                            parent.insert(0, comment)
                        else:  # append
                            parent.append(comment)

                    comments_added += 1

            # Save changes if not in preview mode
            if not preview and comments_added > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            return yaml.dump(
                self._create_result(
                    True,
                    'add_comment',
                    message=f'{"Would add" if preview else "Added"} {comments_added} comment(s)',
                    file_path=file_path,
                    parent_xpath=parent_xpath,
                    comment_text=comment_text,
                    position=position,
                    comments_added=comments_added,
                    preview_mode=preview,
                    details=comment_details if comments_added <= 5 else f'{comments_added} comments added'
                ),
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error adding comment: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'add_comment', error=error_msg),
                default_flow_style=False, sort_keys=False
            )

    async def remove_comment(
            self,
            file_path: str,
            xpath: str,
            preview: bool = False
    ) -> str:
        """
        Remove comment(s) from the XML file.
        Note: XPath for comments uses the comment() function, e.g., "//comment()[contains(., 'text')]"

        Args:
            file_path: Path to the XML file relative to workspace root
            xpath: XPath to the comment(s) to remove
            preview: If True, show what would be removed without actually removing

        Returns:
            YAML string with operation results
        """
        try:
            full_path = self.workspace.full_path(file_path, mkdirs=False)
            if not full_path:
                return yaml.dump(
                    self._create_result(False, 'remove_comment', error=f'Invalid file path: {file_path}'),
                    default_flow_style=False, sort_keys=False
                )

            # Parse the XML file
            tree = etree.parse(full_path)
            root = tree.getroot()

            # Find comments to remove
            comments = root.xpath(xpath)

            if not comments:
                return yaml.dump(
                    self._create_result(
                        False,
                        'remove_comment',
                        message='No comments found matching XPath',
                        xpath=xpath
                    ),
                    default_flow_style=False, sort_keys=False
                )

            comments_removed = 0
            removal_details = []

            for comment in comments:
                # Comments are also etree elements but of type Comment
                if not isinstance(comment, etree._Comment):
                    continue

                parent = comment.getparent()
                if parent is not None:
                    removal_details.append({
                        'comment_text': str(comment).strip(),
                        'parent_tag': parent.tag if hasattr(parent, 'tag') else 'root'
                    })

                    if not preview:
                        parent.remove(comment)

                    comments_removed += 1

            # Save changes if not in preview mode
            if not preview and comments_removed > 0:
                tree.write(full_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

            return yaml.dump(
                self._create_result(
                    True,
                    'remove_comment',
                    message=f'{"Would remove" if preview else "Removed"} {comments_removed} comment(s)',
                    file_path=file_path,
                    xpath=xpath,
                    comments_removed=comments_removed,
                    preview_mode=preview,
                    details=removal_details if comments_removed <= 5 else f'{comments_removed} comments affected'
                ),
                default_flow_style=False, sort_keys=False
            )

        except Exception as e:
            error_msg = f'Error removing comment: {str(e)}'
            self.logger.error(error_msg)
            return yaml.dump(
                self._create_result(False, 'remove_comment', error=error_msg),
                default_flow_style=False, sort_keys=False
            )