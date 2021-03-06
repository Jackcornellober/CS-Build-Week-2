#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def main(args):
    """Main."""

    # if len(argv) != 2:
    #     print(f"usage: {argv[0]} filename", file=sys.stderr)
    #     return 1

    cpu = CPU()
    # print(argv)
    cpu.load('.\\clue.ls8')
    cpu.run()
    return 0

    

if __name__ == "__main__":
    main(['ls8.py', '.\\clue.ls8'])