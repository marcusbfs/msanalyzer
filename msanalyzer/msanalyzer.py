import os
import logging
import argparse
import time

logger = logging.getLogger("msanalyzer")

import MasterSizerReport as msreport


def main():

    start_time = time.time()

    version_message = (
        "MasterSizerReport "
        + msreport.getVersion()
        + os.linesep
        + os.linesep
        + "Author: Marcus Bruno Fernandes Silva"
        + os.linesep
        + "email: marcusbfs@gmail.com"
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
        "--info",
        dest="info",
        default=False,
        help="print aditional information",
        action="store_true",
    )

    parser.add_argument("-v", "--version", action="version", version=version_message)

    args = parser.parse_args()
    # end of args parser

    # calculate results

    # set logging level

    if args.info:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level, format="%(asctime)s - %(name)s: %(message)s")

    logger.info("Arguments passed: {}".format(args))

    reporter = msreport.MasterSizerReport()
    logger.info("Created reporter object")

    xps_file = args.xps
    meanType = list_of_diameterchoices[args.meantype[0]]
    output_dir = args.output_dir
    output_basename = args.output_basename
    number_of_zero_first = int(args.first_zeros[0])
    number_of_zero_last = int(args.last_zeros[0])

    reporter.setXPSfile(xps_file)
    reporter.setDiameterMeanType(meanType)
    reporter.cutFirstZeroPoints(number_of_zero_first, tol=1e-8)
    reporter.cutLastZeroPoints(number_of_zero_last, tol=1e-8)
    reporter.setLogScale(logscale=args.log_scale)
    logger.info("Reporter object setted up")

    # calcualte
    reporter.evaluateData()
    logger.info("Data evaluated")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        logger.info('Directory "{}" created'.format(output_dir))

    #  [('W ignore', None, 'OPTION')],

    # name of outputfiles
    curves = output_basename + "curves"
    curves_data = output_basename + "curves_data.txt"
    PSD_model = output_basename + "model"
    PSD_data = output_basename + "model_parameters"
    excel_data = output_basename + "curve_data"

    reporter.saveFig(output_dir, curves)
    reporter.saveModelsFig(output_dir, PSD_model)
    reporter.saveData(output_dir, curves_data)
    reporter.saveModelsData(output_dir, PSD_data)
    reporter.saveExcel(output_dir, excel_data)
    logger.info("Results saved")

    logger.info("Program finished in {:.3f} seconds".format(time.time() - start_time))


main()
