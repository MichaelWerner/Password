import os
import re
import argparse

def replace_umlauts(text):
    """
    Replace German umlauts and ß in the given text with their equivalents.
    """
    umlaut_map = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "Ä": "AE",
        "Ö": "OE",
        "Ü": "UE",
        "ß": "ss"
    }
    for umlaut, replacement in umlaut_map.items():
        text = text.replace(umlaut, replacement)
    return text

def create_wordlist_from_file(file_path):
    # Read the entire file
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
    
    # Replace umlauts in the text
    contents = replace_umlauts(contents)
    
    # Extract words; the regex \b\w+\b finds sequences of alphanumeric characters (and underscores)
    words = re.findall(r'\b\w+\b', contents)
    
    # Keep only words with at least 5 characters
    words = [word for word in words if len(word) >= 5]
    
    # Remove duplicates. Using a set makes them unique.
    unique_words = set(words)
    
    # Build the output filename in the same directory as the original file.
    directory, original_filename = os.path.split(file_path)
    output_filename = f"wordlist_{original_filename}"
    output_path = os.path.join(directory, output_filename)
    
    # Write each word on its own line in the output file.
    with open(output_path, 'w', encoding='utf-8') as f:
        for word in unique_words:
            f.write(word + "\n")
    
    print(f"Word list created at: {output_path}")

# Example usage:
if __name__ == '__main__':
    # Replace this with the path to your text file.
    file_path = "c:\\users\\micha\\downloads\\why_wars.txt"
    create_wordlist_from_file(file_path)
    

def main():
    parser = argparse.ArgumentParser(description="Create a word list from a text file with words at least 5 characters long.")
    parser.add_argument("file", help="Path to the input text file")
    args = parser.parse_args()
    
    # Check if the provided file exists
    if not os.path.isfile(args.file):
        print(f"Error: The file '{args.file}' does not exist.")
        return

    create_wordlist_from_file(args.file)

if __name__ == '__main__':
    main()