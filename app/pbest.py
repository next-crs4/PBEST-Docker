#! /usr/local/bin/python
import argparse
import os
import sys, errno
import logging
import pandas as pd

TEMPLATE_OUTFILE = '/app/files/detected_samples.xlsx'
SRC_PATH = "/app/src"
OUTPUT_FORMAT = ['tsv', 'csv', 'xlsx']


class pBest(object):
    def __init__(self, args):
        self.logger = self.a_logger(name=self.__class__.__name__, filename=args.logfile)
        self.params = args
        self.logger.info(' === {} ==='.format(self.__class__.__name__))

    def do(self):
        self._check_files()
        detected_samples = self._run(self.params.input_file)
        self.logger.info("Detected Samples: {}".format(detected_samples))
        self._finalize(detected_samples,
                       self.params.output_file,
                       self.params.output_format)



    def _run(self, infile):
        try:
            os.chdir(SRC_PATH)
            cmd = "octave-cli pbest.m {} | tail -1".format(infile)
            result = os.popen(cmd).read().strip()
            detected_samples = [int(x.strip()) for x in result.split(" ") if x ]
        except Exception as e:
            self.logger.error(str(e))
            sys.exit(errno.EAGAIN)
        return sorted(detected_samples)

    def _finalize(self, samples, ofile, oformat):
        try:
            df = pd.read_excel(TEMPLATE_OUTFILE)
            for s in samples:
                df['result'][s - 1] = 1

            self.logger.info("Writing results in {}".format(ofile))

            if 'xlsx' in oformat:
                df.to_excel(ofile, columns=['sample number', 'result'], index=False, engine="xlsxwriter")
            elif 'csv' in oformat:
                df.to_csv(ofile, columns=['sample number', 'result'], index=False, sep=',')
            elif 'tsv' in oformat:
                df.to_csv(ofile, columns=['sample number', 'result'], index=False, sep='\t')

        except Exception as e:
            self.logger.error(str(e))
            sys.exit(errno.EAGAIN)

    def _check_files(self):
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
    parser = argparse.ArgumentParser(prog='pbest',
                                     description='Run PBEST algorithm to identify COVID-19 positive carriers')

    parser.add_argument('--input-file', '-i', metavar="FILE",
                         help='input file (experimental results)',
                         required=True)
    parser.add_argument('--output-file', '-o', metavar="FILE",
                         help='output file (detected samples)',
                         required=True)

    parser.add_argument('--output-format', '-t', type=str,
                        metavar="STR",
                        choices=OUTPUT_FORMAT,
                        default="xlsx",
                        help='Output file format: [{}]'.format(",".join(OUTPUT_FORMAT)))

    parser.add_argument('--force', '-f', action='store_true',
                         default=False,
                         help='force to overwrite output file')

    parser.add_argument('--logfile', type=str, metavar='PATH',
                         help='log file (default=stderr)')

    return parser

def main():
    parser = make_parser()

    args = parser.parse_args()
    app = pBest(args)
    app.do()


if __name__ == "__main__":
    main()
