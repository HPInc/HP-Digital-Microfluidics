from __future__ import annotations
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--test", help="first test")
parser.add_argument("--test", help="second test")
ns = parser.parse_args()
print(ns)
