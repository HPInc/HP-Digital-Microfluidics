from __future__ import annotations

from argparse import _ArgumentGroup, ArgumentParser, Namespace

from devices import joey, wombat, opentrons, dummy_pipettor, bilby_task
from mpam.device import Board, System
from mpam.exerciser import PlatformChoiceExerciser, Task, Exerciser
from mpam.paths import Path
from mpam.types import Reagent
from quantities.SI import uL


class SourceTest(Task):
    def __init__(self) -> None:
        super().__init__(name="display-only",
                         description = "Just bring up the display.",
                         aliases=["display"])

    def add_args_to(self, 
                    group: _ArgumentGroup, # @UnusedVariable
                    parser: ArgumentParser, *,  # @UnusedVariable
                    exerciser: Exerciser  # @UnusedVariable
                    ) -> None:
        ...

        
    def run(self, board: Board, system: System, args: Namespace) -> None:  # @UnusedVariable
        ep = board.extraction_points[0]
        pipettor = ep.pipettor
        assert pipettor is not None
        source = pipettor.source_named("A1")
        assert source is not None
        reagent = Reagent.find("R1")
        source.reagent = reagent
        source.exact_volume = 200*uL
        path = Path.teleport_into(ep, reagent=reagent).to_row(5)
        print(source)
        path.schedule().wait()
        print(source)
        


if __name__ == '__main__':
    platforms = (
                bilby_task.PlatformTask,
                joey.PlatformTask,
                wombat.PlatformTask,
                wombat.YaminonPlatformTask,
                )
    pipettors = (opentrons.PipettorConfig,)
    default_pipettor = dummy_pipettor.PipettorConfig
    # exerciser = InteractiveExerciser(platforms=platforms, pipettors=pipettors)
    exerciser = PlatformChoiceExerciser.for_task(SourceTest, 
                                                 "Interact with a DMF board",
                                                 platforms=platforms,
                                                 pipettors=pipettors,
                                                 default_pipettor=default_pipettor)
    exerciser.parse_args_and_run()