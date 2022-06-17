from __future__ import annotations
from mpam.exerciser import PlatformChoiceExerciser, PlatformChoiceTask
from typing import Optional, Sequence
from devices import joey, wombat, bilby, manual_pipettor
from mpam.exerciser_tasks import DisplayOnly

class InteractiveExerciser(PlatformChoiceExerciser):
    def __init__(self, description: Optional[str] = None,
                 *,
                 platforms: Sequence[PlatformChoiceTask]) -> None:
        if description is None:
            description = "Interact with a DMF board"

        task = DisplayOnly()
        super().__init__(description, task=task, platforms=platforms,
                         default_pipettor=manual_pipettor.PipettorConfig())
    
if __name__ == '__main__':
    platforms = (joey.PlatformTask(),
                 wombat.PlatformTask(),
                 wombat.YaminonPlatformTask(),
                 bilby.PlatformTask())
    exerciser = InteractiveExerciser(platforms=platforms)
    exerciser.parse_args_and_run()