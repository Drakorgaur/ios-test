#!ios/bin/python
import subprocess
import click
from Helpers import helpers as hp
from Helpers import debug as db

logger = hp.get_logger(__name__, ' ')

@click.group()
def main_group():
    pass


@main_group.command(help='run tests for corona.sh. If test in same dir with corona.sh -f/--file not needed')
@click.option('-f', '--file', 'sh', default='corona.sh', help='path to .sh script')
@click.option('-d', '--switch-debug', 'debug', is_flag=True, help='if flag set - using python diff function instead '
                                                                  'bash diff')
@click.option('--dir', '_dir', default=None, help='runs tests in directory.\n Use `./test.py directory` to check'
                                                       'all directories available')
def run(sh, debug, _dir):
    if hp.check_platform():
        logger.error('Test running currently on linux only')
        return
    csv = hp.provide_csv()
    for test in hp.provide_tests(_dir):
        run_test(sh, csv[2], test, debug)


def run_test(sh, csv, expected_output_f, debug):
    logger.info(f'{expected_output_f[:-4]}: ')
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
    else:
        click.echo(click.style('FAIL', fg='red') + '\n\t| ')
        output = db.bash_diff(stdout, expected_output_f, cmd) if debug else db.py_differ(stdout, expected_output)
        print(output)


@main_group.command(help='Shows all available directories for test')
def directory():
    print('\n'.join(hp.get_directories()))


if __name__ == '__main__':
    main_group()
