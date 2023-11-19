import os
import re
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


def get_context(text, term, window=600):
    # This function finds the term in the text and returns the context around it
    for match in re.finditer(term, text):
        start = max(match.start() - window, 0)
        end = min(match.end() + window, len(text))
        yield text[start:end]

def search_and_context(query, directory, index):
    results = defaultdict(list)
    for filename in index.get(query.lower(), set()):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            for context in get_context(content, re.escape(query)):
                results[filename].append(context)
    return results


# Usage Example
directory = '/users/snowsummer/code/gpt/wsdot/pytext/data'  # Replace with your directory path
index = create_index(directory)
query = "abutment"  # Replace with your search term

results = search_and_context(query, directory, index)

for filename, contexts in results.items():
    print(f"\nIn file '{filename}':")
    for context in contexts:
        print(context)
        print("\n---\n")
