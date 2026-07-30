# archiver

A small Python utility that walks a configured directory tree, finds subdirectories
whose names are older than the current year, and archives them into zip files.

## What it does

- Scans a root path for subdirectories
- Selects directories whose names are older than the current year
- Creates a zip archive for each matching directory
- Removes the original directory after a successful archive
- Writes failures to a log file named log.log

## Usage

1. Update the script so it points to the directory you want to scan.
2. Run the script with Python:

   ```bash
   python main.py
   ```

3. Review the generated zip files and the log file if anything fails.

## Notes

- The script expects a valid directory path to be available for processing.
- Any archive or removal errors are logged instead of crashing the script.
