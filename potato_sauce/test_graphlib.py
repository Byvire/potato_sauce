from __future__ import annotations

from absl.testing import absltest
import itertools
import json
import os
from typing import Collection, NamedTuple, Mapping, TypeVar

from potato_sauce import graphlib


T = TypeVar("T")


_TESTDATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "test_data"))



class LongestPathSample(NamedTuple):
    """See: experiment/bunch_of_longest_path_test_cases.py."""
    longest_path_length: int
    start: str
    goal: str
    graph: Mapping[str, set[str]]

    @staticmethod
    def from_json(data: dict) -> LongestPathSample:
        return LongestPathSample(
            longest_path_length=data["longest_path_length"],
            start=data["start"],
            goal=data["goal"],
            graph={node: set(neighbors)
                   for node, neighbors in data["graph"].items()},
        )


def _load_longest_path_workload(path: str) -> list[LongestPathSample]:
    with open(path, "r") as f:
        as_dicts = json.load(f)
    return [LongestPathSample.from_json(data) for data in as_dicts]


class GraphlibTestCase(absltest.TestCase):

    def test_shortest_path_when_start_equals_goal(self):
        self.assertEqual(
            graphlib.shortest_simple_path(0, 0, {0: [1], 1: [0]}),
            [0])

    def test_shortest_path_finds_short_path(self):
        self.assertEqual(graphlib.shortest_simple_path(
            0, 3, {
                0: [1, 2],
                1: [2, 1],  # skipped
                2: [3, 0],
                3: [],
            }),
                         [0, 2, 3])

    def test_reverse_graph(self):
        graph = {
            0: [1, 2, 3],
            1: [0],
            2: [0, 3],
            3: [],
        }
        self.assertEqual(
            graphlib.reverse_graph(graph),
            {
                0: {1, 2},
                1: {0},
                2: {0},
                3: {0, 2},
            })


    def test_longest_simple_path_cant_visit_same_node_twice(self):
        graph = {
            0: [1, 2, 3],
            1: [0],
            2: [0, 3],
            3: [],
        }
        self.assertEqual(graphlib.longest_simple_path(0, 3, graph), [0, 2, 3])

    def test_longest_simple_path_from_node_to_itself(self):
        graph = {
            0: [1, 2, 3],
            1: [0],
            2: [0, 3],
            3: [],
        }
        self.assertEqual(graphlib.longest_simple_path(2, 2, graph), [2])

    def _assert_path_is_simple(self, path):
        self.assertCountEqual(path, set(path))

    def _assert_path_exists_in_graph(self, path: list[T],
                                     graph: Mapping[T, Collection[T]]):
        """Checks that each step in the path is connected by an edge."""
        for (a, b) in itertools.pairwise(path):
            self.assertIn(b, graph[a], f"no edge from {a} to {b}")

    def _run_longest_path_workload(self, workload: list[LongestPathSample]):
        # NB: Since these workloads were generated from previous, simpler
        # versions of the longest_simple_path algorithm, they are change
        # detection tests and not guarantees of correctness. However, that
        # version really seemed to work.
        for i, sample in enumerate(workload):
            with self.subTest(i):
                path = graphlib.longest_simple_path(
                    sample.start, sample.goal, sample.graph)
                # Don't assert that we found the *same* path, just that we found
                # a legitimate path that's the same length.
                self._assert_path_is_simple(path)
                try:
                    self._assert_path_exists_in_graph(path, sample.graph)
                except AssertionError:
                    print(sample)
                    print(path)
                    raise
                self.assertLen(path, sample.longest_path_length)

    def test_medium_graph_longest_simple_path_workload(self):
        # Takes about 0.08 seconds which is low enough we can leave it on.
        self._run_longest_path_workload(_load_longest_path_workload(
            os.path.join(_TESTDATA_DIR, "medium_longest_path_cases.json")))

    @absltest.skip("performance benchmark")
    def test_copious_medium_graph_longest_simple_path_workload(self):
        self._run_longest_path_workload(_load_longest_path_workload(
            os.path.join(_TESTDATA_DIR,
                         "copious_medium_longest_path_cases.json")))

    @absltest.skip("performance benchmark")
    def test_big_graph_longest_simple_path_workload(self):
        # About half a second on bottleneck_longest_simple_path.
        self._run_longest_path_workload(_load_longest_path_workload(
            os.path.join(_TESTDATA_DIR, "big_longest_path_cases.json")))

    @absltest.skip("performance benchmark")
    def test_five_seconds_medium_graph_longest_simple_path_workload(self):
        # Takes 9 seconds to run on the original naive simple path algorithm.
        # More like 3 seconds on bottleneck_longest_simple_path.
        self._run_longest_path_workload(_load_longest_path_workload(
            os.path.join(_TESTDATA_DIR,
                         "five_seconds_medium_longest_path_cases.json")))

    @absltest.skip("performance benchmark (large)")
    def test_two_minutes_medium_graph_longest_simple_path_workload(self):
        # This takes about 30 seconds on the current version of the
        # bottleneck_longest_simple_path algorithm and is intractable on the
        # naive_longest_simple_path algorithm.
        #
        # Level 177 is a doozy.
        self._run_longest_path_workload(_load_longest_path_workload(
            os.path.join(_TESTDATA_DIR,
                         "two_minutes_big_longest_path_cases.json")))

    def test_nodes_with_largest_reachable_sets_on_empty_graph(self):
        self.assertEqual(graphlib.nodes_with_largest_reachable_sets({}), set())

    def test_nodes_with_largest_reachable_sets_when_most_nodes_can_be_reached(self):
        self.assertEqual(
            graphlib.nodes_with_largest_reachable_sets({
                0: {1, 2, 3},  # winner
                1: {0, 4},  # winner
                2: {3},
                3: {2, 4},
                4: {2, 3},
            }),
            {0, 1})

    def test_nodes_with_largest_reachable_sets_with_disjoint_solutions(self):
        self.assertEqual(
            graphlib.nodes_with_largest_reachable_sets({
                0: {1, 2, 3},
                1: {2},
                2: {3},
                3: {1},
                "a": {"b", "c", "d"},
                "b": {"a"},
                "c": {"d"},
                "d": {"c"},
            }),
            {0, "a", "b"})





if __name__ == "__main__":
    absltest.main()
