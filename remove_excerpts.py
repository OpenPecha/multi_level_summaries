import json
from pathlib import Path

def remove_verse_excerpts_recursive(node):
    """
    Recursively traverses the JSON structure and removes the 'verse_text_excerpt' key
    from each dictionary (node) if it exists.
    Modifies the node in place.
    """
    if isinstance(node, dict):
        if "verse_text_excerpt" in node:
            del node["verse_text_excerpt"]
        
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                remove_verse_excerpts_recursive(child)
    elif isinstance(node, list):
        for item in node:
            remove_verse_excerpts_recursive(item)

def main():
    target_file_path_str = "/Users/tenzingayche/Desktop/multi_level_summaries/data/chapter_nine/chapter_one/multilevel_tree_chapter_1.json"
    target_file_path = Path(target_file_path_str)

    if not target_file_path.exists():
        print(f"Error: File not found: {target_file_path}")
        return

    try:
        print(f"Reading JSON data from: {target_file_path}")
        original_data_str = target_file_path.read_text(encoding='utf-8')
        data = json.loads(original_data_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {target_file_path}: {e}")
        return
    except Exception as e:
        print(f"Error reading {target_file_path}: {e}")
        return

    print("Removing 'verse_text_excerpt' fields...")
    remove_verse_excerpts_recursive(data) # Process the data (could be a list or dict at root)

    try:
        print(f"Writing modified JSON data back to: {target_file_path}")
        with open(target_file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Successfully removed 'verse_text_excerpt' fields and updated the file.")
    except Exception as e:
        print(f"Error writing updated JSON to {target_file_path}: {e}")

if __name__ == "__main__":
    main()
