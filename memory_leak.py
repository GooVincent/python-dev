import tracemalloc
import os


class MyObject:
    def __init__(self):
        self.data = os.urandom(100)


def get_data():
    values = []
    for _ in range(100):
        obj = MyObject()
        values.append(obj)
    return values


class WasteMemory:
    @classmethod
    def run(cls):
        deep_values = []
        for _ in range(100):
            deep_values.append(get_data())
            return deep_values


tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()

x = WasteMemory().run()
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'traceback')
top = stats[0]

print('Biggest offender is:')
print('\n'.join(top.traceback.format ()))