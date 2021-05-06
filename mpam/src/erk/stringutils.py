from re import Pattern
from typing import Optional
import re

_camel_case_re: Optional[Pattern] = None

def split_camel_case(s: str) -> list[str]:
    if _camel_case_re is None:
        _camel_case_re = re.compile('(?:^[a-z]|[A-z])[a-z0-9]*')
    return _camel_case_re.findall(s)

if __name__ == '__main__':
    print(split_camel_case("ThisIsATest"))
    print(split_camel_case("thisIsAlsoATest"))  