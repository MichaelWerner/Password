import random
import sys
import math
from zxcvbn import zxcvbn

# Mapping of special characters to their corresponding numbers on a US keyboard
special_char_map = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
}

vowel_map = {
    "a": "1",
    "e": "2",
    "i": "3",
    "o": "4",
    "u": "5",
    "A": "1",
    "E": "2",
    "I": "3",
    "O": "4",
    "U": "5",
}

reverse_vowel_map = {
    "1": "a",
    "2": "e",
    "3": "i",
    "4": "o",
    "5": "u",
    "6": "A",
    "7": "E",
    "8": "I",
    "9": "O",
    "0": "U"    
}

def load_words_from_file(filename):
    """Load words from a file, stripping whitespace."""
    try:
        with open(filename, 'r') as file:
            words = [line.strip() for line in file if len(line.strip()) >= 5]
            if not words:
                raise ValueError("Word list is empty or no valid words found.")
            return words
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Please create the file with valid words.")
        exit()
    except ValueError as ve:
        print(f"Error: {ve}")
        exit()

def generate_memorable_password(words):
    """Generate a memorable password using words from the loaded list."""
    special_chars = ["!","@", "#", "$", "%", "^", "&", "*", "(", ")"]
    num4 = str(random.randint(1000, 9999))
    
    # Pick two random words
    word1 = random.choice(words)
    word2 = random.choice(words)
    # Ensure words are different
    while word1 == word2:
        word2 = random.choice(words)
    
    # Iterate over indices that correspond to every third letter
    for i in range(2, len(word1), 3):
        if word1[i] in vowel_map:
            # Rebuild the string by slicing before, adding the replacement, and slicing after.
            word1 = word1[:i] + vowel_map[word1[i]] + word1[i+1:]

    for i in range(2, len(word2), 3):
        if word2[i] in vowel_map:
            # Rebuild the string by slicing before, adding the replacement, and slicing after.
            word2 = word2[:i] + vowel_map[word2[i]] + word2[i+1:]

    # Assemble the password
    if len(word1) >= 10:
        full_password = f"{word1}{random.choice(special_chars)}{num4}"
    elif len(word2) >= 10:
        full_password = f"{word2}{random.choice(special_chars)}{num4}" 
    else:
        full_password = f"{word1}{random.choice(special_chars)}{word2}{random.choice(special_chars)}{num4}" 

    return full_password


def truncate_password(full_password):
    # Replace special characters with corresponding numbers
    for char in special_char_map:
        full_password = full_password.replace(char, special_char_map[char])

    """Truncate password for second system compliance."""
    truncated = ''.join(char for char in full_password if char.isalnum())[:10]
    # Ensure the last character is not a number
    if truncated[-1].isdigit():
        truncated = truncated[:-1] + reverse_vowel_map[truncated[-1]]  # Replace with a letter
    return truncated

def generate_password_pairs(words, count=10):
    """Generate password pairs for both systems."""
    password_pairs = []
    for _ in range(count):
        full_password = generate_memorable_password(words)
        truncated_password = truncate_password(full_password)
        password_pairs.append((full_password, truncated_password))
    return password_pairs

def format_time(seconds):
    """
    Converts seconds to a human-readable string with years, days, hours, minutes, and seconds.
    """
    intervals = (
        ('years', 31536000),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    )
    result = []
    for name, count in intervals:
        value = int(seconds // count)
        if value:
            result.append(f"{value} {name}")
            seconds -= value * count
    return ', '.join(result) if result else "0 seconds"


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <wordlist_file>")
        exit()
    
    wordlist_file = sys.argv[1]
    words = load_words_from_file(wordlist_file)
    passwords = generate_password_pairs(words)
    for full, truncated in passwords:
        # Evaluate the password using zxcvbn
        time_full = zxcvbn(full)
        time_trunc = zxcvbn(truncated)
        
        # Get the online_no_throttling_10_per_second crack time
        online_time_seconds_full = time_full['crack_times_seconds'].get('online_no_throttling_10_per_second', None)
        online_time_seconds_trunc = time_trunc['crack_times_seconds'].get('online_no_throttling_10_per_second', None)

        print(f"Full: {full} (crack time: {format_time(online_time_seconds_full)})")
        print(f"Truncated: {truncated} (crack time: {format_time(online_time_seconds_trunc)})")
        print(" ")

if __name__ == "__main__":
    main()
