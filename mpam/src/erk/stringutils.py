from re import Pattern
from typing import Optional, Final, Mapping, Union, cast, Sequence
import re
from numpy.lib.arraysetops import isin

_camel_case_re: Optional[Pattern] = None

def split_camel_case(s: str) -> list[str]:
    global _camel_case_re
    if _camel_case_re is None:
        _camel_case_re = re.compile('(?:^[a-z]|[A-z])[a-z0-9_]*')
    return _camel_case_re.findall(s)

_plurals_in_es_re: Optional[Pattern] = None
_plurals_in_ies_re: Optional[Pattern] = None

irregular_plurals: Final[dict[str,str]] = {
    "fish": "fish",
    "sheep": "sheep",
    "matrix": "matrices",
    "vertex": "vertices",
    "person": "people",
    "human": "humans"
    }

def infer_plural(singular: str) -> str:
    global _plurals_in_es_re
    global _plurals_in_ies_re
    global irregular_plurals
    p = irregular_plurals.get(singular, None)
    if p is not None:
        return p
    if _plurals_in_es_re is None:
        _plurals_in_es_re = re.compile('(?:[sz]h?|ch)$')
    if _plurals_in_es_re.search(singular):
        return singular+"es"
    if _plurals_in_ies_re is None:
        _plurals_in_ies_re = re.compile('[^aeiou]y$')
    if _plurals_in_es_re.search(singular):
        return singular[:-1]+"ies"
    if singular.endswith("man"):
        return singular[:-3]+"men"
    return singular+"s"
    
def map_str(d: Union[Mapping, set, tuple, Sequence]) -> str:
    if getattr(d, "items", None) is not None:
        return f"{{{', '.join(f'{k}: {v}' for k,v in cast(Mapping, d).items())}}}"
    if isinstance(d, set):
        return f"{{{', '.join(f'{v}' for v in d)}}}"
    if isinstance(d, tuple):
        return f"({', '.join(f'{v}' for k,v in d)}{',' if len(d) == 1 else ''})"
    if getattr(d, "__iter__", None) is not None:
        return f"[{', '.join(f'{v}' for k,v in d)}]"
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
    
    