import json

from pathlib import Path

def extract_parent_verses(node, parent_data_list):
    """
    Recursively traverses the outline tree, extracts verse_text_excerpt from leaf nodes,
    and combines them for their parent nodes.

    Args:
        node (dict): The current node in the outline tree.
        parent_data_list (list): A list to store the extracted data for parent nodes.
    """
    if "children" in node and node["children"]:
        # This is a parent node. Collect its metadata.
        parent_info = {
            "level": node.get("level"),
            "number": node.get("number"),
            "title": node.get("title"),
            "verses_span": node.get("verses_span")
        }
        
        combined_text = []
        # Recursively call for children to collect their verse excerpts
        for child in node["children"]:
            # If the child is a leaf node, add its verse_text_excerpt
            if not child.get("children"): # Check if it's a leaf node
                if child.get("verse_text_excerpt"):
                    combined_text.append(child["verse_text_excerpt"])
            else:
                # If the child is also a parent, we need to collect its descendants' texts.
                # A temporary list to capture texts from this child's subtree
                temp_child_texts = []
                collect_leaf_texts(child, temp_child_texts)
                combined_text.extend(temp_child_texts)

        if combined_text:
            parent_info["combined_verse_text_excerpt"] = "\n\n".join(combined_text)
            parent_data_list.append(parent_info)

        # Continue traversal for all children, regardless of whether they are leaves or parents
        for child in node["children"]:
            extract_parent_verses(child, parent_data_list)

def collect_leaf_texts(node, text_list):
    """
    Helper function to collect all verse_text_excerpt from leaf nodes within a subtree.
    """
    if not node.get("children"): # It's a leaf node
        if node.get("verse_text_excerpt"):
            text_list.append(node["verse_text_excerpt"])
    else: # It's a parent node, recurse
        for child in node["children"]:
            collect_leaf_texts(child, text_list)


def process_outline_json(input_json_data):
    """
    Processes the input JSON outline to extract parent node metadata and combined verse texts.

    Args:
        input_json_data (list): The parsed JSON data (list of chapters).

    Returns:
        list: A list of dictionaries, each containing parent node metadata and combined verse text.
    """
    extracted_data = []
    for chapter in input_json_data:
        extract_parent_verses(chapter, extracted_data)
    return extracted_data



if __name__ =="__main__":
    outline_data_str = Path('./data/chapter_one/chapter_1_outline.json').read_text()
    outline_data = json.loads(outline_data_str)
    processed_output = process_outline_json(outline_data)

    # Save the processed data to a new JSON file
    output_file_name = "parent_nodes_with_verses.json"
    with open(output_file_name, "w") as f:
        json.dump(processed_output, f, indent=2)

    print(f"Extracted parent node data and combined verse excerpts saved to '{output_file_name}'")
    