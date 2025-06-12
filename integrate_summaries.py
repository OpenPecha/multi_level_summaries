#!/usr/bin/env python3
"""
Integrate individual summaries back into the hierarchical outline structure.
"""

import json
import os
import sys
from typing import Dict, Any, List

# =====================================================
# CONFIGURATION - Update these paths as needed
# =====================================================
OUTLINE_PATH = "data/chojuk/chapter_1/chapter_1_outline.json"
SUMMARIES_DIR = "summaries"
OUTPUT_PATH = "annotated_outline.json"
# =====================================================

def load_outline(outline_path: str) -> List[Dict]:
    """Load the original outline file."""
    try:
        with open(outline_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Outline file not found: {outline_path}")
        print("Please update the OUTLINE_PATH variable in the script.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in outline file: {e}")
        sys.exit(1)

def load_summary(summaries_dir: str, level_id: str) -> Dict:
    """Load a summary file for a specific level."""
    summary_file = os.path.join(summaries_dir, f"{level_id}.json")
    
    if not os.path.exists(summary_file):
        print(f"Warning: Summary file not found for {level_id}")
        return None
    
    try:
        with open(summary_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in summary file {summary_file}: {e}")
        return None

def generate_level_id(node: Dict) -> str:
    """Generate the level identifier used for summary filenames."""
    level_id = node.get('number', '').replace('.', '-')
    
    if node.get('level') == 'chapter':
        level_id = f"chapter-{level_id}"
    elif node.get('level') == 'section':
        level_id = f"section-{level_id}"
    elif node.get('level') == 'subsection':
        level_id = f"subsection-{level_id}"
    elif node.get('level') == 'sub-subsection':
        level_id = f"sub-subsection-{level_id}"
    elif node.get('level') == 'sub-sub-subsection':
        level_id = f"sub-sub-subsection-{level_id}"
    elif node.get('level') == 'sub-sub-sub-subsection':
        level_id = f"sub-sub-sub-subsection-{level_id}"
    
    return level_id

def integrate_summaries(outline: List[Dict], summaries_dir: str) -> List[Dict]:
    """Integrate summaries into the outline structure."""
    
    def process_node(node: Dict) -> Dict:
        """Process a single node and its children."""
        # Create a copy of the node to avoid modifying the original
        processed_node = {}
        
        # Copy all fields except verse_text_excerpt
        for key, value in node.items():
            if key != 'verse_text_excerpt':
                processed_node[key] = value
        
        # Generate level identifier
        level_id = generate_level_id(node)
        
        # Load and integrate summary
        summary_data = load_summary(summaries_dir, level_id)
        
        if summary_data:
            # Add the summary to the node
            processed_node['summary'] = summary_data.get('summary', {})
            print(f"Integrated summary for {level_id}")
        else:
            print(f"No summary found for {level_id}, skipping...")
        
        # Process children recursively
        if 'children' in processed_node and processed_node['children']:
            processed_node['children'] = [process_node(child) for child in processed_node['children']]
        
        return processed_node
    
    # Process all top-level nodes
    return [process_node(node) for node in outline]

def save_annotated_outline(annotated_outline: List[Dict], output_path: str):
    """Save the annotated outline to a file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(annotated_outline, f, ensure_ascii=False, indent=2)
        print(f"Annotated outline saved to: {output_path}")
    except Exception as e:
        print(f"Error saving annotated outline: {e}")
        sys.exit(1)

def count_nodes(outline: List[Dict]) -> int:
    """Count the total number of nodes in the outline."""
    def count_node(node: Dict) -> int:
        count = 1  # Count the current node
        for child in node.get('children', []):
            count += count_node(child)
        return count
    
    return sum(count_node(node) for node in outline)

def count_summaries(summaries_dir: str) -> int:
    """Count the number of summary files in the summaries directory."""
    if not os.path.exists(summaries_dir):
        return 0
    
    json_files = [f for f in os.listdir(summaries_dir) if f.endswith('.json')]
    return len(json_files)

def validate_structure(outline: List[Dict]) -> bool:
    """Validate that the outline structure is correct."""
    
    def validate_node(node: Dict, path: str = "") -> bool:
        current_path = f"{path}/{node.get('number', 'unknown')}"
        
        # Check required fields
        required_fields = ['level', 'number', 'title']
        for field in required_fields:
            if field not in node:
                print(f"Error: Missing required field '{field}' in node {current_path}")
                return False
        
        # Check children structure
        if 'children' in node:
            if not isinstance(node['children'], list):
                print(f"Error: 'children' field must be a list in node {current_path}")
                return False
            
            for i, child in enumerate(node['children']):
                if not validate_node(child, current_path):
                    return False
        
        return True
    
    for i, node in enumerate(outline):
        if not validate_node(node, f"root[{i}]"):
            return False
    
    return True

def print_integration_stats(original_count: int, summaries_count: int, annotated_outline: List[Dict]):
    """Print statistics about the integration process."""
    
    def count_nodes_with_summaries(nodes: List[Dict]) -> int:
        count = 0
        for node in nodes:
            if 'summary' in node:
                count += 1
            count += count_nodes_with_summaries(node.get('children', []))
        return count
    
    integrated_count = count_nodes_with_summaries(annotated_outline)
    
    print("\n" + "="*50)
    print("INTEGRATION STATISTICS")
    print("="*50)
    print(f"Total nodes in outline: {original_count}")
    print(f"Summary files found: {summaries_count}")
    print(f"Nodes with integrated summaries: {integrated_count}")
    print(f"Integration rate: {integrated_count/original_count*100:.1f}%")
    
    if integrated_count < original_count:
        print(f"\nNote: {original_count - integrated_count} nodes are missing summaries.")
        print("You may need to run generate_summaries.py again for missing nodes.")

def main():
    """Main function to orchestrate the integration process."""
    
    print("=== Buddhist Text Summary Integration ===")
    print(f"Outline file: {OUTLINE_PATH}")
    print(f"Summaries directory: {SUMMARIES_DIR}")
    print(f"Output file: {OUTPUT_PATH}")
    print()
    
    # Validate inputs
    if not os.path.exists(OUTLINE_PATH):
        print(f"Error: Outline file not found: {OUTLINE_PATH}")
        print("Please update the OUTLINE_PATH variable in the script.")
        sys.exit(1)
    
    if not os.path.exists(SUMMARIES_DIR):
        print(f"Error: Summaries directory not found: {SUMMARIES_DIR}")
        print("Please run generate_summaries.py first to create the summary files.")
        print("Or update the SUMMARIES_DIR variable in the script.")
        sys.exit(1)
    
    # Load the original outline
    print("Loading original outline...")
    outline = load_outline(OUTLINE_PATH)
    
    # Validate outline structure
    print("Validating outline structure...")
    if not validate_structure(outline):
        print("Error: Invalid outline structure detected.")
        sys.exit(1)
    
    # Count nodes and summaries
    original_count = count_nodes(outline)
    summaries_count = count_summaries(SUMMARIES_DIR)
    
    print(f"Found {original_count} nodes in outline")
    print(f"Found {summaries_count} summary files")
    
    # Integrate summaries
    print("\nIntegrating summaries into outline...")
    annotated_outline = integrate_summaries(outline, SUMMARIES_DIR)
    
    # Save the result
    print(f"\nSaving annotated outline to {OUTPUT_PATH}...")
    save_annotated_outline(annotated_outline, OUTPUT_PATH)
    
    # Print statistics
    print_integration_stats(original_count, summaries_count, annotated_outline)
    
    print(f"\nIntegration complete! Check {OUTPUT_PATH} for the final result.")

if __name__ == "__main__":
    main() 