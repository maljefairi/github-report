# ZZRepo Scanner

## Overview

ZZRepo Scanner is a Python script that scans a repository and makes improvements on the codebase leveraging the power of OpenAI's GPT-4 model. The project aims to bring intelligent coding assistance to your workflow. 

The script navigates through the repository, identifies the file types, and allows the user to select which types to include for the enhancement process. The identified files are then processed by sending their content to OpenAI's GPT-4 model. The received improved code is then saved in a newly created directory.

## Features

- Identifies and counts the number of files and words in a given repository.
- Asks the user to specify which file types to include for processing.
- Leverages OpenAI's GPT-4 model to improve code quality and adherence to best practices.
- The processed files are saved in a unique directory for each run.
- Error handling and logging mechanism to troubleshoot potential issues during code processing.
- Progress tracking of the scanning and processing tasks.

## Installation

You'll need Python 3.6 or later. If not already installed, you can download it from the [Python official website](https://www.python.org/downloads/).

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ZZrepo_scanner.git
   ```
2. Navigate into the project directory:
   ```
   cd ZZrepo_scanner
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the `main.py` script from the command line:
```
python main.py
```

The script will scan the current directory, identify the file types, and ask you to provide the file types to include for processing. Enter the desired file types (comma separated, with no spaces, e.g., .py,.js) and press Enter.

The script will start processing the selected files and will save the improved code in a newly created directory in the `ZZrepo_scanner` directory. The name of this directory starts with `run_version_` followed by the date and run count.

The `settings.txt` file in the output directory keeps track of your settings for future runs. When running the script the next time, you can choose to use these settings again.

## Errors and Logging

If the script encounters an error while processing a file, it will log the error message and continue with the next file. You can review the `error.log` file in the `src/utils` directory for error details.

## Contributing

Feel free to fork the project and make improvements. We're open to any contributions that enhance the functionality and usability of the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.