from __future__ import annotations
from erk.stringutils import match_width

def test(repeated: str, string:str) -> None:
    print(string)
    print(match_width(string, repeating=repeated))
    print()
    
test("=", "This is a test")