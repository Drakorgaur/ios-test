import os
import sys
import logging
from Helpers import timer


class Test:
    def __init__(self, expected_output_f, logger, verbose=0, length=16):
        self.max_length = length
        self.expected_output_f = expected_output_f
        self.timer = None
        self.verbose = verbose
        self.logger = logger

    def start(self):
        if len(self.expected_output_f) > (self.max_length + 3):
            self.logger.info(f'...{self.expected_output_f[-self.max_length:-4]}: ')
        else:
            self.logger.info(f'{self.expected_output_f[:-4]}: ')
        self.timer = timer.Timer() if self.verbose >= 2 else None

    def end(self):
        self.timer.print_time() if self.timer is not None else None


def get_logger(name, terminator='\n'):
    logger = logging.getLogger(name)
    cHandle = logging.StreamHandler()
    cHandle.terminator = terminator
    cHandle.setFormatter(logging.Formatter(fmt='%(message)s'))
    logger.addHandler(cHandle)
    logger.setLevel(logging.INFO)
    return logger


def check_platform():
    return False if sys.platform == 'linux' else True


def provide_csv():
    return [f for f in os.listdir("tests") if os.path.isfile(os.path.join("tests", f))]


def provide_tests(directory):
    path = "tests" if directory is None else f"tests/{directory}"
    for root, directories, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                yield os.path.join(root, file)


def get_directories():
    return [d for d in os.listdir("tests") if os.path.isdir(os.path.join("tests", d))]


def get_dict():
    return {'1': 'osoby.csv',
            '2': 'osoby2.csv',
            '3': 'osoby3.csv'}
