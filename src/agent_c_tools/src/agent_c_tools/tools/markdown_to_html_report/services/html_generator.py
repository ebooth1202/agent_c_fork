"""
HTML Generation Service

Orchestrates the generation of HTML output files from processed markdown documents.
Handles template loading, brand application, asset injection, and file writing.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)


class HtmlGenerationService:
    """
    Service for generating HTML viewer files from document structures.

    This service handles:
    - Template loading and brand application
    - CSS/JS asset injection (Pygments, Mermaid, slugger)
    - File structure injection
    - Writing output to workspace
    """

    def __init__(self, workspace_tool, templates_dir: Optional[Path] = None):
        """
        Initialize the HTML generation service.

        Args:
            workspace_tool: Workspace tool instance for file operations
            templates_dir: Optional path to templates directory (defaults to module templates/)
        """
        self.workspace_tool = workspace_tool
        self.templates_dir = templates_dir or Path(__file__).parent.parent / "templates"

    async def generate_html_output(
        self,
        file_structure: List[Dict[str, Any]],
        title: str,
        output_path_full: str,
        template: str = "markdown-viewer-template.html",
        brand: str = "default"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Generate HTML output from file structure.

        Args:
            file_structure: Processed file structure to inject into template
            title: Document title
            output_path_full: Full path where output should be written
            template: Template filename (default: "markdown-viewer-template.html")
            brand: Brand configuration name (default: "default")

        Returns:
            Tuple of (html_content, error_message)
            - If successful: (html_string, None)
            - If error: (None, error_message)
        """
        try:
            # Load template
            html_template = await self._load_template(template)

            # Apply brand configuration
            html_template = self._apply_brand(html_template, brand)

            # Customize title
            html_template = self._inject_title(html_template, title)

            # Inject CSS and JavaScript assets
            html_template = await self._inject_assets(html_template)

            # Inject file structure
            html_template = self._inject_file_structure(html_template, file_structure)

            # Write to workspace
            success, error = await self._write_to_workspace(output_path_full, html_template)
            if not success:
                return None, error

            return html_template, None

        except Exception as e:
            logger.exception("Error generating HTML output")
            return None, f"Error generating HTML output: {str(e)}"

    async def _load_template(self, template: str) -> str:
        """Load HTML template from templates directory."""
        try:
            from ..templates.html_template_manager import HtmlTemplateManager
            template_manager = HtmlTemplateManager()
            return await template_manager.get_html_template(template)
        except Exception as e:
            logger.error(f"Failed to get HTML template '{template}': {str(e)}")
            raise

    def _apply_brand(self, html_template: str, brand: str) -> str:
        """Apply brand configuration to template."""
        from ..helpers.brand_loader import load_and_apply_brand
        html_template = load_and_apply_brand(html_template, self.templates_dir, brand)
        logger.debug(f"Applied brand '{brand}' to template")
        return html_template

    def _inject_title(self, html_template: str, title: str) -> str:
        """Inject custom title into template."""
        # Default title placeholder constant
        DEFAULT_TITLE_PLACEHOLDER = "<h3 style=\"margin:0 16px 16px 16px;\">Agent C Output Viewer</h3>"

        return html_template.replace(
            DEFAULT_TITLE_PLACEHOLDER,
            f"<h3 style=\"margin:0 16px 16px 16px;\">{title}</h3>"
        )

    async def _inject_assets(self, html_template: str) -> str:
        """Inject CSS and JavaScript assets into template."""
        # Inject Pygments CSS
        html_template = self._inject_pygments_css(html_template)

        # Inject Mermaid.js
        html_template = self._inject_mermaid_js(html_template)

        # Inject JavaScript slugger
        html_template = self._inject_slugger_js(html_template)

        return html_template

    def _inject_pygments_css(self, html_template: str) -> str:
        """Inject Pygments CSS for syntax highlighting."""
        try:
            from ..helpers.markdown_renderer import MarkdownRenderer
            pygments_css = MarkdownRenderer.get_pygments_css('default')

            if pygments_css:
                html_template = html_template.replace('/* $PYGMENTS_CSS */', pygments_css)
                logger.debug("Injected Pygments CSS for syntax highlighting")
            else:
                logger.warning("Pygments CSS not available - syntax highlighting may be limited")
                html_template = html_template.replace('/* $PYGMENTS_CSS */', '/* Pygments not available */')

        except Exception as e:
            logger.error(f"Error injecting Pygments CSS: {e}")
            html_template = html_template.replace('/* $PYGMENTS_CSS */', '/* Error loading Pygments CSS */')

        return html_template

    def _inject_mermaid_js(self, html_template: str) -> str:
        """Inject Mermaid.js for offline diagram rendering."""
        mermaid_path = self.templates_dir / "mermaid.min.js"

        try:
            if mermaid_path.exists():
                with open(mermaid_path, 'r', encoding='utf-8') as f:
                    mermaid_js = f.read()
                html_template = html_template.replace('/* $MERMAID_JS */', mermaid_js)
                logger.debug("Injected Mermaid.js for offline diagram support")
            else:
                logger.warning(f"Mermaid.js not found at {mermaid_path} - diagrams may not render")
                html_template = html_template.replace('/* $MERMAID_JS */', '/* Mermaid.js not available */')

        except Exception as e:
            logger.error(f"Error loading Mermaid.js: {e}")
            html_template = html_template.replace('/* $MERMAID_JS */', '/* Error loading Mermaid.js */')

        return html_template

    def _inject_slugger_js(self, html_template: str) -> str:
        """Inject JavaScript slugger code for TOC consistency."""
        try:
            from ..helpers.slugger import get_javascript_slugger_code
            js_slugger_code = get_javascript_slugger_code()
            html_template = html_template.replace('$SLUGGER_JS_CODE', js_slugger_code)
            logger.debug("Injected JavaScript slugger code")
        except Exception as e:
            logger.error(f"Error injecting slugger code: {e}")
            html_template = html_template.replace('$SLUGGER_JS_CODE', '/* Error loading slugger */')

        return html_template

    def _inject_file_structure(self, html_template: str, file_structure: List[Dict[str, Any]]) -> str:
        """Inject processed file structure into template."""
        json_structure = json.dumps(file_structure, ensure_ascii=False)
        return html_template.replace('$FILE_STRUCTURE', json_structure)

    async def _write_to_workspace(self, output_path: str, content: str) -> Tuple[bool, Optional[str]]:
        """
        Write HTML content to workspace.

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            logger.debug("Writing HTML viewer to output location...")
            write_result = await self.workspace_tool.write(
                path=output_path,
                data=content,
                mode="write"
            )

            # Handle various response formats from workspace tool
            if not write_result or write_result.strip() == "":
                return True, None

            try:
                write_data = json.loads(write_result)
            except json.JSONDecodeError:
                # Check if it's a plain text success message
                if self._is_success_message(write_result):
                    logger.debug(f"Received plain text success message: {write_result}")
                    return True, None
                else:
                    error_msg = f"Invalid response from workspace write: {write_result}"
                    logger.error(error_msg)
                    return False, error_msg

            if 'error' in write_data:
                return False, f"Failed to write HTML file: {write_data['error']}"

            return True, None

        except Exception as e:
            logger.exception("Error writing to workspace")
            return False, f"Error writing to workspace: {str(e)}"

    @staticmethod
    def _is_success_message(message: str) -> bool:
        """Check if message indicates successful write operation."""
        success_indicators = [
            "successfully written",
            "success",
            "data written",
            "file created"
        ]
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in success_indicators)
