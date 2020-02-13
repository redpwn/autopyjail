#!/usr/bin/env python3

import subprocess

if __name__ == '__main__':
    while True:
        data = input('>>> ')

        print(repr(eval(data)))
