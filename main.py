import os
import re
import string
from collections import defaultdict

def get_context(text, term, window=1000):
    # This function finds the term in the text and returns the context around it
    for match in re.finditer(re.escape(term), text, re.IGNORECASE):
        start = max(match.start() - window, 0)
        end = min(match.end() + window, len(text))
        yield text[start:end]

def search_and_context(query, root_directory):
    results = defaultdict(list)

    for directory, subdirs, files in os.walk(root_directory):
        for filename in files:
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for context in get_context(content, query):
                        results[filepath].append(context)
    return results

def highlight_term(text, term):
    # Markdown bold format
    highlighted_text = text.replace(term, f"**{term}**")
    return highlighted_text

def sanitize_filename(filename):
    """Create a valid filename from a string."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = ''.join(c for c in filename if c in valid_chars)
    return cleaned_filename

# Usage Example
script_dir = os.path.dirname(os.path.realpath(__file__)) # Get the directory of the current script
data_dir = os.path.join(script_dir, 'data')  # 'data' is a folder in the same directory as your script

# Prompt the user for a search term
query = input("Enter the search term: ")

results = search_and_context(query, data_dir)

# Create a Markdown file name from the search term
file_name = sanitize_filename(query) + ".md"
file_path = os.path.join(script_dir, file_name)  # Save the result in the same directory as the script

# Write results to a Markdown file
with open(file_path, 'w', encoding='utf-8') as file:
    for filename, contexts in results.items():
        file.write(f"### In file '{filename}':\n")
        for context in contexts:
            highlighted_context = highlight_term(context, query)
            file.write(highlighted_context + "\n\n---\n\n")

print(f"Search results saved in Markdown format to {file_path}")
