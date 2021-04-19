import logging

logger = logging.getLogger(__name__)
from typing import List, Any

import numpy as np

import SizeDistributionBaseModel as PSDBase
from scipy.special import gamma


class Sigmoid(PSDBase.SizeDistributionBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_par_str = ["k", "m"]
        self.model_expression_str = "X(d) = 1 / (1 + (k/d)^m)"
        self.model_name_str = "Sigmoid"
        logger.info("{} object constructed".format(self.model_name_str))

    def specificModel(self, d: float, *args: float) -> Any:
        k = args[0]
        m = args[1]
        return 1.0 / (1.0 + np.power(k / d, m))

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        D50 = self.getDn(x, y, 0.5, 100)
        D84 = self.getDn(x, y, 0.84, 120)
        delta = D84 / D50
        return [D50, delta]

    def getSauterDiameterValue(self) -> float:
        Dprime: float = self.model_par_values[0]
        n = self.model_par_values[1]
        if n > 1:
            return float(Dprime / gamma(1.0 - 1.0 / n))
        return 0.0

    def getSauterDiameterExpression(self) -> str:
        return "Not available"
