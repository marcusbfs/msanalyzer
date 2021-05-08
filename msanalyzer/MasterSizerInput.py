import os
import logging
import io

import numpy as np
import numpy.typing as npt

import fitz

logger = logging.getLogger(__name__)


class MasterSizerInput:
    def __init__(self) -> None:

        self.__text: str = ""

        self.__x_header: str = r"Size (µm)"
        self.__y_header: str = r"Volume In %"

        self.__x_values: list[float] = []
        self.__y_values: list[float] = []

        self.__n_tables: int = 6

        self.__values_per_table: int = 17
        self.__values_last_table: int = 15

    def setFile(self, xps_memory: io.BytesIO, filename: str = "") -> None:

        self.__filename = filename
        doc = fitz.open(stream=xps_memory, filetype="xps")
        page = doc.loadPage(0)
        self.__text = page.getText()
        doc.close()

        logger.info("Raw data loaded from memory")

    def getx(self) -> np.ndarray:
        return np.array(self.__x_values)

    def gety(self) -> np.ndarray:
        return np.array(self.__y_values)

    def extractData(self) -> None:
        lines = self.__text.splitlines()
        n_of_lines = len(lines)

        logger.info("Parsing raw data loaded")

        table_count = 1

        self.__x_values = []
        self.__y_values = []

        i = 0

        while i < n_of_lines:

            line = lines[i]

            # size
            if line == self.__x_header:
                i += 1
                for kk in range(self.__n_tables - 1):
                    # read size
                    for j in range(i, self.__values_per_table + i):
                        line = lines[j]
                        self.__x_values.append(float(line))
                    # updates i
                    i += self.__values_per_table + 2
                    # read volume
                    for j in range(i, self.__values_per_table + i):
                        line = lines[j]
                        self.__y_values.append(float(line))
                    i += self.__values_per_table + 1

                # read last table
                for j in range(i, self.__values_last_table + i + 1):
                    line = lines[j]
                    self.__x_values.append(float(line))
                # updates i
                i += self.__values_last_table + 2
                # read volume
                for j in range(i, self.__values_last_table + i):
                    line = lines[j]
                    self.__y_values.append(float(line))
                i += self.__values_last_table + 1

            else:
                i += 1

        self.__x_values = self.__x_values
        self.__y_values = np.array(self.__y_values) / 100.0
        if len(self.__x_values) != len(self.__y_values) + 1:
            logger.error("len of x and y vectors are mismatched")
            assert len(self.__x_values) == len(self.__y_values) + 1

        logger.info("Length of x: {}".format(len(self.__x_values)))
        logger.info("Length of y: {}".format(len(self.__y_values)))
