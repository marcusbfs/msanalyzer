import argparse
import io
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
from rich.console import Console
from rich.progress import BarColumn, Progress, ProgressColumn, SpinnerColumn, Task
from rich.table import Table
from rich.text import Text

from . import FeedCurve
from . import MasterSizerReport as msreport
from . import MultipleFilesReport as multireport

logger = logging.getLogger("msanalyzer")


fig: plt.figure = None

models_figs: dict = {}  # type: ignore

console = Console()

list_of_diameterchoices = {
    "geo": msreport.DiameterMeanType.geometric,
    "ari": msreport.DiameterMeanType.arithmetic,
}

choices_keys = list(list_of_diameterchoices.keys())

version_message = (
    "MasterSizerReport "
    + msreport.MasterSizerReport.getVersion()
    + os.linesep
    + os.linesep
    + "Author: {}".format(msreport.__author__)
    + os.linesep
    + "email: {}".format(msreport.__email__)
)


class customTimeElapsedColumn(ProgressColumn):
    def render(self, task: Task) -> Text:
        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            return Text(" ", style="progress.elapsed")
        return Text(f"{elapsed:4.1f}s", style="progress.elapsed")


class customTimeRemainingColumn(ProgressColumn):
    def render(self, task: Task) -> Text:
        remaining = task.time_remaining
        if remaining is None:
            return Text("  ", style="progress.remaining")
        return Text(f"{remaining:4.1f}s", style="progress.elapsed")


def get_args(_args: Optional[List[str]] = None) -> argparse.Namespace:
    desc = (
        version_message
        + os.linesep
        + os.linesep
        + "Process arguments for Mastersizer 2000 report analysis"
    )

    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawTextHelpFormatter
    )

    parser = add_common_args(parser)

    # CLI options/flags
    parser.add_argument("xps", nargs="?", default="ms_input.xps", help="XPS file")

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
        "--feed",
        dest="feed",
        default=False,
        action="store_true",
        help="Generates feed data from under and over files",
    )

    return parser.parse_args(args=_args)


def add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
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
        "--no-log-scale",
        dest="log_scale",
        default=False,
        help="plot without using log scale",
        action="store_true",
    )

    parser.add_argument(
        "--info",
        dest="info",
        default=False,
        help="print aditional information",
        action="store_true",
    )

    parser.add_argument("-v", "--version", action="version", version=version_message)
    return parser


def feed_parser(args: Optional[List[str]] = None) -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Generates feed data from under and over files",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # parser.add_argument("--feed", help="unused option", action="store_true")
    parser.add_argument("--under", type=str, help="under data file", required=True)
    parser.add_argument("--over", type=str, help="over data file", required=True)
    parser.add_argument(
        "--uw", type=float, help="under mass flow [kg/s]", required=True
    )
    parser.add_argument("--ow", type=float, help="over mass flow[kg/s]", required=True)
    parser.add_argument("--fw", type=float, help="feed mass flow[kg/s]", required=True)

    parser = add_common_args(parser)

    return parser.parse_args(args=args)


def feed_subcommand(args: argparse.Namespace) -> None:

    # set logging level

    level = logging.INFO if args.info else logging.WARNING
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s: %(message)s")

    under_file = Path(args.under)
    over_file = Path(args.over)
    output_dir = args.output_dir
    output_basename = args.output_basename

    config = FeedCurve.Config(
        mean_type=list_of_diameterchoices[args.meantype[0]],
        first_zeros=int(args.first_zeros[0]),
        last_zeros=int(args.last_zeros[0]),
        log_scale=not args.log_scale,
        under_mass_flow=float(args.uw),
        over_mass_flow=float(args.ow),
        feed_mass_flow=float(args.fw),
    )

    # calculate
    feed = FeedCurve.FeedFromUnderAndOver(under_file, over_file, config)
    feed_reporter = feed.get_feed_reporter()

    feed_reporter.evaluateData()
    logger.info("Data evaluated")
    models: msreport.ModelsData = feed_reporter.evaluateModels()
    logger.info("Models evaluated")
    time.sleep(0.2)

    # name of outputfiles
    output_basename + "curves"
    curves_data = output_basename + "curves_data.txt"
    PSD_model = output_basename + "model"
    PSD_data = output_basename + "model_parameters"
    excel_data = output_basename + "curve_data"
    best_model_basename = "best_models_ranking"

    feed_reporter.saveModelsFig(output_dir, PSD_model)

    feed_reporter.saveData(output_dir, curves_data)
    feed_reporter.saveModelsData(output_dir, PSD_data)
    feed_reporter.saveExcel(output_dir, excel_data)

    logger.info("Results saved")

    logger.info("Analyzing best model")
    feed_reporter.saveBestModelsRanking(output_dir, best_model_basename)

    print("done! results saved in directory '{}'".format(str(output_dir)))
    return


def _real_main(_args: Optional[List[str]] = None) -> None:

    start_time = time.time()

    if _args is None:
        _args = sys.argv[1:]

    # If feed subcommand, treat it soon
    if _args and ("feed" in _args or "--feed" in _args):
        # Remove args
        t_args = []
        for a in _args:
            if not "feed" in a:
                t_args.append(a)
        feed_subcommand(feed_parser(t_args))
        return

    global models_figs

    args = get_args(_args)

    level = logging.INFO if args.info else logging.WARNING

    meanType = list_of_diameterchoices[args.meantype[0]]
    output_dir = args.output_dir
    output_basename = args.output_basename
    number_of_zero_first = int(args.first_zeros[0])
    number_of_zero_last = int(args.last_zeros[0])
    log_scale = not args.log_scale
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

        logger.info("Single file mode")
        progress = Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "(",
            customTimeElapsedColumn(),
            ")",
            "[dim]{task.fields[extra]}",
            console=console,
        )

        reporter: msreport.MasterSizerReport = msreport.MasterSizerReport()
        n_of_models = reporter.getNumberOfModels()
        logger.info("Created reporter object")

        task = progress.add_task("Single mode", total=n_of_models, extra="")

        progress.start()
        callback_fun = lambda: progress.advance(task, 1)

        xps_file = args.xps

        progress.update(task, extra=f"reading {os.path.basename(xps_file)}")
        with open(xps_file, "rb") as xpsfile_mem:
            reporter.setXPSfile(io.BytesIO(xpsfile_mem.read()), xps_file)
            reporter.setDiameterMeanType(meanType)
            reporter.cutFirstZeroPoints(number_of_zero_first, tol=1e-8)
            reporter.cutLastZeroPoints(number_of_zero_last, tol=1e-8)
            reporter.setLogScale(logscale=log_scale)
            logger.info("Reporter object setted up")
            time.sleep(0.2)

        # calculate

        progress.update(task, extra=f"evaluating models")
        reporter.evaluateData()
        logger.info("Data evaluated")
        models: msreport.ModelsData = reporter.evaluateModels()
        logger.info("Models evaluated")
        time.sleep(0.2)

        # name of outputfiles
        curves = output_basename + "curves"
        curves_data = output_basename + "curves_data.txt"
        PSD_model = output_basename + "model"
        PSD_data = output_basename + "model_parameters"
        excel_data = output_basename + "curve_data"
        best_model_basename = "best_models_ranking"

        progress.update(task, extra=f"generating plots")
        fig = reporter.saveFig(output_dir, curves)
        models_figs = reporter.saveModelsFig(
            output_dir, PSD_model, callback=callback_fun
        )
        reporter.saveData(output_dir, curves_data)
        reporter.saveModelsData(output_dir, PSD_data)
        reporter.saveExcel(output_dir, excel_data)
        logger.info("Results saved")

        logger.info("Analyzing best model")
        progress.update(task, extra=f"analyzing best model")
        reporter.saveBestModelsRanking(output_dir, best_model_basename)

        progress.update(task, extra="")
        progress.stop()

        diameters = (10, 25, 50, 75, 90)

        table = Table(header_style="red bold")

        table.add_column("Model")
        table.add_column("Parameters", justify="right")

        for d in diameters:
            table.add_column(f"D{d}", justify="right")

        table.add_column("Mean error", justify="right")
        table.add_column("r^2", justify="right")

        for model in models.models:
            row = []
            row.append(model.name)

            par = ""

            n_par = len(model.parameters)
            for i in range(n_par):
                p = model.parameters[i]
                par += f"{p.repr}: {p.value:.4f} +- {p.stddev:.4f}" + (
                    "\n" if i != n_par - 1 else ""
                )

            row.append(par)

            for d in diameters:
                row.append(f'{model.D[f"D{d}"]:.2f}')

            row.append(f"{100.*model.s:.3f}%")
            row.append(f"{model.r2:.4f}")

            table.add_row(*row, end_section=True)

        console.print(table)

    # calculate results - multiple files input
    else:
        progress = Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "(",
            customTimeElapsedColumn(),
            ")",
            "{task.fields[extra]}",
            console=console,
        )

        number_of_files = len(args.multiple_files)
        task = progress.add_task("Multi mode", total=2 + number_of_files, extra="")
        progress.start()

        number_of_files = len(args.multiple_files)
        logger.info("Multiple files mode - {} files".format(number_of_files))

        f_mem = []
        for f in args.multiple_files:
            extra_field = f"[dim]reading {os.path.basename(f)}"
            progress.update(task, extra=extra_field)
            f_mem.append(io.BytesIO(open(f, "rb").read()))
            time.sleep(0.25)
            progress.advance(task, 1)
        progress.update(task, extra="")

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

        if args.multiple_labels and len(args.multiple_labels) > 1:
            multiReporter.setLabels(args.multiple_labels)

        MultiSizeDistribution_output_file = os.path.join(
            output_dir, "MultiSizeDistribution"
        )
        MultiFrequency_output_file = os.path.join(output_dir, "MultiFrequency")

        progress.update(task, extra="[dim]size distribution plot")
        fig = multiReporter.sizeDistributionPlot(MultiSizeDistribution_output_file)
        time.sleep(0.2)
        progress.advance(task, 1)
        progress.update(task, extra="[dim]frequency plot")
        multiReporter.frequencyPlot(MultiFrequency_output_file)
        time.sleep(0.2)
        progress.advance(task, 1)

        for f in f_mem:
            f.close()

        progress.update(task, extra="")
        progress.stop()
        console.print("[bold green]Done!")

    logger.info("Program finished in {:.3f} seconds".format(time.time() - start_time))


def main(_args: Optional[List[str]] = None) -> None:
    try:
        _real_main(_args=_args)
    except Exception as e:
        console.print("[bold red]An error ocurred!")
        console.print("Please, check if the [bold green]XPS[/] file is correct.")
        if "--info" in sys.argv:
            console.print("[bold blue]Error message:")
            console.print(e)
