# Thylacine
_Thylacine_ is (or, at least, will be, if all goes well) a suite of software for Digital Microfluidics (DMF) platforms.  It is envisioned as containing several pieces:

- __MPDL__, the _Microfluidics Platform Description Language_, is a language for describing and characterizing specific DMF platforms.

- __MPAM__, the _Microfluidics Platform Abstract Machine_, is a low-level model (and associated language) for operations to be performed on DMF platforms characterizable by MPDL.

- __MRL__, the _Microfluidics Recipe Language_, is an intermediate-level programming language for specifying DMF recipes independent of a particular DMF platform.

- __MPSL__, the _Microfluidics Protocol Specification Language_, is a high-level (e.g., near-natural-language) specification language for specifying microfluidics protocols close to the way they are described in the literature, with little or no programming expertise required

- An __MPAM API__ allows MPAM operations to be initiated from programming languages such as Java, C++, and/or Python

- An __MPAM emulator__, likely graphical, implements the MPAM API and can emulate DMF platforms specified by MPDL descriptions.

- An __MPAM interpreter__ reads an MPAM program and executes it by making calls to the MPAM API

- An __MPAM assembler__ converts MPAM programs to equivalent programs in other programming languages

- An __MRL__ compiler takes as input an MPDL description and one or more MRL recipes and outputs an MPAM program that impelemnts the recipes for the platform

- An __MPSL__ compiler takes as input an MPSL specification and translates it into an MRL recipe (and, optionally, from there to an MPAM program).

There will also be MPDL descriptions and MPAM API implementation libraries for various concrete DMF platforms

## Developer Notes

### QuickStart

    cd thylacine/mpam
    export PYTHONPATH=`pwd`/src:`pwd`/tools:`pwd`/target/generated-sources/antlr4

    python tools/wombat.py display-only --min-time 1day --macro-file inputs/macros.dmf

    python tools/joey.py path --clock-speed=500ms --start-pad 0 18 --path 2R3D2R1U

    python tools/pcr.py cs 5 --clock-speed=100ms --shuttles=2 --cycles=2 --pipettor-speed=2 --min-time=1hr

### MyPy

    cd thylacine/mpam
    mypy --ignore-missing-imports --warn-redundant-casts --warn-return-any --warn-unreachable --strict-equality src tools
