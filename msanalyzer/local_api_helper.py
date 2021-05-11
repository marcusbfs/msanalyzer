import io
import logging
import os
from typing import List

from pydantic import BaseModel

from . import MasterSizerReport as msreport
from . import MultipleFilesReport as multireport

logging.getLogger("matplotlib.font_manager").disabled = True


list_of_diameterchoices = {
    "geo": msreport.DiameterMeanType.geometric,
    "ari": msreport.DiameterMeanType.arithmetic,
}


class CommonOptions(BaseModel):
    meanType: str
    zerosLeft: int
    zerosRight: int
    logScale: bool
    multiLabel: bool


class MultiInput(BaseModel):
    xpsfiles: List[str]
    labels: List[str]
    outDir: str
    outName: str


# ==== local api ====================================================================
async def singleModeCompute_helper(
    xpsfile: str, outputName: str, outputDir: str, options: CommonOptions
):
    reporter: msreport.MasterSizerReport = msreport.MasterSizerReport()

    meanType = list_of_diameterchoices[options.meanType]
    number_of_zero_first = options.zerosLeft
    number_of_zero_last = options.zerosRight
    log_scale = options.logScale

    with open(xpsfile, "rb") as xpsfile_mem:
        reporter.setXPSfile(io.BytesIO(xpsfile_mem.read()), xpsfile)
        reporter.setDiameterMeanType(meanType)
        reporter.cutFirstZeroPoints(number_of_zero_first, tol=1e-8)
        reporter.cutLastZeroPoints(number_of_zero_last, tol=1e-8)
        reporter.setLogScale(logscale=log_scale)

    # calculate
    reporter.evaluateData()
    reporter.evaluateModels()

    # name of outputfiles
    curves = outputName + "_curves"
    curves_data = outputName + "_curves_data.txt"
    PSD_model = outputName + "_model"
    PSD_data = outputName + "_model_parameters"
    excel_data = outputName + "_curve_data"
    best_model_basename = outputName + "_best_models_ranking"

    reporter.saveFig(outputDir, curves)
    reporter.saveModelsFig(outputDir, PSD_model)
    reporter.saveData(outputDir, curves_data)
    reporter.saveModelsData(outputDir, PSD_data)
    reporter.saveExcel(outputDir, excel_data)

    reporter.saveBestModelsRanking(outputDir, best_model_basename)


async def multiModeCompute_helper(multiInput: MultiInput, options: CommonOptions):
    len(multiInput.xpsfiles)

    meanType = list_of_diameterchoices[options.meanType]

    f_mem = []
    for f in multiInput.xpsfiles:
        f_mem.append(io.BytesIO(open(f, "rb").read()))

    multiReporter = multireport.MultipleFilesReport(
        f_mem,
        multiInput.xpsfiles,
        meanType,
        options.logScale,
        options.zerosLeft,
        options.zerosRight,
        {},
        options.multiLabel,
    )

    if options.multiLabel and len(multiInput.labels) > 1:
        multiReporter.setLabels(multiInput.labels)

    MultiSizeDistribution_output_file = os.path.join(
        multiInput.outDir, multiInput.outName + "_distribution"
    )
    MultiFrequency_output_file = os.path.join(
        multiInput.outDir, multiInput.outName + "_frequency"
    )

    multiReporter.frequencyPlot(MultiFrequency_output_file)
