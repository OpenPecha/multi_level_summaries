#!/usr/bin/env python3
"""
Generate individual summaries for each node in the Buddhist text outline using Gemini Flash 2.5 API.
"""

import json
import os
import sys
import google.generativeai as genai
from typing import Dict, Any, List
import time

# =====================================================
# CONFIGURATION - Update these paths as needed
# =====================================================
OUTLINE_PATH = "data/chojuk/chapter_1/chapter_1_outline.json"
COMMENTARY_PATH = "data/chojuk/chapter_1/chapter_1_commentary.txt"
SUMMARIES_DIR = "summaries"
# =====================================================

# Configure the Gemini API
def configure_gemini():
    """Configure Gemini API with API key from environment variable."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set it with: export GEMINI_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

def load_files(outline_path: str, commentary_path: str) -> tuple:
    """Load the outline and commentary files."""
    try:
        with open(outline_path, 'r', encoding='utf-8') as f:
            outline = json.load(f)
        
        with open(commentary_path, 'r', encoding='utf-8') as f:
            commentary = f.read()
        
        return outline, commentary
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        print(f"Please check the file paths in the CONFIGURATION section:")
        print(f"  OUTLINE_PATH = '{outline_path}'")
        print(f"  COMMENTARY_PATH = '{commentary_path}'")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in outline file: {e}")
        sys.exit(1)

def create_summary_prompt(outline: List[Dict], current_node: Dict, commentary: str) -> str:
    """Create a detailed prompt for Gemini to generate the summary in Tibetan."""
    
    # Remove verse_text_excerpt from current_node for processing
    node_for_prompt = {k: v for k, v in current_node.items() if k != 'verse_text_excerpt'}
    
    prompt = f"""
You are an expert in Buddhist philosophy and Tibetan language. I need you to generate a comprehensive summary for a specific node in a hierarchical outline of a Buddhist root text.

CONTEXT:
- This is a structured analysis of "{current_node.get('title', 'Unknown')}"
- Node level: {current_node.get('level', 'Unknown')}
- Node identifier: {current_node.get('number', 'Unknown')}
- Verses span: {current_node.get('verses_span', 'Unknown')}

FULL HIERARCHICAL OUTLINE:
{json.dumps(outline, indent=2, ensure_ascii=False)}

CURRENT NODE TO ANALYZE:
{json.dumps(node_for_prompt, indent=2, ensure_ascii=False)}

FULL COMMENTARY TEXT:
{commentary}

INSTRUCTIONS:
Generate a detailed summary in Tibetan language that includes ALL of the following elements. The response must be a valid JSON object with the exact structure shown below:

{{
  "level": "{current_node.get('number', '')}",
  "summary": {{
    "content_summary": "ཚིག་གི་དོན་བསྡུས་པ། [2-5 sentences in Tibetan explaining the main content]",
    "key_concepts": ["དམ་པའི་ཆོས། [Important concepts in Tibetan]", "བྱང་ཆུབ་སེམས། [More concepts]"],
    "transformative_goal": "སྒྱུར་བའི་དམིགས་ཡུལ། [Inner transformation goal in Tibetan]",
    "function_in_hierarchy": "རིམ་པའི་ནང་གི་བྱེད་ལས། [Role in larger structure in Tibetan]",
    "inter_node_relationships": [
      {{
        "related_node_id": "section-1.1",
        "relationship_type": "སྤུན་ཟླ། [sibling/parent/child in Tibetan]",
        "conceptual_bridge": "དོན་གྱི་སྦྲེལ་བ། [Connection explanation in Tibetan]"
      }}
    ],
    "implicit_concepts": ["ཟབ་མོའི་དོན། [Implied concepts in Tibetan]"],
    "pedagogical_strategy": "སློབ་ཁྲིད་ཀྱི་ཐབས། [Teaching approach in Tibetan]",
    "intended_impact_on_reader": "ཀློག་པ་པོར་བསམ་པའི་དམིགས་ཡུལ། [Intended reader impact in Tibetan]",
    "audience_assumptions": "ཉན་པ་པོའི་ཤེས་རྟོགས། [Assumed background knowledge in Tibetan]"
  }}
}}

IMPORTANT REQUIREMENTS:
1. ALL text content must be in Tibetan script
2. The JSON structure must be valid and exactly as shown
3. Focus on the specific node being analyzed within its hierarchical context
4. Use the commentary to understand the deeper meaning
5. Generate meaningful relationships with other nodes based on the full outline
6. Ensure the summary reflects Buddhist philosophical understanding
"""
    
    return prompt

def generate_summary(model, outline: List[Dict], current_node: Dict, commentary: str) -> Dict:
    """Generate a summary for a single node using Gemini API."""
    
    prompt = create_summary_prompt(outline, current_node, commentary)
    
    try:
        response = model.generate_content(prompt)
        
        # Clean the response text to extract JSON
        response_text = response.text.strip()
        
        # Remove any markdown formatting if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse the JSON response
        summary_data = json.loads(response_text)
        
        return summary_data
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response from Gemini for node {current_node.get('number', 'unknown')}: {e}")
        print(f"Raw response: {response.text}")
        return None
    except Exception as e:
        print(f"Error generating summary for node {current_node.get('number', 'unknown')}: {e}")
        return None

def traverse_and_generate(model, outline: List[Dict], commentary: str, summaries_dir: str):
    """Traverse the outline tree and generate summaries for each node."""
    
    def process_node(node: Dict):
        """Process a single node and its children."""
        
        # Generate level identifier for filename
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
        
        summary_file = os.path.join(summaries_dir, f"{level_id}.json")
        
        # Skip if file already exists (for resumability)
        if os.path.exists(summary_file):
            print(f"Skipping {level_id} - summary already exists")
        else:
            print(f"Generating summary for {level_id}: {node.get('title', 'No title')}")
            
            summary = generate_summary(model, outline, node, commentary)
            
            if summary:
                # Save the summary
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, ensure_ascii=False, indent=2)
                print(f"Saved summary for {level_id}")
                
                # Add a small delay to avoid rate limiting
                time.sleep(1)
            else:
                print(f"Failed to generate summary for {level_id}")
        
        # Process children
        for child in node.get('children', []):
            process_node(child)
    
    # Process each top-level node
    for node in outline:
        process_node(node)

def main():
    """Main function to orchestrate the summary generation process."""
    
    print("=== Buddhist Text Summary Generation ===")
    print(f"Outline file: {OUTLINE_PATH}")
    print(f"Commentary file: {COMMENTARY_PATH}")
    print(f"Output directory: {SUMMARIES_DIR}")
    print()
    
    # Validate file paths
    if not os.path.exists(OUTLINE_PATH):
        print(f"Error: Outline file not found: {OUTLINE_PATH}")
        print("Please update the OUTLINE_PATH variable in the script.")
        sys.exit(1)
    
    if not os.path.exists(COMMENTARY_PATH):
        print(f"Error: Commentary file not found: {COMMENTARY_PATH}")
        print("Please update the COMMENTARY_PATH variable in the script.")
        sys.exit(1)
    
    # Create summaries directory
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    
    # Configure Gemini
    print("Configuring Gemini API...")
    model = configure_gemini()
    
    # Load files
    print("Loading outline and commentary files...")
    outline, commentary = load_files(OUTLINE_PATH, COMMENTARY_PATH)
    
    print(f"Loaded outline with {len(outline)} top-level nodes")
    print(f"Commentary length: {len(commentary)} characters")
    
    # Generate summaries
    print("\nStarting summary generation...")
    traverse_and_generate(model, outline, commentary, SUMMARIES_DIR)
    
    print("\nSummary generation complete!")
    print(f"Check the '{SUMMARIES_DIR}' directory for generated summaries.")

if __name__ == "__main__":
    main() 