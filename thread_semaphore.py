import threading

class MultiThreads:
    def __init__(self):
        self._idle_semaphore = threading.Semaphore(0)


if __name__ == '__main__':
    threads = MultiThreads()

    for _ in range(2):
        count = threads._idle_semaphore.release()
        print(f'release: {count}')

    for _ in range(3):
        count = threads._idle_semaphore.acquire(timeout=0)
        print(f'{count}')

    
