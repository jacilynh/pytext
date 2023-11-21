def split_text_file(file_path, num_parts):
    # Read the content of the original file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Calculate the length of each part
    part_length = len(content) // num_parts

    # Split the content into parts
    parts = [content[i:i + part_length] for i in range(0, len(content), part_length)]

    # Adjust the last part to include any remaining content
    if len(parts) > num_parts:
        parts[num_parts-1:] = [''.join(parts[num_parts-1:])]

    # Save each part to a new file
    for i, part in enumerate(parts):
        new_file_name = f"{file_path.rsplit('.', 1)[0]}_{i + 1}.txt"
        with open(new_file_name, 'w', encoding='utf-8') as new_file:
            new_file.write(part)
        print(f"Part {i + 1} saved to {new_file_name}")

# Example usage
file_path = '/Users/Jacilyn/Documents/code/pytext/data/Construction.txt'  # Replace with your file path
num_parts = 5  # Replace with the number of parts you want
split_text_file(file_path, num_parts)
# The code above will split the original file into 5 parts and save each part to a new file.