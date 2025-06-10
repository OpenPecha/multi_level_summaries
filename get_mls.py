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





def get_prompt(outline_json, commentary_text):

    return f"""
# **Hierarchical Chapter Analysis Prompt for Buddhist Root Texts**

## **Objective:**

To generate a comprehensive hierarchical analysis of an entire chapter from a Buddhist root text, creating summaries for each structural node from the ground up (children to parent). This process analyzes the provided chapter structure and generates enriched summaries that capture both explicit content and implicit inter-node conceptual relationships. The output maintains the original hierarchical structure while adding detailed summary analysis for each node.

## **Input:**

1. **chapter\_commentary\_document**: {commentary_text}
2. **chapter\_structure\_document**: {outline_json}

## **Task:**

1. **Parse Chapter Structure**: Analyze the provided JSON structure to understand the hierarchical organization of the chapter (sections, subsections, verse groups, individual verses, etc.)  
2. **Locate Commentary Correspondences**: For each node in the hierarchy, identify relevant sections within the chapter\_commentary\_document that discuss, explain, or elaborate upon that specific structural unit. This commentary will inform the generation of the summary fields.  
3. **Generate Bottom-Up Summaries**: Create comprehensive summaries for each node in the hierarchy, working from the most granular level (individual verses/smallest units) up to the chapter level, ensuring that:  
   * Child node summaries inform parent node summaries.  
   * Implicit conceptual relationships between nodes are captured.  
   * Inter-node thematic connections are identified and integrated.  
4. **Maintain Original Structure**: Return the analysis in the same JSON structure as the input, with added summary fields for each node.

## **Output Format:**

The output will be a JSON object that maintains the exact hierarchical structure of the input chapter\_structure\_document, but with the following additional field added to each node:

### **New Field for Each Node:**

"summary": {  
  "content\_summary": "(String) A concise summary (2-5 sentences) of the core content, main arguments, and purpose of this structural unit",

  "key\_concepts": "(Array of Strings) Primary philosophical terms, practices, or ideas introduced or elaborated in this unit",

  "transformative\_goal": "(String) The primary inner transformation, realization, or development this unit aims to facilitate",

  "function\_in\_hierarchy": "(String) The role and purpose of this unit within the broader chapter structure and argument",

  "inter\_node\_relationships": "(Array of Objects) Connections to sibling, parent, or related nodes, each with:",  
    // "related\_node\_id": "(String) Identifier of the related node",  
    // "relationship\_type": "(String) Type of relationship (builds\_on, contrasts\_with, elaborates, etc.)",  
    // "conceptual\_bridge": "(String) Description of the implicit conceptual connection"

  "implicit\_concepts": "(Array of Strings) Unstated but implied philosophical or practical concepts that emerge from this unit's position in the hierarchy",

  "pedagogical\_strategy": "(String) The teaching method or approach employed in this unit (progressive disclosure, contrast, direct instruction, etc.)",

  "intended\_impact\_on\_reader": "(String) Desired immediate intellectual, emotional, or practical impact on the reader after engaging with this unit",

  "audience\_assumptions": "(String, if inferable) Level of understanding or background this unit assumes from the reader"  
}

## **Processing Instructions:**

### **1\. Hierarchical Analysis Approach:**

* **Bottom-Up Processing**: Begin analysis with the most granular nodes (individual verses or smallest structural units).  
* **Aggregative Summarization**: Parent node summaries must integrate and synthesize their children's content while identifying emergent themes.  
* **Conceptual Bridging**: Identify implicit connections between nodes that may not be explicitly stated but are structurally implied.

### **2\. Commentary Integration:**

* **Targeted Commentary Search**: For each node, locate relevant commentary sections using verse references, section titles, or content matching to inform the analysis.  
* **Informed Analysis**: Use the insights from the commentary to accurately populate the fields in the "summary" object.

### **3\. Inter-Node Relationship Analysis:**

* **Sibling Relationships**: Analyze how nodes at the same hierarchical level relate to each other.  
* **Parent-Child Conceptual Flow**: Identify how detailed concepts in child nodes contribute to broader themes in parent nodes.  
* **Cross-Hierarchical Connections**: Note when concepts introduced in one branch of the hierarchy inform or relate to concepts in other branches.

### **4\. Implicit Concept Identification:**

* **Structural Implications**: Identify concepts that emerge from the arrangement and sequence of the material.  
* **Unstated Assumptions**: Capture philosophical or practical assumptions that underlie the explicit content.  
* **Progressive Development**: Note how concepts develop or evolve across the hierarchical structure.

### **5\. Quality Assurance:**

* **Structural Integrity**: Ensure the output JSON maintains the exact structure and all original fields from the input.  
* **Summary Coherence**: Verify that parent summaries logically encompass and synthesize their children's summaries.

## **Special Considerations:**

### **Handling Complex Hierarchies:**

* **Multi-Level Processing**: For deeply nested structures, ensure each level adds appropriate analytical depth.  
* **Conceptual Granularity**: Match the analytical granularity to the structural granularity of each level.  
* **Thematic Continuity**: Maintain thematic coherence across all hierarchical levels.

### **Commentary Integration Challenges:**

* **Missing Commentary**: If commentary for specific nodes is not found, note this in the summary analysis where relevant.  
* **Overlapping Commentary**: When commentary discusses multiple nodes, distribute insights appropriately across the relevant nodes' summaries.  
* **Commentary Interpretation**: Distinguish between direct commentary explanation and inferential analysis when generating the summaries.

### **Output Validation:**

* **JSON Validity**: Ensure the output is valid JSON that can be parsed.  
* **Completeness**: Verify that every node in the original structure has been enhanced with summary analysis.  
* **Consistency**: Maintain consistent terminology and conceptual frameworks across all summaries.

## **Notes on Processing:**

* Use a processing\_notes field at the root level to document any challenges, ambiguities, or methodological decisions made during analysis.  
* If certain nodes cannot be adequately analyzed due to unclear structure or missing commentary, flag these specifically.  
* Prioritize conceptual accuracy over completeness if trade-offs are necessary.

## **Expected Outcome:**

A comprehensive, hierarchically-structured JSON document that serves as an "AI-ready authoritative interpretation" of the entire chapter, with each structural unit enriched by detailed summaries that capture both explicit content and implicit conceptual relationships, informed by the commentary and structural position within the broader chapter argument.

## **Critical**

* **Please don't include the verse\_text\_excerpt in the output.**  
* **Generate all the results in Tibetan.**
"""

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
    title: str = Field(description="Node title")
    verses_span: Optional[str] = Field(default=None, description="Verse range for this node")
    children: List['Node'] = Field(default_factory=list, description="Child nodes")
    summary: Summary = Field(description="Generated summary for this node")

class ChapterStructure(BaseModel):
    """Model for the entire chapter structure with nodes and their summaries."""
    nodes: List[Node] = Field(description="List of nodes in the chapter hierarchy")
    processing_notes: str = Field(description="Notes on the analysis process")


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

