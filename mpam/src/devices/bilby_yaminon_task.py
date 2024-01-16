from __future__ import annotations
from devices import bilby_task, joey
from devices.wombat import YaminonPlatformTask
from typing import Final, Optional, Sequence
from argparse import Namespace, _ArgumentGroup, ArgumentParser
from dmf.exerciser import PlatformChoiceExerciser, Exerciser,\
    PlatformChoiceTask

class PlatformTask(bilby_task.PlatformTask):
    _yaminon_task: Final[YaminonPlatformTask]
    
    def __init__(self, name:str="Hybrid", 
                 description: Optional[str]="A hybrid of Bilby and Yaminon", 
                 *, aliases: Optional[Sequence[str]]=None)->None:
        super().__init__(name=name, description=description, aliases=aliases)
        self._yaminon_task = YaminonPlatformTask()
        
    def make_board(self, args: Namespace, *, # @UnusedVariable
                   exerciser: PlatformChoiceExerciser # @UnusedVariable
                   )->joey.Board:
        self._add_dll_dir()
        from devices import bilby_yaminon
        return bilby_yaminon.Board()
    
    def setup_config_defaults(self) -> None:
        self._yaminon_task.setup_config_defaults()
        super().setup_config_defaults()
        
    def _check_and_add_args_to(self, group:_ArgumentGroup, 
                               parser:ArgumentParser, 
                               *, processed:set[type[PlatformChoiceTask]], 
                               exerciser:Exerciser)->None:
        if not self._args_needed(PlatformTask, processed):
            return
        self._yaminon_task._check_and_add_args_to(group, parser, exerciser=exerciser, processed=processed)
        super()._check_and_add_args_to(group, parser, exerciser=exerciser, processed=processed)
        