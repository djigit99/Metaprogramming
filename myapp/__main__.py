from .controller import Controller
from os.path import isfile, isdir, dirname
import argparse

class Flags(object):
    pass

parser = argparse.ArgumentParser(description='PHP Documentation Generator')
parser.add_argument("p", type=str, help="Path to directory or file being documented")
parser.add_argument("-t", required=False, type=str, help="Path to directory where to store documentation files(default: current directory)")
parser.add_argument("-r", required=False, action='store_true', help="recursive mode")
args = parser.parse_args(namespace=Flags)

if isfile(Flags.p):
    if not Flags.t:
        Flags.t = dirname(Flags.p)
    elif not isdir(Flags.t):
        print('target directory not found, please enter the correct path')
        exit(1)
    else:
        pass
    Controller(Flags.p, Flags.t)
elif isdir(Flags.p):
    if not Flags.t:
        Flags.t = Flags.p
    elif not isdir(Flags.t):
        print('target directory not found, please enter the correct path')
        exit(1)
    else:
        pass
    if Flags.r:
        Controller(Flags.p, Flags.t, True, True)
    else:
        Controller(Flags.p, Flags.t, True)
else:
    print('file or directory not found, please enter the correct path')
    exit(1)
