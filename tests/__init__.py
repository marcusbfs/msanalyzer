import re
from pathlib import Path
from typing import List

__version__ = "3.8.0"

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


def extract_numbers_from_str(content: str) -> List[float]:
    p = re.compile(r"\d+\.\d+")  # Compile a pattern to capture float values
    floats: List[float] = [
        float(i) for i in p.findall(content)
    ]  # Convert strings to float
    return floats
