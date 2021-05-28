from pathlib import Path

__version__ = "3.7.8"

CURRENT_DIR: Path = Path(__file__).parent
RESOURCES_DIR: Path = CURRENT_DIR / "resources"


def get_file_content_from_line(file: Path, line: int) -> str:
    content = ""
    with open(file, "r") as f:
        for i, _line in enumerate(f.readlines(), 0):
            if i >= line:
                content += _line
    return content
