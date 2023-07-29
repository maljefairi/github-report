```markdown
# Usage Guide

This guide provides instructions on how to use the ZZRepo Scanner.

1. Navigate to the project directory:
   ```
   cd ZZrepo_scanner
   ```
2. Run the `main.py` script from the command line:
   ```
   python main.py
   ```
3. The script will scan the current directory, identify the file types, and ask you to provide the file types to include for processing. Enter the desired file types (comma separated, with no spaces, e.g., .py,.js) and press Enter.

The script will start processing the selected files and will save the improved code in a newly created directory in the `ZZrepo_scanner` directory. The name of this directory starts with `run_version_` followed by the date and run count.

The `settings.txt` file in the output directory keeps track of your settings for future runs. When running the script the next time, you can choose to use these settings again.
```