from abc import ABC, abstractmethod
from typing import List


class MasterSizerInputReader(ABC):
    @abstractmethod
    def setFile(self, filename: str) -> None:
        pass

    @abstractmethod
    def extractData(self) -> None:
        pass

    @abstractmethod
    def getx(self) -> List[float]:
        pass

    @abstractmethod
    def gety(self) -> List[float]:
        pass
