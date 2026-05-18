#!/usr/bin/python3
import argparse
import os
import sys
from pathlib import Path

from pwn import context

from saeg import BANNER, FLAG, FLAG_FILE_NAMES, local_aeg
from testset import FAIL_MAX


EXTRA_TESTS = {
    'ZONG_HENG_CUP_TEST_SET': {
        'path': 'assets/extra_dataset/zonghengcup/',
        'task': {
            'pwn1': FAIL_MAX,
        },
        'libc': 'libc-2.31-x86.so',
        'ld': 'ld-2.31-x86.so',
        'sig': ['libc6_2.23-0ubuntu10_i386.sig'],
        'concurrent': {
            'pwn1': -1,
        },
    },

    'WANG_DING_CUP_TEST_SET': {
        'path': 'assets/extra_dataset/wangdingcup2023/',
        'task': {
            'bin-1': FAIL_MAX,
            'bin-2': FAIL_MAX,
            'bin-4': FAIL_MAX,
            'bin-5': FAIL_MAX,
            'bin-6': FAIL_MAX,
            'bin-10': FAIL_MAX,
        },
        'static': ['bin-1', 'bin-2', 'bin-5', 'bin-6'],
        'sig': ['libc6_2.23-0ubuntu7_i386.sig', 'extra_dataset/extra.sig']
    },

    'ZERATOOL_TEST_SET': {
        'path': 'assets/extra_dataset/zeratool_challenges/',
        'task': {
            'bof1': FAIL_MAX,
            'bof2': FAIL_MAX,
            'bof3': FAIL_MAX,
            'heap0': FAIL_MAX,
            'ret': FAIL_MAX,
        }
    },
}


def chmod_x(path):
    os.chmod(path, os.stat(path).st_mode | 0o111)


def chmod_x_children(path):
    for child in path.glob('*'):
        if child.is_file():
            chmod_x(child)


def write_flags():
    for flag_name in FLAG_FILE_NAMES:
        Path(flag_name).write_text(FLAG)


def clean_flags():
    for flag_name in FLAG_FILE_NAMES:
        Path(flag_name).unlink(missing_ok=True)


def asset_path(root, asset_name):
    return str(root / 'assets' / asset_name)


def task_concurrent(test_set, task_name, concurrent):
    if concurrent is not None:
        return concurrent
    concurrent_setting = test_set.get('concurrent', 1)
    if isinstance(concurrent_setting, dict):
        return concurrent_setting.get(task_name, 1)
    return concurrent_setting


def run_extra_tests(timeout, debug, concurrent):
    context.log_level = 'error'
    root = Path.cwd().resolve()
    result = BANNER

    chmod_x_children(root / 'assets')
    for test_set_name, test_set in EXTRA_TESTS.items():
        result += f"Testing {test_set_name} in {test_set['path']}\n"
        failed = 0
        failed_str = ''
        test_timeout = int(test_set.get('timeout', timeout))
        test_path = root / test_set['path']
        chmod_x_children(test_path)

        for task_name, baseline_time in test_set['task'].items():
            to_test = str(test_path / task_name)
            print(f"Testing {to_test}")
            flirt = [asset_path(root, i) for i in test_set.get('sig')] if 'sig' in test_set else None
            libc = asset_path(root, test_set.get('libc')) if 'libc' in test_set else None
            ld = asset_path(root, test_set.get('ld')) if 'ld' in test_set else None
            if 'static' in test_set and task_name in test_set['static']:
                ld = None
            active_size = task_concurrent(test_set, task_name, concurrent)

            res, cost = local_aeg(to_test, flirt, libc, ld, test_timeout, debug, concurrent=active_size)
            for _ in range(5):
                if (not res and cost < 100) or cost > baseline_time:
                    res, cost = local_aeg(to_test, flirt, libc, ld, test_timeout, debug, concurrent=active_size)

            if res:
                if baseline_time != FAIL_MAX:
                    result += f"Passed, cost {str(cost)[:4]}s,\tbaseline " \
                              f"{str(baseline_time).rjust(5, ' ')}s" \
                              f",\t{'Diff'} {str(baseline_time - cost)[:5]}s" \
                              f",\t Ratio {str(baseline_time / cost)[:5]}x\tat {task_name}\n"
                else:
                    result += f"Passed, cost {str(cost)[:4]}s,\tat {task_name}\n"
            else:
                failed_str += f"Test {task_name} failed\n"
                failed += 1

        result += failed_str
        result += f"Total {len(test_set['task'])} tests, {f'{failed} failed' if failed else 'all passed'}\n"
        result += BANNER

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', '--timeout', help='timeout', default=300, type=int)
    parser.add_argument('-D', '--debug', help='debug', default=False, action='store_true')
    parser.add_argument('-c', '--concurrent', help='maximum concurrent active sim', default=None, type=int)
    args = parser.parse_args()

    try:
        sys.set_int_max_str_digits(0x9999)
    except AttributeError:
        pass

    write_flags()
    try:
        output = run_extra_tests(args.timeout, args.debug, args.concurrent)
        print(output)
        if Path('/test_res').is_dir():
            Path('/test_res/extra_test_result.txt').write_text(output)
    finally:
        clean_flags()
