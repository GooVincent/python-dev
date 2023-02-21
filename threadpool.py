import concurrent.futures as cf
from concurrent.futures import ThreadPoolExecutor
import time
import threading
import queue
import os
import _thread
import asyncio
import functools
from concurrent.futures import wait, as_completed

def task1(close_event, queue):
    print(f"task1 pid={os.getpid()}, tpid={threading.get_ident()}")
    while not close_event.is_set():
        time.sleep(1)
        queue.put("hello")


def task2(close_event, queue):
    print(f"task2 pid={os.getpid()}, tpid={threading.get_ident()}")
    while not close_event.is_set():
        time.sleep(2)
        queue.get("hello")


def task_init(close_event, queue):
    print(f"task_init pid={os.getpid()}, tpid={threading.get_ident()}")
    while not close_event.is_set():
        try:
            time.sleep(0.5)
            print("=="*32)
            print(f"current size: {queue.qsize()}")
        except Exception as exp:
            close_event.set()
        finally:
            pass

def task_sleep1():
    print(f'111 test_task {_thread.get_native_id()} run...')
    time.sleep(1)
    print(f'[{time.time()}] 111 test_task {_thread.get_native_id()} done...')
    raise ValueError("Sleep 1 then raise error")

def task_sleep2():
    # status = close_event.is_set()
    print(f'222 test_task {_thread.get_native_id()} run...')
    time.sleep(2)
    print(f'[{time.time()}] 222 test_task {_thread.get_native_id()} done...')

def task_sleep5():
    # status = close_event.is_set()
    # print(f'555 test_task {_thread.get_native_id()} run...')
    time.sleep(1)
    # print(f'[{time.time()}] 555 test_task {_thread.get_native_id()} done...')

def callback(foo, future):
    try:
        print(f"[{foo}] submit result = {future.result()} ")
    except Exception as exp:
        print(f"!!!!!!{exp}")

def run():

    close_event = threading.Event()
    msg_queue = queue.Queue()
    test_queue = queue.Queue()
    print(f"main pid={os.getpid()}, tpid={threading.get_ident()}")

    for i in range(10):
        test_queue.put(i)

    executor = cf.ThreadPoolExecutor(max_workers=2) 
    futures = [executor.submit(task_sleep5) for _ in range(10)]
    while True:
        # if executor._work_queue.qsize() > 0:
        #     print(f"worker should be full, {executor._work_queue.qsize()}")
        #     time.sleep(1)
        # else:
        #     print(f"add add more work now..")
        
        for future in as_completed(futures):
            future.result()
            print(f" work left={executor._work_queue.qsize()}")
        # time.sleep(1)
        break

    executor.shutdown()
    print('main process Done')


if __name__ == '__main__':
    run()
