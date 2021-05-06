from enum import Enum

class Dir(Enum):
    x: int
    A = (1,1)
    B = (2,2)
    C = (5,5)
    AA = A
    
    def __init__(self, x: int, y: int):
        self.x = x+y

print(list(Dir))

print(Dir.A.x)
print(Dir.AA.x)
print(Dir.AA)