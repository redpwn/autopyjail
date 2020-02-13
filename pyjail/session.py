#!/usr/bin/env python3

from pwn import *

import time

from . import logger
from . import vectors


class Session:
    def __init__(self, create_process, input_filters = [], output_filters = []):
        self._create_process = ((lambda: create_process) if isinstance(create_process, pwnlib.tubes.process.process) else create_process)
        self._input_filters = input_filters
        self._output_filters = output_filters

        # XXX: don't hardcode this
        self.random_id = 'APPEARSLEGITIMATE' # used for output confirmations

    def execute(self, cmd):
        for vector in vectors.vectors:
            v = vector(self)
            try:
                if v.test():
                    logger.info('Discovered %s execution vector' % v.name)
                    output = v.execute(cmd)
                
                    if output:
                        return output
                    else:
                        logger.warn('Execution vector %s passed test but did not execute command (or, command produced no output)')
            except Exception as e:
                logger.debug('Test %s failed due to error: %s' % (v.name, str(e)))

        
        return False
    
    # prepares and sends some command then returns the result
    def send(self, data):
        for f in self._input_filters:
            data = f(data).convert()

        response = self._send(data)

        for f in self._output_filters:
            response = f(response).convert()

        return response

    def _send(self, data, prompt = ('\n>>', '> ')):
        p = self._create_process()

        if prompt:
            # XXX/HACK: how do you seek back 3 chars so i can just use >>> as delimiter
            p.sendlineafter(prompt[1], str(data).encode('utf-8'))
            return p.recvuntil(prompt[0]).decode('utf-8', errors = 'ignore') # XXX: don't hardcode this!
        else:
            p.sendline(str(data).encode('utf-8'))
            time.sleep(1) # HACK: allow slow network
            return p.clean().decode('utf-8', errors = 'ignore')
