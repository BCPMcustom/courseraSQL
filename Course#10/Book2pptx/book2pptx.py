import sys
import os
from parser.markdown_parser import (TableParser, HTMLTableRenderer, MarkdownParser)

def main():
    # sys.argv[0] is always the script name ('book2pptx.py')
    # sys.argv[1] will be the first argument passed ('path_to_markdown.md')
    if len(sys.argv) < 2:
        print("Error: Please provide a file path.")
        print("Usage: python3 book2pptx.py <path_to_markdown.md>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    print(f"Starting book2pptx script with input: {input_path}")

    # 1. Establish where our assets directory lives relative to this main file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    target_path = os.path.join(ASSETS_DIR, input_path)

    print(f"Processing {target_path} through markdown_parser...")

    try:
        # 4. Instantiate your parser and pass the user's terminal variable into it
        parser = MarkdownParser()
        presentation = parser.parse(target_path)
        
        print("Finished processing successfully!")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")
        sys.exit(1)

    print(f"Processing {input_path} through markdown_parser...")
    
    print("Finished processing.")

if __name__ == "__main__":
    main()
