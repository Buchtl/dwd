import pathlib
import zipfile
import io
from typing import Dict

def read_file(file_path: pathlib.Path) -> str:
    """Read a semicolon-delimited CSV file into a list of row dicts."""
    with open(file_path, newline="", encoding="utf-8") as f:
        return f.read()

def read_zip_as_strings(input_file: pathlib.Path):
    result: Dict[str, str] = {}
    with zipfile.ZipFile(input_file, "r") as zf:
        for file_name in zf.namelist():
            if file_name.endswith("/"):
                continue
            with zf.open(file_name) as f:
                text = io.TextIOWrapper(f, encoding="utf-8").read()
                result[file_name] = text
    return result
