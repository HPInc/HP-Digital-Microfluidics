# Setup

    dnf install python3-antlr4-runtime python3-aiohttp python3-pyserial

    aiohttp, requests

# Run

    cd thylacine/mpam
    export PYTHONPATH=`pwd`/src:`pwd`/tools:`pwd`/target/generated-sources/antlr4
    python3 tools/wombat.py display-only --min-time 1day --macro-file inputs/macros.dmf

## pcr

    python3 tools/pcr.py cs 5 --clock-speed=100ms --shuttles=2 --cycles=2 --pipettor-speed=2 --min-time=1hr
    python3 tools/pcr.py cs 25 --clock-speed=500ms --shuttles=2 --cycles=2 --pipettor-speed=2 --min-time=1hr --update-interval=1000ms
    python3 tools/pcr.py cs 25 --clock-speed=500ms --shuttles=2 --cycles=2 --pipettor-speed=2 --min-time=1hr --update-interval=100ms --no-display

## joey

    python tools/joey.py path --clock-speed=500ms --start-pad 0 18 --path 2R3D2R1U
    python tools/joey.py test --clock-speed=500ms

# Class Hierarchy

## engine.py

    ClockRequest = [Ticks,ClockCallback]

    DevCommRequest = Callable[[], Iterable[Updatable]]
    ClockCommRequest = [Ticks,DevCommRequest]

    Engine
      [before,after]_tick(Sequence[ClockRequest])
      on_tick(Sequence[ClockCommRequest])

## device.py

    SystemComponent
      [before,after]_tick(ClockCallback, Optional[DelayType])
      on_tick(Callable[[], Optional[Callback]], Ticks)

    Batch
      [before,on,after]_tick(Sequence[ClockRequest])

    System
      [before,after]_tick(ClockCallback, DelayType)
      on_tick(DevCommRequest, DelayType)
        [Batch,Engine].on_tick
