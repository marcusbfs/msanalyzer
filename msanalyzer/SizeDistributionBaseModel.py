from typing import List

import numpy as np
import logging

logger = logging.getLogger(__name__)

import scipy.optimize


class SizeDistributionBaseModel:
    def __init__(self):
        self.__r_squared: float = 0.0
        self.__std_error_mean: float = 0.0
        self.model_par_values: List[float] = []
        self.model_par_values_std_dev: List[float] = []
        self.model_par_str: List[str] = []
        self.model_expression_str: str = ""
        self.model_name_str: str = ""

    def specificModel(self, d, *args) -> float:
        raise NotImplementedError

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        raise NotImplementedError

    def getSauterDiameterValue(self) -> float:
        raise NotImplementedError

    def getSauterDiameterExpression(self) -> str:
        raise NotImplementedError

    # =================== base class ======================================

    def getRsquared(self) -> float:
        return self.__r_squared

    def getStdErrorMean(self) -> float:
        return self.__std_error_mean

    def compute(self, x: np.ndarray) -> np.ndarray:
        return self.specificModel(x, *self.model_par_values)

    def getModelName(self) -> str:
        return self.model_name_str

    def evaluate(self, x: np.ndarray, y: np.ndarray) -> None:
        logger.info("Evaluating {} parameters".format(self.getModelName()))

        logger_initial_guesses = "Initial guesses are "
        self.model_par_values = self.getInitialGuesses(x, y)
        for symb, val in zip(self.model_par_str, self.model_par_values):
            logger_initial_guesses += "{} = {:.7f}; ".format(symb, val)
        logger.info(logger_initial_guesses)

        # calculate using scipy
        logger.info("Calling scipy curve_fit function")
        popt, pcov = scipy.optimize.curve_fit(
            self.specificModel, x, y, p0=self.model_par_values
        )
        logger.info("popt: {}\n pcov: {}".format(popt, pcov))

        # set outputs parameters and errors infos
        self.model_par_values = popt
        # std dev for each parameters
        self.model_par_values_std_dev = np.sqrt(np.diag(pcov))

        logger_content = "Estimated parameters: "
        for symbol, val, std_dev in zip(
            self.model_par_str, self.model_par_values, self.model_par_values_std_dev
        ):
            logger_content += "{} = {:.7f} +- {:.7}; ".format(symbol, val, std_dev)
        logger.info(logger_content)

        computed_y = self.compute(x)
        # calculate R squared (it is not apropriate to nonlinear regression, but some people love it)
        self.__r_squared = 1.0 - np.sum((y - computed_y) ** 2) / np.sum(
            (y - np.mean(y)) ** 2
        )
        logger.info("R-squared = {:.10f}".format(self.__r_squared))

        # Standard Error of the Regression
        self.__std_error_mean = np.mean(np.abs(y - computed_y))
        logger.info("S = {:.10f}".format(self.__std_error_mean))

        logger.info("Finished estimating {} parameters".format(self.getModelName()))

    def getFormattedOutput(self) -> str:
        model_header = "{} model".format(self.getModelName())
        content = model_header + "\n"
        content += "=" * len(model_header)
        content += "\n\n"
        content += "{}\n\n".format(self.model_expression_str)

        content += "Parameters: \n"
        for symbol, val, std_dev in zip(
            self.model_par_str, self.model_par_values, self.model_par_values_std_dev
        ):
            content += "            {} = {:.10f}    std. dev. = {:.10f}\n".format(
                symbol, val, std_dev
            )
        content += "\n"

        content += "Sauter diameter expression: {}\n".format(
            self.getSauterDiameterExpression()
        )
        content += "Sauter diameter mean: dps = {:.10f}\n".format(
            self.getSauterDiameterValue()
        )

        content += "\n"

        content += "Standard error of the regression (S) = {:.10f}\n".format(
            self.__std_error_mean
        )
        content += "NOTE: S must be <= 2.5 to produce a sufficiently narrow 95% prediction interval.\n"
        content += "\n"

        content += "R-squared = {:.10f}\n".format(self.__r_squared)
        content += "NOTE: R-squared is not trustworthy for nonlinear regression\n"

        return content

    def getDn(self, x: np.ndarray, y: np.ndarray, n: float, DnInitial: float) -> float:
        for i in range(len(x)):
            if y[i] >= n:
                return x[i]
        return DnInitial

    def __repr__(self):
        return self.getModelName()
