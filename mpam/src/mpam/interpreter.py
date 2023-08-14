from __future__ import annotations
from mpam.device import Board
from typing import Final, Any, Optional
from erk.config import ConfigParam
from langsup import dml
from mpam.types import Delayed, Postable
from argparse import _ArgumentGroup, ArgumentParser
from erk.stringutils import conj_str
from langsup.type_supp import Type

class Config:
    dml_dirs: Final = ConfigParam[list[str]]([])
    dml_file_names: Final = ConfigParam[list[str]]([])
    dml_encoding: Final = ConfigParam('ascii')

class DMLInterpreter:
    interp: Final[dml.DMLInterpreter]
    cache_val_as: Final[Optional[str]]
    
    def __init__(self, *, 
                 board: Board, 
                 errors: str='strict',
                 cache_val_as: Optional[str] = None) -> None:
        self.interp = dml.DMLInterpreter(Config.dml_file_names(),
                                         dirs=Config.dml_dirs(), 
                                         board=board, 
                                         encoding=Config.dml_encoding(), 
                                         errors=errors)
        self.cache_val_as = cache_val_as
        
    
    def evaluate(self, expr: str) -> Delayed[tuple[Type, Any]]:
        expr = expr.strip()
        val = Postable[tuple[Type, Any]]()
        (self.interp.evaluate(expr, cache_as=self.cache_val_as)
         .then_call(lambda pair: val.post(pair)))
        return val
    
    def eval_and_print(self, expr: str) -> Delayed[tuple[Type, Any]]:
        print(f"Interactive cmd: {expr}")
        def on_val(pair: tuple[Type, Any]) -> None:
            ret_type, val = pair
            if ret_type is Type.ERROR:
                # assert isinstance(val, dmf_lang.EvaluationError)
                print(f"  Caught exception ({type(val).__name__}): {val}")
            elif ret_type is Type.NO_VALUE:
                print(f"  Interactive command returned without value.")
            else:
                print(f"  Interactive cmd val ({ret_type.name}): {val}")
        return self.evaluate(expr).then_call(on_val)
    
    @classmethod
    def add_args_to(cls, group: _ArgumentGroup,
                    parser: ArgumentParser) -> None: # @UnusedVariable
        Config.dml_dirs.add_arg_to(group, '--macro-dir', '--dml-dir',
                                         action='append',
                                         # type=FileType(),
                                         metavar='FILE',
                                         default_desc = lambda s: "to only search the current directory" if not s else conj_str([f"'{f}'" for f in s]),
                                         help='''A directory to search for DML files.  
                                                 This argument may be specified multiple times.
                                                 The current directory is always searched first
                                                 ''')
        Config.dml_file_names.add_arg_to(group, '--macro-file', '--dml-file',
                                         action='append',
                                         # type=FileType(),
                                         metavar='FILE',
                                         default_desc = lambda s: "no macro files" if not s else conj_str([f"'{f}'" for f in s]),
                                         help='A file containing DMF macro definitions.  This argument may be specified multiple times.')
        Config.dml_encoding.add_arg_to(group, '--dml-encoding',
                                       metavar='ENCODING',
                                       help = "The encoding the DML macro files are written in.")
        
        
        
        