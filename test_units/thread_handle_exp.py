"""Ensure the exception will cause thread or process exist if not catch the exception
"""

import time
from threading import Thread
from multiprocessing import Process


class ThreadRaiseExp(Thread):
    def __init__(self):
        super(ThreadRaiseExp, self).__init__()

    def run(self):
        while True:
            time.sleep(2)
            print(var_not_exist)  # it should raise an exception


class ProcessRaiseExp(Process):
    def __init__(self):
        super(ProcessRaiseExp, self).__init__()

    def run(self):
        while True:
            time.sleep(2)
            print(var_not_exist)  # it should raise an exception


def test_thread():
    t = ThreadRaiseExp()
    t.start()


def test_process():
    p = ProcessRaiseExp()
    p.start()


if __name__ == '__main__':
    # test_thread()
    test_process()
    time.sleep(30)
    print(f'main process exit...')

