from __future__ import annotations

from typing import List, Set
import time

def test_membership_in_list(lst: List[int], val: int) -> bool:
    return val in lst

def test_membership_in_set(s: Set[int], val: int) -> bool:
    return val in s

def benchmark(function, collection, test_val, repetitions=100000):
    start_time = time.time()
    for _ in range(repetitions):
        function(collection, test_val)
    end_time = time.time()
    return end_time - start_time

# For a small collection:
small_list = list(range(10))
small_set = set(small_list)
test_val = 5

print(f"List time: {benchmark(test_membership_in_list, small_list, test_val)}")
print(f"Set time: {benchmark(test_membership_in_set, small_set, test_val)}")

# Now for a larger collection:
large_list = list(range(100000))
large_set = set(large_list)
test_val = 99999  # Worst-case scenario for list, as it's at the end.

print(f"List time: {benchmark(test_membership_in_list, large_list, test_val)}")
print(f"Set time: {benchmark(test_membership_in_set, large_set, test_val)}")
