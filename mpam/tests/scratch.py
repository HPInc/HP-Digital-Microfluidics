from __future__ import annotations

guard = True

class Path: ...

def test() -> None:
    if guard:
        from pathlib import Path
    else:
        global Path
        
    print(Path)
    
test()