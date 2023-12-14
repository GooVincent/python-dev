import time
import random
from functools import wraps

def timer(func):
    """装饰器：打印函数耗时
    """
    @wraps(func)  # wraps可以保留原func的属性
    def decorated(*args, **kwargs):
        st = time.perf_counter()
        ret = func(*args, **kwargs)
        print('{} cost: {} seconds'.format(func.__name__, time.perf_counter() - st))
        return ret

    return decorated


def delayed_start(func=None, *, duration=1):
    """装饰器:在执行被装饰函数前，等待一段时间
        param duration: 需要等待的秒数
    """
    def decorator(_func):
        def wrapper(*args, **kwargs):
            print(f'Wait for {duration} second before starting...')
            time.sleep(duration)
            return _func(*args, **kwargs)
        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


@timer
def sleep_a_while(sleep_time_s):
    time.sleep(sleep_time_s)


def run():
    for _ in range(10):
        sleep_a_while(random.randint(1, 10))


if __name__ == '__main__':
    run()
