from __future__ import annotations

from devices import joey, opentrons, bilby_task
from mpam.exerciser import PlatformChoiceExerciser
import pcr


if __name__ == '__main__':
    platforms = (joey.PlatformTask,
                 bilby_task.PlatformTask)
    pipettors = (opentrons.PipettorConfig,)
    exerciser = PlatformChoiceExerciser.for_task(pcr.CombSynth,
                                                 "Run a combinatorial synthesis protocol",
                                                 platforms=platforms,
                                                 pipettors=pipettors)
    exerciser.parse_args_and_run()