import shutil
import subprocess
from pathlib import Path

import pytest

from . import CURRENT_DIR, RESOURCES_DIR, get_file_content_from_line

BASENAME_dryc = "01_dry_coke_2500rpm_U0T0"

file_dryc: Path = RESOURCES_DIR / (BASENAME_dryc + ".xps")

outdir: Path = CURRENT_DIR / (BASENAME_dryc + "_out_test")
expected_outdir: Path = RESOURCES_DIR / (BASENAME_dryc + "_output")


headers_line_ignore = 10


@pytest.fixture(scope="session", autouse=True)
def create_out_dir_for_01dryc() -> None:  # type: ignore
    if not outdir.is_dir():
        shutil.rmtree(outdir, ignore_errors=True)

    cmd = ["msanalyzer", str(file_dryc), "--output_dir", str(outdir)]
    output = subprocess.call(cmd, shell=True)
    assert outdir.is_dir()

    yield

    shutil.rmtree(outdir, ignore_errors=True)
    assert not outdir.is_dir()


@pytest.mark.parametrize(
    "filename, lines_to_ignore",
    [
        (
            "output_curves_data.txt",
            headers_line_ignore,
        ),
        (
            "best_models_ranking.txt",
            headers_line_ignore,
        ),
        (
            "GGS_output_model_parameters.txt",
            headers_line_ignore,
        ),
        (
            "RRB_output_model_parameters.txt",
            headers_line_ignore,
        ),
        (
            "Sigmoid_output_model_parameters.txt",
            headers_line_ignore,
        ),
        (
            "Log-normal_output_model_parameters.txt",
            headers_line_ignore,
        ),
        (
            "Gaudin-Meloy_output_model_parameters.txt",
            headers_line_ignore,
        ),
    ],
)
def test_single_file_full_output(filename: str, lines_to_ignore: int) -> None:

    assert Path(outdir / filename).is_file()

    content_actual = get_file_content_from_line(outdir / filename, lines_to_ignore)
    content_expected = get_file_content_from_line(
        expected_outdir / filename, lines_to_ignore
    )

    assert content_actual == content_expected
