import json
import unittest
from pathlib import Path
from outline_parser import process_outline_json, extract_parent_verses, collect_leaf_texts

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
        
    def test_process_outline_json(self):
        """Test the main processing function with dummy data"""
        result = process_outline_json(self.dummy_outline)
        
        # Check that we got the expected number of parent nodes
        self.assertEqual(len(result), len(self.expected_output))
        
        # Check that each parent node has the expected fields and values
        for i, parent_node in enumerate(result):
            expected_node = self.expected_output[i]
            
            self.assertEqual(parent_node["level"], expected_node["level"])
            self.assertEqual(parent_node["number"], expected_node["number"])
            self.assertEqual(parent_node["title"], expected_node["title"])
            self.assertEqual(parent_node["verses_span"], expected_node["verses_span"])
            self.assertEqual(parent_node["combined_verse_text_excerpt"], expected_node["combined_verse_text_excerpt"])
    
    def test_collect_leaf_texts(self):
        """Test the leaf text collection function"""
        # Test with a leaf node
        leaf_node = {
            "level": "subsection",
            "number": "1.1.1",
            "title": "Test Subsection",
            "verses_span": "1-3",
            "verse_text_excerpt": "Test verse text",
            "children": []
        }
        
        text_list = []
        collect_leaf_texts(leaf_node, text_list)
        self.assertEqual(text_list, ["Test verse text"])
        
        # Test with a parent node containing leaves
        parent_node = self.dummy_outline[0]["children"][0]  # Section 1.1
        text_list = []
        collect_leaf_texts(parent_node, text_list)
        self.assertEqual(len(text_list), 2)
        self.assertEqual(text_list[0], "These are verses 1-3 of the root text.")
        self.assertEqual(text_list[1], "These are verses 4-5 of the root text.")
    
    def test_extract_parent_verses(self):
        """Test the parent verse extraction function"""
        parent_data_list = []
        extract_parent_verses(self.dummy_outline[0], parent_data_list)
        
        # Should extract data for the chapter and both sections
        self.assertEqual(len(parent_data_list), 3)
        
        # Check the chapter data
        chapter_data = next((item for item in parent_data_list if item["number"] == "1"), None)
        self.assertIsNotNone(chapter_data)
        self.assertEqual(chapter_data["level"], "chapter")
        self.assertEqual(chapter_data["title"], "Test Chapter")
        
        # Check section 1.1 data
        section_1_data = next((item for item in parent_data_list if item["number"] == "1.1"), None)
        self.assertIsNotNone(section_1_data)
        self.assertEqual(section_1_data["level"], "section")
        self.assertEqual(section_1_data["title"], "Test Section 1")
        
        # Check section 1.2 data
        section_2_data = next((item for item in parent_data_list if item["number"] == "1.2"), None)
        self.assertIsNotNone(section_2_data)
        self.assertEqual(section_2_data["level"], "section")
        self.assertEqual(section_2_data["title"], "Test Section 2")

    def test_end_to_end(self):
        """Test the full process with a temporary file"""
        # Create a temporary directory for test data
        test_dir = Path("./test_data")
        test_dir.mkdir(exist_ok=True)
        
        # Write dummy outline to a temporary file
        test_outline_file = test_dir / "test_outline.json"
        with open(test_outline_file, "w") as f:
            json.dump(self.dummy_outline, f, indent=2)
        
        # Process the outline
        outline_data_str = test_outline_file.read_text()
        outline_data = json.loads(outline_data_str)
        processed_output = process_outline_json(outline_data)
        
        # Write the processed output to a temporary file
        output_file = test_dir / "test_output.json"
        with open(output_file, "w") as f:
            json.dump(processed_output, f, indent=2)
        
        # Verify the output file exists
        self.assertTrue(output_file.exists())
        
        # Read the output file and verify its contents
        with open(output_file, "r") as f:
            result = json.load(f)
        
        self.assertEqual(len(result), len(self.expected_output))
        
        # Clean up test files
        test_outline_file.unlink()
        output_file.unlink()
        test_dir.rmdir()

if __name__ == "__main__":
    unittest.main()
