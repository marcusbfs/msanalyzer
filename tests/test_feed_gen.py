from pathlib import Path

from msanalyzer import FeedCurve, MasterSizerReport

from . import CURRENT_DIR, RESOURCES_DIR

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


def test_s() -> None:

    config = FeedCurve.Config(
        first_zeros=0,
        last_zeros=0,
        log_scale=True,
        mean_type=MasterSizerReport.DiameterMeanType.geometric,
        feed_mass_flow=100.0,
        under_mass_flow=20.0,
        over_mass_flow=80.0,
    )

    a = FeedCurve.FeedFromUnderAndOver(file_dryc_01, file_dryc_02, config)
    fr = a.get_feed_reporter()

    fr.evaluateData()
    fr.evaluateModels()

    assert True
