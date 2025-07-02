import json
import argparse
import os

def verify_combined_file(file_path):
    """
    Opens a combined MLS JSON file and prints the title of each top-level entry.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("Error: JSON file is not a list of entries.")
            return

        print(f"Checking top-level entries in: {file_path}\n")
        for i, entry in enumerate(data):
            if isinstance(entry, dict):
                title = entry.get('title', 'No Title')
                level = entry.get('level', 'N/A')
                number = entry.get('number', 'N/A')
                print(f"  {i + 1}. {level} {number}: {title}")
            else:
                print(f"  {i + 1}. Entry is not a valid object.")
        
        print(f"\nFound {len(data)} top-level entries.")

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to parse arguments and run the verification.
    """
    parser = argparse.ArgumentParser(
        description="A script to verify the contents of a combined MLS JSON file by listing top-level titles."
    )
    parser.add_argument(
        "json_file",
        help="Path to the combined MLS JSON file to verify.",
        default="data/chojuk/combined_MLS_en.json",
        nargs="?"
    )
    args = parser.parse_args()

    verify_combined_file(args.json_file)

if __name__ == "__main__":
    main() 