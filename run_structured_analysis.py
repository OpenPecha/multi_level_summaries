#!/usr/bin/env python3
"""
Multi-Level Summary (MLS) extractor using dynamic prompt composition.
Combines outline JSON, commentary text, and prompt template to generate
hierarchical analysis of Buddhist root texts with Tibetan summaries.
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

# =====================================================
# CONFIGURATION - Update these paths as needed
# =====================================================
PROMPT_TEMPLATE_FILE = "data/prompts/multi-level-summary-extractor-prompt.md"
OUTLINE_JSON_FILE = "data/chojuk/chapter_1/updated_outline_with_verses.json"
COMMENTARY_TEXT_FILE = "data/chojuk/chapter_1/chapter_1_commentary.txt"
OUTPUT_FILE = "MLS.json"
# =====================================================

# Pydantic Models for Structured Output
class InterNodeRelationship(BaseModel):
    """Model for relationships between nodes in the hierarchy."""
    related_node_id: str = Field(description="Identifier of the related node")
    relationship_type: str = Field(description="Type of relationship in Tibetan")
    conceptual_bridge: str = Field(description="Description of the conceptual connection in Tibetan")

class Summary(BaseModel):
    """Model for node summary with all required fields in Tibetan."""
    content_summary: str = Field(description="Concise summary (2-5 sentences) of core content in Tibetan")
    key_concepts: List[str] = Field(description="Primary philosophical terms or practices in Tibetan")
    transformative_goal: str = Field(description="Primary inner transformation this unit aims to facilitate in Tibetan")
    function_in_hierarchy: str = Field(description="Role and purpose within the broader structure in Tibetan")
    inter_node_relationships: List[InterNodeRelationship] = Field(description="Connections to related nodes")
    implicit_concepts: List[str] = Field(description="Unstated but implied concepts in Tibetan")
    pedagogical_strategy: str = Field(description="Teaching method employed in this unit in Tibetan")
    intended_impact_on_reader: str = Field(description="Desired impact on reader in Tibetan")
    audience_assumptions: str = Field(description="Assumed background knowledge in Tibetan")

class Node(BaseModel):
    """Model for a hierarchical node with summary."""
    level: str = Field(description="Level type (chapter, section, subsection, etc.)")
    number: str = Field(description="Node number/identifier")
    title: str = Field(description="Node title")
    verses_span: Optional[str] = Field(default=None, description="Verse range for this node")
    children: List['Node'] = Field(default_factory=list, description="Child nodes")
    summary: Summary = Field(description="Generated summary for this node")

# Allow forward references
Node.model_rebuild()

class AnalysisState(BaseModel):
    """State for the LangGraph workflow."""
    prompt_template: str = Field(description="The prompt template")
    outline_json: str = Field(description="The outline JSON content")
    commentary_text: str = Field(description="The commentary text content")
    final_prompt: str = Field(description="The combined prompt ready for LLM")
    result_nodes: List[Node] = Field(default_factory=list, description="Final processed nodes with summaries")
    error_message: Optional[str] = Field(default=None, description="Any error that occurred")

def configure_llm():
    """Configure the LLM for LangChain."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set it with: export GEMINI_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        google_api_key=api_key,
        temperature=0.1,
        top_p=0.8,
        top_k=20,
        max_output_tokens=65536
    )

def load_input_files(state: AnalysisState) -> AnalysisState:
    """Load prompt template, outline JSON, and commentary text."""
    print("📁 Loading input files...")
    
    try:
        # Load prompt template
        with open(PROMPT_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        print(f"✅ Loaded prompt template ({len(prompt_template)} characters)")
        
        # Load outline JSON
        with open(OUTLINE_JSON_FILE, 'r', encoding='utf-8') as f:
            outline_content = f.read()
        print(f"✅ Loaded outline JSON ({len(outline_content)} characters)")
        
        # Load commentary text
        with open(COMMENTARY_TEXT_FILE, 'r', encoding='utf-8') as f:
            commentary_text = f.read()
        print(f"✅ Loaded commentary text ({len(commentary_text)} characters)")
        
        return AnalysisState(
            prompt_template=prompt_template,
            outline_json=outline_content,
            commentary_text=commentary_text,
            final_prompt=""
        )
        
    except FileNotFoundError as e:
        return AnalysisState(
            prompt_template="",
            outline_json="",
            commentary_text="",
            final_prompt="",
            error_message=f"File not found: {e.filename}"
        )
    except Exception as e:
        return AnalysisState(
            prompt_template="",
            outline_json="",
            commentary_text="",
            final_prompt="",
            error_message=f"Failed to load files: {str(e)}"
        )

def compose_prompt(state: AnalysisState) -> AnalysisState:
    """Combine outline JSON and commentary text into the prompt template."""
    if state.error_message:
        return state
    
    print("🔧 Composing final prompt...")
    
    try:
        # Replace placeholders in prompt template
        # Assuming the template has placeholders like {{OUTLINE_JSON}} and {{COMMENTARY_TEXT}}
        final_prompt = state.prompt_template
        
        # If template has specific placeholders, replace them
        if "{{OUTLINE_JSON}}" in final_prompt:
            final_prompt = final_prompt.replace("{{OUTLINE_JSON}}", state.outline_json)
        elif "## **Chapter Structure:**" in final_prompt:
            # Replace the JSON block in the existing template
            start_marker = "```json"
            end_marker = "```\n\n## **Chapter Commentary:**"
            start_idx = final_prompt.find(start_marker)
            end_idx = final_prompt.find(end_marker)
            if start_idx > -1 and end_idx > -1:
                final_prompt = (final_prompt[:start_idx + len(start_marker) + 1] + 
                              state.outline_json + 
                              final_prompt[end_idx:])
        
        if "{{COMMENTARY_TEXT}}" in final_prompt:
            final_prompt = final_prompt.replace("{{COMMENTARY_TEXT}}", state.commentary_text)
        elif "## **Chapter Commentary:**" in final_prompt:
            # Replace the commentary section
            start_marker = "## **Chapter Commentary:**"
            end_marker = "## **Task:**"
            start_idx = final_prompt.find(start_marker)
            end_idx = final_prompt.find(end_marker)
            if start_idx > -1 and end_idx > -1:
                final_prompt = (final_prompt[:start_idx + len(start_marker) + 2] + 
                              state.commentary_text + 
                              "\n\n" + final_prompt[end_idx:])
        
        state.final_prompt = final_prompt
        print(f"✅ Composed final prompt ({len(final_prompt)} characters)")
        
    except Exception as e:
        state.error_message = f"Error composing prompt: {str(e)}"
        print(f"❌ {state.error_message}")
    
    return state

def generate_analysis(state: AnalysisState) -> AnalysisState:
    """Generate the complete hierarchical analysis using the composed prompt."""
    if state.error_message:
        return state
    
    print("🤖 Generating comprehensive analysis with Gemini 2.5 Pro...")
    llm = configure_llm()
    
    try:
        message = HumanMessage(content=state.final_prompt)
        response = llm.invoke([message])
        
        # Parse the JSON response
        response_text = response.content.strip()
        print(f"📄 Received response ({len(response_text)} characters)")
        
        # Clean JSON formatting
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        elif response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse the JSON response
        try:
            analysis_data = json.loads(response_text)
            
            # Convert to Node models with validation
            result_nodes = []
            for node_data in analysis_data:
                node = Node(**node_data)
                result_nodes.append(node)
            
            state.result_nodes = result_nodes
            print("✅ Analysis generation and validation complete")
            
        except json.JSONDecodeError as e:
            state.error_message = f"Invalid JSON response: {e}"
            print(f"❌ JSON parsing error: {e}")
            print("📝 Response preview:", response_text[:500])
        except Exception as e:
            state.error_message = f"Validation error: {e}"
            print(f"❌ Pydantic validation error: {e}")
            
    except Exception as e:
        state.error_message = f"Error calling LLM: {str(e)}"
        print(f"❌ LLM error: {e}")
    
    return state

def save_output(state: AnalysisState) -> AnalysisState:
    """Save the structured output to MLS.json file."""
    if state.error_message:
        print(f"❌ Cannot save due to error: {state.error_message}")
        return state
    
    print(f"💾 Saving Multi-Level Summary to {OUTPUT_FILE}...")
    
    try:
        # Convert to dict for JSON serialization
        output_data = [node.model_dump() for node in state.result_nodes]
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Multi-Level Summary saved successfully to: {OUTPUT_FILE}")
        
        # Print summary statistics
        total_nodes = sum(count_nodes(node) for node in state.result_nodes)
        print(f"📊 Generated summaries for {total_nodes} nodes across the hierarchy")
        
    except Exception as e:
        state.error_message = f"Error saving output: {str(e)}"
        print(f"❌ {state.error_message}")
    
    return state

def count_nodes(node: Node) -> int:
    """Recursively count all nodes in the hierarchy."""
    count = 1  # Count this node
    for child in node.children:
        count += count_nodes(child)
    return count

def create_workflow() -> CompiledStateGraph:
    """Create and compile the LangGraph workflow."""
    
    # Create the graph
    workflow = StateGraph(AnalysisState)
    
    # Add nodes
    workflow.add_node("load_input_files", load_input_files)
    workflow.add_node("compose_prompt", compose_prompt)
    workflow.add_node("generate_analysis", generate_analysis)
    workflow.add_node("save_output", save_output)
    
    # Add edges
    workflow.add_edge("load_input_files", "compose_prompt")
    workflow.add_edge("compose_prompt", "generate_analysis")
    workflow.add_edge("generate_analysis", "save_output")
    workflow.add_edge("save_output", END)
    
    # Set entry point
    workflow.set_entry_point("load_input_files")
    
    # Compile the graph
    return workflow.compile()

def main():
    """Main function to run the Multi-Level Summary extraction workflow."""
    
    print("=== Multi-Level Summary (MLS) Extractor ===")
    print("🔧 Using Dynamic Prompt Composition + Gemini 2.5 Pro")
    print(f"📄 Prompt template: {PROMPT_TEMPLATE_FILE}")
    print(f"📊 Outline JSON: {OUTLINE_JSON_FILE}")
    print(f"📖 Commentary text: {COMMENTARY_TEXT_FILE}")
    print(f"💾 Output file: {OUTPUT_FILE}")
    print()
    
    # Validate input files exist
    files_to_check = [
        (PROMPT_TEMPLATE_FILE, "Prompt template"),
        (OUTLINE_JSON_FILE, "Outline JSON file"),
        (COMMENTARY_TEXT_FILE, "Commentary text file")
    ]
    
    for file_path, file_type in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ Error: {file_type} not found: {file_path}")
            print("Please update the configuration section in the script.")
            sys.exit(1)
    
    # Create and run workflow
    print("🚀 Creating LangGraph workflow...")
    workflow = create_workflow()
    
    print("▶️ Starting Multi-Level Summary extraction...")
    
    # Initialize empty state - the workflow will populate it
    initial_state = AnalysisState(
        prompt_template="",
        outline_json="",
        commentary_text="",
        final_prompt=""
    )
    
    # Run the workflow
    final_state = workflow.invoke(initial_state)
    
    if final_state.error_message:
        print(f"❌ Workflow failed: {final_state.error_message}")
        sys.exit(1)
    else:
        print("\n🎉 Multi-Level Summary extraction complete!")
        print(f"📊 Check {OUTPUT_FILE} for the complete hierarchical analysis with Tibetan summaries.")
        print("✅ All output validated with Pydantic models")

if __name__ == "__main__":
    main() 