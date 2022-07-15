from time import perf_counter
import argparse
import os
import asyncio
from fnutils import async_is_match
from typing import Optional


async def produce(filepath: str, q: asyncio.Queue) -> None:
    """
    This function returns a list of files from a given path
    """
    await find_files_from_dir([filepath], q)


async def consume(regex: str, q: asyncio.Queue) -> None:
    """
    Validate that the given files matches with regex
    """
    while True:
        file = await q.get()
        is_match = await async_is_match(regex, file)
        if is_match:
            print(file)
        q.task_done()


async def find_files_from_dir(dir: list, q: asyncio.Queue) -> None:
    """
    Search recursively for the files in a directory
    """
    if len(dir) <= 1:
        filename = dir[0]
        if not os.path.isdir(filename):
            await q.put(filename)
        else:
            dir_files = [
                os.path.join(filename, directory) for directory in os.listdir(filename)
            ]
            await find_files_from_dir(dir_files, q)
    else:
        mid = len(dir) // 2
        first_half = dir[:mid]
        second_half = dir[mid:]
        await find_files_from_dir(first_half, q)
        await find_files_from_dir(second_half, q)


async def main(path: str, regex: str, ncon: Optional[int]):
    t1_start = perf_counter()
    q = asyncio.Queue()
    files_with_path_list = [os.path.join(
        path, directory) for directory in os.listdir(path)]
    producers = [asyncio.create_task(produce(file, q))
                 for file in files_with_path_list]
    consumers = [asyncio.create_task(consume(regex, q)) for __ in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()
    t1_stop = perf_counter()
    elapsed_time = t1_stop-t1_start
    print("Elapsed time was: ", elapsed_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("regex", help="Regular expression to be compared")
    parser.add_argument("path", help="Path to be compared")
    parser.add_argument("ncon", help="Number of consumers", type=int)
    args = parser.parse_args()
    asyncio.run(main(**args.__dict__))
