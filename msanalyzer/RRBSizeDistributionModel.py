import logging

logger = logging.getLogger(__name__)
from typing import List

import numpy as np

import SizeDistributionBaseModel as PSDBase


class RRB(PSDBase.SizeDistributionBaseModel):
    def __init__(self):
        super().__init__()
        self.model_par_str = ["D'", "n"]
        self.model_expression_str = "X(d) = 1 - exp(-(d/D')^n)"
        self.model_name_str = "RRB"
        logger.info("{} object constructed".format(self.model_name_str))

    def specificModel(self, d, *args) -> float:
        return 1.0 - np.exp(-np.power(d / args[0], args[1]))

    def getInitialGuesses(self, x: np.ndarray, y: np.ndarray) -> List[float]:
        p0 = [100.0, 1.1]
        for i in range(len(x)):
            if y[i] >= 0.632:
                p0[0] = x[i]
                break
        return p0
