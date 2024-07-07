"""
For stuff that ought to be shared between separate mazetangle-related python
projects (eg ofk_game and giftangle).

Long term, it might be simpler to separate the mazetangle level generation from
ofk_game (removing the pygame dependency), at which point this library could go
back into the mazetangle level generation repo.
"""

import collections

from potato_sauce import geom

from typing import Optional, Sequence

class MazeNode:
    def __init__(self, rect: geom.Gridtangle) -> None:
        self.rect = rect
        # left/right/up/down represent legal moves, if any, from this node.
        # These may be mutated after construction to allow circular references.
        self.left: Optional[MazeNode] = None
        self.right: Optional[MazeNode] = None
        self.up: Optional[MazeNode] = None
        self.down: Optional[MazeNode] = None


def _intervals_overlap(alice: tuple[int, int],
                       bob: tuple[int, int]) -> bool:
    """Tests whether two endpoint-inclusive intervals overlap.

    Cribbed from mazetangle.py in ofk_game.
    """
    # They overlap iff the low endpoint of one interval is inside the other
    # interval.
    return ((alice[0] <= bob[0] and bob[0] <= alice[1])
            or (bob[0] <= alice[0] and alice[0] <= bob[1]))


def construct_mazetangle_graph(tiles: Sequence[geom.Gridtangle]
                               ) -> dict[geom.Gridtangle, MazeNode]:
    """Constructs the graph of legal mazetangle moves for the given tiles.

    This must be kept in sync with the Typescript makeTileTouchGraph
    implementation. The graph representations are slightly different because
    only the JS game needs to categorize or animate illegal moves.

    Don't confuse this with mondrian.rect_incidence_graph

    Args:
      tiles: Tiles in the tessellation, with a 1px border space between tiles
        that are "touching" (unlike Mondrian-model tiles, which leave no space
        for a border). The tiles should be non-overlapping and have no
        duplicates, or unexpected behavior may result.

    Returns:
      Node objects representing the graph, in a dict[rect, node] which you'll
      probably use to fetch the start and goal nodes. (Though the result has an
      entry for every tile.)
    """
    by_x_start = collections.defaultdict(set)
    by_x_end = collections.defaultdict(set)
    by_y_start = collections.defaultdict(set)
    by_y_end = collections.defaultdict(set)
    for rect in tiles:
        by_x_start[rect.bottom_left.x].add(rect)
        by_y_start[rect.bottom_left.y].add(rect)
        by_x_end[rect.end.x + 1].add(rect)  # +1 for the 1px border
        by_y_end[rect.end.y + 1].add(rect)

    # Find all horizontal incidences
    lefts = collections.defaultdict(list)
    rights = collections.defaultdict(list)
    for start, starters in by_x_start.items():
        for right in starters:
            for left in by_x_end[start]:
                if _intervals_overlap((right.bottom_left.y - 1, right.top_right.y + 1),
                                      (left.bottom_left.y, left.top_right.y)):
                    lefts[right].append(left)
                    rights[left].append(right)
    # Find all vertical incidences
    ups = collections.defaultdict(list)
    downs = collections.defaultdict(list)
    for start, starters in by_y_start.items():
        for high in starters:
            for low in by_y_end[start]:
                if _intervals_overlap((high.bottom_left.x - 1, high.top_right.x + 1),
                                      (low.bottom_left.x, low.top_right.x)):
                    ups[low].append(high)
                    downs[high].append(low)
    result = {rect: MazeNode(rect) for rect in tiles}
    for rect, node in result.items():
        if len(lefts[rect]) == 1:
            node.left = result[lefts[rect][0]]
        if len(rights[rect]) == 1:
            node.right = result[rights[rect][0]]
        if len(ups[rect]) == 1:
            node.up = result[ups[rect][0]]
        if len(downs[rect]) == 1:
            node.down = result[downs[rect][0]]
    return result
