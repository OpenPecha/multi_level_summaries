# Buddhist Text Summary Generation with Gemini Flash 2.5

This project provides two Python scripts to generate detailed summaries for hierarchical Buddhist text outlines using Google's Gemini Flash 2.5 API, with all summaries generated in Tibetan language.

## 📁 Files Created

- `generate_summaries.py` - Generates individual summaries for each node in the outline
- `integrate_summaries.py` - Combines all summaries back into the hierarchical structure
- `requirements.txt` - Updated with necessary dependencies

## 🔧 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set it as an environment variable:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Configure File Paths

Edit the configuration variables at the top of each script:

**In `generate_summaries.py`:**
```python
# =====================================================
# CONFIGURATION - Update these paths as needed
# =====================================================
OUTLINE_PATH = "data/chojuk/chapter_1/chapter_1_outline.json"
COMMENTARY_PATH = "data/chojuk/chapter_1/chapter_1_commentary.txt"
SUMMARIES_DIR = "summaries"
# =====================================================
```

**In `integrate_summaries.py`:**
```python
# =====================================================
# CONFIGURATION - Update these paths as needed
# =====================================================
OUTLINE_PATH = "data/chojuk/chapter_1/chapter_1_outline.json"
SUMMARIES_DIR = "summaries"
OUTPUT_PATH = "annotated_outline.json"
# =====================================================
```

## 🚀 Usage

### Step 1: Generate Individual Summaries

1. **Configure paths** in `generate_summaries.py` (see configuration section above)
2. **Run the script:**

```bash
python generate_summaries.py
```

This will:
- Create a `summaries/` directory (or the directory specified in `SUMMARIES_DIR`)
- Generate individual JSON files for each node (e.g., `chapter-1.json`, `section-1-1.json`)
- Skip nodes that already have summaries (for resumability)
- Include rate limiting to avoid API quota issues

### Step 2: Integrate Summaries into Outline

1. **Configure paths** in `integrate_summaries.py` (see configuration section above)
2. **Run the script:**

```bash
python integrate_summaries.py
```

This will:
- Load all individual summary files
- Integrate them into the original outline structure
- Remove `verse_text_excerpt` fields
- Create the final output file (default: `annotated_outline.json`)

## 📋 Summary Format

Each generated summary includes the following fields in Tibetan:

```json
{
  "level": "section-1.2",
  "summary": {
    "content_summary": "Main content explanation in Tibetan",
    "key_concepts": ["Buddhist concept 1", "Buddhist concept 2"],
    "transformative_goal": "Inner transformation objective",
    "function_in_hierarchy": "Role in the larger structure",
    "inter_node_relationships": [
      {
        "related_node_id": "section-1.1",
        "relationship_type": "sibling/parent/child",
        "conceptual_bridge": "Connection explanation"
      }
    ],
    "implicit_concepts": ["Implied concept 1", "Implied concept 2"],
    "pedagogical_strategy": "Teaching approach used",
    "intended_impact_on_reader": "Expected reader response",
    "audience_assumptions": "Assumed background knowledge"
  }
}
```

## 🎯 Summary Content Guidelines

The Gemini API is prompted to generate summaries that are:

- **Bottom-up aware**: Understanding the node's role in the larger hierarchy
- **Contextually rich**: Using the full commentary to understand deeper meanings
- **Relationship-focused**: Connecting nodes to siblings, parents, and children
- **Pedagogically informed**: Understanding the teaching strategy
- **Transformatively oriented**: Focusing on inner development goals
- **Culturally appropriate**: Reflecting authentic Buddhist philosophical understanding

## 📊 Features

### Easy Configuration
- All file paths are configured as variables at the top of each script
- No command line arguments needed
- Clear configuration sections for easy customization

### Resumability
- Both scripts can be run multiple times
- `generate_summaries.py` skips nodes that already have summary files
- Perfect for handling API rate limits or interruptions

### Error Handling
- Comprehensive error messages for missing files, invalid JSON, API errors
- Graceful handling of network issues and API quota limits
- Validation of outline structure before processing

### Statistics
- Progress tracking during generation
- Integration statistics showing completion rates
- Node counting and validation

## 🗂️ Directory Structure

```
project/
├── generate_summaries.py
├── integrate_summaries.py
├── requirements.txt
├── summaries/                    # Created by generate_summaries.py
│   ├── chapter-1.json
│   ├── section-1-1.json
│   ├── subsection-1-1-1.json
│   └── ...
├── annotated_outline.json        # Final output
└── data/
    └── chojuk/
        └── chapter_1/
            ├── chapter_1_outline.json
            └── chapter_1_commentary.txt
```

## ⚠️ Important Notes

1. **API Costs**: Each node requires a Gemini API call. Monitor your usage.
2. **Rate Limits**: The script includes 1-second delays between API calls
3. **Tibetan Text**: All summaries are generated in Tibetan script
4. **Large Files**: Commentary files can be large; ensure you have sufficient API quota
5. **Internet Connection**: Stable connection required for API calls
6. **Configuration**: Update file paths in the configuration sections before running

## 🔍 Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $GEMINI_API_KEY

# Set it if missing
export GEMINI_API_KEY="your_key_here"
```

### File Path Issues
- Check that paths in the configuration sections are correct
- Use relative paths from the script's location
- Ensure all directories and files exist

### JSON Parsing Errors
- Check that outline files are valid JSON
- Ensure proper UTF-8 encoding for Tibetan text

### Missing Summaries
- Run `generate_summaries.py` again to fill gaps
- Check the `summaries/` directory for generated files
- Review API quota and rate limits

### Network Issues
- The script will show specific error messages for API failures
- Restart from where it left off (resumability feature)

## 📈 Example Workflow

1. **Configure paths:**
   ```python
   # In generate_summaries.py
   OUTLINE_PATH = "data/chojuk/chapter_1/chapter_1_outline.json"
   COMMENTARY_PATH = "data/chojuk/chapter_1/chapter_1_commentary.txt"
   ```

2. **Generate summaries:**
   ```bash
   python generate_summaries.py
   ```

3. **Check progress:**
   ```bash
   ls summaries/
   # Shows generated .json files for each node
   ```

4. **Configure integration:**
   ```python
   # In integrate_summaries.py
   OUTLINE_PATH = "data/chojuk/chapter_1/chapter_1_outline.json"
   OUTPUT_PATH = "annotated_outline.json"
   ```

5. **Integrate results:**
   ```bash
   python integrate_summaries.py
   ```

6. **Review final output:**
   ```bash
   cat annotated_outline.json
   # Contains the complete hierarchical structure with summaries
   ```

## 🤝 Support

For issues with:
- **Script functionality**: Check error messages and ensure all dependencies are installed
- **Configuration**: Verify file paths in the configuration sections
- **API problems**: Verify your Gemini API key and quota
- **Tibetan text**: Ensure your terminal/editor supports UTF-8 encoding 