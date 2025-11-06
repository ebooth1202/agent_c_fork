# Brand Configuration System

This directory contains brand configuration files for the Markdown to HTML Report tool.

## Overview

Brand configurations allow you to customize the appearance of generated HTML viewers, including:
- Color schemes
- Logos (SVG, image, or text)
- Typography (fonts, weights, line-height)
- Layout spacing

## Available Brands

### `default.json`
Modern, clean design with blue/gray color scheme
- Primary: Blue (#2563eb)
- Clean system fonts
- Minimalist logo (📘 Documentation)

### `centric.json`
Centric Consulting brand
- Primary: Peacock blue (#1f5d82)
- Secondary: Gold (#fdb825)
- Agent C SVG logo with purple/orange accents
- Centric brand colors

## Creating a New Brand

1. **Copy an existing brand file** as a starting point
2. **Modify the JSON** with your brand values
3. **Save as `brand-name.json`** in this directory
4. **Use in tool** with `brand="brand-name"` parameter

## Brand Schema

```json
{
  "name": "Brand Name",
  "description": "Brief description",
  "colors": {
    "primary": "#hexcode",
    "primary_hover": "#hexcode",
    "secondary": "#hexcode",
    "accent": "#hexcode",
    "heading": "#hexcode",
    "text": "#hexcode",
    "text_muted": "#hexcode",
    "sidebar_bg": "#hexcode",
    "sidebar_hover": "#hexcode",
    "sidebar_active": "#hexcode",
    "border": "#hexcode",
    "code_bg": "#hexcode",
    "code_border": "#hexcode",
    "search_bg": "#hexcode",
    "toc_bg": "#hexcode",
    "toc_hover": "#hexcode",
    "link": "#hexcode",
    "link_hover": "#hexcode"
  },
  "logo": {
    "type": "svg|text|image",
    "svg_content": "<svg>...</svg>",
    "text": "Text Logo",
    "url": "path/to/image.png",
    "width": "120px",
    "height": "120px",
    "font_size": "24px",
    "color": "#hexcode",
    "alt": "Alt text"
  },
  "typography": {
    "font_family": "system-ui, -apple-system, sans-serif",
    "headings_font": "system-ui, sans-serif",
    "code_font": "'Monaco', 'Consolas', monospace",
    "base_size": "16px",
    "heading_weight": "600",
    "line_height": "1.7"
  },
  "spacing": {
    "sidebar_width": "280px",
    "content_max_width": "900px",
    "padding_base": "16px"
  }
}
```

## Logo Types

### SVG Logo
```json
"logo": {
  "type": "svg",
  "svg_content": "<svg>...</svg>",
  "width": "120px",
  "height": "120px"
}
```

### Text Logo
```json
"logo": {
  "type": "text",
  "text": "My Brand",
  "font_size": "24px",
  "color": "#2563eb"
}
```

### Image Logo
```json
"logo": {
  "type": "image",
  "url": "https://example.com/logo.png",
  "width": "120px",
  "height": "auto",
  "alt": "My Brand"
}
```

## Usage Examples

### Python Tool
```python
# Use default brand
await tool.generate_md_viewer(
    workspace_start="//my_workspace/",
    output_filename="output.html",
    brand="default"  # or "centric"
)

# Use custom brand
await tool.generate_md_viewer(
    workspace_start="//my_workspace/",
    output_filename="output.html",
    brand="my-custom-brand"  # reads brands/my-custom-brand.json
)
```

### Testing
```bash
cd src/agent_c_tools/src/agent_c_tools/tools/markdown_to_html_report
python user_test.py
```

## CSS Variables Generated

All brand colors are injected as CSS variables:
- `--brand-primary`
- `--brand-secondary`
- `--brand-accent`
- `--brand-heading`
- `--brand-text`
- etc.

The template uses these with fallbacks:
```css
:root {
  --primary: var(--brand-primary, #2563eb);
  --secondary: var(--brand-secondary, #64748b);
}
```

## Templates

Multiple templates can be used with different brands:
- `markdown-viewer-template.html` - Modern template with brand support
- `centric-classic.html` - Original Centric template (preserved)

Specify with `template` parameter:
```python
await tool.generate_md_viewer(
    workspace_start="//my_workspace/",
    output_filename="output.html",
    template="centric-classic.html",
    brand="centric"
)
```
