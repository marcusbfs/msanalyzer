import argparse
import io
import json
import logging
import os
import time
from typing import List

import matplotlib.pyplot as plt
from rich.console import Console
from rich.progress import Progress

from . import MasterSizerReport as msreport
from . import MultipleFilesReport as multireport

logger = logging.getLogger("msanalyzer")


fig: plt.figure = None

models_figs: dict = {}

console = Console()


def main(_args: List[str] = None) -> None:

    start_time = time.time()

    global models_figs

    version_message = (
        "MasterSizerReport "
        + msreport.MasterSizerReport.getVersion()
        + os.linesep
        + os.linesep
        + "Author: {}".format(msreport.__author__)
        + os.linesep
        + "email: {}".format(msreport.__email__)
    )

    desc = (
        version_message
        + os.linesep
        + os.linesep
        + "Process arguments for Mastersizer 2000 report analysis"
    )

    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawTextHelpFormatter
    )

    list_of_diameterchoices = {
        "geo": msreport.DiameterMeanType.geometric,
        "ari": msreport.DiameterMeanType.arithmetic,
    }

    choices_keys = list(list_of_diameterchoices.keys())

    # CLI options/flags
    parser.add_argument("xps", nargs="?", default="ms_input.xps", help="XPS file")

    parser.add_argument(
        "-o",
        "--output_basename",
        default="output_",
        dest="output_basename",
        help="name of output base filenames",
    )

    parser.add_argument(
        "-d",
        "--output_dir",
        default="mastersizer_output",
        dest="output_dir",
        help="name of output directory",
    )

    parser.add_argument(
        "-m",
        "--diameter_mean",
        dest="meantype",
        nargs=1,
        default=[choices_keys[0]],
        help="type of diameter mean which will be used. default is geometric mean",
        choices=choices_keys,
    )

    parser.add_argument(
        "-f",
        "--first_zeros",
        dest="first_zeros",
        nargs=1,
        default=[1],
        help="number of zeros to be left on the beginning of data. Default value is 1",
    )

    parser.add_argument(
        "-l",
        "--last_zeros",
        dest="last_zeros",
        nargs=1,
        default=[1],
        help="number of zeros to be left on the end of data. Default value is 1",
    )

    parser.add_argument(
        "-s",
        "--log-scale",
        dest="log_scale",
        default=False,
        help="plot using log scale",
        action="store_true",
    )

    parser.add_argument(
        "-M",
        "--multiple-files",
        dest="multiple_files",
        nargs="+",
        help="plot multiple data",
    )

    parser.add_argument(
        "--multi-labels",
        dest="multiple_labels",
        nargs="+",
        help="multiple data plot labels",
    )

    parser.add_argument(
        "--multi-no-labels",
        dest="multiple_no_labels",
        default=False,
        help="do not plot labels on multiple plots",
        action="store_true",
    )

    parser.add_argument(
        "--custom-plot-args",
        dest="custom_plot_args",
        nargs=1,
        help="custom matplotlib args",
        default=[{}],
        type=json.loads,
    )

    parser.add_argument(
        "--info",
        dest="info",
        default=False,
        help="print aditional information",
        action="store_true",
    )

    parser.add_argument("-v", "--version", action="version", version=version_message)

    args = parser.parse_args(args=_args)

    level = logging.INFO if args.info else logging.WARNING

    meanType = list_of_diameterchoices[args.meantype[0]]
    output_dir = args.output_dir
    output_basename = args.output_basename
    number_of_zero_first = int(args.first_zeros[0])
    number_of_zero_last = int(args.last_zeros[0])
    log_scale = args.log_scale
    custom_plot_args = args.custom_plot_args[0]

    # end of args parser

    # set logging level
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s: %(message)s")

    logger.info("Arguments passed: {}".format(args))

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        logger.info('Directory "{}" created'.format(output_dir))

    global fig

    # calculate results - one file only input
    if not args.multiple_files:

        progress = Progress(console=console)
        task = progress.add_task("Single mode", total=9)
        progress.start()

        logger.info("Single file mode")

        reporter: msreport.MasterSizerReport = msreport.MasterSizerReport()
        logger.info("Created reporter object")
        progress.advance(task, 1)

        xps_file = args.xps

        with open(xps_file, "rb") as xpsfile_mem:
            reporter.setXPSfile(io.BytesIO(xpsfile_mem.read()), xps_file)
            reporter.setDiameterMeanType(meanType)
            reporter.cutFirstZeroPoints(number_of_zero_first, tol=1e-8)
            reporter.cutLastZeroPoints(number_of_zero_last, tol=1e-8)
            reporter.setLogScale(logscale=log_scale)
            logger.info("Reporter object setted up")
            progress.advance(task, 1)

        # calculate

        reporter.evaluateData()
        logger.info("Data evaluated")
        progress.advance(task, 1)
        reporter.evaluateModels()
        logger.info("Models evaluated")
        progress.advance(task, 1)

        # name of outputfiles
        curves = output_basename + "curves"
        curves_data = output_basename + "curves_data.txt"
        PSD_model = output_basename + "model"
        PSD_data = output_basename + "model_parameters"
        excel_data = output_basename + "curve_data"
        best_model_basename = "best_models_ranking"

        fig = reporter.saveFig(output_dir, curves)
        models_figs = reporter.saveModelsFig(output_dir, PSD_model)
        progress.advance(task, 1)
        reporter.saveData(output_dir, curves_data)
        progress.advance(task, 1)
        reporter.saveModelsData(output_dir, PSD_data)
        progress.advance(task, 1)
        reporter.saveExcel(output_dir, excel_data)
        logger.info("Results saved")
        progress.advance(task, 1)

        logger.info("Analyzing best model")
        reporter.saveBestModelsRanking(output_dir, best_model_basename)
        progress.advance(task, 1)
        progress.stop()

    # calculate results - multiple files input
    else:
        progress = Progress(console=console)
        task = progress.add_task("Multi mode", total=4)
        progress.start()

        number_of_files = len(args.multiple_files)
        logger.info("Multiple files mode - {} files".format(number_of_files))

        f_mem = []
        for f in args.multiple_files:
            f_mem.append(io.BytesIO(open(f, "rb").read()))
        progress.advance(task, 1)

        multiReporter = multireport.MultipleFilesReport(
            f_mem,
            args.multiple_files,
            meanType,
            log_scale,
            number_of_zero_first,
            number_of_zero_last,
            custom_plot_args,
            not args.multiple_no_labels,
        )
        logger.info("Created multiple files reporter object")
        progress.advance(task, 1)

        if args.multiple_labels and len(args.multiple_labels) > 1:
            multiReporter.setLabels(args.multiple_labels)

        MultiSizeDistribution_output_file = os.path.join(
            output_dir, "MultiSizeDistribution"
        )
        MultiFrequency_output_file = os.path.join(output_dir, "MultiFrequency")

        fig = multiReporter.sizeDistributionPlot(MultiSizeDistribution_output_file)
        multiReporter.frequencyPlot(MultiFrequency_output_file)
        progress.advance(task, 1)

        for f in f_mem:
            f.close()

        progress.advance(task, 1)
        progress.stop()

    if not args.info:
        console.print("[green]Done!")

    logger.info("Program finished in {:.3f} seconds".format(time.time() - start_time))
