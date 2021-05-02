from typing import Sized


def foo(x: int, y: str) -> int:
    return x

def bar(l: Sized) -> int:
    return len(l)

class S:
    members: list[int]
    def __init__(self, ns: list[int]) -> None:
        self.members = ns
        
    def __len__(self) -> int:
        return 7

if __name__ == "__main__":
    print(foo(3, "hi"))

    print(bar([1,2,3]))
    
    s = S([1,2,3])

    print(bar(s))