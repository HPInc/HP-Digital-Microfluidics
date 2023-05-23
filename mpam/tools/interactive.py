from __future__ import annotations

from devices import joey, opendrop, wombat, opentrons, manual_pipettor,\
    bilby_task, eselog
from mpam.exerciser import PlatformChoiceExerciser
from mpam.exerciser_tasks import DisplayOnly
from mpam.monitor import Config as monConfig


if __name__ == '__main__':
    platforms = (
                bilby_task.PlatformTask,
                joey.PlatformTask,
                opendrop.PlatformTask,
                wombat.PlatformTask,
                wombat.YaminonPlatformTask,
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
    exerciser.parse_args_and_run()