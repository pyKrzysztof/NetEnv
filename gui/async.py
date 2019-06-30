import asyncio
import time


async def say_after(delay, sentence):
    await asyncio.sleep(delay)
    print(sentence)

async def tasked_main():
    print(f'started at {time.strftime("%X")}')
    task1 = asyncio.create_task(say_after(1, 'yes,'))
    task2 = asyncio.create_task(say_after(2, 'also no.'))
    await task1 # does that,
    await task2 # while also doing that,
    print(f'ended at {time.strftime("%X")}') # for a total of 2 seconds.

async def straightforward_main():
    print(f'started at {time.strftime("%X")}')
    await say_after(1, 'yes,') # does that, 
    await say_after(2, 'also no.') # then starts doing that, 
    print(f'ended at {time.strftime("%X")}') # for a total of 3 seconds.

async def simple_call():
    say_after(1, 'will not show, at all!') # this would never run, as was never awaited.
    await say_after(1, 'this will show, because it was awaited.')


if __name__ == "__main__":
    func = tasked_main
    asyncio.run(func())
    # func()