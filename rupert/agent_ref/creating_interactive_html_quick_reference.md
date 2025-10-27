# Creating Interactive HTML Documentation - Quick Reference

## The Correct Method

**Use the Python script template** - NOT `generate_md_viewer` tool.

## Script Template Location

**Master Template**: `//project/.scratch/create_windows_setup_html.py`

This is the CORRECT, TESTED template that works perfectly.

## To Create New Interactive HTML

### Step 1: Copy the Template
```bash
cp .scratch/create_windows_setup_html.py .scratch/create_[your_doc_name]_html.py
```

### Step 2: Edit 3 Lines in the Script

**Line ~8**: Update markdown input path
```python
with open('rupert/personal/setup_guides/windows_new_user.md', 'r', encoding='utf-8') as f:
# Change to:
with open('path/to/your/document.md', 'r', encoding='utf-8') as f:
```

**Line ~18**: Update HTML title
```python
<title>Windows New User Setup Guide</title>
# Change to:
<title>Your Document Title</title>
```

**Line ~66**: Update sidebar header text
```python
<h2>Windows Setup Guide</h2>
# Change to:
<h2>Your Short Title</h2>
```

**Line ~338**: Update output path
```python
output_path = 'rupert/personal/setup_guides/Windows_Setup_Guide.html'
# Change to:
output_path = 'path/to/your/output.html'
```

### Step 3: Run the Script
```bash
python3 .scratch/create_[your_doc_name]_html.py
```

## Features You Get

✅ Clickable TOC in sidebar with all H1, H2, H3 headings  
✅ Centric purple & gold branding  
✅ Hide button (top-right of sidebar, doesn't cover title)  
✅ Centric logo (bottom-right, above up arrow)  
✅ Code syntax highlighting  
✅ Smooth scrolling & active section highlighting  
✅ Self-contained single HTML file  

## Critical Design Elements (DO NOT CHANGE)

- Sidebar width: **320px**
- Logo position: **bottom: 100px, right: 40px**
- Up arrow position: **bottom: 30px, right: 30px**
- Hide button: **top: 15px, right: 15px** (inside sidebar)
- Sidebar header padding: **50px top** (room for Hide button)
- Colors: **#2c1a5d** (purple), **#fdb825** (gold)

## If Document Content Updates

Just re-run the same script:
```bash
python3 .scratch/create_[your_doc_name]_html.py
```

Script reads markdown fresh each time - no changes needed.

## Successful Examples

- `//project/rupert/agent_c/bokf_analysis/Persona_Positioning_Complete.html`
- `//project/rupert/agent_c/bokf_analysis/Hybrid_Orchestration_Architecture.html`
- `//project/rupert/agent_c/bokf_analysis/BOKF_Replication_Framework.html`
- `//project/rupert/personal/setup_guides/Windows_Setup_Guide.html`

## What NOT to Do

❌ Don't use `generate_md_viewer` tool for single documents  
❌ Don't modify CSS positioning values  
❌ Don't change logo/button placement  
❌ Don't skip embedding the Centric logo as base64  

## Full Documentation

See `//project/rupert/agent_ref/creating_html_documentation_guide.md` for complete details.
