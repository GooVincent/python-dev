from enum import IntEnum
import cv2
import numpy as np
import inspect


class TestEnum(IntEnum):
    FIRST = 0
    SEC = 1


class TestClass:
    userId: int
    taskId: int


def test_run_yeild():
    yield 1
    for i in range(5):
        yield i, 3


def run():
    data = np.random.randn(1, 3, 512, 384).astype(np.float32)
    print(f'{data.shape, data.dtype, type(data.dtype)}')
    
    data = cv2.normalize(data, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)
    print(f'{data.shape, data.dtype, type(data.dtype), cv2.NORM_MINMAX}')
    
    # data = data.astype(np.float32) / info.max # normalize the data to 0 - 1
    # data = 255 * data # Now scale by 255
    # img = data.astype(np.uint8)
    
    if np.dtype(np.float32).type == data.dtype:
        print(f"llllll")
    
    if isinstance(None, np.ndarray):
        print(f"fffff")


def test_assert():
    try:
        assert 1 == 0
        msg = "ok"
    except Exception:
        msg = 'no ok'
    finally:
        return msg


def get_class_members(class_type) -> list:
    """get_class_members
        get all members in a class. im my test python3.8 works
    """
    import inspect

    members = inspect.getmembers(class_type, lambda a:not(inspect.isroutine(a)))
    for k, v in members:
        if "__annotations__" in k:
            return list(v.keys())

    return []

if __name__ == '__main__':    
    
    foo = test_run_yeild()
    first_ele = foo.__next__()
    sp1, sp2 = zip(*foo)
    print(f"{first_ele, sp1, sp2}")
