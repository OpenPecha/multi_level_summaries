import json
import os
import argparse
import re

def get_chapter_number(dir_name):
    """Extracts the chapter number from a directory name like 'chapter_1'."""
    match = re.search(r'\d+', dir_name)
    return int(match.group()) if match else float('inf')

def get_chapter_verse_count(node):
    """Extracts the total number of verses from the top-level node of a chapter."""
    if isinstance(node, list):
        if not node:
            return 0
        node = node[0]
    if isinstance(node, dict) and 'verses_span' in node:
        span = node['verses_span']
        try:
            if '-' in span:
                parts = span.split('-')
                # Handle cases like '1-36'
                if len(parts) == 2:
                    return int(parts[1])
            else:
                # Handle cases like '1'
                return int(span)
        except (ValueError, IndexError):
            print(f"Warning: Could not parse top-level verses_span '{span}' for verse count.")
            return 0
    return 0

def update_verse_spans_recursively(node, offset):
    """
    Recursively traverses a dictionary or list, updating 'verses_span'
    and adding 'global_verses_span' with a cumulative offset.
    """
    if isinstance(node, dict):
        if 'verses_span' in node:
            original_span = node['verses_span']
            try:
                if '-' in original_span:
                    start, end = map(int, original_span.split('-'))
                    new_start = start + offset
                    new_end = end + offset
                    new_span = f"{new_start}-{new_end}"
                else:
                    start = int(original_span)
                    new_start = start + offset
                    new_span = str(new_start)
                
                node['verses_span'] = new_span
                node['global_verses_span'] = new_span
            except ValueError:
                print(f"Warning: Could not parse verses_span '{original_span}'. Skipping update.")

        if 'children' in node:
            update_verse_spans_recursively(node['children'], offset)

    elif isinstance(node, list):
        for item in node:
            update_verse_spans_recursively(item, offset)


def combine_mls_files(root_dir, output_file):
    """
    Finds all MLS_en.json files in subdirectories of root_dir, combines them,
    and writes to output_file with cumulative verse spans.
    """
    combined_data = []
    verse_offset = 0
    
    # Get subdirectories and sort them by chapter number
    try:
        subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
        sorted_subdirs = sorted(subdirs, key=get_chapter_number)
    except FileNotFoundError:
        print(f"Error: Directory not found at '{root_dir}'")
        return

    for subdir in sorted_subdirs:
        mls_path = os.path.join(root_dir, subdir, 'MLS_en.json')
        if os.path.exists(mls_path):
            try:
                with open(mls_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Get verse count for the current chapter before modification
                chapter_verse_count = get_chapter_verse_count(data)

                # Recursively update verse spans with the current offset
                update_verse_spans_recursively(data, verse_offset)
                
                # Handle cases where the data might be in a list
                if isinstance(data, list) and len(data) > 0:
                    # Assuming we should take the first element if it's a list
                    combined_data.append(data[0])
                elif isinstance(data, dict):
                    combined_data.append(data)
                else:
                    print(f"Warning: Unexpected data format in {mls_path}. Skipping.")
                    continue
                
                # Update the offset for the next chapter
                verse_offset += chapter_verse_count

                print(f"Successfully processed and loaded: {mls_path}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {mls_path}: {e}")
        else:
            print(f"Warning: 'MLS_en.json' not found in '{os.path.join(root_dir, subdir)}'. Skipping.")

    if not combined_data:
        print("No data was combined. Exiting.")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=4, ensure_ascii=False)
        print(f"\nSuccessfully combined {len(combined_data)} files into '{output_file}'")
    except Exception as e:
        print(f"Error: Could not write the combined file to '{output_file}': {e}")


def main():
    """
    Main function to parse arguments and run the combination script.
    """
    parser = argparse.ArgumentParser(
        description="A script to combine multiple MLS_en.json files from chapter subdirectories into a single file, creating cumulative verse spans."
    )
    parser.add_argument(
        "root_dir",
        help="The root directory containing chapter subfolders (e.g., 'data/chojuk').",
        default="data/chojuk",
        nargs="?"
    )
    parser.add_argument(
        "--output_file",
        "-o",
        help="Path for the combined output JSON file.",
        default=None
    )
    args = parser.parse_args()

    output_file = args.output_file
    if not output_file:
        output_file = os.path.join(args.root_dir, "combined_MLS_en.json")
    
    combine_mls_files(args.root_dir, output_file)


if __name__ == "__main__":
    main() 