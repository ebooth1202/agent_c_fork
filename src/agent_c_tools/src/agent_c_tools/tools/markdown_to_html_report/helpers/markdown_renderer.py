"""
Markdown to HTML Renderer - Pre-rendering markdown content to HTML.

This module handles the conversion of markdown content to HTML using python-markdown,
and transforms viewer:// protocol links to data-attribute based navigation.
"""

import re
import logging
from typing import Dict, List, Optional, NamedTuple
from html.parser import HTMLParser

try:
    import markdown
    from markdown.extensions.codehilite import CodeHiliteExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.toc import TocExtension
    from markdown.extensions.attr_list import AttrListExtension
    from markdown.extensions.md_in_html import MarkdownInHtmlExtension
    from markdown.extensions.nl2br import Nl2BrExtension
    from markdown.extensions.sane_lists import SaneListExtension
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from pygments.formatters import HtmlFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class TocEntry(NamedTuple):
    """Represents a table of contents entry."""
    level: int          # Heading level (1-6)
    text: str          # Heading text
    anchor_id: str     # Generated anchor ID


class RenderResult(NamedTuple):
    """Result of markdown rendering."""
    html: str                    # Rendered HTML content
    toc_entries: List[TocEntry]  # Table of contents entries
    has_code_blocks: bool        # Whether document contains code blocks


class HeadingExtractor(HTMLParser):
    """Extract heading information from HTML."""

    def __init__(self):
        super().__init__()
        self.headings = []
        self.current_heading = None
        self.current_level = None

    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.current_level = int(tag[1])
            self.current_heading = {
                'level': self.current_level,
                'text': '',
                'anchor_id': ''
            }
            # Extract ID if present
            for attr, value in attrs:
                if attr == 'id':
                    self.current_heading['anchor_id'] = value

    def handle_data(self, data):
        if self.current_heading is not None:
            self.current_heading['text'] += data

    def handle_endtag(self, tag):
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            if self.current_heading:
                self.headings.append(TocEntry(
                    level=self.current_heading['level'],
                    text=self.current_heading['text'].strip(),
                    anchor_id=self.current_heading['anchor_id']
                ))
                self.current_heading = None
                self.current_level = None


class MarkdownRenderer:
    """
    Renders markdown content to HTML with proper link handling and TOC generation.

    Features:
    - Python-markdown with multiple extensions
    - Pygments syntax highlighting
    - viewer:// link transformation to data attributes
    - TOC extraction for right-side navigation
    """

    def __init__(self):
        """Initialize the markdown renderer with configured extensions."""
        if not MARKDOWN_AVAILABLE:
            raise ImportError("python-markdown is required. Install with: pip install markdown")

        # Configure markdown extensions
        self.extensions = [
            FencedCodeExtension(),
            TableExtension(),
            TocExtension(
                permalink=False,  # Don't add permalink symbols
                toc_depth='2-3'   # Only H2 and H3 in TOC
            ),
            AttrListExtension(),
            MarkdownInHtmlExtension(),
            Nl2BrExtension(),
            SaneListExtension()
        ]

        # Add CodeHilite if Pygments is available
        if PYGMENTS_AVAILABLE:
            self.extensions.append(
                CodeHiliteExtension(
                    guess_lang=True,
                    linenums=False,
                    css_class='codehilite'
                )
            )
            logger.info("Markdown renderer initialized with Pygments support")
        else:
            logger.warning("Pygments not available. Syntax highlighting will be limited.")
            self.extensions.append(FencedCodeExtension())

        # Pattern for detecting viewer:// links in HTML
        # Matches: href="viewer://path/to/file.md" or href="viewer://path#anchor"
        self.viewer_link_pattern = re.compile(
            r'href=["\']viewer://([^"\'#]+)(#[^"\']+)?["\']'
        )

    def render_document(self, content: str, doc_path: str) -> RenderResult:
        """
        Render a complete markdown document to HTML.

        Args:
            content: Raw markdown content (with viewer:// links already rewritten)
            doc_path: Document path for context (used in logging)

        Returns:
            RenderResult with HTML, TOC entries, and metadata
        """
        try:
            # Create a fresh markdown instance for each render
            md = markdown.Markdown(extensions=self.extensions)

            # Render markdown to HTML
            html = md.convert(content)

            # Transform viewer:// links to data attributes
            html = self._transform_viewer_links(html)

            # Extract TOC entries from the rendered HTML
            toc_entries = self._extract_toc_entries(html)

            # Check if document has code blocks
            has_code_blocks = '<code' in html or '<pre' in html

            logger.debug(f"Rendered document: {doc_path} ({len(toc_entries)} TOC entries)")

            return RenderResult(
                html=html,
                toc_entries=toc_entries,
                has_code_blocks=has_code_blocks
            )

        except Exception as e:
            logger.error(f"Error rendering markdown for {doc_path}: {e}")
            # Return safe fallback
            return RenderResult(
                html=f"<p><strong>Error rendering document:</strong> {str(e)}</p><pre>{content}</pre>",
                toc_entries=[],
                has_code_blocks=False
            )

    def _transform_viewer_links(self, html: str) -> str:
        """
        Transform viewer:// protocol links to data-attribute based navigation.

        Converts:
            <a href="viewer://docs/faq.md#setup">Link</a>
        To:
            <a href="#" data-doc-path="docs/faq.md" data-doc-anchor="setup">Link</a>

        Args:
            html: Rendered HTML content

        Returns:
            HTML with transformed links
        """
        def replace_link(match):
            path = match.group(1)
            anchor = match.group(2) or ''

            # Remove leading # from anchor if present
            anchor_clean = anchor.lstrip('#') if anchor else ''

            if anchor_clean:
                return f'href="#" data-doc-path="{path}" data-doc-anchor="{anchor_clean}"'
            else:
                return f'href="#" data-doc-path="{path}"'

        transformed = self.viewer_link_pattern.sub(replace_link, html)

        return transformed

    def _extract_toc_entries(self, html: str) -> List[TocEntry]:
        """
        Extract table of contents entries from rendered HTML.

        Looks for H2 and H3 headings with IDs for the right-side TOC.

        Args:
            html: Rendered HTML content

        Returns:
            List of TocEntry objects
        """
        try:
            extractor = HeadingExtractor()
            extractor.feed(html)

            # Filter to only H2 and H3 for right-side TOC
            toc_entries = [
                entry for entry in extractor.headings
                if entry.level in (2, 3) and entry.anchor_id
            ]

            return toc_entries

        except Exception as e:
            logger.warning(f"Error extracting TOC entries: {e}")
            return []

    @staticmethod
    def get_pygments_css(style: str = 'default') -> Optional[str]:
        """
        Get Pygments CSS for syntax highlighting.

        Args:
            style: Pygments style name (default: 'default')
                   Valid styles: default, monokai, vim, vs, friendly, colorful, etc.

        Returns:
            CSS string or None if Pygments unavailable
        """
        if not PYGMENTS_AVAILABLE:
            return None

        try:
            formatter = HtmlFormatter(style=style)
            return formatter.get_style_defs('.codehilite')
        except Exception as e:
            logger.error(f"Error generating Pygments CSS with style '{style}': {e}")
            # Try fallback to default style
            try:
                formatter = HtmlFormatter(style='default')
                logger.warning(f"Falling back to 'default' style")
                return formatter.get_style_defs('.codehilite')
            except Exception as fallback_error:
                logger.error(f"Fallback to default style also failed: {fallback_error}")
                return None


def render_markdown_to_html(content: str, doc_path: str = "") -> RenderResult:
    """
    Convenience function to render markdown to HTML.

    Args:
        content: Markdown content
        doc_path: Optional document path for context

    Returns:
        RenderResult with HTML and metadata
    """
    renderer = MarkdownRenderer()
    return renderer.render_document(content, doc_path)
