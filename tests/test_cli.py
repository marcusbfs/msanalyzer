import shutil
from pathlib import Path

import numpy as np
import pytest

from msanalyzer import cli

from . import (
    CURRENT_DIR,
    RESOURCES_DIR,
    extract_numbers_from_str,
    get_file_content_from_line,
)

BASENAME_dryc_01 = "01_dry_coke_2500rpm_U0T0"
file_dryc_01: Path = RESOURCES_DIR / (BASENAME_dryc_01 + ".xps")

outdir_01_geo: Path = CURRENT_DIR / (BASENAME_dryc_01 + "_out_test_geo")
expected_outdir_01_geo: Path = RESOURCES_DIR / (BASENAME_dryc_01 + "_output_geo")

outdir_01_ari: Path = CURRENT_DIR / (BASENAME_dryc_01 + "_out_test_ari")
expected_outdir_01_ari: Path = RESOURCES_DIR / (BASENAME_dryc_01 + "_output_ari")

BASENAME_dryc_02 = "02_dry_coke_2500rpm_U10T180"
file_dryc_02: Path = RESOURCES_DIR / (BASENAME_dryc_02 + ".xps")

outdir_02: Path = CURRENT_DIR / (BASENAME_dryc_02 + "_out_test")
expected_outdir_02: Path = RESOURCES_DIR / (BASENAME_dryc_02 + "_output")

dir_multi_01_02: Path = CURRENT_DIR / "multi_01_02_dryc_output_outtest"
dir_expected_multi_01_02: Path = RESOURCES_DIR / "multi_01_02_dryc_output"


headers_line_ignore = 10


@pytest.fixture(scope="session", autouse=True)
def create_out_dir_for_01dryc_geometric_mean() -> None:  # type: ignore
    if not outdir_01_geo.is_dir():
        shutil.rmtree(outdir_01_geo, ignore_errors=True)

    cmd = [
        str(file_dryc_01),
        "--output_dir",
        str(outdir_01_geo),
        "--diameter_mean",
        "geo",
    ]
    cli.main(cmd)
    assert outdir_01_geo.is_dir()

    yield

    shutil.rmtree(outdir_01_geo, ignore_errors=True)
    assert not outdir_01_geo.is_dir()


@pytest.fixture(scope="session", autouse=True)
def create_out_dir_for_01dryc_arithmetic_mean() -> None:  # type: ignore
    if not outdir_01_ari.is_dir():
        shutil.rmtree(outdir_01_ari, ignore_errors=True)

    cmd = [
        str(file_dryc_01),
        "--output_dir",
        str(outdir_01_ari),
        "--diameter_mean",
        "ari",
    ]
    cli.main(cmd)
    assert outdir_01_ari.is_dir()

    yield

    shutil.rmtree(outdir_01_ari, ignore_errors=True)
    assert not outdir_01_ari.is_dir()


@pytest.fixture(scope="session", autouse=True)
def create_out_dir_for_multi_01_02() -> None:  # type: ignore
    if not dir_multi_01_02.is_dir():
        shutil.rmtree(dir_multi_01_02, ignore_errors=True)

    cmd = [
        "-M",
        str(file_dryc_01),
        "-M",
        str(file_dryc_02),
        "--output_dir",
        str(dir_multi_01_02),
    ]

    cli.main(_args=cmd)
    assert dir_multi_01_02.is_dir()

    yield

    shutil.rmtree(dir_multi_01_02, ignore_errors=True)
    assert not dir_multi_01_02.is_dir()


@pytest.mark.parametrize(
    "filename, lines_to_ignore",
    [
        ("output_curves_data.txt", headers_line_ignore),
        ("best_models_ranking.txt", headers_line_ignore),
        ("GGS_output_model_parameters.txt", headers_line_ignore),
        ("RRB_output_model_parameters.txt", headers_line_ignore),
        ("Sigmoid_output_model_parameters.txt", headers_line_ignore),
        ("Log-normal_output_model_parameters.txt", headers_line_ignore),
        ("Gaudin-Meloy_output_model_parameters.txt", headers_line_ignore),
    ],
)
def test_single_file_full_output_geometric_mean(
    filename: str, lines_to_ignore: int
) -> None:

    assert Path(outdir_01_geo / filename).is_file()

    content_actual = get_file_content_from_line(
        outdir_01_geo / filename, lines_to_ignore
    )
    content_expected = get_file_content_from_line(
        expected_outdir_01_geo / filename, lines_to_ignore
    )

    actual_numbers = np.array(extract_numbers_from_str(content_actual))
    expected_numbers = np.array(extract_numbers_from_str(content_expected))

    assert np.allclose(actual_numbers, expected_numbers)


@pytest.mark.parametrize(
    "filename, lines_to_ignore",
    [
        ("output_curves_data.txt", headers_line_ignore),
        ("best_models_ranking.txt", headers_line_ignore),
        ("GGS_output_model_parameters.txt", headers_line_ignore),
        ("RRB_output_model_parameters.txt", headers_line_ignore),
        ("Sigmoid_output_model_parameters.txt", headers_line_ignore),
        ("Log-normal_output_model_parameters.txt", headers_line_ignore),
    ],
)
def test_single_file_full_output_arithmetic_mean(
    filename: str, lines_to_ignore: int
) -> None:

    assert Path(outdir_01_ari / filename).is_file()

    content_actual = get_file_content_from_line(
        outdir_01_ari / filename, lines_to_ignore
    )
    content_expected = get_file_content_from_line(
        expected_outdir_01_ari / filename, lines_to_ignore
    )

    actual_numbers = np.array(extract_numbers_from_str(content_actual))
    expected_numbers = np.array(extract_numbers_from_str(content_expected))

    assert np.allclose(actual_numbers, expected_numbers)


def test_multiles_full_output() -> None:
    expected_svgs = [
        f for f in dir_expected_multi_01_02.iterdir() if f.suffix.lower() == ".svg"
    ]
    computed_svgs = [f for f in dir_multi_01_02.iterdir() if f.suffix.lower() == ".svg"]

    assert len(expected_svgs) == len(computed_svgs)
