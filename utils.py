import os
import fnmatch
import json

# List of directories to ignore
IGNORED_DIRS = ['__pycache__', '.git', '.venv', '.docker', '.pipenv']

# List of file types/extensions to ignore
IGNORED_FILE_TYPES = ['.pyc', '.pyo', '.pyd', '.whl', '.zip', '.tar', '.gz', '.rar', '.7z', '.dll', '.so', '.dylib']

def get_all_files(directory, file_types, ignore_patterns):
    code_data = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]  # Filter out unwanted directories
        for file in files:
            file_ext = os.path.splitext(file)[-1].lower()
            if file_ext in IGNORED_FILE_TYPES:  # Skip files with unwanted file types
                continue
            file_path = os.path.join(root, file)
            file_path = os.path.abspath(file_path)  # Ensure path is absolute
            relative_path = os.path.relpath(file_path, directory)
            if is_ignored(relative_path, ignore_patterns):
                continue
            if file_ext in file_types and file != 'scannerPro2.py':
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    code_data.append((relative_path, file_content))
    return code_data


# Function to remove previous output files
def remove_previous_output(directory, pattern='scanned*.txt'):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                os.remove(os.path.join(root, file))

# Function to ask user for inputs
def ask_user_inputs(all_file_types, repository_path):
    print('The file types found in the directory are:')
    included_file_types = []
    for file_type in all_file_types:
        file_count, word_count = count_files_and_words(repository_path, file_type)
        include = input(f'Do you want to include files of type {file_type} ({file_count} files, {word_count} words)? (y/n) ')
        if include.lower() == 'y':
            included_file_types.append(file_type)
    max_words_input = input('How many words do you want to include in each file? Leave blank for no splitting: ')
    max_words = int(max_words_input) if max_words_input.isdigit() else 1500
    include_tree = input('Do you want to include the directory tree? (y/n): ')
    additional_text = input("Do you want to add any text after 'This is the prompt number {}'? Enter the text or leave it blank: ")
    return included_file_types, max_words, include_tree, additional_text

# Function to parse .gitignore file for ignore patterns
def parse_gitignore(directory):
    gitignore_path = os.path.join(directory, ".gitignore")
    if not os.path.exists(gitignore_path):
        return []
    with open(gitignore_path, "r") as file:
        lines = file.read().split("\n")
    return lines

# Function to check if the given path is ignored
def is_ignored(path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

# Function to get all files in the directory matching the file types and not matching the ignore patterns
def get_all_files(directory, file_types, ignore_patterns):
    code_data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            if is_ignored(relative_path, ignore_patterns):
                continue
            file_ext = os.path.splitext(file)[-1].lower()
            if file_ext in file_types and file != 'scannerPro2.py':
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    code_data.append((relative_path, file_content))
    return code_data

# Function to get all unique file types in the directory
def get_file_types(directory):
    file_types = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[-1].lower()
            file_types.add(file_ext)
    return file_types

# Function to count the number of files and words of the given file type in the directory
def count_files_and_words(directory, file_type):
    file_count = 0
    word_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[-1].lower()
            if file_ext == file_type:
                file_count += 1
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        word_count += len(f.read().split())
                except UnicodeDecodeError:
                    print(f"Skipped file due to UnicodeDecodeError: {os.path.join(root, file)}")
    return file_count, word_count

# Function to split text into chunks of max_words
def split_text(text, max_words):
    words = text.split()
    chunks = []
    chunk = []
    count = 0
    for word in words:
        if count + len(word.split()) <= max_words:
            chunk.append(word)
            count += len(word.split())
        else:
            chunks.append(' '.join(chunk))
            chunk = [word]
            count = len(word.split())
    chunks.append(' '.join(chunk))
    return chunks

# Function to generate the directory tree
def generate_directory_tree(directory):
    tree = ''
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree += '{}{}/\n'.format(indent, os.path.basename(root))
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            tree += '{}{}\n'.format(sub_indent, file)
    return tree
