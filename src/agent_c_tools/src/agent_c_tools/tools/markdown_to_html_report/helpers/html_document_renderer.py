"""
HTML Document Renderer - Orchestrates the markdown-to-HTML rendering pipeline.

This module processes an entire DocRegistry, converting markdown content to HTML
and preparing documents for embedding in the final HTML viewer.
"""

import logging
from typing import Dict, Any

from .doc_registry import DocRegistry, DocMeta
from .markdown_renderer import MarkdownRenderer, RenderResult

logger = logging.getLogger(__name__)


class HtmlDocumentRenderer:
    """
    Orchestrates the rendering of all documents in a registry from markdown to HTML.

    This is the main entry point for the pre-rendering pipeline.
    """

    def __init__(self):
        """Initialize the renderer."""
        self.md_renderer = MarkdownRenderer()
        self.stats = {
            'total_docs': 0,
            'rendered_docs': 0,
            'failed_docs': 0,
            'total_toc_entries': 0
        }

    def render_registry(self, markdown_registry: DocRegistry) -> tuple[DocRegistry, Dict[str, Any]]:
        """
        Render all documents in a registry from markdown to HTML.

        Args:
            markdown_registry: DocRegistry with markdown content (already link-rewritten)

        Returns:
            Tuple of (html_registry, render_stats)
            - html_registry: New DocRegistry with HTML content
            - render_stats: Dictionary with rendering statistics
        """
        logger.info(f"Starting HTML rendering for {len(markdown_registry.by_path)} documents")

        html_registry = DocRegistry()
        doc_metadata = {}  # Store additional metadata per document

        self.stats['total_docs'] = len(markdown_registry.by_path)

        for path, doc in markdown_registry.by_path.items():
            try:
                # Render markdown to HTML
                render_result = self.md_renderer.render_document(doc.content, path)

                # Create new DocMeta with HTML content
                html_doc = DocMeta(
                    path=doc.path,
                    display_name=doc.display_name,
                    content=render_result.html,  # HTML instead of markdown
                    anchors=doc.anchors
                )

                html_registry.add_document(html_doc)

                # Store TOC metadata for later use in template
                doc_metadata[path] = {
                    'toc': [
                        {
                            'level': entry.level,
                            'text': entry.text,
                            'anchor': entry.anchor_id
                        }
                        for entry in render_result.toc_entries
                    ],
                    'has_code': render_result.has_code_blocks
                }

                self.stats['rendered_docs'] += 1
                self.stats['total_toc_entries'] += len(render_result.toc_entries)

                logger.debug(f"Rendered: {path} ({len(render_result.toc_entries)} TOC entries)")

            except Exception as e:
                logger.error(f"Failed to render document {path}: {e}")
                self.stats['failed_docs'] += 1

                # Add document with error message
                error_doc = DocMeta(
                    path=doc.path,
                    display_name=doc.display_name,
                    content=f"<p><strong>Error rendering document:</strong> {str(e)}</p>",
                    anchors=doc.anchors
                )
                html_registry.add_document(error_doc)
                doc_metadata[path] = {'toc': [], 'has_code': False}

        logger.info(
            f"HTML rendering complete: {self.stats['rendered_docs']} succeeded, "
            f"{self.stats['failed_docs']} failed, "
            f"{self.stats['total_toc_entries']} total TOC entries"
        )

        # Store metadata in registry for easy access
        html_registry._doc_metadata = doc_metadata

        return html_registry, self.stats.copy()


def render_registry_to_html(markdown_registry: DocRegistry) -> tuple[DocRegistry, Dict[str, Any]]:
    """
    Convenience function to render a registry from markdown to HTML.

    Args:
        markdown_registry: DocRegistry with markdown content

    Returns:
        Tuple of (html_registry, render_stats)
    """
    renderer = HtmlDocumentRenderer()
    return renderer.render_registry(markdown_registry)
