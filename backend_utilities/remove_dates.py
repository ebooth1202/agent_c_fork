#!/usr/bin/env python3
"""
Script to remove date entries from markdown files.
Finds patterns like '**Date**: 2025-01-20' and removes them.
"""

import re
from pathlib import Path


# List of date entry prefixes to search for and remove
# Add new entries here as needed
DATE_PATTERNS = [
    'Date',
    'Last Updated',
    'Created',
    'Modified',
]


def remove_dates_from_file(file_path):
    """Remove date patterns from a markdown file."""
    try:
        # Read the file content
        content = file_path.read_text(encoding='utf-8')
        modified_content = content

        # Build pattern from the list
        # Matches: '**Date**: 2024-01-15', 'Date: 2024', etc.
        for prefix in DATE_PATTERNS:
            # Escape any special regex characters in the prefix
            escaped_prefix = re.escape(prefix)
            # Pattern: optional bold (**), prefix, optional bold (**), colon, date
            pattern = rf'\*?\*?{escaped_prefix}\*?\*?:\s*\d{{4}}(?:-\d{{2}}-\d{{2}})?'
            modified_content = re.sub(pattern, '', modified_content)

        # Only write if content changed
        if modified_content != content:
            file_path.write_text(modified_content, encoding='utf-8')
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all markdown files."""
    # Start from current directory
    root_dir = Path('.')

    # Find all .md files recursively
    md_files = list(root_dir.rglob('*.md'))

    if not md_files:
        print("No markdown files found.")
        return

    print(f"Found {len(md_files)} markdown files.")

    modified_count = 0
    for md_file in md_files:
        if remove_dates_from_file(md_file):
            print(f"Modified: {md_file}")
            modified_count += 1

    print(f"\nProcessed {len(md_files)} files, modified {modified_count} files.")


if __name__ == '__main__':
    main()
