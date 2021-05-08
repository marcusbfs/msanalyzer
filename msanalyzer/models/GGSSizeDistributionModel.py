import logging

logger = logging.getLogger(__name__)
from typing import List, Any

import numpy as np

from . import SizeDistributionBaseModel as PSDBase


class GGS(PSDBase.SizeDistributionBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_par_str = ["k", "m"]
        self.model_expression_str = "X(d) = (d/k)^m"
        self.model_name_str = "GGS"
        logger.info("{} object constructed".format(self.model_name_str))

    def specificModel(
        self, d: PSDBase.ArrayOrFloat, *args: float
    ) -> PSDBase.ArrayOrFloat:
        return np.array(np.power(d / args[0], args[1]))

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        return [np.max(x), 1.0]

    def getSauterDiameterValue(self) -> float:
        k = self.model_par_values[0]
        m = self.model_par_values[1]
        if m > 1:
            k * (m - 1.0) / m
        return 0.0

    def getSauterDiameterExpression(self) -> str:
        return "dps = k*(m - 1)/m for m> 1"
