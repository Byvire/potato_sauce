"""Generic graph-related utilities."""

import collections
import random
from typing import Callable, Collection, Iterator, Mapping, Optional, TypeVar


T = TypeVar("T")


def shortest_simple_path(start: T,
                         goal: T,
                         graph: Mapping[T, Collection[T]]) -> list[T]:
    """Shortest simple path between the given nodes in a directed graph.

    Raises ValueError if goal is not reachable from start. (If you need to
    check, see nodes_reachable_from().
    """
    parents = {start: start}
    next_round = [start]
    parents = {}
    while next_round:
        current_round, next_round = next_round, []
        for node in current_round:
            if node == goal:
                return _shortest_path_work_backward(start, goal, parents)
            for neighbor in graph[node]:
                if neighbor not in parents:
                    parents[neighbor] = node
                    next_round.append(neighbor)
    raise ValueError("start not reachable from goal")


def _shortest_path_work_backward(start: T,
                                 goal: T,
                                 parents: Mapping[T, T]) -> list[T]:
    current = goal
    backpath = []
    while True:
        backpath.append(current)
        if current == start:
            return backpath[::-1]
        current = parents[current]


def nodes_reachable_from(start: T,
                         graph: Mapping[T, Collection[T]],
                         reached: Optional[set[T]] = None) -> set[T]:
    """Finds all nodes reachable from the given node in the directed graph."""
    if reached is None:
        reached = set()
    if start in reached:
        return reached
    reached.add(start)
    try:
        graph[start]
    except KeyError:
        print("Key error from", start, graph)
    for neighbor in graph[start]:
        nodes_reachable_from(neighbor, graph, reached)
    return reached


def reverse_graph(graph: Mapping[T, Collection[T]]) -> dict[T, set[T]]:
    """Returns a copy of the graph with all the edge directions reversed."""
    reversed_graph = collections.defaultdict(set)
    for node, neighbors in graph.items():
        reversed_graph[node]  # initialize
        for neighbor in neighbors:
            reversed_graph[neighbor].add(node)
    return dict(reversed_graph)


def naive_longest_simple_path(start: T,
                              goal: T,
                              graph: Mapping[T, Collection[T]]) -> list[T]:
    """Finds the longest simple path from start to goal in the digraph.

    This solves an NP-hard problem! Either have tight bounds on the input size
    or set a timeout (eg with level_opt.run_with_timeout_on_unix_threadhostile).

    Raises ValueError if goal is not reachable from start. (If you need to
    check, see nodes_reachable_from().
    """
    reversed_graph = reverse_graph(graph)
    can_reach_goal = nodes_reachable_from(goal, reversed_graph)
    if start not in can_reach_goal:
        raise ValueError(
            "longest_simple_path: goal must be reachable from start")
    return _naive_longest_simple_path_impl(
        [start], goal, graph,
        (lambda path: path[-1] not in can_reach_goal))


def _naive_longest_simple_path_impl(
        sofar: list[T],
        goal: T,
        graph: Mapping[T, Collection[T]],
        prune: Callable[[list[T]], bool],
        # shared output parameter
        best_path: Optional[list[T]] = None) -> list[T]:
    """Finds the longest simple path to goal prefixed with sofar, if one exists.

    Args:
      sofar: prefix simple path. If best_path is updated by this call, the new
        value will have sofar as a prefix.
      goal: Where we're trying to find the longest path to.
      prune: Predicate such that if prune(path) is true for a path, that means
        it's impossible for path to be the prefix to a solution.
      best_path: Output parameter. Only to be set by recursive calls.
    """
    if best_path is None:
        best_path = []
    if sofar[-1] == goal:
        if len(sofar) > len(best_path):
            best_path[:] = sofar
        return best_path
    if prune(sofar):
        return best_path
    for neighbor in graph[sofar[-1]]:
        if neighbor in sofar:
            continue
        sofar.append(neighbor)
        _naive_longest_simple_path_impl(sofar, goal, graph, prune, best_path)
        sofar.pop()
    return best_path


def _graph_without_node(remove: T,
                        graph: Mapping[T, set[T]],
                        leave_node: bool = False) -> dict[T, set[T]]:
    """A shallow-ish copy of the graph with the given node removed.

    If leave_node, only remove the edges to/from the node but leave the node in
    the graph.
    """
    without = {}
    for node, neighbors in graph.items():
        if node == remove:
            if leave_node:
                without[node] = set()
        elif remove in neighbors:
            without[node] = neighbors.difference({remove})
        else:
            without[node] = neighbors
    return without


def _compute_node_bottlesets(
        goal: T,
        graph: Mapping[T, Collection[T]]) -> dict[T, set[T]]:
    """Computes the bottleset of each node with respect to the goal.

    The bottleset of a node N, with respect to a goal, is the set of other nodes
    from which all paths to the goal must go through N.

    This is useful because: Suppose you have three nodes, A, B, and G, where
    A is in the bottleset of B with respect to goal G (notated Bottleset(B, G)).
    Then longest_simple_path(A, G) == longest_simple_path(A, B) joined with
    longest_simple_path(B, G).

    Also note that for any node N in Bottleset(B, G), we have
    Bottleset(N, B) == Bottleset(N, G). So when we make a divide-and-conquer
    recursive call, we don't have to recompute all the bottlesets.
    """
    result = {}
    reversed_graph = reverse_graph(graph)
    can_reach_goal = nodes_reachable_from(goal, reversed_graph)
    for bottleneck in graph:
        if bottleneck not in can_reach_goal:
            # Fast path performance optimization, shaves a few seconds off
            # benchmarks. (Makes precomputation ~50% faster.)
            result[bottleneck] = set()
            continue
        result[bottleneck] = can_reach_goal.difference(
            nodes_reachable_from(
                goal, _graph_without_node(bottleneck, reversed_graph, True)),
            {bottleneck})
    assert result[goal] == can_reach_goal.difference({goal})

    return result


def bottleneck_longest_simple_path(
        start: T,
        goal: T,
        graph: Mapping[T, Collection[T]],
        # Non-public parameters, callers should not set these:
        #
        # Precomputed "bottlesets" of each node, see _compute_node_bottlesets().
        bottlesets: Optional[dict[T, set[T]]] = None,
        # Given a node, which nodes' bottlesets is it in?
        inverse_bottlesets: Optional[dict[T, set[T]]] = None,
        # Nodes already in the path to 'start'. We can't revisit these.
        forbid: Optional[set[T]] = None,
) -> list[T]:
    """Recursive longest simple path function with "bottleset" optimization.

    This takes advantage of some cases where you can divide and conquer as
    described in the _compute_node_bottlesets() docstring.

    Public parameters (start, goal, and graph) are the same as for
    naive_longest_simple_path. Other parameters should not be used.

    Returns a longest path if goal is reachable from start, or [] if not.
    """
    if start == goal:
        return [goal]
    if bottlesets is None:
        bottlesets = _compute_node_bottlesets(goal, graph)
    if inverse_bottlesets is None:
        # Using this, instead of looping through bottlesets[goal], gives a more
        # than 2x speedup on the "two_minutes_big_longest_path_cases" workload.
        inverse_bottlesets = reverse_graph(bottlesets)
    if forbid is None:
        forbid = set()
    if start in forbid or start not in bottlesets[goal]:
        return []
    # Two major cases:
    # If start is in the bottleset of anything in goal, then we divide and conquer.
    bottleneck = None
    for candidate in bottlesets[goal].intersection(inverse_bottlesets[start]):
        bottleneck = candidate
        assert start != bottleneck
        if bottleneck in forbid:
            return []
        break

    if bottleneck is not None:
        first_leg = bottleneck_longest_simple_path(
            start, bottleneck, graph, bottlesets, inverse_bottlesets, forbid
        )[:-1]
        if not first_leg:
            return []
        second_leg = bottleneck_longest_simple_path(
            bottleneck, goal, graph, bottlesets, inverse_bottlesets,
            forbid.union(set(first_leg)))
        if not second_leg:
            return []
        return first_leg + second_leg
    # Second major case: There are at least two disjoint paths to the goal, and
    # we need to check every option, like a naive longest-path search would.
    forbid = forbid.union({start})
    recursive_results = [
        bottleneck_longest_simple_path(
            neighbor, goal, graph, bottlesets, inverse_bottlesets, forbid)
        for neighbor in graph[start]
    ]
    recursive_results = [path for path in recursive_results if path]
    if not recursive_results:
        return []
    return [start] + max(recursive_results, key=len)


# Prefered longest_simple_path implementation for general use.
longest_simple_path = bottleneck_longest_simple_path


def nodes_with_largest_reachable_sets(
        graph: Mapping[T, Collection[T]]) -> set[T]:
    """Finds the nodes for which len(nodes_reachable_from(n, graph)) is highest.

    This takes worst case quadratic time in the number of nodes+edge, but
    expected case linear time, I think. Or n*log(n), e.g. if the graph is a
    complete DAG. But I haven't proven this.

    Why this works: For nodes A and B, if A is in reachable(B) then
    len(reachable(A)) <= len(reachable(B)).
    """
    # Nodes for which reachable set is certainly smaller than the maximum.
    bounded_suboptimal = set()
    # Nodes whose reachable set is <= the size of the largest found so far.
    bounded_best_yet = set()

    best_reachable_size = 0
    best_knowns = dict()

    visit_order = list(graph)
    random.shuffle(visit_order)
    for node in visit_order:
        if node in bounded_suboptimal or node in bounded_best_yet:
            continue
        reachable = nodes_reachable_from(node, graph)
        if len(reachable) == best_reachable_size:
            # At least two nodes are now tying for first place, with disjoint
            # reachable sets.
            best_knowns[node] = reachable
            bounded_best_yet.update(reachable)
        if len(reachable) > best_reachable_size:
            bounded_suboptimal.update(bounded_best_yet)
            bounded_best_yet = set(reachable)  # copy!
            best_knowns = {node: reachable}
            best_reachable_size = len(reachable)

    # Now we have one or more optimal nodes in best_knowns.keys(), and
    # an unknown number of other optimal nodes in their reachable sets
    # (best_knowns.values()).
    result = set()
    reverse = reverse_graph(graph)
    for node, reachable in best_knowns.items():
        result.add(node)
        result.update(reachable.intersection(nodes_reachable_from(node, reverse)))
    return result
