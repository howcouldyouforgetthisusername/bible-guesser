"""
Loads the King James Version of the Bible from Project Gutenberg.
"""

import os

import requests

KJV_URL = "http://www.gutenberg.org/cache/epub/10/pg10.txt"
KJV_PATH = "assets/kjv.txt"
PREAMBLE_NUM_LINES = 103


def get_remote_kjv() -> str:
    """
    Get the complete text of the King James Version of the Bible from Project Gutenberg.
    """
    response = requests.get(KJV_URL)
    return response.text


def write_kjv(file_path: str = KJV_PATH) -> None:
    """
    Ensure that the King James Version of the Bible is available locally at the given path.
    Trims off the preamble and the testament titles.
    """
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            seen_first_kings = False
            seen_second_kings = False
            for line in get_remote_kjv().splitlines()[PREAMBLE_NUM_LINES:]:
                if line in {
                    "The Old Testament of the King James Version of the Bible",
                    "The New Testament of the King James Bible",
                    "Otherwise Called:",
                    "Commonly Called:",
                    "The Third Book of the Kings",
                    "The Fourth Book of the Kings",
                }:
                    continue
                if not seen_first_kings and line == "The First Book of the Kings":
                    seen_first_kings = True
                    continue
                if not seen_second_kings and line == "The Second Book of the Kings":
                    seen_second_kings = True
                    continue
                file.write(line + "\n")


def read_kjv_text(file_path: str = KJV_PATH) -> str:
    """
    Read the KJV text from the given path. If the path doesn't exist, try to download it.
    """
    write_kjv(file_path)
    with open(file_path, "r") as f:
        return f.read()
