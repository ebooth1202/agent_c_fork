
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
    import os
    import json
    
    # Check input files
    print("Input files available:")
    for root, dirs, files in os.walk('/workspace_files'):
        for file in files:
            filepath = os.path.join(root, file)
            print(f"  {filepath}")
except Exception as e:
    print(f"Error executing code: {str(e)}", file=sys.stderr)

# Restore stdout and get output
sys.stdout = sys.__stdout__
output = stdout.getvalue()
print(output)  # Print to actual stdout for container capture
