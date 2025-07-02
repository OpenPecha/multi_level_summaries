import json
import argparse
import os

def parse_span(span):
    """Parses a verse span string like '1-36' or '37' into a start and end integer."""
    if '-' in span:
        start, end = map(int, span.split('-'))
        return start, end
    else:
        num = int(span)
        return num, num

def verify_verse_spans(file_path):
    """
    Verifies that the verse spans in a combined MLS JSON file are continuous
    at the top chapter level.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return

    print(f"Verifying top-level chapter verse spans in '{file_path}'...")

    last_end_verse = 0
    gaps_found = False

    # We only check the top-level chapters for continuity
    for chapter in data:
        if 'global_verses_span' in chapter:
            span_str = chapter['global_verses_span']
            start_verse, end_verse = parse_span(span_str)

            if start_verse != last_end_verse + 1:
                gaps_found = True
                print(f"  - GAP DETECTED: Missing verses between chapter ending at {last_end_verse} and chapter starting at {start_verse}.")
            
            last_end_verse = end_verse
        else:
            print(f"Warning: Chapter entry found without a 'global_verses_span'. Entry: {chapter.get('title', 'N/A')}")


    if not gaps_found:
        print("\nVerification complete. No gaps found in verse spans.")
    else:
        print(f"\nVerification complete. Gaps were found. Last verse checked was {last_end_verse}.")


def main():
    """
    Main function to parse arguments and run the verification script.
    """
    parser = argparse.ArgumentParser(
        description="A script to verify the continuity of top-level chapter verse spans in a combined MLS JSON file."
    )
    parser.add_argument(
        "file_path",
        help="Path to the combined MLS JSON file to verify.",
        nargs="?",
        default=None
    )
    args = parser.parse_args()

    file_to_verify = args.file_path
    if not file_to_verify:
        # Default to the output of the other script if no path is provided
        default_dir = 'data/chojuk'
        file_to_verify = os.path.join(default_dir, "combined_MLS_en.json")
    
    if not os.path.exists(file_to_verify):
        print(f"Error: The default file '{file_to_verify}' does not exist. Please provide a path.")
        return

    verify_verse_spans(file_to_verify)


if __name__ == "__main__":
    main() 