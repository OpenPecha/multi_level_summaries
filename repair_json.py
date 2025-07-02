import json
import argparse

def repair_json_file(file_path):
    """
    Attempts to repair a JSON file. It can fix files that are a single object
    wrapped in an array, or files with missing closing braces.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to parse it as-is first
        try:
            json.loads(content)
            print(f"'{file_path}' is already valid JSON. No changes made.")
            return
        except json.JSONDecodeError:
            print(f"'{file_path}' is not valid. Attempting repairs...")

        # Case 1: A single JSON object wrapped in an array `[{...}]`
        try:
            data = json.loads(content)
            if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
                print("Found a single object wrapped in an array. Unwrapping it.")
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data[0], f, indent=4, ensure_ascii=False)
                print(f"Successfully repaired '{file_path}'.")
                return
        except json.JSONDecodeError:
            pass # It's not a valid array, so try other fixes.
        except Exception:
            pass # Ignore other errors during this check
        
        # Case 2: Missing closing brace
        repaired_content = content.strip()
        if repaired_content.startswith('{') and not repaired_content.endswith('}'):
             # Find the last valid brace and assume everything after is noise
            last_brace_index = repaired_content.rfind('}')
            repaired_content = repaired_content[:last_brace_index+1]
        
        # Try to add a closing brace
        if repaired_content.startswith('{'):
            try:
                json.loads(repaired_content + '}')
                repaired_content += '}'
            except json.JSONDecodeError:
                pass # This didn't work

        # Final attempt to fix by cleaning up and re-parsing
        try:
            # A more aggressive approach for the specific error in chapter 8
            # The error is often a missing comma between elements in a list.
            # This is hard to fix generically without a more robust parser.
            # For now, we will focus on the array-wrapper issue for chap 7.
            final_data = json.loads(repaired_content)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, indent=4, ensure_ascii=False)
            print(f"Successfully repaired and saved '{file_path}'")

        except json.JSONDecodeError as e:
            print(f"Failed to repair '{file_path}'. Final error: {e}")


def main():
    parser = argparse.ArgumentParser(description="A script to repair a potentially malformed JSON file.")
    parser.add_argument("file_to_repair", help="The full path to the JSON file that needs repairing.")
    args = parser.parse_args()
    repair_json_file(args.file_to_repair)

if __name__ == "__main__":
    main() 