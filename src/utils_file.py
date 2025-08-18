import pathlib

def read_file(file_path: pathlib.Path) -> str:
    """Read a semicolon-delimited CSV file into a list of row dicts."""
    with open(file_path, newline="", encoding="utf-8") as f:
        return f.read()
