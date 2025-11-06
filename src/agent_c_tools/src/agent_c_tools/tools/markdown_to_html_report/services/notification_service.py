"""
Notification Service

Handles the creation and sending of markdown notifications to the UI via the bridge.
Centralizes all notification logic to follow DRY principles.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class NotificationBuilder:
    """Builds markdown notification content for different output types."""

    @staticmethod
    def build_markdown_notification(output_info: Dict[str, Any]) -> str:
        """
        Create markdown content for result media events.

        Args:
            output_info: Dictionary containing output information
                - type: 'html' or 'docx'
                - output_filename: Name of generated file
                - output_path: Full path to generated file
                - file_system_path: OS-specific file system path
                - file_count: Number of files processed (for HTML)
                - style: Style used (for DOCX)

        Returns:
            Formatted markdown string for notification
        """
        try:
            # Build markdown notification
            output_type = output_info.get('type', 'html')

            if output_type == 'docx':
                markdown_content = f"""### ✅ Word Document Generated Successfully

**Output File:** `{output_info.get('output_filename', 'Unknown')}`

**Full Path:** `{output_info.get('output_path', 'Unknown')}`

**Style:** {output_info.get('style', 'default')}
"""
            else:
                # HTML viewer output
                markdown_content = f"""### ✅ HTML Viewer Generated Successfully

**Output File:** `{output_info.get('output_filename', 'Unknown')}`

**Full Path:** `{output_info.get('output_path', 'Unknown')}`

**Files Processed:** {output_info.get('file_count', 0)}
"""

            # Add file system path if available
            if output_info.get('file_system_path'):
                markdown_content += f"\n**File System Path:** `{output_info['file_system_path']}`\n"

            return markdown_content

        except Exception as e:
            logger.error(f"Failed to create result markdown: {str(e)}")
            # Return basic markdown as fallback
            return f"""### ✅ File Generated Successfully

**Output:** `{output_info.get('output_filename', 'Unknown')}`

**Files Processed:** {output_info.get('file_count', 0)}
"""


class NotificationSender:
    """Sends notifications via the bridge to the UI."""

    @staticmethod
    async def send_markdown_notification(
        markdown_content: str,
        tool_context: Dict[str, Any],
        sent_by_class: str
    ) -> None:
        """
        Send markdown notification via bridge.

        Args:
            markdown_content: Markdown formatted notification content
            tool_context: Tool context containing bridge reference
            sent_by_class: Name of the class sending the notification

        Raises:
            No exceptions - logs warnings if bridge unavailable
        """
        try:
            bridge = tool_context.get('bridge')
            if bridge:
                await bridge.raise_render_media_markdown(markdown_content, sent_by_class)
            else:
                logger.warning("Bridge not available in tool_context, skipping media event")
        except Exception as e:
            logger.error(f"Failed to send notification via bridge: {str(e)}")
