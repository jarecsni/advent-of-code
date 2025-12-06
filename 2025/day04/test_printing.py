#!/usr/bin/env python3
"""
Unit tests for Day 4: Printing Department
"""

import unittest
import os
from printing import (
    parse_grid, count_neighbors, count_accessible_rolls,
    find_accessible_rolls, remove_accessible_rolls, solve
)


class TestParseGrid(unittest.TestCase):
    """Test cases for parse_grid function"""
    
    def test_simple_grid(self):
        """Test parsing a simple grid"""
        text = "..@\n@.@\n..@"
        grid = parse_grid(text)
        self.assertEqual(len(grid), 3)
        self.assertEqual(len(grid[0]), 3)
        self.assertEqual(grid[0], ['.', '.', '@'])
        self.assertEqual(grid[1], ['@', '.', '@'])
        self.assertEqual(grid[2], ['.', '.', '@'])
    
    def test_empty_spaces(self):
        """Test grid with only empty spaces"""
        text = "...\n...\n..."
        grid = parse_grid(text)
        self.assertEqual(len(grid), 3)
        self.assertTrue(all(cell == '.' for row in grid for cell in row))


class TestCountNeighbors(unittest.TestCase):
    """Test cases for count_neighbors function"""
    
    def test_corner_position(self):
        """Test counting neighbors at corner (0,0)"""
        grid = parse_grid("@@.\n@@.\n...")
        # Position (0,0) has neighbors at (0,1), (1,0), (1,1)
        self.assertEqual(count_neighbors(grid, 0, 0), 3)
    
    def test_edge_position(self):
        """Test counting neighbors at edge (0,1)"""
        grid = parse_grid("@@@\n@@@\n...")
        # Position (0,1) has neighbors at (0,0), (0,2), (1,0), (1,1), (1,2)
        self.assertEqual(count_neighbors(grid, 0, 1), 5)
    
    def test_center_position(self):
        """Test counting neighbors at center (1,1)"""
        grid = parse_grid("@@@\n@@@\n@@@")
        # Position (1,1) has 8 neighbors, all are @
        self.assertEqual(count_neighbors(grid, 1, 1), 8)
    
    def test_isolated_roll(self):
        """Test isolated roll with no neighbors"""
        grid = parse_grid("...\n.@.\n...")
        self.assertEqual(count_neighbors(grid, 1, 1), 0)
    
    def test_one_neighbor(self):
        """Test roll with one neighbor"""
        grid = parse_grid("...\n@@.\n...")
        self.assertEqual(count_neighbors(grid, 1, 0), 1)
        self.assertEqual(count_neighbors(grid, 1, 1), 1)
    
    def test_diagonal_neighbors(self):
        """Test counting diagonal neighbors"""
        grid = parse_grid("@.@\n.@.\n@.@")
        # Center has 4 diagonal neighbors
        self.assertEqual(count_neighbors(grid, 1, 1), 4)


class TestCountAccessibleRolls(unittest.TestCase):
    """Test cases for count_accessible_rolls function"""
    
    def test_all_isolated(self):
        """Test grid where all rolls are isolated (0 neighbors each)"""
        grid = parse_grid("@.@\n...\n@.@")
        # All 4 rolls have 0 neighbors, so all are accessible
        self.assertEqual(count_accessible_rolls(grid), 4)
    
    def test_small_cluster(self):
        """Test small cluster"""
        grid = parse_grid("@@\n@@")
        # Each roll has 3 neighbors, so all 4 are accessible
        self.assertEqual(count_accessible_rolls(grid), 4)
    
    def test_line_of_rolls(self):
        """Test horizontal line of rolls"""
        grid = parse_grid("@@@@@")
        # End rolls have 1 neighbor, middle rolls have 2 neighbors
        # All have < 4 neighbors, so all 5 are accessible
        self.assertEqual(count_accessible_rolls(grid), 5)
    
    def test_dense_cluster(self):
        """Test dense 3x3 cluster"""
        grid = parse_grid("@@@\n@@@\n@@@")
        # Corner rolls: 3 neighbors (accessible)
        # Edge rolls: 5 neighbors (not accessible)
        # Center roll: 8 neighbors (not accessible)
        # 4 corners are accessible
        self.assertEqual(count_accessible_rolls(grid), 4)
    
    def test_no_rolls(self):
        """Test grid with no rolls"""
        grid = parse_grid("...\n...\n...")
        self.assertEqual(count_accessible_rolls(grid), 0)


class TestFindAccessibleRolls(unittest.TestCase):
    """Test cases for find_accessible_rolls function"""
    
    def test_simple_grid(self):
        """Test finding accessible rolls in simple grid"""
        grid = parse_grid("@.@\n...\n@.@")
        accessible = find_accessible_rolls(grid)
        # All 4 rolls have 0 neighbors, so all are accessible
        self.assertEqual(len(accessible), 4)
        self.assertIn((0, 0), accessible)
        self.assertIn((0, 2), accessible)
        self.assertIn((2, 0), accessible)
        self.assertIn((2, 2), accessible)
    
    def test_dense_cluster(self):
        """Test finding accessible rolls in dense cluster"""
        grid = parse_grid("@@@\n@@@\n@@@")
        accessible = find_accessible_rolls(grid)
        # Only corners have < 4 neighbors
        self.assertEqual(len(accessible), 4)


class TestRemoveAccessibleRolls(unittest.TestCase):
    """Test cases for remove_accessible_rolls function"""
    
    def test_single_iteration(self):
        """Test removal when all rolls are accessible in one go"""
        grid = parse_grid("@.@\n...\n@.@")
        removed = remove_accessible_rolls(grid)
        self.assertEqual(removed, 4)
        # All rolls should be removed
        for row in grid:
            for cell in row:
                self.assertEqual(cell, '.')
    
    def test_multiple_iterations(self):
        """Test removal requiring multiple iterations"""
        # Create a 3x3 cluster
        grid = parse_grid("@@@\n@@@\n@@@")
        removed = remove_accessible_rolls(grid)
        # First iteration: 4 corners (3 neighbors each)
        # Second iteration: 4 edges (now have < 4 neighbors)
        # Third iteration: 1 center
        self.assertEqual(removed, 9)
    
    def test_no_accessible_rolls(self):
        """Test grid with no accessible rolls initially"""
        grid = parse_grid("...\n...\n...")
        removed = remove_accessible_rolls(grid)
        self.assertEqual(removed, 0)
    
    def test_partial_removal(self):
        """Test that removal creates new accessible rolls"""
        # Line of 5 rolls
        grid = parse_grid("@@@@@")
        removed = remove_accessible_rolls(grid)
        # All should eventually be removed
        self.assertEqual(removed, 5)


class TestSolve(unittest.TestCase):
    """Test cases for solve function"""
    
    def test_example_file_part_one(self):
        """Test Part One with example.txt -> 13 accessible rolls"""
        test_dir = os.path.dirname(__file__)
        example_path = os.path.join(test_dir, "example.txt")
        result = solve(example_path, remove_all=False)
        self.assertEqual(result, 13)
    
    def test_example_file_part_two(self):
        """Test Part Two with example.txt -> 43 total removed"""
        test_dir = os.path.dirname(__file__)
        example_path = os.path.join(test_dir, "example.txt")
        result = solve(example_path, remove_all=True)
        self.assertEqual(result, 43)
    
    def test_example_specific_cases(self):
        """Test specific patterns from the example"""
        # Top-left corner area from example
        grid = parse_grid("..@@.\n@@@@.")
        # Position (0,2): 4 neighbors - not accessible
        # Position (0,3): 3 neighbors - accessible
        self.assertEqual(count_neighbors(grid, 0, 2), 4)
        self.assertEqual(count_neighbors(grid, 0, 3), 3)


if __name__ == "__main__":
    unittest.main()
