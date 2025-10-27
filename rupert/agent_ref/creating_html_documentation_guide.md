# Creating Standalone HTML Documentation Files

## Overview

This guide documents the correct method for creating professional, standalone HTML documentation files with clickable table of contents, proper formatting, and Centric branding.

**Working Example**: `//project/rupert/agent_c/bokf_analysis/Persona_Positioning_Complete.html`

---

## The Problem with generate_md_viewer Tool

The `generate_md_viewer` tool is designed for **multiple markdown files** with a tree-based navigation structure. When used with a **single markdown file**, it:
- ❌ Does NOT create a proper table of contents from headings
- ❌ Only shows the document title in sidebar
- ❌ Has poor positioning of UI elements (Hide button covers title)
- ❌ No logo placement control

**Do NOT use `generate_md_viewer` for single-document HTML files.**

---

## The Correct Approach: Custom Standalone HTML

### Step 1: Create Python Script to Build HTML

Create a Python script that:
1. Reads the markdown file content
2. Embeds markdown content directly in JavaScript variable
3. Embeds Centric logo as base64
4. Includes proper CSS styling
5. Includes JavaScript to build TOC from headings dynamically

### Step 2: Script Template

```python
#!/usr/bin/env python3
"""
Create standalone HTML documentation with proper TOC and branding
"""
import base64
import json

# Read Centric logo
with open('logos/Centric_C_logo-01 (1).png', 'rb') as f:
    c_logo_b64 = base64.b64encode(f.read()).decode('utf-8')

# Read markdown content
with open('path/to/your/document.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Escape for JavaScript
markdown_escaped = json.dumps(markdown_content)

# HTML template with embedded content
html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Document Title</title>
    
    <!-- External dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/languages/yaml.min.js"></script>
    
    <style>
        [CSS STYLES HERE - see full template below]
    </style>
</head>
<body>
    [HTML STRUCTURE HERE - see full template below]
    
    <script>
        const markdownContent = {markdown_escaped};
        [JAVASCRIPT HERE - see full template below]
    </script>
</body>
</html>'''

# Write output
with open('output/path/document.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
```

---

## Critical Design Elements

### 1. Sidebar Layout

```css
#sidebar {
    width: 320px;
    background: #f8f9fa;
    border-right: 1px solid #ddd;
    overflow-y: auto;
    position: relative;
    flex-shrink: 0;
}

#sidebar-header {
    padding: 50px 20px 20px 20px;  /* 50px top padding for Hide button */
    background: #2c1a5d;            /* Centric purple */
    color: white;
    position: sticky;
    top: 0;
    z-index: 10;
}

#sidebar-header h2 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
}
```

**Key Points**:
- 320px width provides good balance
- 50px top padding in header leaves room for Hide button
- Sticky header with Centric purple background (#2c1a5d)
- Header stays visible while scrolling TOC

### 2. Hide Button Positioning

```css
#toggle-sidebar {
    position: absolute;
    top: 15px;                      /* Fixed to top of sidebar */
    right: 15px;                    /* Fixed to right of sidebar */
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 4px;
    padding: 6px 12px;
    cursor: pointer;
    font-size: 12px;
    color: white;
}
```

**Key Points**:
- Position absolute within sidebar
- Top-right placement (15px from edges)
- Semi-transparent white background
- Does NOT cover document title

### 3. Table of Contents Styling

```css
#toc {
    list-style: none;
    padding: 20px;
}

#toc a {
    color: #333;
    text-decoration: none;
    display: block;
    padding: 8px 12px;
    border-radius: 4px;
    transition: all 0.2s;
    font-size: 13px;
}

#toc a.active {
    background: rgba(44, 26, 93, 0.1);  /* Light Centric purple */
    color: #2c1a5d;                     /* Centric purple */
    font-weight: 600;
    border-left: 3px solid #fdb825;     /* Centric gold accent */
}

/* Heading level hierarchy */
#toc .h1 {
    font-weight: 600;
    font-size: 14px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #dee2e6;
}

#toc .h2 {
    margin-left: 15px;
    font-size: 13px;
}

#toc .h3 {
    margin-left: 30px;
    font-size: 12px;
    color: #666;
}
```

**Key Points**:
- Clear visual hierarchy (H1 > H2 > H3)
- Active section highlighted with Centric purple and gold
- Indentation shows heading levels
- Smooth hover effects

### 4. Centric Logo Positioning

```css
#logo {
    position: fixed;
    bottom: 100px;              /* 100px from bottom (above up arrow) */
    right: 40px;                /* 40px from right */
    opacity: 0.6;
    z-index: 998;               /* Below up arrow (999) */
}

#logo img {
    width: 55px;                /* Logo size */
    height: auto;
}
```

**Key Points**:
- Fixed position at bottom-right
- 100px from bottom keeps it ABOVE the up arrow (which is at 30px)
- 40px from right provides good spacing
- 55px width is readable but not obtrusive
- z-index 998 keeps it below up arrow (999)

### 5. Up Arrow Button

```css
#back-to-top {
    position: fixed;
    bottom: 30px;               /* 30px from bottom */
    right: 30px;                /* 30px from right */
    background: #2c1a5d;        /* Centric purple */
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;                 /* Hidden by default */
    transition: opacity 0.3s, transform 0.3s;
    font-size: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 999;               /* Above logo */
}

#back-to-top.visible {
    opacity: 0.8;
}
```

**Key Points**:
- 50px circular button at bottom-right
- Appears when scrolled down 300px (via JavaScript)
- z-index 999 ensures it's above logo (998)
- 70px vertical separation from logo (100px - 30px)

---

## JavaScript Requirements

### 1. Build TOC from Headings

```javascript
function buildTOC() {
    const content = document.getElementById('markdown-content');
    const toc = document.getElementById('toc');
    const headings = content.querySelectorAll('h1, h2, h3');
    
    headings.forEach((heading, index) => {
        // Create ID if needed
        if (!heading.id) {
            heading.id = heading.textContent.trim().toLowerCase()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/(^-|-$)/g, '') + '-' + index;
        }
        
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#' + heading.id;
        a.textContent = heading.textContent;
        a.className = heading.tagName.toLowerCase();  // h1, h2, or h3
        
        a.addEventListener('click', (e) => {
            e.preventDefault();
            heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // Highlight briefly
            const orig = heading.style.backgroundColor;
            heading.style.backgroundColor = 'rgba(253,184,37,0.2)';
            setTimeout(() => heading.style.backgroundColor = orig, 1500);
            
            // Update active
            updateActiveTOC(a);
        });
        
        li.appendChild(a);
        toc.appendChild(li);
    });
}
```

**Key Points**:
- Automatically creates IDs for headings (slugified)
- Adds click handlers for smooth scrolling
- Highlights clicked heading briefly (Centric gold)
- Updates active state in TOC

### 2. Active Section Tracking

```javascript
function setupScrollHandlers() {
    const contentDiv = document.getElementById('content');
    const backToTop = document.getElementById('back-to-top');
    const headings = document.querySelectorAll('#markdown-content h1, #markdown-content h2, #markdown-content h3');
    
    contentDiv.addEventListener('scroll', () => {
        // Show/hide back to top button
        if (contentDiv.scrollTop > 300) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
        
        // Update active TOC link
        let currentHeading = null;
        headings.forEach(h => {
            const rect = h.getBoundingClientRect();
            if (rect.top >= 0 && rect.top < window.innerHeight / 3) {
                currentHeading = h;
            }
        });
        
        if (currentHeading) {
            const activeLink = document.querySelector(`#toc a[href="#${currentHeading.id}"]`);
            updateActiveTOC(activeLink);
        }
    });
}
```

**Key Points**:
- Tracks scroll position to highlight current section
- Shows up arrow after scrolling 300px
- Updates TOC active state automatically

### 3. Markdown Rendering

```javascript
function initPage() {
    if (typeof marked === 'undefined') {
        setTimeout(initPage, 100);  // Wait for marked.js to load
        return;
    }
    
    // Configure marked
    marked.setOptions({
        breaks: true,
        gfm: true
    });
    
    // Render markdown
    const html = marked.parse(markdownContent);
    document.getElementById('markdown-content').innerHTML = html;
    
    // Apply syntax highlighting
    if (typeof hljs !== 'undefined') {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }
    
    // Build TOC
    buildTOC();
    
    // Setup scroll handlers
    setupScrollHandlers();
}
```

**Key Points**:
- Waits for external libraries to load
- Renders markdown with marked.js
- Applies syntax highlighting with highlight.js
- Builds TOC after content is rendered

---

## Content Styling

### Headers

```css
#markdown-content h1 {
    color: #2c1a5d;                     /* Centric purple */
    border-bottom: 3px solid #fdb825;   /* Centric gold */
    padding-bottom: 12px;
    margin: 40px 0 20px 0;
    font-size: 2em;
}

#markdown-content h2 {
    color: #2c1a5d;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 10px;
    margin: 32px 0 16px 0;
    font-size: 1.6em;
}

#markdown-content h3 {
    color: #2c1a5d;
    margin: 24px 0 12px 0;
    font-size: 1.3em;
}
```

### Code Blocks

```css
#markdown-content pre {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-left: 4px solid #fdb825;     /* Centric gold accent */
    border-radius: 6px;
    padding: 20px;
    overflow-x: auto;
    margin: 20px 0;
}

#markdown-content code {
    background: #f8f9fa;
    padding: 3px 6px;
    border-radius: 3px;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    color: #e83e8c;                     /* Pink for inline code */
}
```

### Other Elements

```css
#markdown-content strong {
    color: #2c1a5d;                     /* Centric purple */
    font-weight: 600;
}

#markdown-content blockquote {
    border-left: 4px solid #fdb825;     /* Centric gold */
    padding-left: 20px;
    margin: 20px 0;
    color: #666;
    font-style: italic;
}
```

---

## Centric Branding Colors

Use these exact colors for consistency:

```css
/* Primary colors */
--centric-purple: #2c1a5d;
--centric-gold: #fdb825;

/* Backgrounds */
--sidebar-bg: #f8f9fa;
--content-bg: #ffffff;
--code-bg: #f8f9fa;

/* Text */
--text-primary: #333;
--text-secondary: #666;
--text-muted: #999;

/* Borders */
--border-light: #dee2e6;
--border-medium: #ddd;
```

---

## Full Template Location

The complete, working template is in:
```
//project/.scratch/create_standalone_persona_html.py
```

**To create a new HTML doc**:
1. Copy this script
2. Update input markdown path
3. Update output HTML path
4. Update document title in HTML template
5. Run the script

---

## Testing Checklist

Before considering the HTML complete, verify:

### Layout
- [ ] Sidebar is 320px wide
- [ ] Sidebar header is Centric purple (#2c1a5d)
- [ ] Document title visible in sidebar header
- [ ] Hide button is top-right, NOT covering title
- [ ] TOC shows all H1, H2, H3 headings
- [ ] TOC has proper indentation (H1 → H2 → H3)

### Functionality
- [ ] Clicking TOC link scrolls smoothly to section
- [ ] Clicked heading highlights briefly (gold background)
- [ ] Current section is highlighted in TOC
- [ ] Hide button toggles sidebar visibility
- [ ] Up arrow appears after scrolling down 300px
- [ ] Up arrow scrolls back to top smoothly

### Branding
- [ ] Centric C logo visible bottom-right
- [ ] Logo is ABOVE up arrow (no overlap)
- [ ] Logo is 55-60px wide
- [ ] Logo has slight transparency (opacity: 0.6-0.7)
- [ ] Centric purple used in headers
- [ ] Centric gold used in accents

### Content
- [ ] All markdown rendered correctly
- [ ] Code blocks have syntax highlighting
- [ ] Code blocks have gold left border
- [ ] Inline code is styled differently (pink)
- [ ] Bold text is Centric purple
- [ ] Links work and are styled
- [ ] Images display (if any)

### Mobile/Responsive
- [ ] Sidebar width works on different screens
- [ ] Content is readable on narrow screens
- [ ] Touch scrolling works on mobile

---

## Common Mistakes to Avoid

### ❌ DON'T: Use generate_md_viewer for Single Documents
```python
# This creates poor UI for single docs
generate_md_viewer(
    workspace_start="//project/path/document.md",
    output_filename="output.html"
)
```

### ❌ DON'T: Position Logo Too Low
```css
#logo {
    bottom: 20px;  /* TOO LOW - overlaps up arrow at 30px */
}
```

### ❌ DON'T: Cover Title with Hide Button
```css
#toggle-sidebar {
    top: 5px;      /* TOO HIGH - covers title */
    left: 10px;    /* WRONG SIDE */
}
```

### ❌ DON'T: Forget to Embed Logo as Base64
```html
<!-- This won't work when file is shared -->
<img src="../logos/logo.png">

<!-- Correct - embedded base64 -->
<img src="data:image/png;base64,iVBORw0KG...">
```

### ❌ DON'T: Forget to Escape Markdown for JavaScript
```python
# Wrong - will break on quotes/newlines
html = f'const markdown = "{markdown_content}";'

# Correct - use json.dumps
html = f'const markdown = {json.dumps(markdown_content)};'
```

---

## Why This Approach Works

1. **Fully Self-Contained**: Everything embedded (markdown, logo, styles, scripts)
2. **Shareable**: Single HTML file works anywhere
3. **Professional**: Proper branding and polish
4. **Functional**: Real TOC with navigation and active tracking
5. **Maintainable**: Clear structure, well-documented
6. **Performant**: No external file dependencies except CDN libraries

---

## Quick Start Command

```bash
# Navigate to project root
cd /Users/Ebooth/Agent_C/agent_c_fork

# Copy the template script
cp .scratch/create_standalone_persona_html.py .scratch/create_my_doc.py

# Edit paths in the script
# - Update markdown input path
# - Update HTML output path  
# - Update document title

# Run it
python3 .scratch/create_my_doc.py

# Open the result
open path/to/output.html
```

---

## Summary

**Use this method for**: Single markdown documents that need professional HTML output with TOC

**Key Success Factors**:
- Embed everything (markdown, logo, styles)
- Build TOC dynamically from headings
- Proper positioning (logo above arrow, hide button top-right)
- Centric branding colors throughout
- Smooth interactions (scrolling, highlighting)

**Reference Implementation**: `//project/rupert/agent_c/bokf_analysis/Persona_Positioning_Complete.html`
