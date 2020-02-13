#!/usr/bin/env python3

# ' => \', \ => \\, \n => \n
def sanitize_python_apostrophe(cmd):
    return cmd.replace('\\', '\\\\').replace('\'', '\\\'').replace('\n', '\\n')
