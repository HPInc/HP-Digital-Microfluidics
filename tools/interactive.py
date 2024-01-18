from __future__ import annotations

from argparse import Namespace

from devices import joey, opendrop, wombat, opentrons, manual_pipettor, \
    bilby_task, eselog, bilby_yaminon_task
from dmf import pipettor
from dmf.device import Board, System
from dmf.exerciser import PlatformChoiceExerciser, Task
from dmf.monitor import Config as monConfig
from lang import dml


class DisplayOnly(Task):
    def __init__(self) -> None:
        super().__init__(name="display-only",
                         description = "Just bring up the display.")
        pass

        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        # Nothing to do as a task.  We will set min_time to None, so the board
        # will stay up until the user is done with it.
        pass

if __name__ == '__main__':
    platforms = (
                bilby_task.PlatformTask,
                joey.PlatformTask,
                opendrop.PlatformTask,
                wombat.PlatformTask,
                wombat.YaminonPlatformTask,
                bilby_yaminon_task.PlatformTask,
                )
    pipettors = (opentrons.PipettorConfig,)
    components = (eselog.ESELogConfig,)
    default_pipettor = manual_pipettor.PipettorConfig
    # exerciser = InteractiveExerciser(platforms=platforms, pipettors=pipettors)
    monConfig.min_time.default = None
    exerciser = PlatformChoiceExerciser.for_task(DisplayOnly, 
                                                 "Interact with a DMF board",
                                                 platforms=platforms,
                                                 pipettors=pipettors,
                                                 components=components,
                                                 default_pipettor=default_pipettor)
    pipettor.Config.value_formatter(dml.Type.default_formatter)
    exerciser.parse_args_and_run()