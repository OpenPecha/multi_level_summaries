import json
from pathlib import Path

def process_node_recursive(node):
    """
    Recursively traverses the outline tree and modifies it in place:
    - If a node is a leaf node, leaves it as is
    - If a node has children, combines all verse_text_excerpt from its descendants
      and adds it to the node with the key "verse_text_excerpt"
    - Ensures verse_text_excerpt appears before children in the output JSON
    
    Args:
        node (dict): The current node in the outline tree to process.
        
    Returns:
        bool: True if this node or any of its descendants has verse text, False otherwise.
    """
    # Check if this node has children
    if "children" in node and node["children"]:
        # This is a parent node
        has_text = False
        all_verse_texts = []
        
        # Process all children first (depth-first traversal)
        for child in node["children"]:
            child_has_text = process_node_recursive(child)
            has_text = has_text or child_has_text
            
            # If child has verse_text_excerpt, collect it
            if child_has_text and "verse_text_excerpt" in child and child["verse_text_excerpt"]:
                all_verse_texts.append(child["verse_text_excerpt"].strip())
        
        # Combine all collected verse texts for this parent node
        if all_verse_texts:
            # Store verse_text_excerpt to add it in the correct position later
            verse_text = "\n\n".join(all_verse_texts)
            has_text = True
        else:
            verse_text = None
        
        # To ensure verse_text_excerpt appears before children in the output,
        # we need to reorder the node dictionary
        if has_text:
            # Create a new ordered dictionary with the desired field order
            reordered_node = {}
            
            # Copy all fields except 'children' and 'verse_text_excerpt'
            for key, value in node.items():
                if key != "children" and key != "verse_text_excerpt":
                    reordered_node[key] = value
            
            # Add verse_text_excerpt before children
            if verse_text:
                reordered_node["verse_text_excerpt"] = verse_text
            
            # Add children at the end
            if "children" in node:
                reordered_node["children"] = node["children"]
            
            # Replace the node's contents with our reordered version
            # This is a bit of a hack but works because we're modifying the dict in-place
            node.clear()
            node.update(reordered_node)
        
        return has_text
    else:
        # This is a leaf node, leave it as is
        return "verse_text_excerpt" in node and bool(node["verse_text_excerpt"])

def process_outline_json(input_json_data):
    """
    Processes the input JSON outline and modifies it in place to add verse_text_excerpt
    to each parent node by combining text from its children.

    Args:
        input_json_data (list): The parsed JSON data (list of chapters).

    Returns:
        list: The modified JSON data with verse_text_excerpt added to parent nodes.
    """
    # Create a deep copy to avoid modifying the input directly (if needed)
    # processed_data = copy.deepcopy(input_json_data)
    
    # Process each chapter
    for chapter in input_json_data:
        process_node_recursive(chapter)
    
    return input_json_data

if __name__ == "__main__":
    chapter_dirs = list(Path("./data/chojuk").iterdir())
    chapter_dirs.sort()

    for chapter_dir in chapter_dirs:
        chapter_outline_file = chapter_dir / "outline_bo.json"
        output_file_name = chapter_dir / "updated_outline_with_verses_bo.json"
    
        try:
            # Read the input JSON file
            print(f"Reading outline from {chapter_outline_file}...")
            outline_data_str = chapter_outline_file.read_text(encoding='utf-8')
            outline_data = json.loads(outline_data_str)
            
            # Process the outline, adding verse_text_excerpt to parent nodes
            print("Processing outline and combining verses for parent nodes...")
            processed_outline = process_outline_json(outline_data)
            
            # Save the updated outline with verse_text_excerpt at all levels
            with open(output_file_name, "w", encoding='utf-8') as f:
                json.dump(processed_outline, f, indent=2, ensure_ascii=False)
            
            print(f"Updated outline with combined verses saved to '{output_file_name}'")
            
        except Exception as e:
            print(f"Error processing outline: {str(e)}")

    # text_dir = Path('./data/Phadoe/')

    # text_outline_file = text_dir / "outline_bo.json"
    # output_file_name = text_dir / "updated_outline_with_verses_bo.json"

    # try:
    #     # Read the input JSON file
    #     print(f"Reading outline from {text_outline_file}...")
    #     outline_data_str = text_outline_file.read_text(encoding='utf-8')
    #     outline_data = json.loads(outline_data_str)
        
    #     # Process the outline, adding verse_text_excerpt to parent nodes
    #     print("Processing outline and combining verses for parent nodes...")
    #     processed_outline = process_outline_json(outline_data)
        
    #     # Save the updated outline with verse_text_excerpt at all levels
    #     with open(output_file_name, "w", encoding='utf-8') as f:
    #         json.dump(processed_outline, f, indent=2, ensure_ascii=False)
        
    #     print(f"Updated outline with combined verses saved to '{output_file_name}'")
        
    # except Exception as e:
    #     print(f"Error processing outline: {str(e)}")