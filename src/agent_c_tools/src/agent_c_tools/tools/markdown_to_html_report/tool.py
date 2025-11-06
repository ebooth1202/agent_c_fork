"""
Markdown Tools - Refactored with Registry-based Architecture

This module now uses the new DocRegistry + LinkRewriter architecture
for cleaner, more maintainable markdown processing.
"""

import json
import logging
from pathlib import Path
from typing import Optional

from agent_c.toolsets.tool_set import Toolset
from agent_c.toolsets.json_schema import json_schema
from .helpers.doc_registry import DocRegistry
from .helpers.registry_builder import build_registry_and_tree, validate_registry_integrity
from .helpers.html_document_renderer import render_registry_to_html
from .services.docx_generator import DocxGenerator
from ..workspace.tool import WorkspaceTools
from ...helpers.path_helper import create_unc_path, ensure_file_extension, os_file_system_path, has_file_extension, normalize_path
from ...helpers.validate_kwargs import validate_required_fields
from ...helpers.workspace_result_parser import parse_workspace_result

logger = logging.getLogger(__name__)

# Constants for magic values
class Constants:
    """Configuration constants for the markdown tools."""
    DEFAULT_TITLE = "Agent C Output Viewer"
    DEFAULT_TITLE_PLACEHOLDER = "<h3 style=\"margin:0 16px 16px 16px;\">Agent C Output Viewer</h3>"
    MARKDOWN_EXTENSIONS = ['md', 'markdown']
    DOCX_EXTENSIONS = ['.md', '.markdown']


class MarkdownToHtmlReportTools(Toolset):
    """
    Transforms your Markdown documents into beautiful, interactive HTML reports and Word documents.
    Your agent can create professional presentations, documentation, and reports that are easy to share,
    navigate, and read across different platforms and devices.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="markdown_viewer", use_prefix=False)
        # Get workspace tools for file operations
        self.workspace_tool: Optional[WorkspaceTools] = None
        self.file_collector = None
        self.docx_converter = DocxGenerator()

        # Services - will be initialized in post_init after workspace_tool is available
        self.html_service = None
        self.notification_service = None
        self.response_builder = None

    async def post_init(self):
        from .services.html_generator import HtmlGenerationService
        from .services.notification_service import NotificationBuilder, NotificationSender
        from .helpers.response_builder import ResponseBuilder

        self.workspace_tool = self.tool_chest.available_tools.get("WorkspaceTools")

        # Initialize services
        self.html_service = HtmlGenerationService(self.workspace_tool)
        self.notification_builder = NotificationBuilder()
        self.notification_sender = NotificationSender()
        self.response_builder = ResponseBuilder()

    @json_schema(
        description="Generate an interactive HTML viewer for markdown files in a workspace directory",
        params={
            "workspace_start": {
                "type": "string",
                "description": "A UNC to either the starting folder containing the markdown files or a single markdown file ",
                "required": True
            },
            "output_filename": {
                "type": "string",
                "description": "The name of the output HTML file to generate (can be a simple filename or full UNC path)",
                "required": True
            },
            "title": {
                "type": "string",
                "description": "Optional title for the HTML viewer (displayed in the sidebar)",
                "required": False
            },
            "files_to_ignore": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Optional flat list of filenames to ignore when generating the HTML viewer. Does not support folder level differentiation.",
                "required": False,
                "default": []
            },
            "template": {
                "type": "string",
                "description": "Optional template filename (e.g., 'markdown-viewer-template.html', 'centric-classic.html'). Defaults to 'markdown-viewer-template.html'",
                "required": False
            },
            "brand": {
                "type": "string",
                "description": "Optional brand configuration name (e.g., 'default', 'centric'). Defaults to 'centric'. Brand configs in templates/brands/ control colors, logos, and typography.",
                "required": False,
                "default": "centric"
            }
        }
    )
    async def generate_md_viewer(self, **kwargs) -> str:
        """Generate an interactive HTML viewer for markdown files in a workspace directory."""
        # Validate required fields
        success, validation_error = validate_required_fields(
            kwargs, ["workspace_start", "output_filename"])
        if not success:
            return self.response_builder.create_error_response(validation_error)

        # Extract parameters
        workspace_start = kwargs.get('workspace_start')
        output_filename = kwargs.get('output_filename')
        title = kwargs.get('title', 'Agent C Output Viewer')
        files_to_ignore = kwargs.get('files_to_ignore', [])
        tool_context = kwargs.get('tool_context', {})
        template = kwargs.get('template', 'markdown-viewer-template.html')
        brand = kwargs.get('brand', 'centric')

        try:
            # Parse the workspace_start UNC path using the existing robust workspace parser
            error, workspace_obj, relative_path = self.workspace_tool._parse_unc_path(workspace_start)

            if error:
                return self.response_builder.create_error_response(f"Invalid workspace path '{workspace_start}': {error}")

            if not workspace_obj:
                return self.response_builder.create_error_response(f"Workspace not found for path '{workspace_start}'")

            workspace_path = workspace_obj.name
            input_path = relative_path or ""

            # Validate and process paths
            input_path_full, output_path_full, path_error = await self._validate_and_process_paths(
                workspace_path, input_path, output_filename)
            if path_error:
                return self.response_builder.create_error_response(path_error)

            # PIPELINE: Collect → Registry → Link Rewriting → Template

            # Step 1: Determine if input is a file or directory and collect appropriately
            if has_file_extension(input_path, Constants.MARKDOWN_EXTENSIONS):
                # Single file mode
                registry, ui_tree, warnings = await self._handle_single_file_with_registry(
                    input_path_full, input_path)
            else:
                # Directory mode - use new registry builder (includes link rewriting)
                registry, ui_tree, warnings = await build_registry_and_tree(
                    self.workspace_tool,
                    mode='directory',
                    root_path=input_path_full,
                    files_to_ignore=files_to_ignore,
                    tool_context=tool_context
                )

                # NEW: Render markdown to HTML (eliminates need for JS safety processing)
                logger.info("Rendering markdown to HTML...")
                registry, render_stats = render_registry_to_html(registry)
                logger.info(f"HTML rendering stats: {render_stats}")

                # Log warnings if any
                if warnings:
                    for warning in warnings:
                        logger.warning(warning)

            if not registry.by_path:
                return self.response_builder.create_error_response("No markdown files found to process")

            # Step 2: Validate registry integrity
            issues = validate_registry_integrity(registry)
            if issues:
                logger.warning(f"Registry validation issues: {issues}")

            # Step 3: Build final structure for template
            final_structure = self._build_template_structure(registry, ui_tree)

            # Step 4: Generate HTML output
            html_content, html_error = await self.html_service.generate_html_output(
                final_structure, title, output_path_full, template, brand
            )
            if html_error:
                return self.response_builder.create_error_response(html_error)

            # Step 5: Raise media event
            await self._raise_media_event(output_filename, output_path_full, len(registry.by_path), tool_context)

            # Return success response
            message = f"Successfully generated HTML viewer at {output_filename}."
            logger.debug(message)

            return self.response_builder.create_success_response(
                message,
                output_file=output_filename,
                output_path=output_path_full,
                workspace=workspace_path,
                file_count=len(registry.by_path),
                registry_stats=registry.stats(),
                warnings=warnings if warnings else []
            )

        except Exception as e:
            logger.exception("Error generating markdown viewer")
            return self.response_builder.create_error_response(f"Error generating markdown viewer: {str(e)}")

    @json_schema(
        description="Generate an interactive HTML viewer with custom file hierarchy structure. Supports both relative paths (with workspace) and fully qualified UNC paths (without workspace).",
        params={
            "workspace": {
                "type": "string",
                "description": "Optional workspace name for resolving relative file paths. If omitted, all paths in custom_structure must be fully qualified UNC paths (e.g., '//workspace_name/path/to/file.md'). When provided, relative paths in custom_structure are resolved against this workspace.",
                "required": False
            },
            "output_filename": {
                "type": "string",
                "description": "The name of the output HTML file to generate (can be a simple filename or full UNC path)",
                "required": True
            },
            "custom_structure": {
                "type": "string",
                "description": "JSON string defining custom hierarchy. File paths can be: 1) Fully qualified UNC paths starting with '//' (e.g., '//workspace/path/file.md'), 2) Relative paths if workspace parameter provided (e.g., 'docs/file.md'), or 3) Mix of both. Example: '{\"items\": [{\"type\": \"folder\", \"name\": \"Getting Started\", \"children\": [{\"type\": \"file\", \"name\": \"Introduction\", \"path\": \"//my_workspace/intro.md\"}]}, {\"type\": \"file\", \"name\": \"API Reference\", \"path\": \"api.md\"}]}'",
                "required": True
            },
            "title": {
                "type": "string",
                "description": "Optional title for the HTML viewer (displayed in the sidebar)",
                "required": False
            },
            "template": {
                "type": "string",
                "description": "Optional template filename (e.g., 'markdown-viewer-template.html', 'centric-classic.html'). Defaults to 'markdown-viewer-template.html'",
                "required": False
            },
            "brand": {
                "type": "string",
                "description": "Optional brand configuration name (e.g., 'default', 'centric'). Defaults to 'default'. Brand configs in templates/brands/ control colors, logos, and typography.",
                "required": False
            }
        }
    )
    async def generate_custom_md_viewer(self, **kwargs) -> str:
        """
        Generate an interactive HTML viewer with custom file hierarchy structure.

        Supports three path resolution modes:
        1. Fully qualified paths: All paths start with '//' (workspace parameter not needed)
        2. Relative paths: workspace parameter provided, paths resolved against it
        3. Hybrid: Mix of fully qualified and relative paths in same structure
        """
        success, validation_error = validate_required_fields(
            kwargs, ["output_filename", "custom_structure"])

        # Validate required fields
        if not success:
            return self.response_builder.create_error_response(validation_error)

        workspace = kwargs.get('workspace')  # Optional now
        output_filename = kwargs.get('output_filename')
        custom_structure_json = kwargs.get('custom_structure')
        title = kwargs.get('title', 'Custom Markdown Viewer')
        template = kwargs.get('template', 'markdown-viewer-template.html')
        brand = kwargs.get('brand', 'default')
        tool_context = kwargs.get('tool_context', {})

        try:
            # Parse the custom structure JSON
            try:
                custom_structure = json.loads(custom_structure_json)
            except json.JSONDecodeError as e:
                return self.response_builder.create_error_response(f"Invalid JSON in custom_structure: {str(e)}")

            # Create base path for file resolution (None if workspace not provided)
            base_path = f"//{workspace}" if workspace else None

            # NEW PIPELINE: Custom Structure → Registry → Link Rewriting → Template

            # Step 1: Build registry from custom structure (includes link rewriting)
            registry, ui_tree, warnings = await build_registry_and_tree(
                self.workspace_tool,
                mode='custom',
                custom_structure=custom_structure,
                base_path=base_path
            )

            # NEW: Render markdown to HTML (eliminates need for JS safety processing)
            logger.info("Rendering markdown to HTML...")
            registry, render_stats = render_registry_to_html(registry)
            logger.info(f"HTML rendering stats: {render_stats}")

            # Log warnings if any
            if warnings:
                for warning in warnings:
                    logger.warning(warning)

            if not registry.by_path:
                return self.response_builder.create_error_response("No valid markdown files found in the custom structure")

            # Step 2: Validate registry integrity
            issues = validate_registry_integrity(registry)
            if issues:
                logger.warning(f"Registry validation issues: {issues}")

            # Step 3: Build final structure for template
            final_structure = self._build_template_structure(registry, ui_tree)

            # Step 4: Create UNC output filename and generate HTML
            output_filename = ensure_file_extension(output_filename, 'html')
            if not output_filename.startswith('//'):
                if workspace:
                    output_path_full = create_unc_path(workspace, output_filename)
                else:
                    return self.response_builder.create_error_response(
                        "When workspace is not provided, output_filename must be a fully qualified UNC path (e.g., '//workspace/path/file.html')"
                    )
            else:
                output_path_full = output_filename

            html_content, html_error = await self.html_service.generate_html_output(
                final_structure, title, output_path_full, template, brand
            )
            if html_error:
                return self.response_builder.create_error_response(html_error)

            # Step 5: Raise media event
            await self._raise_media_event(output_filename, output_path_full, len(registry.by_path), tool_context)

            message = f"Successfully generated custom HTML viewer at {output_filename}."
            logger.debug(message)

            return self.response_builder.create_success_response(
                message,
                output_file=output_filename,
                output_path=output_path_full,
                workspace=workspace,
                file_count=len(registry.by_path),
                structure_type="custom",
                registry_stats=registry.stats(),
                warnings=warnings if warnings else []
            )

        except Exception as e:
            logger.exception("Error generating custom markdown viewer")
            return self.response_builder.create_error_response(f"Error generating custom markdown viewer: {str(e)}")

    # Preserve existing markdown_to_docx method unchanged
    @json_schema(
        description="Convert a markdown file to Word (DOCX) format",
        params={
            "workspace": {
                "type": "string",
                "description": "The workspace containing the markdown file",
                "required": True
            },
            "input_path": {
                "type": "string",
                "description": "The relative path to the markdown file to convert",
                "required": True
            },
            "output_filename": {
                "type": "string",
                "description": "filename for the output Word document",
                "required": False
            },
            "style": {
                "type": "string",
                "description": "Style template to use",
                "enum": ["default", "academic", "business", "minimal"],
                "required": False,
                "default": "default"
            },
            "include_toc": {
                "type": "boolean",
                "description": "Whether to include a table of contents",
                "required": False,
                "default": True
            },
            "page_break_level": {
                "type": "integer",
                "description": "Insert page breaks before headings of this level (1-6)",
                "required": False,
                "default": 1
            }
        }
    )
    async def markdown_to_docx(self, **kwargs) -> str:
        """Convert a markdown file to Word (DOCX) format."""
        # This method is preserved unchanged from the original implementation
        # as it doesn't need the new link processing architecture

        if not self.docx_converter.docx_conversion_available:
            return self.response_builder.create_error_response("Required dependencies not available. Please install python-markdown, python-docx, and beautifulsoup4.")

        # Validate required fields
        success, validation_error = validate_required_fields(
            kwargs, ["workspace", "input_path"])
        if not success:
            return self.response_builder.create_error_response(validation_error)

        workspace = kwargs.get('workspace')
        input_path = kwargs.get('input_path')
        output_filename = kwargs.get('output_filename')
        style = kwargs.get('style', 'default')
        include_toc = kwargs.get('include_toc', True)
        page_break_level = kwargs.get('page_break_level', 1)
        tool_context = kwargs.get('tool_context', {})

        try:
            # Process paths
            input_path_full = create_unc_path(workspace, input_path)

            if not has_file_extension(input_path_full, Constants.DOCX_EXTENSIONS):
                return self.response_builder.create_error_response(f"Input file '{input_path_full}' is not a markdown file.")

            input_filename = normalize_path(input_path_full).split('/')[-1]

            # Determine output path
            if not output_filename:
                # Use the same name as the input but with .docx extension
                output_filename = Path(input_filename).stem + ".docx"
                output_path_full = f"//{workspace}/{output_filename}"
            elif not output_filename.startswith('//'):
                # Ensure it has .docx extension
                output_filename = ensure_file_extension(output_filename, 'docx')
                output_path_full = f"//{workspace}/{output_filename}"
            else:
                output_path_full = output_filename

            # Read and Process the markdown file
            error, workspace_obj, relative_path = self.workspace_tool.validate_and_get_workspace_path(input_path_full)
            if error:
                raise ValueError(f"Error reading file: {error}")
            file_content = await workspace_obj.read_internal(relative_path)

            if file_content.startswith('{"error":'):
                raise ValueError(f"Error reading file: {file_content}")

            # Convert markdown to Word document
            docx_content_bytes = await self.docx_converter.convert_to_docx(
                file_content, style, include_toc, page_break_level)

            try:
                write_result = await self.workspace_tool.internal_write_bytes(
                    path=output_path_full,
                    data=docx_content_bytes,
                    mode="write",
                )
            except Exception as e:
                logger.error(f"Error writing docx file: {e}")
                return self.response_builder.create_error_response(f"Failed to write Word document: {str(e)}")

            # Parse the write result using the helper function
            success, write_data, error_msg = parse_workspace_result(write_result, "write operation")
            if not success:
                return self.response_builder.create_error_response(f"Failed to write Word document: {error_msg}")

            # Get file system path
            file_system_path = os_file_system_path(self.workspace_tool, output_path_full)

            # Create output info dictionary for media event
            output_info = {
                "type": "docx",
                "output_filename": output_filename,
                "output_path": output_path_full,
                "file_system_path": file_system_path,
                "style": style
            }

            # Generate and raise markdown content for the result
            try:
                markdown_content = self.notification_builder.build_markdown_notification(output_info)
                await self.notification_sender.send_markdown_notification(
                    markdown_content,
                    tool_context,
                    self.__class__.__name__
                )
            except Exception as e:
                logger.error(f"Failed to raise media event: {str(e)}")

            return self.response_builder.create_success_response(
                f"Successfully converted markdown to Word document at {output_path_full}",
                input_file=input_path_full,
                output_file=output_path_full,
                workspace=workspace,
                style=style
            )

        except Exception as e:
            logger.exception("Error converting markdown to Word document")
            return self.response_builder.create_error_response(f"Error converting markdown to Word document: {str(e)}")


    async def _handle_single_file_with_registry(self, input_path_full: str, input_path: str) -> tuple[DocRegistry, list[dict], list[str]]:
        """Handle single file processing using the new registry approach."""
        try:
            error, workspace_obj, relative_path = self.workspace_tool.validate_and_get_workspace_path(input_path_full)
            if error:
                raise ValueError(f"Input path '{input_path}' is not accessible: {error}")

            # Read file content
            file_content = await workspace_obj.read_internal(relative_path)
            if file_content.startswith('{"error":'):
                raise ValueError(f"Error reading file at {input_path}: {file_content}")

            # Create registry with single document
            registry = DocRegistry()

            # Create DocMeta for the single file
            from .helpers.doc_registry import DocMeta

            display_name = Path(input_path).stem.replace('_', ' ').replace('-', ' ').title()

            doc = DocMeta(
                display_name=display_name,
                path=Path(input_path).name,  # Use just filename for single file
                anchors=set(),
                content=file_content
            )

            registry.add_document(doc)

            # Apply link rewriting
            from .helpers.link_rewriter import rewrite_all_documents
            registry = rewrite_all_documents(registry)

            # NEW: Render markdown to HTML
            logger.info("Rendering single file to HTML...")
            registry, render_stats = render_registry_to_html(registry)
            logger.info(f"HTML rendering stats: {render_stats}")

            # Create simple UI tree
            ui_tree = [{
                'name': display_name,
                'type': 'file',
                'path': doc.path
            }]

            logger.debug(f"Created single file registry: {input_path}")
            return registry, ui_tree, []  # No warnings for single file

        except Exception as e:
            raise ValueError(f"Error processing single file: {str(e)}")

    @staticmethod
    def _build_template_structure(registry: DocRegistry, ui_tree: list[dict]) -> list[dict]:
        """Build final structure for template injection."""
        # Get document metadata (TOC, etc.) if available
        doc_metadata = getattr(registry, '_doc_metadata', {})

        # Add content and metadata to the UI tree structure
        def add_content_to_tree(items):
            for item in items:
                if item.get('type') == 'file':
                    path = item.get('path')
                    doc = registry.by_path.get(path)
                    if doc:
                        item['content'] = doc.content  # Now HTML instead of markdown
                        # Add TOC metadata if available
                        metadata = doc_metadata.get(path, {})
                        if metadata.get('toc'):
                            item['toc'] = metadata['toc']
                elif item.get('type') == 'folder' and 'children' in item:
                    add_content_to_tree(item['children'])

        # Deep copy to avoid modifying original
        import copy
        final_structure = copy.deepcopy(ui_tree)
        add_content_to_tree(final_structure)

        return final_structure



    @staticmethod
    async def _validate_and_process_paths(workspace: str, input_path: str, output_filename: str) -> tuple:
        """Validate and process input/output paths."""
        try:
            # Normalize input path for cross-platform compatibility
            # Handle Windows root path "\\" or "\" -> convert to ""
            if input_path in ['\\', '\\\\', '/', '']:
                input_path = ""  # Root of workspace
            else:
                input_path = input_path.replace('\\', '/').strip('/')

            # Create UNC input path
            input_path_full = create_unc_path(workspace, input_path)

            # Create UNC output filename
            output_filename = ensure_file_extension(output_filename, 'html')
            if not output_filename.startswith('//'):
                output_path_full = create_unc_path(workspace, output_filename)
            else:
                output_path_full = output_filename

            return input_path_full, output_path_full, None
        except Exception as e:
            return None, None, f"Error processing paths: {str(e)}"

    async def _raise_media_event(self, output_filename: str, output_path_full: str, file_count: int, tool_context: dict):
        """Generate and raise media event for the result."""
        try:
            # Get file system path
            file_system_path = os_file_system_path(self.workspace_tool, output_path_full)

            # Create output info dictionary
            output_info = {
                "output_filename": output_filename,
                "output_path": output_path_full,
                "file_system_path": file_system_path,
                "file_count": file_count
            }

            # Generate markdown content using notification builder
            markdown_content = self.notification_builder.build_markdown_notification(output_info)

            # Send notification using notification sender
            await self.notification_sender.send_markdown_notification(
                markdown_content,
                tool_context,
                self.__class__.__name__
            )
        except Exception as e:
            logger.error(f"Failed to raise media event: {str(e)}")


# Register the toolset
Toolset.register(MarkdownToHtmlReportTools, required_tools=['WorkspaceTools'])