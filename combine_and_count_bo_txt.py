import os
import argparse

def combine_and_count_lines(root_dir):
    """
    Finds all files with 'root' in their name and ending with 'bo.txt'
    in subdirectories of root_dir, combines their content, and counts the
    non-empty lines.
    """
    total_lines = 0
    file_count = 0
    
    print(f"Searching for files containing 'root' and ending with 'bo.txt' in '{root_dir}'...")

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if "root" in file and file.endswith("bo.txt"):
                file_path = os.path.join(subdir, file)
                file_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        non_empty_lines = [line for line in lines if line.strip()]
                        total_lines += len(non_empty_lines)
                        print(f"  - Processed {file_path} ({len(non_empty_lines)} non-empty lines)")
                except Exception as e:
                    print(f"  - Error processing {file_path}: {e}")

    if file_count == 0:
        print("\nNo files containing 'root' and ending with 'bo.txt' were found.")
        return

    print(f"\nFound and processed {file_count} files.")
    
    if total_lines == 0:
        print("No text found in any of the processed files.")
    else:
        print(f"Total number of non-empty lines: {total_lines}")


def main():
    """
    Main function to parse arguments and run the script.
    """
    parser = argparse.ArgumentParser(
        description="A script to combine all '*root*...bo.txt' files and count the non-empty lines."
    )
    parser.add_argument(
        "root_dir",
        help="The root directory to search for files containing 'root' and ending with 'bo.txt'.",
        default="data/chojuk",
        nargs="?"
    )
    args = parser.parse_args()
    
    combine_and_count_lines(args.root_dir)


if __name__ == "__main__":
    main() 