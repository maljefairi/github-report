```markdown
# API Reference

This document provides an overview of all functions in the ZZRepo Scanner project.

- `main.py`: The script that drives the entire process.
    - `main()`: The main function. It's responsible for orchestrating the entire scanning and processing process.

- `utils.py`: Contains helper functions for the main script.
    - `get_scanner_dir()`: Returns the directory of the current script.
    - `text_file_word_count(file_path)`: Counts the words in a text file.
    - `get_exclude_list()`: Retrieves the list of directories to exclude.
    - `count_files_and_words(path, file_type, exclude_list)`: Counts the number of files and words of a given type in a directory.
    - `get_file_types(path, exclude_list)`: Retrieves a list of all unique file types in a directory.
    - `ask_user_inputs(file_types, path)`: Asks the user for the file types to include.
    - `load_or_request_settings(all_file_types, path)`: Loads the settings from the settings file if it exists, otherwise requests new settings from the user.
    - `call_openai_api(file_content)`: Sends the file content to OpenAI API for processing.
    - `process_files(path, included_file_types, exclude_dir, output_dir)`: Processes all the files in the list and saves the processed files in the output directory.
    - `save_settings(included_file_types, output_dir)`: Saves the settings for the next run.
```