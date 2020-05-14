import logging

logger = logging.getLogger(__name__)
from typing import List

import numpy as np
from scipy.special import erf

import SizeDistributionBaseModel as PSDBase


class LogNormal(PSDBase.SizeDistributionBaseModel):
    def __init__(self):
        super().__init__()
        self.model_par_str = ["D50", "delta"]
        self.model_expression_str = (
            "X(d) = 0.5*[1 + erf(Z)]; Z = ln[(d/D50) / (sqrt(2) * ln(delta) ) ]"
        )
        self.model_name_str = "LogNormal"
        logger.info("{} object constructed".format(self.model_name_str))
        self.sqrt2 = np.sqrt(2.0)

    def specificModel(self, d, *args) -> float:
        D50 = args[0]
        delta = args[1]
        Z = np.log((d / D50) / (self.sqrt2 * np.log(delta)))
        return 0.5 * (1 + erf(Z))

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        D50 = 100.0
        D84 = 120
        delta = 1.0
        for i in range(len(x)):
            if y[i] >= 0.5:
                D50 = x[i]
                break
        for i in range(len(x)):
            if y[i] >= 0.84:
                D84 = x[i]
                break
        delta = D84 / D50
        return [D50, delta]
