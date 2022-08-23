from __future__ import annotations

from devices import joey, opendrop, wombat, opentrons, manual_pipettor
from erk.basic import ValOrFn
from mpam.exerciser import PlatformChoiceExerciser, PlatformChoiceTask
from mpam.exerciser_tasks import DisplayOnly


def if_available(name: str) -> ValOrFn[PlatformChoiceTask]:
    ...

if __name__ == '__main__':
    platforms = (
                "devices.bilby.PlatformTask",
                joey.PlatformTask,
                opendrop.PlatformTask,
                wombat.PlatformTask,
                wombat.YaminonPlatformTask,
                )
    pipettors = (opentrons.PipettorConfig,)
    default_pipettor = manual_pipettor.PipettorConfig
    # exerciser = InteractiveExerciser(platforms=platforms, pipettors=pipettors)
    exerciser = PlatformChoiceExerciser.for_task(DisplayOnly, 
                                                 "Interact with a DMF board",
                                                 platforms=platforms,
                                                 pipettors=pipettors,
                                                 default_pipettor=default_pipettor)
    exerciser.parse_args_and_run()