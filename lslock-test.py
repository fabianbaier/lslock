#!/usr/bin/env python

import fcntl
import multiprocessing
import os
import sys
import time


def main():
    """
    Main function to create locked files for test purposes of lslock.py
    """
    assert len(sys.argv) == 2, 'Less or more parameters provided as needed'

    path = "/tmp/lslock-test"

    assert os.path.isdir(path), 'Test path {} does not exist!'.format(path)

    print('Testpath {} exists.'.format(path))
    raw_wait = sys.argv[1]
    assert raw_wait.isdigit() is True, ('Input {} is not a digit'.format(
                                        raw_wait))

    wait = int(sys.argv[1])
    assert wait < 60, 'Please choose a lower wait time value'

    stack = [path]
    while stack:
        path = stack.pop()
        stack += check_dir(path, wait)


def lock_file(file, wait):
    """
    Locks the file in /tmp/lslock-test and subdirectories
    """
    print('Process with PID {} trying to lock {}...'.format(os.getpid(), file))
    f = open(file, "r")
    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        print('File {} locked successfully for {} seconds.'.format(file, wait))
        time.sleep(wait)
    except OSError as err:
        print('Could not lock {}: {}'.format(file, err))


def check_dir(dir_path, wait):
    """
    Lock all files beneath a directory and filter symbolic links to avoid loops
    """
    dirs = []
    try:
        for f in os.listdir(dir_path):
            item_path = os.path.join(dir_path, f)
            if not os.path.islink(item_path):
                if os.path.isdir(item_path):
                    dirs.append(item_path)
                else:
                    p = multiprocessing.Process(target=lock_file,
                                                args=(item_path, wait))
                    p.start()

    except OSError as e:
        pass

    return dirs


if __name__ == "__main__":
    main()
