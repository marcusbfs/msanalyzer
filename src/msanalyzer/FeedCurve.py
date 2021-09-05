import io
import logging
from dataclasses import dataclass
from pathlib import Path

from .MasterSizerReport import DiameterMeanType, MasterSizerReport

logger = logging.getLogger(__name__)


@dataclass
class Config:
    mean_type: DiameterMeanType
    first_zeros: int
    last_zeros: int
    log_scale: bool
    under_mass_flow: float  # kg/s
    over_mass_flow: float  # kg/s
    feed_mass_flow: float  # kg/s


class FeedFromUnderAndOver:
    def __init__(self, under_file: Path, over_file: Path, config: Config) -> None:

        logger.info("Constructing object")
        self._under_reporter: MasterSizerReport = MasterSizerReport()
        self._over_reporter: MasterSizerReport = MasterSizerReport()
        self._feed_reporter: MasterSizerReport = MasterSizerReport()

        self._config = config

        with open(under_file, "rb") as xpsfile_mem:
            self._under_reporter.setXPSfile(
                io.BytesIO(xpsfile_mem.read()), str(under_file)
            )
            self._under_reporter.setDiameterMeanType(config.mean_type)
            # self._under_reporter.cutFirstZeroPoints(config.first_zeros, tol=1e-8)
            # self._under_reporter.cutLastZeroPoints(config.last_zeros, tol=1e-8)
            self._under_reporter.setLogScale(logscale=config.log_scale)

        with open(over_file, "rb") as xpsfile_mem:
            self._over_reporter.setXPSfile(
                io.BytesIO(xpsfile_mem.read()), str(over_file)
            )
            self._over_reporter.setDiameterMeanType(config.mean_type)
            # self._over_reporter.cutFirstZeroPoints(config.first_zeros, tol=1e-8)
            # self._over_reporter.cutLastZeroPoints(config.last_zeros, tol=1e-8)
            self._over_reporter.setLogScale(logscale=config.log_scale)

        logger.info("Calling under.evaluatedata()")
        self._under_reporter.evaluateData()
        logger.info("Calling over.evaluatedata()")
        self._over_reporter.evaluateData()

        feed_y = (
            self._over_reporter.getYvalues() * config.over_mass_flow
            + self._under_reporter.getYvalues() * config.under_mass_flow
        ) / config.feed_mass_flow

        self._feed_reporter.setXandY(self._under_reporter.getRawXvalues(), feed_y)
        self._feed_reporter.setDiameterMeanType(config.mean_type)
        self._feed_reporter.cutFirstZeroPoints(config.first_zeros, tol=1e-8)
        self._feed_reporter.cutLastZeroPoints(config.last_zeros, tol=1e-8)
        self._feed_reporter.setLogScale(logscale=config.log_scale)

    def get_feed_reporter(self) -> MasterSizerReport:
        return self._feed_reporter
