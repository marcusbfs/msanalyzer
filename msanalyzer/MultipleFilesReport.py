import os
import warnings

warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
import logging

from typing import List
import matplotlib
import matplotlib.pyplot as plt

import MasterSizerReport as msreport

logger = logging.getLogger(__name__)


class MultipleFilesReport:
    # constructor
    def __init__(
        self,
        files: List[str],
        meanType: msreport.DiameterMeanType,
        logScale: bool,
        number_of_zero_first: int,
        number_of_zero_last: int,
        custom_plot_dict: dict,
        show_labels: bool,
    ):
        self.__files: List[str] = files
        self.__number_of_files: int = len(self.__files)
        self.__meanType: msreport.DiameterMeanType = meanType
        self.__log_scale: bool = logScale
        self.__number_of_zero_first: int = number_of_zero_first
        self.__number_of_zero_last: int = number_of_zero_last
        self.__reporters: List[msreport.MasterSizerReport] = []
        self.__labels: List[str] = []
        self.__custom_plot_kwargs: dict = custom_plot_dict
        self.__show_labels: bool = show_labels

        self.__create_reporters()

    # public methods

    def sizeDistributionPlot(self, output_path: str) -> None:
        # plot
        logger.info("sizeDistributionPlot called")

        fig, ax = plt.subplots()
        ax.set_ylabel("volume fraction (dX) [-]")
        ax.grid()

        ax.tick_params(axis="y", which="both")

        if self.__log_scale:
            ax.set_xlabel("log scale - diameter [$\mu m$]")
            msreport.MasterSizerReport.formatLogScaleXaxis(ax)
        else:
            ax.set_xlabel("diameter [$\mu m$]")

        for reporter, labelName in zip(self.__reporters, self.__labels):
            logger.info('Adding curve of file "{}"'.format(reporter.getInputFile()))

            ax.plot(
                reporter.getXmeanValues(),
                reporter.getYvalues(),
                linestyle="--",
                # marker="o",
                label=labelName,
                **self.__custom_plot_kwargs,
            )

        if self.__show_labels:
            ax.legend()

        filename = os.path.join(output_path + ".svg")
        plt.savefig(filename, dpi=1200)

        logger.info('Saved multiuple curves to "{}"'.format(filename))
        return fig
        # end of plot

    def frequencyPlot(self, output_path: str) -> None:
        # plot
        logger.info("frequencyPlot called")

        fig, ax = plt.subplots()
        ax.set_ylabel("cumulative distribution (X) [-]")
        ax.grid()

        ax.tick_params(axis="y", which="both")

        if self.__log_scale:
            ax.set_xlabel("log scale - diameter [$\mu m$]")
            msreport.MasterSizerReport.formatLogScaleXaxis(ax)
        else:
            ax.set_xlabel("diameter [$\mu m$]")

        for reporter, labelName in zip(self.__reporters, self.__labels):
            logger.info('Adding curve of file "{}"'.format(reporter.getInputFile()))

            ax.plot(
                reporter.getXmeanValues(),
                reporter.getCumulativeYvalues(),
                linestyle="--",
                # marker="o",
                label=labelName,
            )

        if self.__show_labels:
            ax.legend()

        filename = os.path.join(output_path + ".svg")
        plt.savefig(filename, dpi=1200)

        logger.info('Saved multiuple curves to "{}"'.format(filename))
        # end of plot

    def setLabels(self, labels: List[str]) -> None:
        assert len(labels) == len(self.__reporters)
        self.__labels = labels
        return

    # private methods

    def __create_reporters(self) -> None:
        for f in self.__files:
            logger.info('Setting up file "{}"'.format(f))
            reporter = msreport.MasterSizerReport()
            logger.info('Created reporter object for file "{}"'.format(f))

            reporter.setXPSfile(f)
            reporter.setDiameterMeanType(self.__meanType)
            reporter.cutFirstZeroPoints(self.__number_of_zero_first, tol=1e-8)
            reporter.cutLastZeroPoints(self.__number_of_zero_last, tol=1e-8)
            reporter.setLogScale(logscale=self.__log_scale)

            reporter.evaluateData()

            self.__reporters.append(reporter)
            self.__labels.append(reporter.getInputFile())

            logger.info('Reporter object for file "{}" setted up'.format(f))

    def __check_all_files_exist(self) -> List[str]:
        doesnt_exist: List[str] = []
        for f in self.__files:
            if not os.path.isfile(f):
                doesnt_exist.append(f)
        return doesnt_exist
