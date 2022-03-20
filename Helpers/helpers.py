import os
import sys
import logging
from Helpers import timer
import re


class Stats:
    def __init__(self):
        """
        self.is_all is switcher. Standard behavior - only passed tests write it's time
        """
        self.passed = 0
        self.failed = 0
        self.time_passed = 0
        self.time_failed = 0
        self.is_all = False

    def test_passed(self):
        self.passed = self.passed + 1

    def test_failed(self):
        self.failed = self.failed + 1

    def add_time(self, time, positive):
        if positive:
            self.test_passed()
            self.time_passed = self.time_passed + time
        else:
            self.test_failed()
            self.time_failed = self.time_failed + time

    def print_stats(self):
        output = f'''
        ------------------[ STATISTIC ]------------------
               total tests      | {self.passed + self.failed}
        ----------------------- | -----------------------
        Tests passed : {self.passed}
        Tests failed : {self.failed}
        
        success ratio: {self.passed / (self.passed + self.failed) * 100}%
        -------------------------------------------------
               total time       | {(self.time_passed + self.time_failed):0.4f}s
        ----------------------- | -----------------------
        total passed tests time | {self.time_passed:0.4f}s
        total failed tests time | {self.time_failed:0.4f}s
        '''
        print(output)


class Test:
    def __init__(self, logger, stats, verbose=0, length=16):
        self.stats = stats
        self.max_length = length
        self.expected_output_f = None
        self.timer = None
        self.verbose = verbose
        self.logger = logger

    def start(self, expected_output_f):
        self.expected_output_f = expected_output_f
        if len(self.expected_output_f) > (self.max_length + 3):
            self.logger.info(f'...{self.expected_output_f[-self.max_length:-4]}: ')
        else:
            self.logger.info(f'{self.expected_output_f[:-4]}: ')
        self.timer = timer.Timer() if self.verbose >= 2 else None

    def end(self, positive):
        self.timer.stop()
        self.stats.add_time(self.timer.get_time(), positive)
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
    csv, zip_ = list(), list()
    for f in os.listdir("tests"):
        if os.path.isfile(os.path.join("tests", f)):
            print(f)
            if re.search(r'csv$', f):
                csv.append(f)
            if '.bz2' in f or '.gz' in f:
                zip_.append(f)
    return csv, zip_


def provide_tests(directory, folder):
    path = "tests" if directory is None else f"tests/{directory}"
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.txt') and str(folder) in root:
                yield os.path.join(root, file)


def get_directories():
    return [d for d in os.listdir("tests") if os.path.isdir(os.path.join("tests", d))]


def get_dict():
    return {'1': 'osoby.csv',
            '2': 'osoby2.csv',
            '3': 'osoby3.csv'}
