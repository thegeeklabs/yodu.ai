import json
import os
import threading
from contextlib import suppress

from steem.blockchain import Blockchain


def get_last_line(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            f.seek(-2, 2)
            while f.read(1) != b"\n":
                f.seek(-2, 1)
            return f.readline()


def get_previous_block_num(block):
    if not block:
        return -1

    if type(block) == bytes:
        block = block.decode('utf-8')

    if type(block) == str:
        block = json.loads(block)

    return int(block['previous'][:8], base=16)


def run(filename):
    b = Blockchain()
    # automatically resume from where we left off
    # previous + last + 1
    start_block = get_previous_block_num(get_last_line(filename)) + 2
    if start_block == 1:
        start_block = 66384718
    print("Block Number: " + str(start_block))
    with open(filename, 'a+') as file:
        for block in b.stream_from(start_block=start_block, full_blocks=False, batch_operations=True):
            file.write(json.dumps(block, sort_keys=True) + '\n')


def run_threaded(filename, start_block):
    b = Blockchain()
    with open(filename, 'a+') as file:
        for block in b.stream_from(start_block=start_block, full_blocks=False, batch_operations=True):
            file.write(json.dumps(block, sort_keys=True) + '\n')


if __name__ == '__main__':
    output_file = '/Users/shashank/PycharmProjects/yodu/data/steem.blockchain.json'
    with suppress(KeyboardInterrupt):
        run(output_file)
