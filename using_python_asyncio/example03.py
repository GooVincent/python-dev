import time
import asyncio

async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')

def blocking():
    time.sleep(.5)
    print(f"{time.ctime()} Hello from a thread!")

loop = asyncio.get_event_loop()
task = loop.create_task(main())
print('1')
loop.run_in_executor(None, blocking)
print('2')
loop.run_until_complete(task)
print('3')
pending = asyncio.all_tasks(loop=loop)
print('4')

for task in pending:
    print('5')
    task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
print('6')
loop.run_until_complete(group)
print('7')
loop.close()
print('8')
