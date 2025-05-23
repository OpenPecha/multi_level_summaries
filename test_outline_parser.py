import json
import unittest
import copy
from pathlib import Path
from outline_parser import process_outline_json, process_node_recursive

class TestOutlineParser(unittest.TestCase):
    def setUp(self):
        # Create dummy outline data for testing
        self.dummy_outline = [
            {
                "level": "chapter",
                "number": "1",
                "title": "Test Chapter",
                "verses_span": "1-10",
                "children": [
                    {
                        "level": "section",
                        "number": "1.1",
                        "title": "Test Section 1",
                        "verses_span": "1-5",
                        "children": [
                            {
                                "level": "subsection",
                                "number": "1.1.1",
                                "title": "Test Subsection 1",
                                "verses_span": "1-3",
                                "verse_text_excerpt": "These are verses 1-3 of the root text.",
                                "children": []
                            },
                            {
                                "level": "subsection",
                                "number": "1.1.2",
                                "title": "Test Subsection 2",
                                "verses_span": "4-5",
                                "verse_text_excerpt": "These are verses 4-5 of the root text.",
                                "children": []
                            }
                        ]
                    },
                    {
                        "level": "section",
                        "number": "1.2",
                        "title": "Test Section 2",
                        "verses_span": "6-10",
                        "children": [
                            {
                                "level": "subsection",
                                "number": "1.2.1",
                                "title": "Test Subsection 3",
                                "verses_span": "6-8",
                                "verse_text_excerpt": "These are verses 6-8 of the root text.",
                                "children": []
                            },
                            {
                                "level": "subsection",
                                "number": "1.2.2",
                                "title": "Test Subsection 4",
                                "verses_span": "9-10",
                                "verse_text_excerpt": "These are verses 9-10 of the root text.",
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
        
        # Expected output after processing
        self.expected_output = [
            {
                "level": "chapter",
                "number": "1",
                "title": "Test Chapter",
                "verses_span": "1-10",
                "combined_verse_text_excerpt": "These are verses 1-3 of the root text.\n\nThese are verses 4-5 of the root text.\n\nThese are verses 6-8 of the root text.\n\nThese are verses 9-10 of the root text."
            },
            {
                "level": "section",
                "number": "1.1",
                "title": "Test Section 1",
                "verses_span": "1-5",
                "combined_verse_text_excerpt": "These are verses 1-3 of the root text.\n\nThese are verses 4-5 of the root text."
            },
            {
                "level": "section",
                "number": "1.2",
                "title": "Test Section 2",
                "verses_span": "6-10",
                "combined_verse_text_excerpt": "These are verses 6-8 of the root text.\n\nThese are verses 9-10 of the root text."
            }
        ]
        
    def test_process_node_recursive(self):
        """Test the recursive node processing function with dummy data"""
        # Make a deep copy of the dummy outline to avoid modifying the original
        test_outline = copy.deepcopy(self.dummy_outline)
        
        # Process the test chapter node
        result = process_node_recursive(test_outline[0])
        
        # Check that function returns True since there is verse text
        self.assertTrue(result)
        
        # Check that the chapter node now has verse_text_excerpt
        self.assertIn("verse_text_excerpt", test_outline[0])
        
        # Check that the verse text in the chapter includes all leaf node texts
        chapter_text = test_outline[0]["verse_text_excerpt"]
        self.assertIn("These are verses 1-3 of the root text.", chapter_text)
        self.assertIn("These are verses 4-5 of the root text.", chapter_text)
        self.assertIn("These are verses 6-8 of the root text.", chapter_text)
        self.assertIn("These are verses 9-10 of the root text.", chapter_text)
        
        # Check that each section also has verse_text_excerpt
        section1 = test_outline[0]["children"][0]
        self.assertIn("verse_text_excerpt", section1)
        self.assertIn("These are verses 1-3 of the root text.", section1["verse_text_excerpt"])
        self.assertIn("These are verses 4-5 of the root text.", section1["verse_text_excerpt"])
        
        section2 = test_outline[0]["children"][1]
        self.assertIn("verse_text_excerpt", section2)
        self.assertIn("These are verses 6-8 of the root text.", section2["verse_text_excerpt"])
        self.assertIn("These are verses 9-10 of the root text.", section2["verse_text_excerpt"])
    
    def test_process_outline_json(self):
        """Test the main processing function with dummy data"""
        # Make a deep copy of the dummy outline to avoid modifying the original
        test_outline = copy.deepcopy(self.dummy_outline)
        
        # Process the test outline
        result = process_outline_json(test_outline)
        
        # The result should be the same object as the input, modified in place
        self.assertEqual(id(result), id(test_outline))
        
        # Check that the chapter node has verse_text_excerpt
        self.assertIn("verse_text_excerpt", result[0])
        
        # Check that all verse text from leaves is included
        chapter_text = result[0]["verse_text_excerpt"]
        for text in ["These are verses 1-3 of the root text.", 
                    "These are verses 4-5 of the root text.",
                    "These are verses 6-8 of the root text.",
                    "These are verses 9-10 of the root text."]:
            self.assertIn(text, chapter_text)
            
        # Check that each section has verse_text_excerpt with appropriate text
        section1_text = result[0]["children"][0]["verse_text_excerpt"]
        self.assertIn("These are verses 1-3 of the root text.", section1_text)
        self.assertIn("These are verses 4-5 of the root text.", section1_text)
        self.assertNotIn("These are verses 6-8 of the root text.", section1_text)
        
        section2_text = result[0]["children"][1]["verse_text_excerpt"]
        self.assertIn("These are verses 6-8 of the root text.", section2_text)
        self.assertIn("These are verses 9-10 of the root text.", section2_text)
        self.assertNotIn("These are verses 1-3 of the root text.", section2_text)

    def test_end_to_end(self):
        """Test the full process with a temporary file"""
        # Create a temporary directory for test data
        test_dir = Path("./test_data")
        test_dir.mkdir(exist_ok=True)
        
        # Write dummy outline to a temporary file
        test_outline_file = test_dir / "test_outline.json"
        with open(test_outline_file, "w", encoding='utf-8') as f:
            json.dump(self.dummy_outline, f, indent=2, ensure_ascii=False)
        
        # Process the outline
        outline_data_str = test_outline_file.read_text(encoding='utf-8')
        outline_data = json.loads(outline_data_str)
        processed_outline = process_outline_json(outline_data)
        
        # Write the processed output to a temporary file
        output_file = test_dir / "updated_outline.json"
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(processed_outline, f, indent=2, ensure_ascii=False)
        
        # Verify the output file exists
        self.assertTrue(output_file.exists())
        
        # Read the output file and verify its contents
        with open(output_file, "r", encoding='utf-8') as f:
            result = json.load(f)
        
        # Check that the result has the same structure as the original but with verse_text_excerpt added
        self.assertEqual(len(result), len(self.dummy_outline))
        
        # Check that chapter has verse_text_excerpt
        chapter = result[0]
        self.assertIn("verse_text_excerpt", chapter)
        
        # Check that all sections have verse_text_excerpt
        for section in chapter["children"]:
            self.assertIn("verse_text_excerpt", section)
        
        # Clean up test files
        test_outline_file.unlink()
        output_file.unlink()
        test_dir.rmdir()

if __name__ == "__main__":
    unittest.main()
