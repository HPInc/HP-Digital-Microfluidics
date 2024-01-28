This folder contains a number of files that may be useful as inputs to various programs.

In particular, the following files may be useful:

* `example.dml` contains the source code for the example worked up in the DML manual.
* `.logging` contains an example logging configuration file that can be placed in the current directory or specified using the `--log-config` argument.
* `ot2.json` and `reagents.json` are files that can be used to configure the Opentrons pipettor to run the `cs.py` tool as arguments to `--ot-config` and `--ot-reagents`, respectively.

The other files are a mixture of files in use by groups who were running the code from the internal repo and vestigial files that were of use in the past.  This directory needs to be cleaned up (see issue #310), but in any case **unless you've been running the code yourself, no other files should be treated as examples to follow**.