from __future__ import annotations

import logging
from typing import Final, ClassVar, Mapping, Sequence, Union, Optional


class LoggingLevel:
    desc: Final[str]
    level: Final[int]
    
    built_in: ClassVar[Mapping[str, LoggingLevel]]
    
    @classmethod
    def options(cls) -> Sequence[str]:
        levels = list(cls.built_in.values())
        levels.sort(key=lambda x: x.level)
        return [level.desc for level in levels]

    def __init__(self, desc: str, level: int) -> None:
        self.desc = desc
        self.level = level
        
    def __repr__(self) ->str:
        return f"{type(self).__name__}('{self.desc}', {self.level})"
        
    @classmethod
    def find(cls, level: Union[str, int]) -> LoggingLevel:
        if isinstance(level, int):
            return LoggingLevel(str(level), level)
        val = cls.built_in.get(level.upper(), None)
        if val is not None:
            return val
        try:
            return cls.find(int(level))
        except ValueError:
            raise ValueError(f"Couldn't find logging level for '{level}'")
    
        
LoggingLevel.built_in = {
    "DEBUG": LoggingLevel("DEBUG", logging.DEBUG),
    "INFO": LoggingLevel("INFO", logging.INFO),
    "WARN": LoggingLevel("WARN", logging.WARNING),
    "WARNING": LoggingLevel("WARNING", logging.WARNING),
    "ERROR": LoggingLevel("ERROR", logging.ERROR),
    "CRITICAL": LoggingLevel("CRITICAL", logging.CRITICAL)
    }
        

class LoggingSpec:
    level: LoggingLevel
    name: Optional[str]
    fmt_name: Optional[str]
    
    def __init__(self, level: Union[LoggingLevel, str, int], *,
                 name: Optional[str] = None,
                 fmt_name: Optional[str] = None) -> None:
        if not isinstance(level, LoggingLevel):
            level = LoggingLevel.find(level)
        self.level = level
        self.name = name
        self.fmt_name = fmt_name
        
    def __repr__(self) -> str:
        name = "" if self.name is None else f", name='{self.name}'"
        fmt_name = "" if self.fmt_name is None else f", name='{self.fmt_name}'"
        return f"{type(self).__name__}({self.level}{name}{fmt_name})"
        
    
    
logging_levels = LoggingLevel.options()
logging_formats = {
    'compact': '%(levelname)7s|%(module)s|%(message)s',
    'detailed': '%(relativeCreated)6d|%(levelname)7s|%(threadName)s|%(filename)s:%(lineno)s:%(funcName)s|%(message)s', 
    }


