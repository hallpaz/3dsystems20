from itertools import tee
from typing import Iterator, Optional, Tuple


# Make an iterator over the adjacent pairs: (-1, 0), (0, 1), ..., (N - 2, N - 1)
def make_pair_range(N: int, start=-1) -> Iterator[Tuple[int, int]]:
    i, j = tee(range(start, N))
    next(j, None)
    return zip(i, j)