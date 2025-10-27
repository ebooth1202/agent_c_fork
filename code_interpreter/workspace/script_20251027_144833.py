
import os
import sys

# Set up input/output paths
INPUT_DIR = "/input"
OUTPUT_DIR = "/output"

# Add input files info
input_files = []

# Redirect stdout to capture print statements
from io import StringIO
stdout = StringIO()
sys.stdout = stdout

try:
    # Execute user code
    #!/usr/bin/env python3
    import base64
    import json
    import os
    
    print("Current directory:", os.getcwd())
    print("\nLooking for files...")
    
    # Read Centric logo
    logo_found = False
    for path in ['logos/Centric_C_logo-01 (1).png', 'Centric_C_logo-01 (1).png']:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                c_logo_b64 = base64.b64encode(f.read()).decode('utf-8')
            print(f"✅ Found logo at: {path}")
            logo_found = True
            break
    
    if not logo_found:
        print("⚠️ Logo not found, using empty string")
        c_logo_b64 = ""
    
    # Read markdown content
    md_path = 'ifm/OPTIMIZATION_COMPLETE.md'
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        print(f"✅ Read markdown: {len(markdown_content)} characters")
    else:
        print(f"❌ Markdown not found at: {md_path}")
        print("Available files:", os.listdir('.'))
        raise FileNotFoundError(md_path)
    
    # Escape for JavaScript
    markdown_escaped = json.dumps(markdown_content)
    
    html_content = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IFI Team Optimization - Complete</title>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                display: flex;
                height: 100vh;
                overflow: hidden;
            }
            #sidebar {
                width: 320px;
                background: #f8f9fa;
                border-right: 1px solid #ddd;
                overflow-y: auto;
                flex-shrink: 0;
            }
            #sidebar-header {
                padding: 50px 20px 20px;
                background: #2c1a5d;
                color: white;
                position: sticky;
                top: 0;
                z-index: 10;
            }
            #sidebar-header h2 { font-size: 16px; font-weight: 600; }
            #toggle-sidebar {
                position: absolute;
                top: 15px;
                right: 15px;
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 4px;
                padding: 6px 12px;
                cursor: pointer;
                font-size: 12px;
                color: white;
            }
            #toc { list-style: none; padding: 20px; }
            #toc a {
                color: #333;
                text-decoration: none;
                display: block;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 13px;
            }
            #toc a:hover { background: #e9ecef; }
            #toc a.active {
                background: rgba(44, 26, 93, 0.1);
                color: #2c1a5d;
                font-weight: 600;
                border-left: 3px solid #fdb825;
            }
            #toc .h1 { font-weight: 600; margin-top: 12px; }
            #toc .h2 { margin-left: 15px; }
            #toc .h3 { margin-left: 30px; font-size: 12px; color: #666; }
            #content { flex: 1; overflow-y: auto; padding: 40px 80px; }
            #markdown-content { max-width: 900px; }
            #markdown-content h1 {
                color: #2c1a5d;
                border-bottom: 3px solid #fdb825;
                padding-bottom: 12px;
                margin: 40px 0 20px;
            }
            #markdown-content h2 {
                color: #2c1a5d;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 10px;
                margin: 32px 0 16px;
            }
            #markdown-content h3 { color: #2c1a5d; margin: 24px 0 12px; }
            #markdown-content table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }
            #markdown-content table th {
                background: #2c1a5d;
                color: white;
                padding: 12px;
                text-align: left;
            }
            #markdown-content table td { padding: 12px; border-bottom: 1px solid #dee2e6; }
            #markdown-content table tr:hover { background: #f8f9fa; }
            #markdown-content code {
                background: #f8f9fa;
                padding: 3px 6px;
                border-radius: 3px;
                font-family: Monaco, monospace;
                font-size: 0.9em;
                color: #e83e8c;
            }
            #markdown-content pre {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-left: 4px solid #fdb825;
                border-radius: 6px;
                padding: 20px;
                overflow-x: auto;
                margin: 20px 0;
            }
            #markdown-content pre code { background: none; padding: 0; color: inherit; }
            #back-to-top {
                position: fixed;
                bottom: 30px;
                right: 30px;
                background: #2c1a5d;
                color: white;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                opacity: 0;
                font-size: 24px;
            }
            #back-to-top.visible { opacity: 0.8; }
            #back-to-top:hover { opacity: 1; }
        </style>
    </head>
    <body>
        <div id="sidebar">
            <div id="sidebar-header">
                <button id="toggle-sidebar">Hide</button>
                <h2>IFI Team Optimization</h2>
            </div>
            <ul id="toc"></ul>
        </div>
        <div id="content">
            <div id="markdown-content"></div>
        </div>
        <div id="back-to-top">↑</div>
        <script>
            const markdownContent = ''' + markdown_escaped + ''';
            
            function initPage() {
                if (typeof marked === 'undefined') {
                    setTimeout(initPage, 100);
                    return;
                }
                marked.setOptions({ breaks: true, gfm: true });
                document.getElementById('markdown-content').innerHTML = marked.parse(markdownContent);
                if (typeof hljs !== 'undefined') {
                    document.querySelectorAll('pre code').forEach(b => hljs.highlightElement(b));
                }
                buildTOC();
                setupScrollHandlers();
            }
            
            function buildTOC() {
                const headings = document.querySelectorAll('#markdown-content h1, #markdown-content h2, #markdown-content h3');
                const toc = document.getElementById('toc');
                headings.forEach((h, i) => {
                    if (!h.id) h.id = h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + i;
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.href = '#' + h.id;
                    a.textContent = h.textContent;
                    a.className = h.tagName.toLowerCase();
                    a.addEventListener('click', (e) => {
                        e.preventDefault();
                        h.scrollIntoView({ behavior: 'smooth' });
                    });
                    li.appendChild(a);
                    toc.appendChild(li);
                });
            }
            
            function setupScrollHandlers() {
                const content = document.getElementById('content');
                const btn = document.getElementById('back-to-top');
                content.addEventListener('scroll', () => {
                    btn.classList.toggle('visible', content.scrollTop > 300);
                });
                btn.addEventListener('click', () => {
                    content.scrollTo({ top: 0, behavior: 'smooth' });
                });
            }
            
            document.getElementById('toggle-sidebar').addEventListener('click', () => {
                document.body.classList.toggle('sidebar-hidden');
                document.getElementById('toggle-sidebar').textContent = 
                    document.body.classList.contains('sidebar-hidden') ? 'Show' : 'Hide';
            });
            
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initPage);
            } else {
                initPage();
            }
        </script>
    </body>
    </html>'''
    
    output_path = 'IFI_Team_Optimization_Complete.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ HTML file created: {output_path}")
    print(f"\nTo view it:")
    print(f"1. The file is in the code output directory")
    print(f"2. Download it from the outputs")
    print(f"3. Open in your browser")
except Exception as e:
    print(f"Error executing code: {str(e)}", file=sys.stderr)

# Restore stdout and get output
sys.stdout = sys.__stdout__
output = stdout.getvalue()
print(output)  # Print to actual stdout for container capture
