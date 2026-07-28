"""Archive directories older than the current year into zip files."""

import configparser
import os
import shutil
import zipfile
from datetime import date


def lazy_logger(log: str) -> None:
    """Append a log message to the log file."""
    with open("log.log", "a+", encoding="utf-8") as file:
        file.write(log)
        file.write("\n")


def main():
    """Archive year-based directories that are older than the current year."""
    YEAR = str(date.today().year)
    dirs_to_zip = []

    cfg = configparser.ConfigParser()
    path = cfg["archiver"]["hr_path"] if cfg.read("nothing") else None
    if path is None or not os.path.isdir(path):
        lazy_logger("Failed to read secrets.")
        return

    for root, dirs, _ in os.walk(path, topdown=False):
        for d in dirs:
            target = root + "\\" + d
            if len(d) == len(YEAR) and d < YEAR and os.path.isdir(target):
                dirs_to_zip.append(target)

    for directory in dirs_to_zip:
        print(f"Zipping {directory}...")
        if os.path.isfile(directory + ".zip"):
            lazy_logger(f"Zipper, {directory}.zip already exists.")
            print(f"Zipped {directory}.")
            try:
                shutil.rmtree(directory)
            except Exception as e:
                lazy_logger(f"Failed to remove directory.\n{directory}\n{e}")
            continue
        try:
            with zipfile.ZipFile(
                f"{directory}.zip", "w", zipfile.ZIP_DEFLATED
            ) as zip_file:
                for root, _, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            zip_file.write(
                                file_path, os.path.relpath(file_path, directory)
                            )
                        else:
                            lazy_logger(f"Zipper, {file_path} not file.")
                            return 1
        except Exception as e:
            lazy_logger(f"Failed to zip something in {directory}.\n{e}")
            continue
        print(f"Zipped {directory}.")
        shutil.rmtree(directory)


if __name__ == "__main__":
    main()
