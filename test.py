#!ios/bin/python
import subprocess
import click
from Helpers import helpers as hp
from Helpers import debug as db
from Helpers import timer as time

logger = hp.get_logger(__name__, ' ')


@click.group()
def main_group():
    pass


@main_group.command(help='run tests for corona.sh. If test in same dir with corona.sh -f/--file not needed')
@click.option('-f', '--file', 'sh', default='corona', help='path to .sh script')
@click.option('-d', '--switch-debug', 'debug', is_flag=True, help='if flag set - using python diff function instead '
                                                                  'bash diff')
@click.option('--dir', '_dir', default=None, help='runs tests in directory.\n Use `./test.py directory` to check'
                                                  'all directories available')
@click.option('-v', '--verbose', count=True, help='set debugging level')
@click.option('-s', '--stats', 'statistic', is_flag=True, help='shows statistic at the end')
def run(sh, debug, _dir, verbose, statistic):
    if hp.check_platform():
        logger.error('Test running currently on linux only')
        return
    csv, zip_ = hp.provide_csv()
    stats = hp.Stats()
    test = hp.Test(verbose=verbose, stats=stats, logger=logger)
    for test_data in hp.provide_tests(_dir, 1):
        run_test(sh, csv[0], test_data, debug, test)
    for test_data in hp.provide_tests(_dir, 2):
        run_test(sh, zip_[0], test_data, debug, test)
    for test_data in hp.provide_tests(_dir, 2):
        run_test(sh, zip_[1], test_data, debug, test)
    stats.print_stats() if statistic else None


def run_test(sh, csv, expected_output_f, debug, test):
    test.start(expected_output_f)
    with open(expected_output_f) as f:
        cmd = f.readline()[:-1]
        expected_output = f.read()
        exp_arr = expected_output.split('\n')
        exp_arr.sort()
        expected_output = '\n'.join([line.rstrip() for line in exp_arr[1:]]) + '\n'
    response = subprocess.Popen(f'./{sh} {cmd} {csv}', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                encoding='utf-8', shell=True)
    stdout, stderr = response.communicate()
    lines = stdout.splitlines()
    lines.sort()
    stdout = '\n'.join([line.rstrip() for line in lines]) + '\n'
    if stdout == expected_output:
        click.echo(click.style('OK', fg='green'))
        test.end(positive=True)
    else:
        click.echo(click.style('FAIL', fg='red') + '\n\t| ')
        output = db.bash_diff(stdout, expected_output_f, cmd) if debug else db.py_differ(stdout, expected_output)
        print(output)
        test.end(positive=False)


@main_group.command(help='Shows all available directories for test')
def directory():
    print('\n'.join(hp.get_directories()))


@main_group.command(help='check your test\'s time\nUse timer `./corona.sh [OPTIONS] [COMMAND] [LOG1[LOG2]...]`'
                         'full code in quotes')
@click.argument('test')
def timer(test):
    tm = time.Timer()
    tm.start()
    sp = subprocess.Popen(test, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          encoding='utf-8', shell=True)
    sp.communicate()
    tm.print_time()


@main_group.command()
def test():
    for x in hp.provide_tests(None, 2):
        print(x)


if __name__ == '__main__':
    main_group()
