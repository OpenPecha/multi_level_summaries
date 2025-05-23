# Hierarchical Chapter Analysis Prompt for Buddhist Root Texts

## Objective

To generate a comprehensive hierarchical analysis of an entire chapter from a Buddhist root text, creating summaries for each structural node from the ground up (children to parent). This process analyzes the provided chapter structure and generates enriched summaries that capture both explicit content and implicit inter-node conceptual relationships. The output maintains the original hierarchical structure while adding detailed summary analysis for each node.

## Input

- **chapter_commentary_document**: The full text of the Buddhist commentary for the target chapter (e.g., `chapter_1_commentary.txt`)
- **chapter_structure_document**: A JSON file containing the hierarchical structure of the chapter (e.g., `updated_outline.json`). This file contains:
  - Hierarchical node structure
  - Verse references
  - Section identifications
  - Existing metadata for each structural unit

> **Note**: The `verse_text_excerpt` attribute, if present in the input chapter_structure_document, should be disregarded and excluded from the output.

## Task

1. **Parse Chapter Structure**: Analyze the provided JSON structure to understand the hierarchical organization of the chapter (sections, subsections, verse groups, individual verses, etc.)

2. **Locate Commentary Correspondences**: For each node in the hierarchy, identify relevant sections within the chapter_commentary_document that discuss, explain, or elaborate upon that specific structural unit.

3. **Generate Bottom-Up Summaries**: Create comprehensive summaries for each node in the hierarchy, working from the most granular level (individual verses/smallest units) up to the chapter level, ensuring that:
   - Child node summaries inform parent node summaries
   - Implicit conceptual relationships between nodes are captured
   - Inter-node thematic connections are identified and integrated

4. **Maintain Original Structure**: Return the analysis in the same JSON structure as the input, with added summary fields for each node, and ensuring the `verse_text_excerpt` attribute is not present.

## Output Format

The output will be a JSON object that maintains the exact hierarchical structure of the input chapter_structure_document (excluding `verse_text_excerpt`), but with the following additional fields added to each node:

### New Fields for Each Node

```json
"summary": {
  "content_summary": "(String) A concise summary (2-5 sentences) of the core content, main arguments, and purpose of this structural unit",
  
  "key_concepts": "(Array of Strings) Primary philosophical terms, practices, or ideas introduced or elaborated in this unit",
  
  "transformative_goal": "(String) The primary inner transformation, realization, or development this unit aims to facilitate",
  
  "function_in_hierarchy": "(String) The role and purpose of this unit within the broader chapter structure and argument",
  
  "inter_node_relationships": "(Array of Objects) Connections to sibling, parent, or related nodes, each with:",
  // "related_node_id": "(String) Identifier of the related node",
  // "relationship_type": "(String) Type of relationship (builds_on, contrasts_with, elaborates, etc.)",
  // "conceptual_bridge": "(String) Description of the implicit conceptual connection"
  
  "implicit_concepts": "(Array of Strings) Unstated but implied philosophical or practical concepts that emerge from this unit's position in the hierarchy",
  
  "commentary_insights": "(String, Optional) Key interpretations or clarifications from the commentary specific to this unit",
  
  "commentary_citation": "(String, Optional) Specific reference to commentary sections discussing this unit",
  
  "pedagogical_strategy": "(String) The teaching method or approach employed in this unit (progressive disclosure, contrast, direct instruction, etc.)",
  
  "audience_assumptions": "(String, if inferable) Level of understanding or background this unit assumes from the reader"
},

"functional_transformative_analysis_of_root_text_unit": {
  "transformative_goal_of_root_text_unit": "(String) The primary inner transformation, realization, or development this root text section aims to facilitate in the reader.",
  
  "means_of_transformation": "(String) How this section attempts to produce its intended transformation (e.g., through logical argument, evocative imagery, etc.).",
  
  "prerequisite_realizations": "(Array of Strings) Prior insights or understandings the reader must have to fully engage with this section.",
  
  "progressive_insights": "(Array of Strings) The sequence of realizations or understandings this section attempts to generate in the reader.",
  
  "obstacles_addressed": "(Array of Strings) Cognitive, emotional or practical hindrances this section helps the reader overcome.",
  
  "practice_implications": "(String) How the content of this section might inform or modify meditation practice or daily conduct."
}
```

## Processing Instructions

### 1. Hierarchical Analysis Approach

- **Bottom-Up Processing**: Begin analysis with the most granular nodes (individual verses or smallest structural units)
- **Aggregative Summarization**: Parent node summaries must integrate and synthesize their children's content while identifying emergent themes
- **Conceptual Bridging**: Identify implicit connections between nodes that may not be explicitly stated but are structurally implied
- **Attribute Exclusion**: Ensure the `verse_text_excerpt` attribute is not included in the output for any node.

### 2. Commentary Integration

- **Targeted Commentary Search**: For each node, locate relevant commentary sections using verse references, section titles, or content matching
- **Contextual Commentary Application**: Apply commentary insights specifically to the structural unit being analyzed, not just to individual verses
- **Citation Precision**: Provide specific page numbers, sections, or identifiers from the commentary document

### 3. Inter-Node Relationship Analysis

- **Sibling Relationships**: Analyze how nodes at the same hierarchical level relate to each other
- **Parent-Child Conceptual Flow**: Identify how detailed concepts in child nodes contribute to broader themes in parent nodes
- **Cross-Hierarchical Connections**: Note when concepts introduced in one branch of the hierarchy inform or relate to concepts in other branches

### 4. Implicit Concept Identification

- **Structural Implications**: Identify concepts that emerge from the arrangement and sequence of the material
- **Unstated Assumptions**: Capture philosophical or practical assumptions that underlie the explicit content
- **Progressive Development**: Note how concepts develop or evolve across the hierarchical structure

### 5. Quality Assurance

- **Structural Integrity**: Ensure the output JSON maintains the exact structure and all original fields (except `verse_text_excerpt`) from the input
- **Summary Coherence**: Verify that parent summaries logically encompass and synthesize their children's summaries
- **Citation Accuracy**: Ensure all commentary references are precise and verifiable

## Special Considerations

### Handling Complex Hierarchies

- **Multi-Level Processing**: For deeply nested structures, ensure each level adds appropriate analytical depth
- **Conceptual Granularity**: Match the analytical granularity to the structural granularity of each level
- **Thematic Continuity**: Maintain thematic coherence across all hierarchical levels

### Commentary Integration Challenges

- **Missing Commentary**: If commentary for specific nodes is not found, note this in the summary
- **Overlapping Commentary**: When commentary discusses multiple nodes, distribute insights appropriately
- **Commentary Interpretation**: Distinguish between direct commentary explanation and inferential analysis

### Output Validation

- **JSON Validity**: Ensure the output is valid JSON that can be parsed
- **Completeness**: Verify that every node in the original structure has been enhanced with summary analysis
- **Consistency**: Maintain consistent terminology and conceptual frameworks across all summaries
- **Attribute Exclusion Check**: Confirm `verse_text_excerpt` is absent from all nodes in the output.

## Notes on Processing

- Use a `processing_notes` field at the root level to document any challenges, ambiguities, or methodological decisions made during analysis
- If certain nodes cannot be adequately analyzed due to unclear structure or missing commentary, flag these specifically
- Prioritize conceptual accuracy over completeness if trade-offs are necessary

## Expected Outcome

A comprehensive, hierarchically-structured JSON document that serves as an "AI-ready authoritative interpretation" of the entire chapter. Each structural unit will be enriched by detailed summaries and functional transformative analysis, capturing both explicit content and implicit conceptual relationships, informed by the commentary and structural position within the broader chapter argument. The `verse_text_excerpt` attribute will be excluded from the output.

> **Important**: I don't need python script. I need the output JSON.