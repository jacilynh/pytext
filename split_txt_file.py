import os

def split_text_file(file_path, num_parts, output_dir):
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

    # Save each part to a new file in the output directory
    base_name = os.path.basename(file_path).rsplit('.', 1)[0]
    for i, part in enumerate(parts):
        new_file_name = f"{base_name}_{i + 1}.txt"
        new_file_path = os.path.join(output_dir, new_file_name)
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(part)
        print(f"Part {i + 1} saved to {new_file_path}")

def split_all_files_in_directory(source_dir, num_parts, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for file_name in os.listdir(source_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(source_dir, file_name)
            split_text_file(file_path, num_parts, target_dir)

# Example usage
source_dir = '/Users/Jacilyn/Documents/code/pytext/data/long'  # Replace with your source directory
target_dir = '/Users/Jacilyn/Documents/code/pytext/data/txt'  # Replace with your target directory
num_parts = 5
split_all_files_in_directory(source_dir, num_parts, target_dir)
