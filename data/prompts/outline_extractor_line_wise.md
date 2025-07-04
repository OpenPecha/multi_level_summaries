# Outline Extractor Prompt for Buddhist Texts



## Task Description



I am providing you with two texts: a Buddhist root text and its commentary. Your task is to generate a comprehensive hierarchical outline of the root text, based on the structure, divisions, and thematic groupings presented in its accompanying commentary. The output should be in JSON format.



The commentary provides the lens through which the root text's structure should be outlined. The outline should clearly delineate all levels of organization for the root text, as implied or explicitly stated by the commentary's discussion.



## Expected Hierarchical Levels



- **Chapters** in the root text (as demarcated by the commentary)

- **Sections** within those chapters (as demarcated by the commentary)

- **Subsections** within those sections (as demarcated by the commentary)

- Any further subdivisions of the root text that the commentary highlights



## Key Requirements



1. For each level in this outline of the root text, you must provide its corresponding line number span from the root text.



2. For the last level of each branch (i.e., leaf nodes with no further children), you must also include the exact text of those lines from the root text.



3. If the commentary explicitly names these divisions or sections of the root text (e.g., when the commentary says "Now we explain Chapter 1 of the root text: The Awakening Mind," or "This section of the root text, lines X-Y, deals with Understanding Emptiness"), please use those names for the title field in the JSON.



4. If the commentary doesn't provide explicit names but clearly structures its explanation around certain line groups, use generic but descriptive labels for the title (e.g., "Thematic Grouping of lines A-B").



5. The number field should reflect the sequential numbering (e.g., "1", "1.1", "1.1.1").



## Input Texts



### Root Text



```

[Paste the Buddhist root text here. Ensure it is complete and accurately formatted, as the LLM will need to extract line text directly from it.]

```



### Commentary Text



```

[Paste the commentary on the root text here.]

```



## Output Format



Please provide the full outline tree for the root text, as structured by the commentary, in JSON format. The JSON should follow this structure. Note that `line_text_excerpt` is only included for leaf nodes (items with an empty children array).



```json

[

  {

    "level": "chapter-1",               // e.g., "1", "2"

    "title": "[Title derived from Commentary, or a descriptive title if none in Commentary]",

    "lines_span": "[start]-[end]",  // e.g., "1-25"

    // No "line_text_excerpt" here as it's a parent node

    "children": [

      {

        "level": "section-1.1",           // e.g., "1.1", "1.2"

        "title": "[Title derived from Commentary, or a descriptive title if none in Commentary]",

        "lines_span": "[start]-[end]",  // e.g., "1-10"

        // No "line_text_excerpt" here if it has children

        "children": [

          {

            "level": "subsection-1.1.1",      // e.g., "1.1.1", "1.1.2"

            "title": "[Title derived from Commentary, or a descriptive title if none in Commentary]",

            "lines_span": "[start]-[end]",  // e.g., "1-5"

            "line_text_excerpt": "[Exact text of lines [start]-[end] from the Root Text, as this is a leaf node]",  // Included for leaf nodes

            "children": []           // Empty, indicating a leaf node

          },

          {

            "level": "subsection-1.1.2",

            "title": "[Title derived from Commentary, or a descriptive title if none in Commentary]",

            "lines_span": "[start]-[end]",  // e.g., "6-10"

            "line_text_excerpt": "[Exact text of lines [start]-[end] from the Root Text, as this is a leaf node]",  // Included for leaf nodes

            "children": []           // Empty, indicating a leaf node

          }

        ]

      },

      {

        "level": "section-1.2",

        "title": "[Title derived from Commentary, or a descriptive title if none in Commentary]",

        "line_span": "[start]-[end]",  // e.g., "11-25"

        "line_text_excerpt": "[Exact text of lines [start]-[end] from the Root Text, if this section has NO children and is a leaf node]",  // Example if this section were a leaf

        "children": []               // If this section is a leaf node, otherwise it would have children.

      }

    ]

  }

  // ... more chapters

]

```



## Detailed Requirements



1. A full hierarchical outline of the root text in JSON format.



2. The structure (chapters, sections, subsections, etc.) and their delineations for the root text outline must be derived solely from how the commentary discusses, divides, and explains the root text.



3. Accurate line number spans (e.g., "1-5", "23-29", field name `lines_span`) from the root text for every item in the outline.



4. The exact line text (field name `line_text_excerpt`) corresponding to the `lines_span` from the root text must be included only for leaf nodes (i.e., the last level of any branch, where the children array is empty). Parent nodes should not have the `line_text_excerpt` field or it can be null.



5. Use titles for the root text sections/chapters that are explicitly mentioned or strongly implied by the commentary. If no explicit title is given by the commentary for a division it makes, use a concise, descriptive title for that part of the root text.



6. The `level` field in the JSON should indicate the type of division (e.g., "chapter", "section", "subsection").





7. Nested structures should be represented using the `children` array. If an item has no further subdivisions, its children array should be empty.



8. I want all the Titles of section, subsections and child sections in Tibetan.



Please generate the JSON outline.

