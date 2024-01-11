from __future__ import annotations

from .processes import MixSequenceLibrary, PM, MixSequence

dilution_sequences = MixSequenceLibrary()

dilution_sequences.register(2,
  MixSequence(0.0,
    ((0,0), (0,-1),),
    (
     (PM(0,1),),
    ),
    fully_mixed=(0, 1),
    size=(1, 2),
    lead_offset=(0, 1)
   )
)

dilution_sequences.register(2.5,
  MixSequence(0.09999999999999998,
    ((0,0), (0,1), (-1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
    ),
    fully_mixed=(0, 1),
    size=(2, 2),
    lead_offset=(1, 0)
   )
)


dilution_sequences.register(3,
  MixSequence(0.09090909090909094,
    ((0,0), (-1,0), (0,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
     (PM(0,2),),
    ),
    fully_mixed=(0, 2),
    size=(2, 2),
    lead_offset=(1, 0)
   )
)

dilution_sequences.register(3,
  MixSequence(0.09090909090909094,
    ((0,0), (-1,0), (1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
     (PM(0,2),),
    ),
    fully_mixed=(0, 2),
    size=(3, 1),
    lead_offset=(1, 0)
   )
)

dilution_sequences.register(3,
  MixSequence(0.10000000000000009,
    ((0,0), (-1,0), (0,-1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
    ),
    fully_mixed=(0, 1, 2),
    size=(2, 2),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(3,
  MixSequence(0.10000000000000009,
    ((0,0), (-1,0), (1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
    ),
    fully_mixed=(0, 1, 2),
    size=(3, 1),
    lead_offset=(1, 0)
   )
)

dilution_sequences.register(3.5,
  MixSequence(0.021739130434782594,
    ((0,0), (0,1), (-1,0), (1,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
     (PM(1,3),),
     (PM(0,1),),
    ),
    fully_mixed=(0, 1),
    size=(3, 2),
    lead_offset=(1, 0)
   )
)                            

dilution_sequences.register(4,
  MixSequence(0.0,
    ((0,0), (1,0), (0,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
    ),
    fully_mixed=(0, 2),
    size=(2, 2),
    lead_offset=(0, 0)
   )
)


dilution_sequences.register(4,
  MixSequence(0.0,
    ((0,0), (0,-1), (0,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
    ),
    fully_mixed=(0, 2),
    size=(3, 1),
    lead_offset=(1, 0)
   )
)

dilution_sequences.register(4,
  MixSequence(0.0,
    ((0,0), (0,1), (1,1), (11,0),),
    (
     (PM(0,1),),
     (PM(0,3), PM(1,2),),
    ),
    fully_mixed=(0, 1, 2, 3),
    size=(2, 2),
    lead_offset=(0, 0)
   )
)

dilution_sequences.register(4.5,
  MixSequence(0.020000000000000018,
    ((0,0), (1,0), (0,1), (-1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,1),),
     (PM(0,3),),
    ),
    fully_mixed=(0, 3),
    size=(3, 2),
    lead_offset=(1, 0)
   )
)

dilution_sequences.register(5,
  MixSequence(0.07692307692307687,
    ((0,0), (-1,0), (-1,-1), (0,-1),),
    (
     (PM(0,1),),
     (PM(1,2),),
     (PM(0,1),),
     (PM(0,3),),
    ),
    fully_mixed=(0, 3),
    size=(2, 2),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(5,
  MixSequence(0.08333333333333326,
    ((0,0), (0,-1), (1,-1), (1,0), (-1,-1),),
    (
     (PM(0,1),),
     (PM(1,2),),
     (PM(0,1), PM(3,2),),
     (PM(1,4),),
     (PM(0,1),),
     (PM(0,3), PM(1,2),),
    ),
    fully_mixed=(0, 1, 2, 3, 4),
    size=(3, 2),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(5.5,
  MixSequence(0.03846153846153855,
    ((0,0), (1,0), (0,1), (1,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(2,3),),
     (PM(0,2),),
    ),
    fully_mixed=(0, 2),
    size=(2, 2),
    lead_offset=(0, 0)
   )
)

dilution_sequences.register(6,
  MixSequence(0.07407407407407407,
    ((0,0), (0,1), (0,-1), (-1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,2),),
     (PM(0,3),),
    ),
    fully_mixed=(0, 3),
    size=(2, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(6,
    MixSequence(0.10000000000000009,
    ((0,0), (-1,0), (0,-1), (1,-1), (1,0), (-1,-1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,1), PM(2,3),),
     (PM(0,4), PM(1,5),),
    ),
    fully_mixed=(0, 1, 2, 3, 4, 5),
    size=(3, 2),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(7,
  MixSequence(0.018181818181818188,
    ((0,0), (-1,0), (-1,1), (0,1), (1,1),),
    (
     (PM(0,1),),
     (PM(1,2),),
     (PM(0,1),),
     (PM(0,3),),
     (PM(3,4),),
     (PM(0,3),),
    ),
    fully_mixed=(0, 3),
    size=(3, 2),
    lead_offset=(1, 0)
   )
)

dilution_sequences.register(7,
  MixSequence(0.05555555555555558,
    ((0,0), (1,0), (-1,0), (0,-1), (0,1), (1,-1), (-1,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,1),),
     (PM(0,2), PM(1,5),),
     (PM(0,4), PM(2,6), PM(3,5),),
     (PM(1,5),),
    ),
    fully_mixed=(0, 1, 2, 3, 4, 5, 6),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(8,
  MixSequence(0.0,
    ((0,0), (1,0), (0,-1), (0,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
    ),
    fully_mixed=(0, 3),
    size=(2, 3),
    lead_offset=(0, 1)
   )
)

dilution_sequences.register(8,
  MixSequence(0.0,
    ((0,0), (-1,0), (-1,1), (0,1), (1,0), (1,1), (-2,0), (-2,1),),
    (
     (PM(0,1),),
     (PM(0,3), PM(1,2),),
     (PM(0,4), PM(1,6), PM(2,7), PM(3,5),),
    ),
    fully_mixed=(0, 1, 2, 3, 4, 5, 6, 7),
    size=(4, 2),
    lead_offset=(2, 0)
   )
)

dilution_sequences.register(9,
  MixSequence(0.01754385964912286,
    ((0,0), (0,-1), (0,1), (1,0), (-1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,1),),
     (PM(0,3),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(9,
  MixSequence(0.0714285714285714,
    ((0,0), (0,-1), (-1,-1), (0,1), (1,0), (-1, 1), (-1,0), (1,1), (1,-1),),
    (
     (PM(0,1),),
     (PM(0,3), PM(1,2),),
     (PM(0,4), PM(3,5),),
     (PM(0,1), PM(3,7),),
     (PM(0,4), PM(1,2),),
     (PM(0,3), PM(1,8), PM(4,7), PM(6,2),),
     (PM(3,5),),
    ),
    fully_mixed=(0, 1, 2, 3, 4, 5, 6, 7, 8),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(10,
  MixSequence(0.06896551724137934,
    ((0,0), (1,0), (1,-1), (0,-1), (0,1),),
    (
     (PM(0,1),),
     (PM(1,2),),
     (PM(0,1),),
     (PM(0,3),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(2, 3),
    lead_offset=(0, 1)
   )
)

dilution_sequences.register(10,
  MixSequence(0.08333333333333326,
    ((0,0), (0,-1), (-1,-1), (-2,-1), (1,0), (1,-1), (-1,0), (-2,0), (2,0), (2,-1),),
    (
     (PM(0,1),),
     (PM(0,4), PM(1,2),),
     (PM(0,6), PM(1,5), PM(2,3), PM(4,8),),
     (PM(5,9), PM(6,7),),
     (PM(0,6), PM(1,5),),
     (PM(5,9), PM(6,7),),
     (PM(4,5), PM(6,2), PM(7,3), PM(8,9),),
    ),
    fully_mixed=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    size=(5, 2),
    lead_offset=(2, 1)
   )
)

dilution_sequences.register(11,
  MixSequence(0.034482758620689724,
    ((0,0), (0,-1), (0,1), (-1,1), (-1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(2,3),),
     (PM(0,2),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(2, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(12,
  MixSequence(0.06779661016949157,
    ((0,0), (0,-1), (1,0), (-1,0), (0,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,4),),
     (PM(0,3),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(15,
  MixSequence(0.06666666666666665,
    ((0,0), (0,-1), (0,1), (-1,0), (1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)
dilution_sequences.register(16,
  MixSequence(0.06666666666666665,
    ((0,0), (0,-1), (0,1), (-1,0), (1,0),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(20,
  MixSequence(0.06557377049180324,
    ((0,0), (1,0), (0,-1), (-1,0), (-1,1), (0,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(3,4),),
     (PM(0,3),),
     (PM(0,5),),
    ),
    fully_mixed=(0, 5),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(25,
  MixSequence(0.05668016194331993,
    ((0,0), (-1,0), (1,0), (0,-1), (0,1), (1,1), (-1,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,4),),
     (PM(4,5),),
     (PM(0,4),),
     (PM(4,6),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(32,
  MixSequence(0.06464646464646462,
    ((0,0), (-1,0), (0,-1), (1,0), (0,1), (-1,1), (1,1),),
    (
     (PM(0,1),),
     (PM(0,2),),
     (PM(0,3),),
     (PM(0,4),),
     (PM(4,5),),
     (PM(0,4),),
     (PM(4,5),),
     (PM(4,6),),
     (PM(0,4),),
    ),
    fully_mixed=(0, 4),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(50,
  MixSequence(0.011457036114570385,
    ((0,0), (-1,0), (1,1), (1,0), (0,1), (-1,1), (0,-1), (-1,-1), (1,-1),),
    (
     (PM(0,1),),
     (PM(1,2),),
     (PM(0,1),),
     (PM(0,3),),
     (PM(0,4),),
     (PM(4,5),),
     (PM(0,4),),
     (PM(0,6),),
     (PM(6,7),),
     (PM(0,6),),
     (PM(6,8),),
     (PM(0,6),),
    ),
    fully_mixed=(0, 6),
    size=(3, 3),
    lead_offset=(1, 1)
   )
)

dilution_sequences.register(100,
  MixSequence(0.05110451443771935,
    ((0,0), (-1,0), (-1,1), (-2,0), (0,1), (1,0), (2,0), (1,1), (0,-1), (-1,-1), (1,-1),),
    (
     (PM(0,1),),
     (PM(1,2),),
     (PM(0,1),),
     (PM(1,3),),
     (PM(0,1),),
     (PM(0,4),),
     (PM(0,5),),
     (PM(5,6),),
     (PM(0,5),),
     (PM(5,6),),
     (PM(5,7),),
     (PM(0,5),),
     (PM(0,8),),
     (PM(8,9),),
     (PM(0,8),),
     (PM(8,10),),
     (PM(0,8),),
    ),
    fully_mixed=(0, 8),
    size=(5, 3),
    lead_offset=(2, 1)
   )
)