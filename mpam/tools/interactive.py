from __future__ import annotations

from devices import joey, wombat, bilby, manual_pipettor, opentrons, opendrop
from mpam.exerciser import PlatformChoiceExerciser

from mpam.exerciser_tasks import DisplayOnly



if __name__ == '__main__':
    platforms = (
                bilby.PlatformTask,
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