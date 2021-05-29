from pathlib import Path
from typing import List

__version__ = "3.7.8"

CURRENT_DIR: Path = Path(__file__).parent
RESOURCES_DIR: Path = CURRENT_DIR / "resources"


def get_file_content_from_line(
    file: Path, line: int, ignore_lines: List[int] = []
) -> str:
    content = ""
    with open(file, "r") as f:
        for i, _line in enumerate(f.readlines(), start=1):
            if i >= line and i not in ignore_lines:
                content += _line
    return content
