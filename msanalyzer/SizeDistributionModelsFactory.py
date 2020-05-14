
import logging

logger = logging.getLogger(__name__)
from typing import List

import SizeDistributionBaseModel as PSDBase
from RRBSizeDistributionModel import RRB
from GGSSizeDistributionModel import GGS
from LogNormalSizeDistributionModel import LogNormal


def getPSDModelsList() -> List[PSDBase.SizeDistributionBaseModel]:
    return [RRB(), GGS(), LogNormal()]