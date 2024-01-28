# HP Digital Microfluidics Software Platform and Language

## OVERVIEW

This repository contains the **HP Digital Microfluidics Software Platform** and an interpreter for the **Digital Microfluidics Language (DML)**.  Together, these two components assist in the developmental testing and interactive use of DMF boards as well as the development and running of protocols for these boards, both in simulation and on actual hardware.

The platform is a Python 3 package (`dmf`) which can simulate and/or drive DMF boards with arbitrary size, well configuration, and pipettor targets (e.g., lid holes), and which have available controllable internal or external components such as magnets, sensors, heaters/chillers, power supplies, and fans.  The repository contains board models for the [`opendrop`](https://www.gaudi.ch/OpenDrop/) board as well as for several versions of the “`Joey`” platform being developed at Hewlett-Packard[^joey].

[^joey]: The full `Joey` board is available in simulation, and the `Wombat` version drives a portion of the `Joey` board using an `Opendrop` controller.  Other included configurations (`Bilby`, `hybrid`) require middleware software not included in this repository.

The platform models/drives fluid transfer to and from the board by means of pipettors, and it includes a `manual` pipettor which prompts a user to perform the transfer and a `simulated` pipettor for use in protocol development and simulation.  There is also a pipettor model for driving the [Opentrons OT-2 pipetting robot](https://opentrons.com/products/robots/ot-2/).

The platform also contains a [graphical user interface](assets/gui-example.jpg) that allows both interactive manipulation of the board (by clicking the mouse to modify cell state and control the clock as well as by typing DML statements) and visualization of running protocols, including cell states, drop size and composition, well contents, heater temperatures and directions, and magnet states.

The platform supports defining protocols in two ways:

1. Simple (and even reasonably complex) protocols can be written using the domain-friendly [DML language](<doc/Introduction to DML.pdf>).  Protocols (and other functions and actions) can be preloaded into the `interactive` tool by using the `--dml-file` command-line argument and then executed by typing their names (and any associated parameters) into the `Expr:` box in the GUI.

2. More complicated protocols, including features of the platform not (yet) available in DML (e.g., n-way mixes and n-times dilutions, multi-zone thermocycling, and sophisticated drop traffic control) can be written in Python by creating a subclass of the `dmf.Task` class.  See [`tools/support/pcr.py`](tools/support/pcr.py) for several examples of Python-implemented protocols and [`tools/interactive.py`](tools/interactive.py) for a model for creating a command-line program to drive such a protocol.

## INSTALLATION

Once the repository has been cloned,

1. Ensure that you are running Python version **3.10**.  As of this writing, the code has been tested with version `3.10.9`.  Later versions might work; earlier ones may well not.

2. Install required packages by running
   ```
   pip -r requirements.txt
   ```

3. Ensure that the following subdirectories of the repository root directory are on your `PYTHONPATH` variable:

   * `src`
   * `tools`
   * `stubs`
   * `target/generated-sources/antlr4`

## RUNNING

To run `tools/interactive.py` (or any protocol-specific Python script), simply run it using a Python 3 interpreter.  Follow the script name by the name of the board model and any board- or protocol-specific command line arguments.  For example,

```
python3 tools/interactive.py joey --clock-speed=100ms --dml-dir inputs --dml-file my-protocol.dml --hole 6,4
```

specifies that the tool should 

1. use the `joey` model,
2. set the initial clock speed to 100 ms per clock tick,
3. search for DML files in the `inputs` folder,
4. pre-load the `my-protocol.dml` DML file, which will likely include functions and actions that define the protocol, and
5. tell the system that the board being used has a pre-drilled pipetting hole above the cell at `(6,4)` (i.e., the sixth column in the fourth row).


The DMF platform has a large number of command-line options.  A complete list, with explanations and default values, can be obtained by specifying `--help` after the board name.  To obtain a list of available board models, specify `--help` following the script name, before any further arguments.

## DEVELOPING

To develop (rather than simply use) the platform, a bit more will be required.  A full set of extra Python packages required to do any of these tasks can be installed by running

```
pip -r dev-install.txt
```
Tools for many of these tasks can be found in the `dev-tools` directory, which should be added to `PYTHONPATH`.

### DML Grammar

The grammar for the DML language can be found in the [`grammar`](grammar) directory.  The parser ([`dml.g4`](grammar/dml.g4)) and lexer ([`commonLexer.g4`](grammar/commonLexer.g4)) are written in [ANTLR4](https://www.antlr.org/).  

If you modify the grammar, you will need a copy of ANTLR.  The current code was compiled using version 4.9.2.  You should configure the ANTLR tool to emit code to `target/generated-sources/antlr4` and should check in any changed emitted files.  The Python code implementing the language is in [`src/lang`](src/lang).

### Board and Component Models

The intention was/is that new board and component (e.g., pipettor or sensor) models would be described in a declarative **Board Description Language** and no Python expertise would be needed beyond perhaps writing glue code to talk to the actual hardware.

That, unfortunately, is not there yet, so the best advice is probably to look at existing models like the [`joey`](src/devices/joey.py) board model, the [simulated](src/devices/dummy_pipettor.py) pipettor model, and the [`eselog`](src/devices/eselog.py) sensor model.  All of these (and more) are in the `devices` package in the [`src/devices`](src/devices) directory.


### API Documentation

Some of the code contains documentation comments that contain [Sphinx](https://www.sphinx-doc.org/en/master/)-based markup that can be extracted as web-based API documentation.[^apidoc]  This documentation can be extracted by running `dev-tools/build_doc.py` from within the `api-doc` directory.

[^apidoc]: An unfortunately small portion of it.  Even worse, much of it is severely out of date and should certainly not be trusted at this point.

### Mixing and Dilution Sequences

Optimal multi-drop mixing and dilution sequences can be found by running `mix_ga_placed.py` and `dilution_ga_placed.py`, both found in the `dev-tools` directory.  These take as command-line arguments, respectively, the number of drops to mix, e.g.,

```
python3 mix_ga_placed.py 7
```

to get an even mixture of seven drops, and the “fold” of the dilution, e.g.,

```
python3 dilution_ga_place.py 1.2
```

to get a 1.2x (that is, 5:4) dilution.

These scripts use a genetic algorithm to evolve the solutions, and the many parameters controlling the process can be found by adding `--help`.  The only one likely to be of use is `--full`, which tells the system to look for a solution in which all of the drops are fully mixed or diluted.  Without this, the solution will have only a single drop fully mixed or diluted.

The final emitted result should be added to `src/dmf/mixing.py` or `src/dmf/dilution.py`.[^mixes]

[^mixes]: As of this writing these files contain single-drop and full mixes for up to twelve drops and dilution sequences for 2x through 12x (including 2.5x, 3.5x, 4.5x, and 5.5x), as well as 15x, 16x, 20x, 25x, 32x, 50x, and 100x.

### Linking to C++ Code

For some board models, you may need to interface with C++ code in order to communicate with the board.  For the `bilby` model, we used [`pybind`](https://pybind11.readthedocs.io/) to wrap the C++ code.  The `dev-tools/pylider_stubs.py` tool (based on the `pybind11-stubgen` package) can be used to automatically generate stub files and put them in the `stubs` directory.  As always, use the `--help` argument to get a listing of the available command-line arguments.  In particular, this script was developed to generate stubs for a module named `pyglider`, but the `--module` argument can be used to replace this by the name of your module.

## A Note on Issues in the Repo

When the decision was made to open-source this codebase, it was also decided that the internal issues list should also be brought over, as the open issues contain ideas about a number of planned improvements (including thoughts on implementation)[^branches]  Unfortunately, GitHub makes it ***really*** difficult to copy issues and comments from a repo on one server to one on another.  If all has gone well, we've managed to approximate it so that all issues on the public repository have the same numbers they had on the internal repository.  There are, however, the following things to bear in mind:

[^branches]: For the same reason, the entire commit history of the repo was copied over, as there were unfinished branches working on several of these issues.  Issue-related branches are named `issue.NNN` (with leading zeroes) for issue `NNN`.

* All issues and comments show up as having been added by @EvanKirshenbaum in late January, 2024.
   * Each has a note at the end identifying the original poster and date
* Commits that reference the issues don't show up on the commit page.
   * Instead, there is an extra (first) comment that lists the commits and their commit dates.
* Comments that refer to issues with higher numbers correctly link to those issues, but there's no "mention" indication in the timeline of the target issue, so you'll have to search to see if anybody mentioned an issue.
* There are references to internal codenames and early names for this project and related ones.
   * In particular, "Thylacine" and "MPAM" both refer to this codebase, and "the macro language" is what's now called DML.