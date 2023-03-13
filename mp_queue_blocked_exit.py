""" Test multiptocess.Queue blocked the process exit.

"""
import time
import multiprocessing as mp
from multiprocessing import Process, Queue
from threading import Thread
import numpy as np

def run(q):
    print('put start')
    print(f'sub process {type(q)}, {q.qsize()}, {q}')
    
    test_size = 4*1024  # test_size bigger like 1024*1024, it will blocked the process exit
    arg = np.zeros((1, test_size)).astype(np.uint8)
    q.put(arg)
    
    print('put done')
    time.sleep(1.0)
    print(f'run exit, {q.qsize()}')


def run_forever():
    start = time.time()
    while True:
        time.sleep(1)
        if time.time() >= start + 3:
            break


def main():
    mp.set_start_method('spawn')
    # ctx = mp.get_context('spawn')
    # q = ctx.Queue()
    # p = ctx.Process(target=run, args=(q,))

    q = Queue()
    p = Process(target=run, args=((q),))
    t = Thread(target=run_forever)

    print(f'init {type(q)}, {q.qsize()}, {q}')

    t.start()
    p.start()

    # q.get()
    p.join()
    print('sub process join done')

    t.join()
    print('main process exit')


if __name__ == "__main__":
    main()
