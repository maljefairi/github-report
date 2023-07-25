import os
import fnmatch
import codecs
from typing import List, Tuple

def get_file_types(path: str) -> List[str]:
    """Get a list of all unique file types in a directory."""
    file_types = set()
    for root, _, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[-1]
            file_types.add(ext)
    return list(file_types)

def count_files_and_words(path: str, file_type: str) -> Tuple[int, int]:
    """Count the number of files and words for a given file type in a directory."""
    file_count, word_count = 0, 0
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(file_type):
                file_count += 1
                with codecs.open(os.path.join(root, file), 'r', 'utf-8', errors='ignore') as f:
                    word_count += len(f.read().split())
    return (file_count, word_count)

def ask_user_inputs(file_types: List[str], path: str) -> List[str]:
    """Ask user for the file types to include."""
    while True:
        included_file_types = input("Please provide the file types to include (comma separated, with no spaces, e.g., .py,.js): ").split(',')
        if all(file_type in file_types for file_type in included_file_types):
            return included_file_types
        print("Please provide valid file types.")

def ask_user_for_previous_settings() -> str:
    """Ask user if they want to use previous settings."""
    while True:
        use_prev_settings = input("Do you want to use the previous settings? (yes/no): ").lower()
        if use_prev_settings in ['yes', 'no']:
            return use_prev_settings
        print("Please provide a valid response (yes/no).")

def parse_gitignore(path: str) -> List[str]:
    """Parse the .gitignore file and get a list of ignore patterns."""
    ignore_patterns = []
    gitignore = os.path.join(path, '.gitignore')
    if os.path.isfile(gitignore):
        with open(gitignore, 'r') as file:
            ignore_patterns = [line.strip() for line in file]
    return ignore_patterns

def get_all_files(path: str, included_file_types: List[str], ignore_patterns: List[str]) -> List[Tuple[str, str]]:
    """Get all files with specified file types in a directory, excluding those matching the ignore patterns."""
    all_files = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns) and os.path.splitext(f)[-1] in included_file_types]
        for file in files:
            with codecs.open(os.path.join(root, file), 'r', 'utf-8', errors='ignore') as f:
                file_content = f.read()
            all_files.append((os.path.join(root, file), file_content))
    return all_files