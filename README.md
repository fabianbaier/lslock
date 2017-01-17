# LSLOCK #

Lslock.py is a program, that accepts a directory argument and prints the PIDs and paths of all files locked beneath it. Write a test program, lslock-test, that launches a few background processes to lock files in the directory /tmp/lslock-test and verifies that your lslock does indeed find all the locks. If more than one process holds a lock on the same file — for example, a parent and one of its children — it is okay to list the lock multiple times.

### Syntax ###

lslock accepts a path on the filesystem and checks if any file beneath it contains a lock. If so, it will print PIDs and PATHs to stdout accordingly. The syntax looks like this:

`python lslock.py /path/to/be/checked`

### Short Example ###
`fa@bi:~# python lslock.py /tmp/lslock-test`
#### Output ####
`File /tmp/lslock-test/me is locked and runs with PID 19654`

### Testing ###

You can test lslock by using this handy test script:

`python lslock-test.py <keep alive time in seconds>`

In order to test successful make sure:

* The fixed directory `/tmp/lslock-test` exists
* In the testing directory `/tmp/lslock-test` you have at least one subfolder with file
* You are using Ubuntu 16.04 or similar with access to /proc/locks

#### Example ####
1) Create tmp files and dirs:

```
mkdir /tmp/lslock-test
touch /tmp/lslock-test/lock1
mkdir /tmp/lslock-test/dir2
touch /tmp/lslock-test/dir2/lock2
mkdir /tmp/lslock-test/dir2/dir4
touch /tmp/lslock-test/dir2/dir4/lock4
mkdir /tmp/lslock-test/dir2/dir3
touch /tmp/lslock-test/dir2/dir3/lock3
mkdir /tmp/lslock-test/dir5
touch /tmp/lslock-test/dir5/lock5
touch /tmp/lslock-test/dir5/lock51
```

2) Run `lslock-test.py` before you check with `lslock.py`: `fa@bi:~# python lslock-test.py 20`

##### Output #####
```
fa@bi:~# python lslock-test.py 30
Testpath /tmp/lslock-test exists.
Process with PID 2945 trying to lock /tmp/lslock-test/lock1...
File /tmp/lslock-test/lock1 locked successfully for 30 seconds.
Process with PID 2946 trying to lock /tmp/lslock-test/dir5/lock5...
File /tmp/lslock-test/dir5/lock5 locked successfully for 30 seconds.
Process with PID 2947 trying to lock /tmp/lslock-test/dir5/lock51...
File /tmp/lslock-test/dir5/lock51 locked successfully for 30 seconds.
Process with PID 2948 trying to lock /tmp/lslock-test/dir2/lock2...
File /tmp/lslock-test/dir2/lock2 locked successfully for 30 seconds.
Process with PID 2949 trying to lock /tmp/lslock-test/dir2/dir4/lock4...
File /tmp/lslock-test/dir2/dir4/lock4 locked successfully for 30 seconds.
Process with PID 2950 trying to lock /tmp/lslock-test/dir2/dir3/lock3...
File /tmp/lslock-test/dir2/dir3/lock3 locked successfully for 30 seconds.
```

3) Run `lslock.py` to see if it actually detects our locked files in the test directory with: `fa@bi:~# python lslock.py /tmp/lslock-test`
```
fa@bi:~# python lslock.py /tmp/lslock-test
File /tmp/lslock-test/lock1 is locked and runs with PID 2945
File /tmp/lslock-test/dir5/lock5 is locked and runs with PID 2946
File /tmp/lslock-test/dir5/lock51 is locked and runs with PID 2947
File /tmp/lslock-test/dir2/lock2 is locked and runs with PID 2948
File /tmp/lslock-test/dir2/dir4/lock4 is locked and runs with PID 2949
File /tmp/lslock-test/dir2/dir3/lock3 is locked and runs with PID 2950
```

### FAQ ###

* os.stat() is working with 'follow_symlinks=False' fine under MacOS but throws error under Ubuntu 16.04 e.g.
* Throwing AssertionError if syntax is wrong or values are not as expected
* Using a stack approach for large data set [`e.g. python lslock.py /`]
* http://ls.pwd.io/2014/08/python-threads-vs-processes/
* https://docs.python.org/3/library/fcntl.html
* https://docs.python.org/3/library/functions.html#open
* http://stackoverflow.com/questions/3474382/how-do-i-run-two-python-loops-concurrently
* https://en.wikipedia.org/wiki/Global_interpreter_lock
* https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python
