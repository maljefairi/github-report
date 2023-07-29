import os
from datetime import datetime
from pathlib import Path
from utils.utils import load_or_request_settings, process_files, save_settings, get_file_types, count_files_and_words, get_exclude_list, get_scanner_dir

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

OUTPUT_DIR_PREFIX = "run_version_"
# Define the REPOSITORY_PATH
REPOSITORY_PATH = Path(os.getcwd())

ZZREPO_SCANNER_DIR = Path(REPOSITORY_PATH) / "ZZrepo_scanner"

def main():
    # Get exclude list from exclude.txt
    exclude_list = get_exclude_list()

    # Exclude ZZrepo_scanner from processing
    scanner_dir = get_scanner_dir()
    exclude_list.append(scanner_dir) if Path(scanner_dir).is_dir() else None

    # Create an output directory for this run with the current date and run count
    today_date = datetime.now().strftime("%Y_%m_%d")
    run_count = len([d for d in os.listdir(ZZREPO_SCANNER_DIR) if today_date in d and os.path.isdir(d)]) + 1 if ZZREPO_SCANNER_DIR.is_dir() else 1
    output_dir = ZZREPO_SCANNER_DIR / (OUTPUT_DIR_PREFIX + today_date + '_' + str(run_count))
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get file types
    all_file_types = get_file_types(REPOSITORY_PATH, exclude_list)

    # Display count of files and words for each file type
    for file_type in all_file_types:
        file_count, word_count = count_files_and_words(REPOSITORY_PATH, file_type, exclude_list)
        print(f"For file type {file_type}: {file_count} files, {word_count} words")
    
    # Load previous or request new settings
    included_file_types = load_or_request_settings(all_file_types, REPOSITORY_PATH)

    # Process the files
    process_files(REPOSITORY_PATH, included_file_types, exclude_list, output_dir)

    # Save settings for next time
    save_settings(included_file_types, output_dir)

if __name__ == '__main__':
    main()
