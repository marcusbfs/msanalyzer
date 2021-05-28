import logging

logger = logging.getLogger(__name__)
from typing import List

import numpy as np
from scipy.special import gamma

from . import SizeDistributionBaseModel as PSDBase

ArrayOrFloat = PSDBase.ArrayOrFloat


class RRB(PSDBase.SizeDistributionBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_par_str = ["D63", "n"]
        self.model_expression_str = "X(d) = 1 - exp(-(d/D63)^n)"
        self.model_name_str = "RRB"
        logger.info("{} object constructed".format(self.model_name_str))

    def specificModel(self, d: ArrayOrFloat, *args: float) -> ArrayOrFloat:
        return np.array(1.0 - np.exp(-np.power(d / args[0], args[1])))

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        return [self.getDn(x, y, 0.632, 100), 1.0]

    def getSauterDiameterValue(self) -> float:
        Dprime: float = self.model_par_values[0]
        n = self.model_par_values[1]
        if n > 1:
            return float(Dprime / gamma(1.0 - 1.0 / n))
        return 0.0

    def getSauterDiameterExpression(self) -> str:
        return "dps = D63/gamma(1 - 1/n) for n > 1"
