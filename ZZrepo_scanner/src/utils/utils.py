import os
import json
import codecs
import logging
import time
from typing import List, Tuple
from pathlib import Path
from dotenv import load_dotenv
import openai
import backoff
import fnmatch

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SETTINGS_FILE = "settings.txt"
IGNORE_DIR = ['ZZrepo_scanner']
PROGRESS_FILE = "progress.json"
LOG_FILE = "error.log"
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)

def get_scanner_dir():
    return os.path.dirname(os.path.realpath(__file__))

def text_file_word_count(file_path: Path) -> int:
    """
    Counts the words in a text file
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()
    return len(data.split())

def get_exclude_list() -> List[str]:
    exclude_txt = Path(__file__).parent / 'exclude.txt'
    with open(exclude_txt, 'r') as file:
        exclude_list = [line.strip() for line in file if line.strip()]
    return exclude_list

def count_files_and_words(path: Path, file_type: str, exclude_list: List[str]) -> Tuple[int, int]:
    """Count the number of files and words of a given type in a directory."""
    file_count = 0
    word_count = 0
    for root, _, files in os.walk(path):
        if any(x in root for x in exclude_list):
            continue
        for file in files:
            if file.endswith(file_type) and not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_list):
                file_path = os.path.join(root, file)
                word_count += text_file_word_count(Path(file_path))
                file_count += 1
    return file_count, word_count

def get_file_types(path: Path, exclude_list: List[str]) -> List[str]:
    """Get a list of all unique file types in a directory."""
    file_types = set()
    for root, _, files in os.walk(path):
        if any(x in root for x in exclude_list):
            continue
        for file in files:
            if not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_list):
                ext = os.path.splitext(file)[-1]
                file_types.add(ext)
    return list(file_types)

def ask_user_inputs(file_types: List[str], path: Path) -> List[str]:
    """Ask user for the file types to include."""
    while True:
        included_file_types = input("Please provide the file types to include (comma separated, with no spaces, e.g., .py,.js): ").split(',')
        if all(file_type in file_types for file_type in included_file_types):
            return included_file_types
        print("Please provide valid file types.")

def load_or_request_settings(all_file_types: list, path: Path) -> List[str]:
    """Loads the settings from the settings file if it exists, otherwise it requests new settings from the user."""
    settings_file = path / SETTINGS_FILE
    if settings_file.is_file():
        load_previous = input('Do you want to run with the previous settings? (y/n) ')
        if load_previous.lower() == 'y':
            with settings_file.open('r') as file:
                settings = json.load(file)
            return settings['included_file_types']
    return ask_user_inputs(all_file_types, path)

@backoff.on_exception(backoff.expo,
                      (openai.error.RateLimitError, openai.error.OpenAIError),
                      max_time=300)
def call_openai_api(file_content):
    """Send the file content to OpenAI API for processing."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert coder. fix the logic, errors, threats, concerns, and rewrite the code based on best practices. you will reply with nothing but the new code"},
            {"role": "user", "content": file_content}
        ],
        temperature=0.5,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']['content']

def process_files(path: Path, included_file_types: List[str], exclude_dir: List[str], output_dir: Path):
    """Processes all the files in the list 'all_files' and saves the processed files in 'output_dir'."""
    all_files = []
    for file_type in included_file_types:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(file_type) and os.path.basename(root) not in exclude_dir:
                    file_path = os.path.join(root, file)
                    word_count = text_file_word_count(Path(file_path))
                    all_files.append((file_path, word_count))
    
    total_files = len(all_files)
    progress = {}
    i = 0
    while i < total_files:
        file_path, word_count = all_files[i]
        try:
            print(f"Processing file {i + 1}/{total_files}...")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()
            new_content = call_openai_api(file_content)
            new_file_path = output_dir / Path(file_path).relative_to(path)
            new_file_path.parent.mkdir(parents=True, exist_ok=True)
            with codecs.open(new_file_path, 'w', 'utf-8') as new_file:
                new_file.write(new_content)
        except OSError as e:
            logging.error(f"Failed to process {file_path}. Error: {e}")
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API call failed for {file_path}. Error: {e}")
        else:
            progress[str(file_path)] = i
            with open(output_dir / PROGRESS_FILE, 'w') as progress_file:
                json.dump(progress, progress_file)
            print(f"Successfully processed file {i + 1}/{total_files}.")
            i += 1
        time.sleep(1)

def save_settings(included_file_types: List[str], output_dir: Path):
    """Saves the settings for the next run."""
    settings = {
        'included_file_types': included_file_types,
    }
    with open(output_dir / SETTINGS_FILE, 'w') as file:
        json.dump(settings, file)
