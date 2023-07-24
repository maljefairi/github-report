import os
import json
import glob
from dotenv import load_dotenv
from utils import get_file_types, ask_user_inputs, parse_gitignore, get_all_files, count_files_and_words
import openai
import time

# Load the OpenAI key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define constants
SETTINGS_FILE = "settings.txt"
PROGRESS_FILE = "progress.json"
REPOSITORY_PATH = '.'
OUTPUT_DIR_PREFIX = "run_version_"

def delete_gpt_files(path):
    for file in glob.glob(f"{path}/**/*GPT.*", recursive=True):
        os.remove(file)

def load_or_request_settings(all_file_types):
    if os.path.isfile(SETTINGS_FILE):
        load_previous = input('Do you want to run with the previous settings? (y/n) ')
        if load_previous.lower() == 'y':
            with open(SETTINGS_FILE, 'r') as file:
                settings = json.load(file)
            return settings['included_file_types']
    return ask_user_inputs(all_file_types, REPOSITORY_PATH)

def process_files(all_files, output_dir):
    total_files = len(all_files)
    progress = {}
    for i, (file_path, file_content) in enumerate(all_files):
        if 'GPT' not in file_path:
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
            improved_code = response['choices'][0]['message']['content']
            new_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + 'GPT' + os.path.splitext(os.path.basename(file_path))[1])
            with open(new_file, 'w') as f:
                f.write(improved_code)
            progress[file_path] = True
            with open(os.path.join(output_dir, PROGRESS_FILE), 'w') as file:
                json.dump(progress, file)
            print(f'Processed file {i+1}/{total_files} ({(i+1)/total_files*100:.2f}%)')

def save_settings(included_file_types, output_dir):
    settings = {
        'included_file_types': included_file_types,
    }
    with open(os.path.join(output_dir, SETTINGS_FILE), 'w') as file:
        json.dump(settings, file)

def main():
    # Get version for this run
    run_version = str(int(time.time()))
    output_dir = OUTPUT_DIR_PREFIX + run_version

    # Create output directory for this run
    os.mkdir(output_dir)

    # Delete previous GPT.* files
    delete_gpt_files(REPOSITORY_PATH)
    
    # Get file types
    all_file_types = get_file_types(REPOSITORY_PATH)

    # Display count of files and words for each file type
    for file_type in all_file_types:
        file_count, word_count = count_files_and_words(REPOSITORY_PATH, file_type)
        print(f"For file type {file_type}: {file_count} files, {word_count} words")
    
    # Load previous or request new settings
    included_file_types = load_or_request_settings(all_file_types)
    
    # Get files to process
    ignore_patterns = parse_gitignore(REPOSITORY_PATH)
    ignore_patterns.append(OUTPUT_DIR_PREFIX + '*')  # Exclude output directories from the scan
    all_files = get_all_files(REPOSITORY_PATH, included_file_types, ignore_patterns)

    # Processing files
    process_files(all_files, output_dir)

    # Save settings for next time
    save_settings(included_file_types, output_dir)


if __name__ == '__main__':
    main()
