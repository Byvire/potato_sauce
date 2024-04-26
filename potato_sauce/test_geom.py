from absl.testing import absltest

from potato_sauce import geom
from potato_sauce.proto import geom_pb2


class GeometryTestCase(absltest.TestCase):

    def test_vector_addition_yields_a_vector(self):
        self.assertEqual(geom.Vector(3, 4),
                         geom.Vector(1, 0) + geom.Vector(2, 4))

    def test_vector_plus_point_equals_point_left(self):
        self.assertEqual(geom.Point(3, 4),
                         geom.Vector(1, 0) + geom.Point(2, 4))

    def test_vector_plus_point_equals_point_right(self):
        self.assertEqual(geom.Point(3, 4),
                         geom.Point(1, 0) + geom.Vector(2, 4))

    def test_vector_project_onto_other_vector(self):
        self.assertEqual(geom.Vector(1, 0),
                         geom.Vector(1, 4).project_onto(geom.Vector(5, 0)))

    def test_vector_zero_project_onto_other_vector(self):
        self.assertEqual(geom.Vector(0, 0),
                         geom.Vector(0, 0).project_onto(geom.Vector(5, -8)))

    def test_angle_from_origin_degrees_cardinal_east(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(5, 0)), 0)

    def test_angle_from_origin_degrees_cardinal_north(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(0, 5)), 90)

    def test_angle_from_origin_degrees_cardinal_west(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(-5, 0)), 180)

    def test_angle_from_origin_degrees_cardinal_south(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(0, -5)), 270)

    def test_angle_from_origin_degrees_quadrant_1(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(1, 1)), 45)

    def test_angle_from_origin_degrees_quadrant_2(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(-1, 1)), 135)

    def test_angle_from_origin_degrees_quadrant_3(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(-1, -1)), 225)

    def test_angle_from_origin_degrees_quadrant_4(self):
        self.assertEqual(geom.angle_from_origin_degrees(geom.Point(1, -1)), 315)

    def test_solve_quadratic_one_solution(self):
        self.assertEqual(geom.solve_quadratic(1, -4, 4), [2])

    def test_solve_quadratic_no_solutions(self):
        self.assertEqual(geom.solve_quadratic(1, 0, 4), [])

    def test_solve_quadratic_two_solutions(self):
        self.assertEqual(sorted(geom.solve_quadratic(1, 0, -4)), [-2, 2])

    def test_circle_intersections_circles_too_far_away(self):
        alice = geom.Circle(geom.Point(1, 2), 10)
        bob = geom.Circle(geom.Point(100, -100), 50)
        self.assertEqual(geom.circle_intersections(alice, bob), [])

    def test_circle_intersections_nested_circles_with_single_intersection(self):
        alice = geom.Circle(geom.Point(10, 10), 2)
        bob = geom.Circle(geom.Point(10, 11), 1)
        self.assertEqual(geom.circle_intersections(alice, bob),
                         [geom.Point(10, 12)])

    def test_circle_intersections_nested_circles_with_no_intersection(self):
        alice = geom.Circle(geom.Point(10, 10), 2)
        bob = geom.Circle(geom.Point(10, 10.95), 1)  # barely not touching
        self.assertEqual(geom.circle_intersections(alice, bob), [])

    def test_circle_intersection_horizontal_centers_two_intersections(self):
        alice = geom.Circle(geom.Point(10, 10), 2**0.5)
        bob = geom.Circle(geom.Point(12, 10), 2**0.5)
        result = sorted(geom.circle_intersections(alice, bob))
        self.assertLen(result, 2)
        self.assertSequenceAlmostEqual(result[0], geom.Point(11, 9))
        self.assertSequenceAlmostEqual(result[1], geom.Point(11, 11))

    def test_circle_intersection_vertical_centers_two_intersections(self):
        alice = geom.Circle(geom.Point(10, 10), 2**0.5)
        bob = geom.Circle(geom.Point(10, 12), 2**0.5)
        result = sorted(geom.circle_intersections(alice, bob))
        self.assertLen(result, 2)
        self.assertSequenceAlmostEqual(result[0], geom.Point(9, 11))
        self.assertSequenceAlmostEqual(result[1], geom.Point(11, 11))

    def test_circle_intersection_general_case_with_intersection(self):
        alice = geom.Circle(geom.Point(10, 10), 7)
        bob = geom.Circle(geom.Point(14, 8), 5)
        result = geom.circle_intersections(alice, bob)
        self.assertLen(result, 2)
        self.assertNotEqual(result[0], result[1])
        # The answers aren't neat for this one. The important part is we get
        # two distinct points that live on both circles.
        self.assertAlmostEqual((result[0] - bob.center).magnitude(), bob.radius)
        self.assertAlmostEqual((result[1] - bob.center).magnitude(), bob.radius)
        self.assertAlmostEqual((result[0] - alice.center).magnitude(),
                               alice.radius)
        self.assertAlmostEqual((result[1] - alice.center).magnitude(),
                               alice.radius)

    def test_circle_intersection_general_case_with_intersection_real_failure_case(self):
        # At one point the computed intersection of these circles was
        # Point(x=26.000000305602363, y=50.229161739349365)
        # and Point(x=25.99999969439765, y=-22.22916078567505).
        # Which is 38.16 away from both circles' centers, ie way way wrong.
        # This turned out to be caused by a breakdown of the floating-point
        # quadratic formula solver, when the two solutions lay on a nearly
        # vertical line. The solution was to make our "vertical line" check more
        # aggressive.
        alice = geom.Circle(geom.Point(38.0, 14.0), 13)
        bob = geom.Circle(geom.Point(14.0, 14.000000202446214), 13)
        result = geom.circle_intersections(alice, bob)
        self.assertLen(result, 2)
        self.assertNotEqual(result[0], result[1])
        # The answers aren't neat for this one. The important part is we get
        # two distinct points that live on both circles.
        self.assertAlmostEqual((result[0] - bob.center).magnitude(), bob.radius)
        self.assertAlmostEqual((result[1] - bob.center).magnitude(), bob.radius)
        self.assertAlmostEqual((result[0] - alice.center).magnitude(),
                               alice.radius)
        self.assertAlmostEqual((result[1] - alice.center).magnitude(),
                               alice.radius)

    def test_circle_intersection_with_all_small_coordinates(self):
        # Smallness is a special case that can cause a recursive call. We want
        # to not eat the whole stack and crash if everything is small.
        smol = 0.000001
        alice = geom.Circle(geom.Point(smol * 10, smol * 10), smol * 2**0.5)
        bob = geom.Circle(geom.Point(smol * 10, smol * 12), smol * 2**0.5)
        result = sorted(geom.circle_intersections(alice, bob))
        self.assertLen(result, 2)
        self.assertSequenceAlmostEqual(result[0], geom.Point(smol * 9, smol * 11))
        self.assertSequenceAlmostEqual(result[1], geom.Point(smol * 11, smol * 11))

    def test_circle_intersection_returns_nothing_if_circles_are_same(self):
        self.assertLen(geom.circle_intersections(
            geom.Circle(geom.Point(1, 1), 3),
            geom.Circle(geom.Point(1, 1), 3)),
                       0)

    def test_grid_coord_converts_from_proto(self):
        self.assertEqual(
            geom.GridCoord(3, -5),
            geom.GridCoord.from_proto(geom_pb2.GridCoord(x=3, y=-5)))

    def test_grid_coord_converts_to_proto(self):
        self.assertEqual(geom_pb2.GridCoord(x=3, y=-5),
                         geom.GridCoord(3, -5).to_proto())

    def test_grid_bottom_left_of_cell(self):
        grid = geom.Grid(cell_width=10, cell_height=15,
                         bottom_left=geom.Point(20, 40))
        self.assertEqual(grid.cell_bottom_left(geom.GridCoord(5, 10)),
                         geom.Point(70, 190))

    def test_grid_center_of_cell(self):
        grid = geom.Grid(cell_width=10, cell_height=15,
                         bottom_left=geom.Point(20, 40))
        self.assertEqual(grid.cell_center(geom.GridCoord(5, 10)),
                         geom.Point(75, 197.5))

    def test_grid_locating_cell_for_point(self):
        grid = geom.Grid(cell_width=10, cell_height=15,
                         bottom_left=geom.Point(20, 40))
        self.assertEqual(grid.find_cell(geom.Point(75, 197)),
                         geom.GridCoord(5, 10))

    def test_grid_converts_to_and_from_json(self):
        original = geom.Grid(cell_width=10, cell_height=15,
                         bottom_left=geom.Point(-20, 40))
        reloaded = geom.Grid.from_json_dict(original.to_json_dict())

        self.assertEqual(original.cell_center(geom.GridCoord(2, 4)),
                         reloaded.cell_center(geom.GridCoord(2, 4)))

    def test_gridtangle_value_error_if_bottom_left_above_top_right(self):
        with self.assertRaises(ValueError):
            geom.Gridtangle(geom.GridCoord(3, 5), geom.GridCoord(8, 4))

    def test_gridtangle_proto_conversion_round_trip(self):
        rect = geom.Gridtangle(geom.GridCoord(1, 3), geom.GridCoord(8, 7))
        self.assertEqual(rect, geom.Gridtangle.from_proto(rect.to_proto()))

    def test_gridtangle_overlap_corner_only(self):
        self.assertTrue(
            geom.Gridtangle(
                geom.GridCoord(0, 0), geom.GridCoord(3, 3)).overlaps(
                    geom.Gridtangle(geom.GridCoord(3, 3), geom.GridCoord(5, 8))))

    def test_gridtangle_overlap_left_edge_only(self):
        #    XX
        # XXXXX
        #    XX
        self.assertTrue(
            geom.Gridtangle(
                geom.GridCoord(0, 0), geom.GridCoord(3, 3)).overlaps(
                    geom.Gridtangle(geom.GridCoord(-3, 2), geom.GridCoord(1, 2))))

    def test_gridtangle_overlap_case_where_only_centers_overlap(self):
        #  X
        # XXX
        #  X
        self.assertTrue(
            geom.Gridtangle(
                geom.GridCoord(0, 1), geom.GridCoord(3, 1)).overlaps(
                    geom.Gridtangle(geom.GridCoord(1, 0), geom.GridCoord(1, 3))))

    def test_gridtangle_not_overlap_rectangles_are_far_in_both_dimensions(self):
        self.assertFalse(
            geom.Gridtangle(
                geom.GridCoord(0, 1), geom.GridCoord(3, 1)).overlaps(
                    geom.Gridtangle(geom.GridCoord(100, 1000),
                                    geom.GridCoord(103, 1008))))

    def test_gridtangle_not_overlap_that_are_adjacent(self):
        self.assertFalse(
            geom.Gridtangle(
                geom.GridCoord(0, 1), geom.GridCoord(3, 1)).overlaps(
                    geom.Gridtangle(geom.GridCoord(0, 2), geom.GridCoord(4, 3))))

    def test_gridtangle_intersection_when_overlapping(self):
        self.assertEqual(
            geom.gridtangle_intersection(
                geom.Gridtangle(geom.GridCoord(1, 3), geom.GridCoord(10, 8)),
                geom.Gridtangle(geom.GridCoord(4, 1), geom.GridCoord(7, 11))),
            geom.Gridtangle(geom.GridCoord(4, 3), geom.GridCoord(7, 8)))

    def test_gridtangle_contains_point_in_middle(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110)
                            ).contains_coord(geom.GridCoord(3, 105)))

    def test_gridtangle_not_contains_point_below(self):
        self.assertFalse(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110)
                            ).contains_coord(geom.GridCoord(3, 99)))

    def test_gridtangle_not_contains_point_to_left(self):
        self.assertFalse(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110)
                            ).contains_coord(geom.GridCoord(-3, 102)))

    def test_gridtangle_contains_bottom_left(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110)
                            ).contains_coord(geom.GridCoord(1, 100)))

    def test_gridtangle_contains_top_right(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110)
                            ).contains_coord(geom.GridCoord(6, 110)))

    def test_gridtangle_contains_itself(self):
        rect = geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
        self.assertTrue(rect.contains_rect(rect))

    def test_gridtangle_contains_smaller_rect(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .contains_rect(
                geom.Gridtangle(geom.GridCoord(2, 101),
                                geom.GridCoord(4, 105))))

    def test_gridtangle_does_not_contain_overlapping_rect(self):
        self.assertFalse(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .contains_rect(
                geom.Gridtangle(geom.GridCoord(-1, 101),
                                geom.GridCoord(4, 105))))

    def test_gridtangle_adjacency_on_left(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .touches_rect(geom.Gridtangle(
                geom.GridCoord(-3, 102), geom.GridCoord(0, 110))))

    def test_gridtangle_adjacency_vertical(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .touches_rect(
                geom.Gridtangle(geom.GridCoord(2, 90), geom.GridCoord(3, 99))))

    def test_gridtangle_adjacency_excluding_diagonal_touch(self):
        self.assertFalse(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .touches_rect(
                geom.Gridtangle(geom.GridCoord(-1, 90), geom.GridCoord(0, 99))))

    def test_gridtangle_adjacency_allowing_diagonal_touch(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .touches_rect(
                geom.Gridtangle(geom.GridCoord(-1, 90), geom.GridCoord(0, 99)),
                diagonal_counts=True,
            ))

    def test_gridtangle_overlapping_counts_as_touching(self):
        self.assertTrue(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .touches_rect(geom.Gridtangle(
                geom.GridCoord(4, 103), geom.GridCoord(4, 105))))

    def test_gridtangle_being_far_as_hell_away_does_not_count_as_touching(self):
        self.assertFalse(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .touches_rect(geom.Gridtangle(
                geom.GridCoord(1000, 103), geom.GridCoord(2000, 105))))

    def test_gridtangle_being_far_as_hell_away_does_not_count_as_touching_even_with_diagonal_enabled(self):
        self.assertFalse(
            geom.Gridtangle(geom.GridCoord(1, 100), geom.GridCoord(6, 110))
            .touches_rect(geom.Gridtangle(
                geom.GridCoord(1000, 103), geom.GridCoord(2000, 105)),
                          diagonal_counts=True))


if __name__ == "__main__":
    absltest.main()
