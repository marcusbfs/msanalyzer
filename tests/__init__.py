import re
from pathlib import Path

__version__ = "3.7.8"

CURRENT_DIR: Path = Path(__file__).parent
RESOURCES_DIR: Path = CURRENT_DIR / "resources"


def get_file_content_from_line(file: Path, line: int) -> str:
    content = ""
    with open(file, "r") as f:
        for i, _line in enumerate(f.readlines(), start=1):
            if i >= line:
                content += _line
    return content


def ignore_decimals_in_str(content: str, up_to: int = 5) -> str:
    re_pattern = r"(\d+\.\d{" + str(up_to) + r"})\d*"
    return re.sub(re_pattern, r"\1", content)
