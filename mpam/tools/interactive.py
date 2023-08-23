from __future__ import annotations

from devices import joey, opendrop, wombat, opentrons, manual_pipettor,\
    bilby_task, eselog, bilby_yaminon_task
from mpam.exerciser import PlatformChoiceExerciser
from mpam.exerciser_tasks import DisplayOnly
from mpam.monitor import Config as monConfig
from mpam import pipettor
from langsup import type_supp


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
    pipettor.Config.value_formatter(type_supp.Type.default_formatter)
    exerciser.parse_args_and_run()