from enum import Enum, unique
import warnings

warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
import logging

from typing import List
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.optimize
import pandas as pd

from MasterSizerInput import MasterSizerInput

logger = logging.getLogger(__name__)
__version__: str = "1.2.0"


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
        self.__Dp__RRB: float = 0.0
        self.__n__RRB: float = 0.0
        self.__Dp_std_dev__RRB: float = 0.0
        self.__n_std_dev__RRB: float = 0.0
        self.__r_squared__RRB: float = 0.0
        self.__std_error_of_the_regression__RRB: float = 0.0
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

        # self.evaluateData()

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
        self.__evaluateRRBParameters()

    def cutLastNPoints(self, number_of_points: int) -> None:
        self.__x_data = self.__x_data[:-number_of_points].copy()
        self.__y_data = self.__y_data[:-number_of_points].copy()
        self.__number_of_points = len(self.__y_data)
        logger.info("Cutted the last {} null points".format(number_of_points))
        logger.info("New length of x: {}".format(len(self.__x_data)))
        # self.evaluateData()

    def cutFirstNPoints(self, number_of_points: int) -> None:
        self.__x_data = self.__x_data[number_of_points:].copy()
        self.__y_data = self.__y_data[number_of_points:].copy()
        self.__number_of_points = len(self.__y_data)
        logger.info("Cutted the first {} null points".format(number_of_points))
        logger.info("New length of x: {}".format(len(self.__x_data)))
        # self.evaluateData()

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

    def saveExcel(self, base_filename: str) -> None:
        data = np.transpose(
            [self.__x_data_mean, self.__y_data, self.__cumulative_y_vals]
        )
        df = pd.DataFrame(data, columns=self.__headers)
        filename = base_filename + ".xlsx"
        df.to_excel(filename, index=False)
        logger.info('Exported data to excel file: "{}"'.format(filename))
        return

    def saveFig(self, base_filename: str) -> None:
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

        # ax1.legend()
        # ax2.legend()

        filename = base_filename + ".svg"
        plt.savefig(filename, dpi=1200)
        logger.info('Saved curves to "{}"'.format(filename))
        # end of plot

    def saveRRBFig(self, base_filename: str) -> None:
        # plot
        fig, ax = plt.subplots()

        ax.set_ylabel(u"Cumulative distribution (X) [-]")
        ax.grid()

        ax.plot(
            self.__x_data_mean,
            self.evalRRB(self.__x_data_mean),
            label="RRB Model",
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

        filename = base_filename + ".svg"
        plt.savefig(filename, dpi=1200)
        logger.info('Saved RRB curve to "{}"'.format(filename))
        # end of plot

    def saveData(self, data_filename: str) -> None:
        header = "%10s\t%10s\t%10s" % (
            self.__headers[0],
            self.__headers[1],
            self.__headers[2],
        )
        np.savetxt(
            data_filename,
            np.transpose([self.__x_data_mean, self.__y_data, self.__cumulative_y_vals]),
            fmt="%15.10f",
            header=header,
        )
        logger.info('Saved curves data to "{}"'.format(data_filename))

    def saveRRBdata(self, data_filename: str) -> None:
        content = "RRB model\n"
        content += "=========\n\n"
        content += "X(d) = 1 - exp(-(d/D')^n)\n\n"
        content += "Parameters: \n"
        content += "            D' = {:.10f}   std. dev. = {:.10f}\n".format(
            self.__Dp__RRB, self.__Dp_std_dev__RRB
        )
        content += "            n  = {:.10f}   std. dev. = {:.10f}\n".format(
            self.__n__RRB, self.__n_std_dev__RRB
        )
        content += "\n"
        content += "Standard error of the regression (S) = {:.10f}\n".format(
            self.__std_error_of_the_regression__RRB
        )
        content += "NOTE: S must be <= 2.5 to produce a sufficiently narrow 95% prediction interval.\n"
        content += "\n"
        content += "R-squared = {:.10f}\n".format(self.__r_squared__RRB)
        content += "NOTE: R-squared is not trustworthy for nonlinear regression\n"
        content += "\n"
        with open(data_filename + ".txt", "w") as of:
            of.write(content)
        logger.info('Saved RRB data to "{}"'.format(data_filename + ".txt"))
        return

    def evalRRB(self, d: float) -> float:
        return self.__RRBModel(d, self.__Dp__RRB, self.__n__RRB)

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

    def getRRBparameters(self) -> List[float]:
        return (self.__Dp__RRB, self.__n__RRB)

    def getVersion(self) -> str:
        return self.__version

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
        # self.evaluateData()

    def __setVolInPerFile(self, filename: str) -> None:
        self.__vol_in_per_filename = filename

    def __setDiametersFile(self, filename: str) -> None:
        self.__diameters_filename = filename

    def __getInitialRRBParameters(self) -> list:
        # get inital guesses
        p0 = [100.0, 1.1]
        for i in range(self.__number_of_points):
            if self.__cumulative_y_vals[i] >= 0.632:
                p0[0] = self.__x_data_mean[i]
                break
        logger.info(
            "Initial guesses are D' = {:.7f} and n = {:.7f}".format(p0[0], p0[1])
        )
        return p0

    def __evaluateRRBParameters(self) -> None:

        logger.info("Evaluating RRB parameters")
        # get inital guesses
        p0 = self.__getInitialRRBParameters()

        # calculate using scipy
        logger.info("Calling scipy curve_fit function")
        self.__popt, self.__pcov = scipy.optimize.curve_fit(
            self.__RRBModel, self.__x_data_mean, self.__cumulative_y_vals, p0=p0
        )

        # set outputs parameters and errors infos
        self.__Dp__RRB = self.__popt[0]
        self.__n__RRB = self.__popt[1]

        # std dev for each parameters
        std_devs = np.sqrt(np.diag(self.__pcov))
        self.__Dp_std_dev__RRB = std_devs[0]
        self.__n_std_dev__RRB = std_devs[1]
        logger.info(
            "Estimated parameters: D' = {:.7f} +- {:.7f} and n = {:.7f} +- {:.7f}".format(
                self.__Dp__RRB,
                self.__Dp_std_dev__RRB,
                self.__n__RRB,
                self.__n_std_dev__RRB,
            )
        )

        # calculate R squared (it is not apropriate to nonlinear regression, but some people love it)
        self.__r_squared__RRB = 1.0 - np.sum(
            (self.__cumulative_y_vals - self.evalRRB(self.__x_data_mean)) ** 2
        ) / np.sum((self.__cumulative_y_vals - np.mean(self.__cumulative_y_vals)) ** 2)
        logger.info("R-squared = {:.10f}".format(self.__r_squared__RRB))

        # Standard Error of the Regression
        self.__std_error_of_the_regression__RRB = np.mean(
            np.abs(self.__cumulative_y_vals - self.evalRRB(self.__x_data_mean))
        )
        logger.info("S = {:.10f}".format(self.__std_error_of_the_regression__RRB))
        logger.info("Finished estimating RRB parameters")

        return

    def __RRBModel(self, d, dp, n) -> float:
        return 1.0 - np.exp(-np.power(d / dp, n))

    def __isFloatEqual(self, x: float, y: float, tol: float = 1e-10) -> bool:
        return np.abs(x - y) < tol


def getVersion() -> str:
    return __version__