# Multi-Level Summaries

<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

## Multi-Level Summaries
A tool for extracting hierarchical outlines and summaries from Buddhist texts using root text and commentary.

## Owner(s)

- [@ngawangtrinley](https://github.com/ngawangtrinley)
- [@kaldan007](https://github.com/kaldan007)
- [@gayche](https://github.com/gayche)


## Table of contents
<p align="center">
  <a href="#project-description">Project description</a> •
  <a href="#who-this-project-is-for">Who this project is for</a> •
  <a href="#project-dependencies">Project dependencies</a> •
  <a href="#instructions-for-use">Instructions for use</a> •
  <a href="#contributing-guidelines">Contributing guidelines</a> •
  <a href="#additional-documentation">Additional documentation</a> •
  <a href="#how-to-get-help">How to get help</a> •
  <a href="#terms-of-use">Terms of use</a>
</p>
<hr>

## Project description

Multi-Level Summaries is a tool that helps you extract hierarchical outlines and summaries from Buddhist texts using their root text and commentary. The project uses large language models to analyze the structure of texts as explained in their commentaries, and then extracts verse text at different hierarchical levels for summarization and study.

The tool works in two main steps:
1. **Outline Extraction**: Using a specialized prompt on Gemini, the tool extracts a comprehensive hierarchical outline of the root text based on the structure, divisions, and thematic groupings presented in its commentary.
2. **Verse Text Processing**: The outline parser script then processes the JSON outline to extract and combine verse text for all nodes in the hierarchy, including parent nodes that don't have direct verse text in the initial extraction.

## Who this project is for
This project is intended for Buddhist scholars, researchers, and practitioners who want to better understand the structure and content of Buddhist texts through their commentaries, and generate multi-level summaries for study and analysis.

## Project dependencies
Before using Multi-Level Summaries, ensure you have:
* Python 3.7+
* Access to Gemini API or another capable large language model
* JSON processing capabilities


## Instructions for use
Get started with Multi-Level Summaries by preparing your root text and commentary files.

### Install Multi-Level Summaries
1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/OpenPecha/multi_level_summaries.git
    cd multi_level_summaries
    ```

2. Install required dependencies.

    ```bash
    pip install -r requirements.txt
    ```

### Prepare Your Texts
1. Prepare your root text file and commentary text file in plain text format.
2. Organize your files in the `data` directory, following the existing structure.

### Extract Outline Using LLM
1. Use the outline extractor prompt with Gemini or another capable LLM. The full prompt is available in the project at `data/prompts/outline_extractor_prompt.md`.

    The prompt is designed to generate a comprehensive hierarchical outline of the root text based on the structure presented in its commentary. It instructs the LLM to:
    - Extract the hierarchical structure (chapters, sections, subsections) from the commentary
    - Provide verse number spans for each level
    - Include the exact verse text for leaf nodes only
    - Use titles derived from the commentary where available
    
    The output will be in JSON format with the following structure:

    ```json
    [
      {
        "level": "chapter",
        "number": "1",
        "title": "[Title derived from Commentary]",
        "verses_span": "[start]-[end]",
        "children": [
          {
            "level": "section",
            "number": "1.1",
            "title": "[Title derived from Commentary]",
            "verses_span": "[start]-[end]",
            "children": [
              {
                "level": "subsection",
                "number": "1.1.1",
                "title": "[Title derived from Commentary]",
                "verses_span": "[start]-[end]",
                "verse_text_excerpt": "[Exact text of verses from the Root Text]",
                "children": []
              }
            ]
          }
        ]
      }
    ]
    ```

2. Save the generated JSON outline to a file (e.g., `chapter_1_outline.json`) in the appropriate data directory.

### Process the Outline
1. Run the outline parser script to extract verse text for all nodes in the hierarchy.

    ```bash
    python outline_parser.py
    ```

    This script will:
    - Parse the JSON outline
    - Extract verse text from leaf nodes
    - Combine verse text for parent nodes
    - Generate a new JSON file with verse text for all nodes

2. The processed output will be saved to `parent_nodes_with_verses.json`.

### Troubleshoot Multi-Level Summaries

<table>
  <tr>
   <td>
    Issue
   </td>
   <td>
    Solution
   </td>
  </tr>
  <tr>
   <td>
    LLM output token limit prevents generating the full outline
   </td>
   <td>
    Only extract text at leaf nodes in the initial prompt, then use the outline_parser.py script to process and combine verse text for parent nodes.
   </td>
  </tr>
  <tr>
   <td>
    JSON parsing errors
   </td>
   <td>
    Ensure the LLM output is valid JSON. You may need to fix formatting issues manually before processing.
   </td>
  </tr>
  <tr>
   <td>
    Missing verse text in output
   </td>
   <td>
    Check that your root text file contains all verses referenced in the outline and that verse spans are correctly specified.
   </td>
  </tr>
</table>


## Contributing guidelines
If you'd like to help out, check out our [contributing guidelines](/CONTRIBUTING.md).


## Additional documentation
_Include links and brief descriptions to additional documentation._

For more information:
* [Reference link 1](#)
* [Reference link 2](#)
* [Reference link 3](#)


## How to get help
* File an issue.
* Email us at openpecha[at]gmail.com.
* Join our [discord](https://discord.com/invite/7GFpPFSTeA).


## Terms of use
Multi-Level Summaries is licensed under the [MIT License](/LICENSE.md).
