#!/usr/bin/env python3

from pyjail import *
from pwn import *


context.log_level = 'DEBUG'

if __name__ == '__main__':
    p = lambda: process('./fakepython')
    pj = session.Session(p())

    output = pj.execute('id')

    print('Command `id` produced output:\n' + str(output))
