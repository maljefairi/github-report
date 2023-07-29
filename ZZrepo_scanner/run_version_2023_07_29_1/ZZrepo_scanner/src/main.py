import os
from datetime import datetime
from pathlib import Path
from utils.utils import (
    load_or_request_settings, 
    process_files, 
    save_settings, 
    get_file_types, 
    count_files_and_words, 
    get_exclude_list, 
    get_scanner_dir
)

OUTPUT_DIR_PREFIX = "run_version_"
REPOSITORY_PATH = Path(os.getcwd())
ZZREPO_SCANNER_DIR = REPOSITORY_PATH / "ZZrepo_scanner"

def main():
    exclude_list = get_exclude_list()
    scanner_dir = get_scanner_dir()
    if Path(scanner_dir).is_dir():
        exclude_list.append(scanner_dir)

    today_date = datetime.now().strftime("%Y_%m_%d")
    run_count = sum(1 for d in ZZREPO_SCANNER_DIR.iterdir() if d.is_dir() and today_date in d.name) + 1
    output_dir = ZZREPO_SCANNER_DIR / f"{OUTPUT_DIR_PREFIX}{today_date}_{run_count}"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_file_types = get_file_types(REPOSITORY_PATH, exclude_list)

    for file_type in all_file_types:
        file_count, word_count = count_files_and_words(REPOSITORY_PATH, file_type, exclude_list)
        print(f"For file type {file_type}: {file_count} files, {word_count} words")

    included_file_types = load_or_request_settings(all_file_types, REPOSITORY_PATH)

    process_files(REPOSITORY_PATH, included_file_types, exclude_list, output_dir)

    save_settings(included_file_types, output_dir)

if __name__ == '__main__':
    main()