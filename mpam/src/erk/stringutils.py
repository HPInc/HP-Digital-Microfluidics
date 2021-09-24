from __future__ import annotations
from typing import Optional, Final, Mapping, Union, cast, Sequence
from erk.basic import LazyPattern

_camel_case_re = LazyPattern('(?:^[a-z]|[A-z])[a-z0-9_]*')

def split_camel_case(s: str) -> list[str]:
    global _camel_case_re
    return _camel_case_re.value.findall(s)

_plurals_in_es_re = LazyPattern('(?:[sz]h?|ch|x)$')
_plurals_in_ies_re = LazyPattern('[^aeiou]y$') 

irregular_plurals: Final[dict[str,str]] = {
    "fish": "fish",
    "sheep": "sheep",
    "matrix": "matrices",
    "vertex": "vertices",
    "person": "people",
    "human": "humans"
    }

_cached_plurals: dict[str,str] = {}

def infer_plural(singular: str) -> str:
    p = _cached_plurals.get(singular, None)
    if p is not None:
        return p
    if len(singular) == 0:
        raise ValueError(f"Empty string in infer_plural")
    lowered = singular.lower()
    def found_plural(stem: str, suffix: str) -> str:
        if singular[-1].isupper():
            suffix = suffix.upper()
        plural = stem+suffix 
        _cached_plurals[singular] = plural
        return plural

    p = irregular_plurals.get(lowered, None)
    if p is not None:
        return found_plural("", p)
    elif _plurals_in_es_re.value.search(lowered):
        return found_plural(singular, "es")        
    elif _plurals_in_ies_re.value.search(lowered):
        return found_plural(singular[:-1], "ies")
    elif lowered.endswith("man"):
        return found_plural(singular[:-3], "men")
    else:
        return found_plural(singular, "s")

def noun(n: float, singular: str, plural: Optional[str] = None,
         *, tolerance: float = 0):
    if tolerance == 0:
        if n == 1:
            return singular
    elif n >= 1-tolerance and n <= 1+tolerance:
        return singular
    return plural if plural is not None else infer_plural(singular)
    
    
def map_str(d: Union[Mapping, set, tuple, Sequence]) -> str:
    if getattr(d, "items", None) is not None:
        return f"{{{', '.join(f'{k}: {v}' for k,v in cast(Mapping, d).items())}}}"
    if isinstance(d, set):
        return f"{{{', '.join(f'{v}' for v in d)}}}"
    if isinstance(d, tuple):
        return f"({', '.join(f'{v}' for v in d)}{',' if len(d) == 1 else ''})"
    if getattr(d, "__iter__", None) is not None:
        return f"[{', '.join(f'{v}' for v in d)}]"
    assert False, f"{d} is somehow not a Mapping, set, tuple, or Sequence"

def fmt_dict(d: Mapping) -> str:
    return f"{{{', '.join(f'{k}: {v}' for k,v in d.items())}}}"

if __name__ == '__main__':
    print(split_camel_case("ThisIsATest"))
    print(split_camel_case("thisIsAlsoATest"))
    
    print(infer_plural("apple"))
    print(infer_plural("church"))  
    print(infer_plural("miss"))
    print(infer_plural("lily"))
    print(infer_plural("monkey"))
    print(infer_plural("vertex"))
    print(infer_plural("woman"))  
    print(infer_plural("man"))  
    
    