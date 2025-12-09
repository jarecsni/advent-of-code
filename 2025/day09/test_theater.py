#!/usr/bin/env python3
"""Unit tests for Day 9: Movie Theater Tiles."""

import unittest
import os
from theater import (
    parse_tiles,
    find_largest_rectangle,
    part1,
    part2,
    build_polygon_boundary,
    build_valid_tiles,
    point_in_polygon,
)

# Get the directory containing this test file
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestParseTiles(unittest.TestCase):
    """Test tile coordinate parsing."""
    
    def test_parse_example_file(self):
        """Test parsing the example input file."""
        tiles = parse_tiles(os.path.join(TEST_DIR, 'example.txt'))
        self.assertEqual(len(tiles), 8)
        self.assertIn((7, 1), tiles)
        self.assertIn((11, 1), tiles)
        self.assertIn((2, 5), tiles)
    
    def test_parse_coordinates(self):
        """Test that coordinates are parsed as integers."""
        tiles = parse_tiles(os.path.join(TEST_DIR, 'example.txt'))
        for x, y in tiles:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
    
    def test_all_expected_tiles_present(self):
        """Test that all expected tiles from example are present."""
        tiles = parse_tiles(os.path.join(TEST_DIR, 'example.txt'))
        expected = {(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)}
        self.assertEqual(set(tiles), expected)


class TestFindLargestRectangle(unittest.TestCase):
    """Test rectangle area calculation."""
    
    def test_example_largest_rectangle(self):
        """Test that example input produces area of 50."""
        tiles = parse_tiles(os.path.join(TEST_DIR, 'example.txt'))
        area = find_largest_rectangle(tiles)
        self.assertEqual(area, 50)
    
    def test_two_tiles_same_row(self):
        """Test rectangle with tiles in same row (height = 1)."""
        tiles = [(0, 0), (5, 0)]
        area = find_largest_rectangle(tiles)
        # Width: |5-0|+1 = 6, Height: |0-0|+1 = 1, Area: 6
        self.assertEqual(area, 6)
    
    def test_two_tiles_same_column(self):
        """Test rectangle with tiles in same column (width = 1)."""
        tiles = [(0, 0), (0, 5)]
        area = find_largest_rectangle(tiles)
        # Width: |0-0|+1 = 1, Height: |5-0|+1 = 6, Area: 6
        self.assertEqual(area, 6)
    
    def test_two_tiles_diagonal(self):
        """Test rectangle with tiles at diagonal corners."""
        tiles = [(0, 0), (3, 4)]
        area = find_largest_rectangle(tiles)
        # Width: |3-0|+1 = 4, Height: |4-0|+1 = 5, Area: 20
        self.assertEqual(area, 20)
    
    def test_square_rectangle(self):
        """Test square rectangle (equal width and height)."""
        tiles = [(0, 0), (5, 5)]
        area = find_largest_rectangle(tiles)
        # Width: 6, Height: 6, Area: 36
        self.assertEqual(area, 36)
    
    def test_multiple_tiles_finds_maximum(self):
        """Test that maximum area is found among multiple tile pairs."""
        tiles = [(0, 0), (1, 1), (10, 10)]
        area = find_largest_rectangle(tiles)
        # Largest should be (0,0) to (10,10): 11 × 11 = 121
        self.assertEqual(area, 121)
    
    def test_negative_coordinates(self):
        """Test that negative coordinates work correctly."""
        tiles = [(-5, -5), (5, 5)]
        area = find_largest_rectangle(tiles)
        # Width: |5-(-5)|+1 = 11, Height: |5-(-5)|+1 = 11, Area: 121
        self.assertEqual(area, 121)
    
    def test_order_independence(self):
        """Test that tile order doesn't affect result."""
        tiles1 = [(0, 0), (5, 5)]
        tiles2 = [(5, 5), (0, 0)]
        area1 = find_largest_rectangle(tiles1)
        area2 = find_largest_rectangle(tiles2)
        self.assertEqual(area1, area2)
    
    def test_adjacent_tiles(self):
        """Test rectangle with adjacent tiles (minimal rectangle)."""
        tiles = [(0, 0), (1, 0)]
        area = find_largest_rectangle(tiles)
        # Width: 2, Height: 1, Area: 2
        self.assertEqual(area, 2)
    
    def test_example_specific_rectangles(self):
        """Test specific rectangle examples from problem description."""
        tiles = parse_tiles(os.path.join(TEST_DIR, 'example.txt'))
        
        # Rectangle between (2,5) and (9,7): width=8, height=3, area=24
        # But we're looking for max, which is 50
        
        # Verify the tiles we're checking exist
        self.assertIn((2, 5), tiles)
        self.assertIn((11, 1), tiles)
        
        # Calculate area between (2,5) and (11,1)
        width = abs(11 - 2) + 1  # 10
        height = abs(1 - 5) + 1  # 5
        expected_area = width * height  # 50
        self.assertEqual(expected_area, 50)


class TestPart1(unittest.TestCase):
    """Test part 1 solution."""
    
    def test_part1_with_example(self):
        """Test part 1 with example input."""
        tiles = parse_tiles(os.path.join(TEST_DIR, 'example.txt'))
        result = part1(tiles)
        self.assertEqual(result, 50)
    
    def test_part1_returns_integer(self):
        """Test that part 1 returns an integer."""
        tiles = parse_tiles(os.path.join(TEST_DIR, 'example.txt'))
        result = part1(tiles)
        self.assertIsInstance(result, int)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_minimum_tiles(self):
        """Test with minimum number of tiles (2)."""
        tiles = [(0, 0), (1, 1)]
        area = find_largest_rectangle(tiles)
        self.assertEqual(area, 4)  # 2×2
    
    def test_three_tiles_collinear_horizontal(self):
        """Test with three tiles in a horizontal line."""
        tiles = [(0, 0), (5, 0), (10, 0)]
        area = find_largest_rectangle(tiles)
        # Max should be (0,0) to (10,0): 11×1 = 11
        self.assertEqual(area, 11)
    
    def test_three_tiles_collinear_vertical(self):
        """Test with three tiles in a vertical line."""
        tiles = [(0, 0), (0, 5), (0, 10)]
        area = find_largest_rectangle(tiles)
        # Max should be (0,0) to (0,10): 1×11 = 11
        self.assertEqual(area, 11)
    
    def test_large_coordinates(self):
        """Test with large coordinate values."""
        tiles = [(0, 0), (1000, 1000)]
        area = find_largest_rectangle(tiles)
        self.assertEqual(area, 1001 * 1001)


class TestPolygonBoundary(unittest.TestCase):
    """Test polygon boundary construction."""

    def test_boundary_includes_red_tiles(self):
        """Test that boundary includes all red tiles."""
        tiles = [(0, 0), (5, 0), (5, 5), (0, 5)]
        boundary = build_polygon_boundary(tiles)
        for tile in tiles:
            self.assertIn(tile, boundary)

    def test_horizontal_connection(self):
        """Test that horizontal connections are added."""
        tiles = [(0, 0), (5, 0)]
        boundary = build_polygon_boundary(tiles)
        # Should include all tiles from (0,0) to (5,0)
        for x in range(6):
            self.assertIn((x, 0), boundary)

    def test_vertical_connection(self):
        """Test that vertical connections are added."""
        tiles = [(0, 0), (0, 5)]
        boundary = build_polygon_boundary(tiles)
        # Should include all tiles from (0,0) to (0,5)
        for y in range(6):
            self.assertIn((0, y), boundary)

    def test_square_boundary(self):
        """Test boundary of a square."""
        tiles = [(0, 0), (3, 0), (3, 3), (0, 3)]
        boundary = build_polygon_boundary(tiles)
        # Should have 4 corners + edges
        # Top: (0,0) to (3,0) = 4 tiles
        # Right: (3,0) to (3,3) = 4 tiles (but (3,0) already counted)
        # Bottom: (3,3) to (0,3) = 4 tiles (but (3,3) already counted)
        # Left: (0,3) to (0,0) = 4 tiles (but both already counted)
        # Total unique: 4 + 3 + 3 + 2 = 12
        self.assertEqual(len(boundary), 12)


class TestPointInPolygon(unittest.TestCase):
    """Test point-in-polygon algorithm."""

    def test_point_inside_square(self):
        """Test point inside a square polygon."""
        polygon = [(0, 0), (4, 0), (4, 4), (0, 4)]
        self.assertTrue(point_in_polygon(2, 2, polygon))

    def test_point_outside_square(self):
        """Test point outside a square polygon."""
        polygon = [(0, 0), (4, 0), (4, 4), (0, 4)]
        self.assertFalse(point_in_polygon(5, 5, polygon))

    def test_point_on_boundary(self):
        """Test point on polygon boundary."""
        polygon = [(0, 0), (4, 0), (4, 4), (0, 4)]
        # Point on edge - behavior may vary, just verify it doesn't crash
        result = point_in_polygon(0, 2, polygon)
        self.assertIsInstance(result, bool)

    def test_point_inside_triangle(self):
        """Test point inside a triangle."""
        polygon = [(0, 0), (4, 0), (2, 3)]
        self.assertTrue(point_in_polygon(2, 1, polygon))

    def test_point_outside_triangle(self):
        """Test point outside a triangle."""
        polygon = [(0, 0), (4, 0), (2, 3)]
        self.assertFalse(point_in_polygon(0, 5, polygon))


class TestBuildValidTiles(unittest.TestCase):
    """Test valid tile set construction."""

    def test_example_valid_tiles_count(self):
        """Test that example produces correct number of valid tiles."""
        tiles = parse_tiles(os.path.join(TEST_DIR, "example.txt"))
        valid_tiles = build_valid_tiles(tiles)
        # Should have 8 red + 22 green boundary + 16 interior = 46
        self.assertEqual(len(valid_tiles), 46)

    def test_valid_tiles_include_red(self):
        """Test that valid tiles include all red tiles."""
        tiles = parse_tiles(os.path.join(TEST_DIR, "example.txt"))
        valid_tiles = build_valid_tiles(tiles)
        for tile in tiles:
            self.assertIn(tile, valid_tiles)

    def test_simple_square_valid_tiles(self):
        """Test valid tiles for a simple square."""
        tiles = [(0, 0), (3, 0), (3, 3), (0, 3)]
        valid_tiles = build_valid_tiles(tiles)
        # Should include boundary (12) + interior (2×2=4) = 16
        self.assertEqual(len(valid_tiles), 16)


class TestPart2(unittest.TestCase):
    """Test part 2 solution."""

    def test_part2_with_example(self):
        """Test part 2 with example input."""
        tiles = parse_tiles(os.path.join(TEST_DIR, "example.txt"))
        result = part2(tiles)
        self.assertEqual(result, 24)

    def test_part2_returns_integer(self):
        """Test that part 2 returns an integer."""
        tiles = parse_tiles(os.path.join(TEST_DIR, "example.txt"))
        result = part2(tiles)
        self.assertIsInstance(result, int)

    def test_part2_less_than_or_equal_part1(self):
        """Test that part 2 result is <= part 1 (more constraints)."""
        tiles = parse_tiles(os.path.join(TEST_DIR, "example.txt"))
        result1 = part1(tiles)
        result2 = part2(tiles)
        self.assertLessEqual(result2, result1)

    def test_part2_simple_square(self):
        """Test part 2 with a simple square polygon."""
        tiles = [(0, 0), (3, 0), (3, 3), (0, 3)]
        result = part2(tiles)
        # Entire 4×4 area should be valid
        self.assertEqual(result, 16)


if __name__ == "__main__":
    unittest.main()


