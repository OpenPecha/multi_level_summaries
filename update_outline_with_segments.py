#!/usr/bin/env python3
"""
Script to update outline JSON file with segment text from root text file.

Usage: python update_outline_with_segments.py
"""

import json
import sys
from pathlib import Path


def read_root_text(file_path):
    """Read the root text file and return list of lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Remove trailing newlines but preserve the text
        return [line.rstrip('\n') for line in lines]
    except FileNotFoundError:
        print(f"Error: Root text file '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading root text file: {e}")
        sys.exit(1)


def extract_segment_text(root_lines, segments_span):
    """
    Extract text from root_lines based on segments_span.
    
    Args:
        root_lines: List of text lines from root file
        segments_span: String like "1-12" or "4-4"
    
    Returns:
        String containing the extracted segment text
    """
    if not segments_span:
        return ""
    
    try:
        # Parse the span (e.g., "1-12" -> start=1, end=12)
        start_str, end_str = segments_span.split('-')
        start = int(start_str)
        end = int(end_str)
        
        # Convert to 0-based indexing for Python lists
        start_idx = start - 1
        end_idx = end - 1
        
        # Validate indices
        if start_idx < 0 or end_idx >= len(root_lines) or start_idx > end_idx:
            print(f"Warning: Invalid span '{segments_span}' for text with {len(root_lines)} lines")
            return ""
        
        # Extract the text
        segment_lines = root_lines[start_idx:end_idx + 1]
        return '\n'.join(segment_lines)
        
    except ValueError as e:
        print(f"Warning: Could not parse segments_span '{segments_span}': {e}")
        return ""
    except Exception as e:
        print(f"Warning: Error extracting segment '{segments_span}': {e}")
        return ""


def update_node_with_segment_text(node, root_lines):
    """
    Recursively update a node and its children with segment_text field.
    
    Args:
        node: Dictionary representing a node in the outline
        root_lines: List of text lines from root file
    """
    # Add segment_text field to current node
    if 'segments_span' in node:
        segment_text = extract_segment_text(root_lines, node['segments_span'])
        node['segment_text'] = segment_text
    else:
        node['segment_text'] = ""
    
    # Recursively process children
    if 'children' in node:
        for child in node['children']:
            update_node_with_segment_text(child, root_lines)


def update_outline_with_segments(outline_path, root_text_path):
    """
    Main function to update outline JSON with segment text.
    
    Args:
        outline_path: Path to the outline JSON file
        root_text_path: Path to the root text file
    """
    # Read the root text file
    print(f"Reading root text from: {root_text_path}")
    root_lines = read_root_text(root_text_path)
    print(f"Loaded {len(root_lines)} lines from root text file")
    
    # Read the outline JSON file
    print(f"Reading outline from: {outline_path}")
    try:
        with open(outline_path, 'r', encoding='utf-8') as f:
            outline_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Outline file '{outline_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in outline file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading outline file: {e}")
        sys.exit(1)
    
    print(f"Loaded outline with {len(outline_data)} top-level nodes")
    
    # Update each top-level node
    print("Updating nodes with segment text...")
    for node in outline_data:
        update_node_with_segment_text(node, root_lines)
    
    # Write the updated outline back to the file
    print(f"Writing updated outline to: {outline_path}")
    try:
        with open(outline_path, 'w', encoding='utf-8') as f:
            json.dump(outline_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing updated outline file: {e}")
        sys.exit(1)
    
    print("✓ Successfully updated outline with segment text!")


def main():
    """Main entry point."""
    # Define file paths
    outline_path = Path("./data/diamond_sutra/outline_bo.json")
    root_text_path = Path("./data/diamond_sutra/root_bo.txt")
    
    # Check if files exist
    if not outline_path.exists():
        print(f"Error: Outline file '{outline_path}' does not exist.")
        sys.exit(1)
    
    if not root_text_path.exists():
        print(f"Error: Root text file '{root_text_path}' does not exist.")
        sys.exit(1)
    
    # Update the outline
    update_outline_with_segments(outline_path, root_text_path)


if __name__ == "__main__":
    main() 