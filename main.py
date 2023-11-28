import os
import re
import string
from collections import defaultdict

def tokenize(text):
    # Split text into words, remove punctuation, and lower case
    return re.findall(r'\b\w+\b', text.lower())


def create_index(directory):
    index = defaultdict(set)
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                for word in tokenize(file.read()):
                    index[word].add(filename)
    return index

def get_context(text, term, window=1000):
    # This function finds the term in the text and returns the context around it
    for match in re.finditer(term, text):
        start = max(match.start() - window, 0)
        end = min(match.end() + window, len(text))
        yield text[start:end]

def search_and_context(query, directory, index):
    results = defaultdict(list)
    query_lower = query.lower()  # Convert query to lowercase
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read().lower()  # Convert content to lowercase
                if query_lower in content:  # Check if query is in content
                    for context in get_context(content, re.escape(query_lower)):
                        results[filename].append(context)
    return results

def sanitize_filename(filename):
    """Create a valid filename from a string."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    return cleaned_filename

# Usage Example
# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Relative path to the data directory from the script
data_dir = os.path.join(script_dir, 'data')  # 'data' is a folder in the same directory as your script

index = create_index(data_dir)
query = "bridge"  # Replace with your search term

results = search_and_context(query, data_dir, index)

# Create a valid file name from the search term
file_name = sanitize_filename(query) + ".txt"
file_path = os.path.join(script_dir, file_name)  # Save the result in the same directory as the script

# Write results to a file
with open(file_path, 'w', encoding='utf-8') as file:
    for filename, contexts in results.items():
        file.write(f"In file '{filename}':\n")
        for context in contexts:
            file.write(context + "\n\n---\n\n")

print(f"Search results saved to {file_path}")