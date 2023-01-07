from __future__ import annotations
from argparse import ArgumentParser, Namespace

parser = ArgumentParser()
parser.add_argument("--foo", action='append', type=int, default=[])
args: Namespace = parser.parse_args()

print(args)