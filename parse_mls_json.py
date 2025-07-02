import json
import argparse

def display_summary_outline(node, indent_level=0):
    """
    Recursively parses a node from the MLS JSON and prints its outline.
    """
    if not isinstance(node, dict):
        return
        
    indent = "    " * indent_level
    print(f"{indent}- {node.get('level', 'N/A')} {node.get('number', '')}: {node.get('title', 'No Title')} ({node.get('verses_span', 'N/A')})")

    children = node.get('children', [])
    for child in children:
        display_summary_outline(child, indent_level + 1)

def main():
    """
    Main function to load the JSON file and start the parsing.
    """
    parser = argparse.ArgumentParser(
        description="A script to parse a Multi-Level Summary (MLS) JSON file and display its hierarchical outline."
    )
    parser.add_argument(
        "json_file",
        help="Path to the MLS JSON file to parse.",
        default="data/chojuk/combined_MLS_en.json",
        nargs="?" # Make the argument optional, with a default.
    )
    args = parser.parse_args()

    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            mls_data = json.load(f)
        
        print(f"Parsing outline for: {args.json_file}\n")
        if isinstance(mls_data, list):
            for item in mls_data:
                display_summary_outline(item)
        else:
            display_summary_outline(mls_data)

    except FileNotFoundError:
        print(f"Error: File not found at '{args.json_file}'")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{args.json_file}'. Please check file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 