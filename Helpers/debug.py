import os
import difflib
import subprocess


def py_differ(stdout, expected_output):
    differ = difflib.Differ()
    lines = list()
    ret = list()
    for output in [stdout, expected_output]:
        arr = ([line for line in output.split('\n')])
        arr.sort()
        lines.append(arr)
    for line in differ.compare(lines[0], lines[1]):
        if line[0] == '+':
            ret.append(f'\t| expected: {line[1:]}\n\t| ')
        elif line[0] == '-':
            ret.append(f'\t| your out: {line[1:]}')
    return '\n'.join(ret)


def bash_diff(stdout, expected_output_f, cmd):
    path = os.path.dirname(os.path.abspath(__file__))
    with open('tmp.txt', "w") as f:
        f.write(cmd + '\n' + stdout)
    response = subprocess.Popen(f'diff {path}/{expected_output_f} {path}/tmp.txt', stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8', shell=True)
    stdout, _ = response.communicate()
    return stdout
