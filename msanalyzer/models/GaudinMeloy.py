import logging

logger = logging.getLogger(__name__)
from typing import List

import numpy as np

from . import SizeDistributionBaseModel as PSDBase

ArrayOrFloat = PSDBase.ArrayOrFloat


class GaudinMeloy(PSDBase.SizeDistributionBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_par_str = ["Dmax", "n"]
        self.model_expression_str = "X(d) = 1 - [1 - (d/Dmax)]^n"
        self.model_name_str = "Gaudin-Meloy"
        logger.info("{} object constructed".format(self.model_name_str))

    def specificModel(self, d: ArrayOrFloat, *args: float) -> ArrayOrFloat:
        return np.array(1.0 - np.power(1.0 - d / args[0], args[1]))

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        return [np.max(x), 1.0]

    def getSauterDiameterValue(self) -> float:
        Dprime: float = self.model_par_values[0]
        self.model_par_values[1]
        return 0.0

    def getSauterDiameterExpression(self) -> str:
        return "non-available"
