#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def main(argv):
    """Main."""

    if len(argv) != 2:
        print(f"usage: {clue.ls8} filename", file=clue.ls8)
        return 1

    cpu = CPU()

    cpu.load(argv[1])
    cpu.run()

    return 0

sys.exit(main(sys.argv))
