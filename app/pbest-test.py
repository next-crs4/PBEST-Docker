#! /usr/local/bin/python3

import argparse
import os
import sys, errno
import logging
import random as rnd
import pandas as pd

N_POOLS = 48
N_SAMPLES = 384
MAX_CARRIERS = 10
INPUT_FILE = '/app/files/pooling384_48_by_sample.txt'
TEMPLATE_OUTFILE = '/app/files/exp_carriers_results.xlsx'
SRC_PATH = "/app/src"

class CarriersAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for v in values:
            if not  v in range(1,N_SAMPLES):
                raise argparse.ArgumentError(self, "carriers must be between 1 and {}".format(N_SAMPLES))
        setattr(namespace, self.dest, values)

class pBestTest(object):
    def __init__(self, args):
        self.logger = self.a_logger(name=self.__class__.__name__, filename=args.logfile)
        self.action = args.action
        self.params = args
        self.logger.info(' === {} ==='.format(self.__class__.__name__))

    def do(self):
        self.logger.info('Action: {}'.format(self.action.upper()))
        getattr(self, self.action)()

    def random(self):
        self._check_files()
        carriers = rnd.sample(range(1, N_SAMPLES + 1), self.params.number)
        self._do(carriers)


    def select(self):
        self._check_files()
        carrriers = self.params.carriers
        self._do(carrriers)

    def _do(self, carriers):
        self.logger.info('Carriers: {}'.format(carriers))

        pools = self._get_pools(carriers, self.params.input_file)
        self.logger.info("Pools to be set in: {}".format(pools))

        self._set_pools(pools, self.params.output_file)

        if self.params.run:
            self.logger.info("Running pbest script")
            self._run(carriers, self.params.output_file)

    def _run(self, carriers, ofile):
        try:
            ofile = os.path.abspath(ofile)
            os.chdir(SRC_PATH)
            cmd = "octave-cli pbest.m {} | tail -1".format(ofile)
            result = os.popen(cmd).read().strip()
            detected_samples = [int(x.strip()) for x in result.split(" ") if x ]
        except Exception as e:
            self.logger.error(str(e))
            sys.exit(errno.EAGAIN)

        self.logger.info("Carriers: {}".format(sorted(carriers)))
        self.logger.info("Detected Samples: {}".format(detected_samples))
        if sorted(carriers) == sorted(detected_samples):
            self.logger.info("Testing successful!!!")
        else:
            self.logger.warning("Testing failed!!!")

    def _set_pools(self, pools, ofile):
        try:
            df = pd.read_excel(TEMPLATE_OUTFILE)
            for p in pools:
                self.logger.info("Setting pool {}".format(p))
                df['result'][p - 1] = 1
            df.to_excel(ofile, columns=['pool number', 'result'], index = False, engine="xlsxwriter")
        except Exception as e:
            self.logger.error(str(e))
            sys.exit(errno.EAGAIN)

    def _get_pools(self, carriers, ifile):
        pools = list()
        for c in carriers:
            try:
                cmd = "grep -w sample_{} {} | cut -f2-".format(c, ifile)
                p = os.popen(cmd).read().strip().split("\t")
                self.logger.info("Sample {} in pools {}".format(c, p))
                pools.extend(p)
            except Exception as e:
                self.logger.error(str(e))
        return sorted(set([int(x) for x in pools]))

    def _check_files(self):
        self.params.input_file = os.path.abspath(INPUT_FILE)
        if not os.path.exists(self.params.input_file):
            self.logger.error("Missing input file {}".format(self.params.input_file))
            sys.exit(errno.EEXIST)

        if not os.path.exists(TEMPLATE_OUTFILE):
            self.logger.error("Missing template output file {}".format(TEMPLATE_OUTFILE))
            sys.exit(errno.EEXIST)

        if os.path.exists(self.params.output_file) and not self.params.force:
            self.logger.error("Output file already exists {}".format(self.params.output_file))
            sys.exit(errno.EEXIST)

    def a_logger(self, name, level="INFO", filename=None, mode="a"):
        log_format = '%(asctime)s|%(levelname)-8s|%(name)s |%(message)s'
        log_datefmt = '%Y-%m-%d %H:%M:%S'
        logger = logging.getLogger(name)
        if not isinstance(level, int):
            try:
                level = getattr(logging, level)
            except AttributeError:
                raise ValueError("unsupported literal log level: %s" % level)
            logger.setLevel(level)
        if filename:
            handler = logging.FileHandler(filename, mode=mode)
        else:
            handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format, datefmt=log_datefmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

def make_parser():
    parser = argparse.ArgumentParser(prog='pbest-test',
                                     description='create dummy .xlsx files and test it')

    all_grp = argparse.ArgumentParser(add_help=False)
    all_grp.add_argument('--output-file', '-o', metavar="FILE",
                         help='output xlsx file',
                         required=True)
    all_grp.add_argument('--force', '-f', action='store_true',
                         default=False,
                         help='force to overwrite output file')
    all_grp.add_argument('--run', '-r', action='store_true',
                         default=False,
                         help='run pbest script')
    all_grp.add_argument('--logfile', type=str, metavar='PATH',
                         help='log file (default=stderr)')

    random_grp = argparse.ArgumentParser(add_help=False)
    random_grp.add_argument('--number', '-n', type=int, metavar='INTEGER',
                            choices=range(1,MAX_CARRIERS+1),
                            help='number of asymptomatic carriers to be created',
                            required=True)

    sel_grp = argparse.ArgumentParser(add_help=False)

    sel_grp.add_argument('--carriers', '-c',
                         type=int,
                         metavar="INT",
                         nargs='+',
                         action=CarriersAction,
                         help='list of asymptomatic carriers to be created',
                         required=True)

    subparsers = parser.add_subparsers(dest='action')
    subparsers.add_parser('random', parents=[random_grp, all_grp])
    subparsers.add_parser('select', parents=[sel_grp, all_grp])

    return parser

def main():
    parser = make_parser()

    args = parser.parse_args()
    app = pBestTest(args)
    app.do()


if __name__ == "__main__":
    main()
