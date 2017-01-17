#!/usr/bin/env python

import os
import sys


def main():
    """
    Main function to check for locked files
    """

    assert len(sys.argv) == 2, 'Less or more parameters provided as needed'

    dir_path = sys.argv[1]

    assert os.path.isdir(dir_path), ('Provided parameter {} '
                                     'is not a dir.'.format(dir_path))

    locks = get_locks()
    stack = [dir_path]
    while stack:
        dir_path = stack.pop()
        stack += check_dir(dir_path, locks)


def get_locks():
    """
    Function to get the /proc/locks INODE, PID information
    and saves it in a dictionary
    """
    locks = {}
    locks_path = '/proc/locks'
    assert os.path.isfile(locks_path) is True, ('File {} is not a file '
                                                'or does not exist.'.format
                                                (locks_path))
    with open(locks_path, 'r') as f:
        for line in f:
            str_pid = line.split(' ')[6]
            assert str_pid.isdigit() is True, ('PID: {} in line {} of {} '
                                               'is not a digit'.format
                                               (str_pid, line, locks_path))

            file_pid = int(str_pid)
            str_inode = line.split(' ')[7].split(':')[2]
            assert str_inode.isdigit() is True, ('Inode: {} in line {} of {} '
                                                 'is not a digit'.format
                                                 (str_inode, line, locks_path))

            file_inode = int(str_inode)
            locks[file_inode] = file_pid
    return locks


def check_file(file, locks):
    """
    Prints the INODE, PIDs and PATHS of locked files
    """
    try:
        file_inode = os.stat(file).st_ino

        assert type(file_inode) is int, 'Inode is not an integer'

        if file_inode in locks:
            print('File {} is locked and runs with PID {}'.format(
                file, locks[file_inode]))

    except OSError as err:
        print('OSError for {}: {}'.format(file, err))


def check_dir(dir_path, locks):
    """
    Checks for all locked files beneath the given directory and returns
    list of subdirectories
    """
    dirs = []
    try:
        for f in os.listdir(dir_path):
            item_path = os.path.join(dir_path, f)
            if not os.path.islink(item_path):
                if os.path.isdir(item_path):
                    dirs.append(item_path)
                else:
                    check_file(item_path, locks)

    except OSError as err:
        print('OSError for {}: {}'.format(file, err))

    return dirs


if __name__ == "__main__":
    main()
