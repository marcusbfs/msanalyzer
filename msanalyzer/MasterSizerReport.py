from datetime import date
from textwrap import wrap
from enum import Enum, unique
import os
import warnings

warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
import logging

from typing import List
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from MasterSizerInput import MasterSizerInput

from RRBSizeDistributionModel import RRB
from SizeDistributionBaseModel import SizeDistributionBaseModel
from SizeDistributionModelsFactory import getPSDModelsList

logger = logging.getLogger(__name__)
__version__: str = "2.0.0"
__author__: str = "Marcus Bruno Fernandes Silva"
__email__: str = "marcusbfs@gmail.com"


@unique
class DiameterMeanType(Enum):
    geometric = 1
    arithmetic = 2


class MasterSizerReport:
    def __init__(self):
        self.__diameters_filename: str = ""
        self.__vol_in_per_filename: str = ""
        self.__number_of_points: int = 0
        self.__x_data: np.array = None
        self.__x_data_geomean: np.array = None
        self.__x_data_aritmeticmean: np.array = None
        self.__y_data: np.array = None
        self.__x_data_mean: np.array = None
        self.__cumulative_y_vals: np.array = None
        self.__diff_of_cumulative_y_vals: np.array = None
        self.__ms_input: MasterSizerInput = MasterSizerInput()
        self.__version: str = __version__
        self.__input_xps_file: str = ""
        self.__meantype: DiameterMeanType = DiameterMeanType.geometric
        self.__headers: List[str] = [
            "diameter [microns]",
            "volume fraction [-]",
            "cumulative volume fraction [-]",
        ]
        self.__log_scale: bool = False
        self.__models: List[SizeDistributionBaseModel] = getPSDModelsList()
        self.__num_of_models: int = len(self.__models)

    # Public
    def setDataFiles(
        self, x_filename: str, y_filename: str, isCommaSeparator: bool = False
    ) -> None:

        self.__ms_input.setDataFiles(x_filename, y_filename, isCommaSeparator)
        self.__updateXY_data()

    def setLogScale(self, logscale: bool = True) -> None:
        self.__log_scale = logscale
        logger.info("Log scale setted to {}".format(logscale))

    def setXPSfile(self, xps_filename: str) -> None:
        self.__input_xps_file = xps_filename
        logger.info('XPS file setted to "{}"'.format(xps_filename))
        self.__ms_input.setXPSfile(xps_filename)
        self.__updateXY_data()

    def setXandY(self, x_vals, y_vals) -> None:
        self.__x_data = x_vals
        self.__y_data = y_vals
        assert len(self.__x_data) == len(self.__y_data) + 1

    def genCumulativeSizeDistribution(self) -> None:
        self.__cumulative_y_vals = np.zeros(self.__number_of_points)
        for i in range(1, self.__number_of_points):
            self.__cumulative_y_vals[i] = (
                self.__y_data[i] + self.__cumulative_y_vals[i - 1]
            )

    def genDiffCumulativeSizeDistribution(self) -> None:
        self.__diff_of_cumulative_y_vals = np.diff(
            self.__cumulative_y_vals, prepend=0.0
        ) / np.diff(self.__x_data_mean, prepend=1.0)

    # saving files

    def saveExcel(self, output_dir: str, base_filename: str) -> None:
        data = np.transpose(
            [self.__x_data_mean, self.__y_data, self.__cumulative_y_vals]
        )
        df = pd.DataFrame(data, columns=self.__headers)
        filename = os.path.join(output_dir, base_filename + ".xlsx")
        df.to_excel(filename, index=False)
        logger.info('Exported data to excel file: "{}"'.format(filename))
        return

    def saveFig(self, output_dir: str, base_filename: str) -> None:
        # plot
        fig, ax1 = plt.subplots()
        ax2 = plt.twinx()
        ax1.set_ylabel(u"volume fraction (dX) [-]")
        ax2.set_ylabel(u"Cumulative distribution (X) [-]")
        ax2.grid()

        ax1_color = "#1f77b4"
        ax2_color = "red"

        ax1.tick_params(axis="y", colors=ax1_color, which="both")
        ax1.plot(
            self.getXmeanValues(),
            self.getYvalues(),
            linestyle="--",
            marker="o",
            color=ax1_color,
            label="dX",
        )

        ax2.tick_params(axis="y", colors=ax2_color, which="both")
        ax2.plot(
            self.getXmeanValues(),
            self.getCumulativeYvalues(),
            linestyle="--",
            marker="o",
            color=ax2_color,
            label="X",
        )

        if self.__log_scale:
            ax1.set_xlabel(u"log scale - diameter [$\mu m$]")
            self.__format_LogScale_Xaxis(ax1)
        else:
            ax1.set_xlabel(u"diameter [$\mu m$]")

        filename = os.path.join(output_dir, base_filename + ".svg")
        plt.savefig(filename, dpi=1200)
        logger.info('Saved curves to "{}"'.format(filename))
        # end of plot

    def saveModelsFig(self, output_dir: str, base_filename: str) -> None:

        for model in self.__models:
            # plot
            fig, ax = plt.subplots()

            ax.set_ylabel(u"Cumulative distribution (X) [-]")
            ax.grid()

            ax.plot(
                self.__x_data_mean,
                model.compute(self.__x_data_mean),
                label="{} Model".format(model.getModelName()),
                linestyle="--",
                color="red",
            )
            ax.scatter(
                self.__x_data_mean,
                self.__cumulative_y_vals,
                label="Data",
                facecolors="none",
                edgecolors="black",
            )

            ax.legend()

            if self.__log_scale:
                ax.set_xlabel(u"log scale - diameter [$\mu m$]")
                self.__format_LogScale_Xaxis(ax)
            else:
                ax.set_xlabel(u"diameter [$\mu m$]")

            filename = os.path.join(
                output_dir, model.getModelName() + "_" + base_filename + ".svg"
            )
            plt.savefig(filename, dpi=1200)
            logger.info('Saved {} curve to "{}"'.format(model.getModelName(), filename))
            # end of plot

    def saveData(self, output_dir: str, data_filename: str) -> None:
        output_file = os.path.join(output_dir, data_filename)
        header = "%10s\t%10s\t%10s" % (
            self.__headers[0],
            self.__headers[1],
            self.__headers[2],
        )
        np.savetxt(
            output_file,
            np.transpose([self.__x_data_mean, self.__y_data, self.__cumulative_y_vals]),
            fmt="%15.10f",
            header=header,
        )

        content = self.getTxtFilesHeader()
        with open(output_file, "r+") as f:
            content += f.read()

        with open(output_file, "w") as f:
            f.write(content)

        logger.info('Saved curves data to "{}"'.format(output_file))

    def saveModelsData(self, output_dir: str, data_filename: str) -> None:
        for model in self.__models:
            output_file = os.path.join(
                output_dir, model.getModelName() + "_" + data_filename + ".txt"
            )
            content = self.getTxtFilesHeader()
            content += model.getFormattedOutput()
            with open(output_file, "w") as of:
                of.write(content)
            logger.info(
                'Saved {} data to "{}"'.format(model.getModelName(), output_file)
            )
        return

    def saveBestModelsRanking(self, output_dir: str, base_filename: str) -> None:
        output_file = os.path.join(output_dir, base_filename + ".txt")
        logger.info(
            "Searching best R-squared (highest value) and best S (lowest value) models"
        )

        ranking_models_S_based = sorted(
            self.__models, key=lambda x: x.getStdErrorMean()
        )
        logger.info("Ranking based on S: {}".format(ranking_models_S_based))
        ranking_models_r2_based = sorted(
            self.__models, key=lambda x: x.getRsquared(), reverse=True
        )
        logger.info("Ranking based on R-squared: {}".format(ranking_models_r2_based))

        file_content = self.getTxtFilesHeader()
        file_content += "Best models\n"
        file_content += "===========\n\n"

        file_content += (
            "Ranking based on S (standard error mean). Lowest value is better.\n\n"
        )

        i = 1
        for model in ranking_models_S_based:
            file_content += "  #{:02d} - {}: S = {:.7f}\n".format(
                i, model.getModelName(), model.getStdErrorMean()
            )
            i += 1

        file_content += "\n"
        file_content += (
            "Ranking based on R-squared (not trustworthy). Highest value is better.\n\n"
        )

        i = 1
        for model in ranking_models_r2_based:
            file_content += "  #{:02d} - {}: R-squared = {:.7f}\n".format(
                i, model.getModelName(), model.getRsquared()
            )
            i += 1

        with open(output_file, "w") as of:
            of.write(file_content)
        logger.info('Saved best model rankings to "{}"'.format(output_file))

    def evaluateData(self) -> None:
        # Extract data
        self.__number_of_points = len(self.__y_data)

        # Get x values means
        self.__x_data_geomean = np.sqrt(self.__x_data[1:] * self.__x_data[:-1])
        self.__x_data_aritmeticmean = 0.5 * (self.__x_data[1:] + self.__x_data[:-1])

        # Use geometric mean for default values of x
        self.setDiameterMeanType(self.__meantype)

        self.genCumulativeSizeDistribution()

        self.genDiffCumulativeSizeDistribution()
        for model in self.__models:
            model.evaluate(self.__x_data_mean, self.__cumulative_y_vals)

    def cutLastNPoints(self, number_of_points: int) -> None:
        self.__x_data = self.__x_data[:-number_of_points].copy()
        self.__y_data = self.__y_data[:-number_of_points].copy()
        self.__number_of_points = len(self.__y_data)
        logger.info("Cutted the last {} null points".format(number_of_points))
        logger.info("New length of x: {}".format(len(self.__x_data)))

    def cutFirstNPoints(self, number_of_points: int) -> None:
        self.__x_data = self.__x_data[number_of_points:].copy()
        self.__y_data = self.__y_data[number_of_points:].copy()
        self.__number_of_points = len(self.__y_data)
        logger.info("Cutted the first {} null points".format(number_of_points))
        logger.info("New length of x: {}".format(len(self.__x_data)))

    def cutLastZeroPoints(
        self, number_of_lefting_zeros: int, tol: float = 1e-10
    ) -> None:
        total_zeros = 0

        for i in range(self.__number_of_points - 1, -1, -1):
            if self.__isFloatEqual(0.0, self.__y_data[i], tol=tol):
                total_zeros += 1
            else:
                break

        if total_zeros >= number_of_lefting_zeros:
            self.cutLastNPoints(total_zeros - number_of_lefting_zeros - 1)

    def cutFirstZeroPoints(
        self, number_of_lefting_zeros: int, tol: float = 1e-10
    ) -> None:
        total_zeros = 0

        for i in range(self.__number_of_points):
            if self.__isFloatEqual(0.0, self.__y_data[i], tol=tol):
                total_zeros += 1
            else:
                break

        if total_zeros >= number_of_lefting_zeros:
            self.cutFirstNPoints(total_zeros - number_of_lefting_zeros - 1)

    # Getters
    def getNumberOfPoints(self) -> int:
        return self.__number_of_points

    def getGeometricMeanXvalues(self) -> np.array:
        return self.__x_data_geomean

    def getAritmeticMeanXvalues(self) -> np.array:
        return self.__x_data_geomean

    def getCumulativeYvalues(self) -> np.array:
        return self.__cumulative_y_vals

    def getDiffOfCumulativeYvalues(self) -> np.array:
        return self.__diff_of_cumulative_y_vals

    def getYvalues(self) -> np.array:
        return self.__y_data

    def getXmeanValues(self) -> np.array:
        return self.__x_data_mean

    def getTxtFilesHeader(self) -> str:
        content = ""
        content += " msanalyzer {} \n\n".format(__version__)
        content += " Author: {} \n".format(__author__)
        content += " email: {} \n\n".format(__email__)
        content += ' file analyzed: "{}" \n'.format(os.path.abspath(self.__input_xps_file))
        content += " Date: {} \n".format(date.today().strftime("%d-%b-%Y"))
        content = self.getBorderedText(content)
        content += "\n\n"
        return content

    def getBorderedText(self, text: str):
        lines = text.splitlines()
        width = max(len(s) for s in lines)
        res = ["+" + "-" * width + "+"]
        for s in lines:
            res.append("|" + (s + " " * width)[:width] + "|")
        res.append("+" + "-" * width + "+")
        return "\n".join(res)

    @staticmethod
    def getVersion() -> str:
        return __version__

    # Setters
    def setGeometricMean(self) -> None:
        self.__x_data_mean = self.__x_data_geomean

    def setArithmeticMean(self) -> None:
        self.__x_data_mean = self.__x_data_aritmeticmean

    def setDiameterMeanType(self, typed: DiameterMeanType) -> None:
        self.__meantype = typed
        if DiameterMeanType.geometric == typed:
            self.setGeometricMean()
        elif DiameterMeanType.arithmetic == typed:
            self.setArithmeticMean()
        logger.info("Diameter mean type setted to {}".format(typed))

    # Private
    def __format_LogScale_Xaxis(self, xaxis: matplotlib.axes.Axes) -> None:
        from matplotlib.ticker import ScalarFormatter

        xaxis.set_xscale("log")
        xaxis.set_xlabel(u"log scale - diameter [$\mu m$]")
        for axis in [xaxis.xaxis, xaxis.yaxis]:
            axis.set_major_formatter(ScalarFormatter())
        return

    def __updateXY_data(self) -> None:
        self.__x_data = self.__ms_input.getx()
        self.__y_data = self.__ms_input.gety()
        self.__number_of_points = len(self.__y_data)

    def __setVolInPerFile(self, filename: str) -> None:
        self.__vol_in_per_filename = filename

    def __setDiametersFile(self, filename: str) -> None:
        self.__diameters_filename = filename

    def __isFloatEqual(self, x: float, y: float, tol: float = 1e-10) -> bool:
        return np.abs(x - y) < tol
