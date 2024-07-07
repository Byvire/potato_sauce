from absl.testing import absltest

from potato_sauce import mazetangle_sauce
from potato_sauce import geom


class MazetangleSauceTestCase(absltest.TestCase):

    def test_two_way_connection_horizontal(self):
        left = geom.Gridtangle(geom.GridCoord(0, 0), geom.GridCoord(8, 5))
        right = geom.Gridtangle(geom.GridCoord(10, -1), geom.GridCoord(12, 5))
        misaligned_left = geom.Gridtangle(geom.GridCoord(0, 100), geom.GridCoord(8, 110))

        graph = mazetangle_sauce.construct_mazetangle_graph([misaligned_left, left, right])

        self.assertEqual(graph[left].right, graph[right])
        self.assertEqual(graph[right].left, graph[left])
        # Extra sanity checks
        self.assertIsNone(graph[left].up)
        self.assertIsNone(graph[left].down)
        self.assertIsNone(graph[right].up)
        self.assertIsNone(graph[right].down)

    def test_two_way_connection_vertical(self):
        down = geom.Gridtangle(geom.GridCoord(0, 0), geom.GridCoord(8, 5))
        up = geom.Gridtangle(geom.GridCoord(0, 7), geom.GridCoord(8, 17))
        misaligned_up = geom.Gridtangle(geom.GridCoord(100, 7), geom.GridCoord(102, 17))

        graph = mazetangle_sauce.construct_mazetangle_graph([misaligned_up, down, up])

        self.assertEqual(graph[up].down, graph[down])
        self.assertEqual(graph[down].up, graph[up])
        # Extra sanity checks
        self.assertIsNone(graph[down].left)
        self.assertIsNone(graph[down].right)
        self.assertIsNone(graph[up].left)
        self.assertIsNone(graph[up].right)

    def test_asymmetric_connection_left_to_right(self):
        dots = [
            geom.Gridtangle(geom.GridCoord(-1, 0), geom.GridCoord(0, 0)),
            geom.Gridtangle(geom.GridCoord(-1, 2), geom.GridCoord(0, 2)),
            geom.Gridtangle(geom.GridCoord(-1, 4), geom.GridCoord(0, 4)),
        ]
        right = geom.Gridtangle(geom.GridCoord(2, 0), geom.GridCoord(4, 20))

        graph = mazetangle_sauce.construct_mazetangle_graph(dots + [right])

        for dot in dots:
            self.assertEqual(graph[dot].right, graph[right])
        self.assertIsNone(graph[right].left)

    def test_asymmetric_connection_right_to_left(self):
        dots = [
            geom.Gridtangle(geom.GridCoord(-1, 0), geom.GridCoord(0, 0)),
            geom.Gridtangle(geom.GridCoord(-1, 2), geom.GridCoord(0, 2)),
            geom.Gridtangle(geom.GridCoord(-1, 4), geom.GridCoord(0, 4)),
        ]
        left = geom.Gridtangle(geom.GridCoord(-10, 0), geom.GridCoord(-3, 20))

        graph = mazetangle_sauce.construct_mazetangle_graph(dots + [left])

        for dot in dots:
            self.assertEqual(graph[dot].left, graph[left])
        self.assertIsNone(graph[left].right)

    def test_asymmetric_connection_down_to_up(self):
        dots = [
            geom.Gridtangle(geom.GridCoord(0, -1), geom.GridCoord(0, 0)),
            geom.Gridtangle(geom.GridCoord(2, -1), geom.GridCoord(2, 0)),
            geom.Gridtangle(geom.GridCoord(4, -1), geom.GridCoord(4, 0)),
        ]
        up = geom.Gridtangle(geom.GridCoord(0, 2), geom.GridCoord(10, 20))

        graph = mazetangle_sauce.construct_mazetangle_graph(dots + [up])

        for dot in dots:
            self.assertEqual(graph[dot].up, graph[up])
        self.assertIsNone(graph[up].down)

    def test_asymmetric_connection_up_to_down(self):
        dots = [
            geom.Gridtangle(geom.GridCoord(0, -1), geom.GridCoord(0, 0)),
            geom.Gridtangle(geom.GridCoord(2, -1), geom.GridCoord(2, 0)),
            geom.Gridtangle(geom.GridCoord(4, -1), geom.GridCoord(4, 0)),
        ]
        down = geom.Gridtangle(geom.GridCoord(0, -10), geom.GridCoord(10, -3))

        graph = mazetangle_sauce.construct_mazetangle_graph(dots + [down])

        for dot in dots:
            self.assertEqual(graph[dot].down, graph[down])
        self.assertIsNone(graph[down].up)


if __name__ == "__main__":
    absltest.main()
