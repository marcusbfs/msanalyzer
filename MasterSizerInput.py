import os
import logging

import numpy as np

import fitz

logger = logging.getLogger(__name__)


class MasterSizerInput:
    def __init__(self):

        self.__text: str = ""

        self.__x_header: str = r"Size (µm)"
        self.__y_header: str = r"Volume In %"

        self.__x_values = []
        self.__y_values = []

        self.__n_tables: int = 6

        self.__values_per_table: int = 17
        self.__values_last_table: int = 15

    def setXPSfile(self, input_xps: str) -> None:

        if not os.path.exists(input_xps):
            print('File "' + input_xps + '" doesnt not exist')
            raise (FileNotFoundError)

        logger.info('Extracting data from "{}"'.format(input_xps))
        doc = fitz.open(input_xps)
        page = doc.loadPage(0)
        self.__text = page.getText()
        doc.close()

        self.__extractData()

    def setDataFiles(
        self, x_filename: str, y_filename: str, isCommaSeparator: bool = False
    ) -> None:

        self.__x_values = np.loadtxt(x_filename)
        self.__y_values = np.loadtxt(y_filename) / 100.0
        assert len(self.__x_values) == len(self.__y_values) + 1

    def getx(self) -> np.array:
        return self.__x_values

    def gety(self) -> np.array:
        return self.__y_values

    def __extractData(self) -> None:
        lines = self.__text.splitlines()
        n_of_lines = len(lines)

        table_count = 1

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

        self.__x_values = np.array(self.__x_values)
        self.__y_values = np.array(self.__y_values) / 100.0
        if len(self.__x_values) != len(self.__y_values) + 1:
            logger.error("len of x and y vectors are mismatched")
            assert len(self.__x_values) == len(self.__y_values) + 1

        logger.info("X values: {}".format(len(self.__x_values)))
        logger.info("Y values: {}".format(len(self.__y_values)))
