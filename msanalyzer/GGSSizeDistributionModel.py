import logging

logger = logging.getLogger(__name__)
from typing import List

import numpy as np

import SizeDistributionBaseModel as PSDBase


class GGS(PSDBase.SizeDistributionBaseModel):
    def __init__(self):
        super().__init__()
        self.model_par_str = ["k", "m"]
        self.model_expression_str = "X(d) = (d/k)^m"
        self.model_name_str = "GGS"
        logger.info("{} object constructed".format(self.model_name_str))

    def specificModel(self, d, *args) -> float:
        return np.power(d/args[0], args[1])

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        return [np.max(x), 1.0]
