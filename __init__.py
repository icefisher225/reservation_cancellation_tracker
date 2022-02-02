from __future__ import annotations
from typing import *


class ResList:
    def __init__(self, f: list[str]):
        self.items: dict[str, str] = dict(f)

    def __iter__(self) -> Iterator[str]:
        return iter(self.items.values())


def pretty(*, header: Iterable[str]) -> None:
    for i in header:
        assert isinstance(i, int)
        print(i)


# pretty([1, 2, 3])
# pretty((4, 5, 6))
r = ResList(["hello", "there"])
pretty(header=r)
