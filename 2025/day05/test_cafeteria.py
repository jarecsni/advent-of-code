#!/usr/bin/env python3
"""
Tests for Day 5: Cafeteria
"""

import unittest
from cafeteria import parse_input, is_fresh, solve_part_one, solve_part_two, merge_ranges


class TestParseInput(unittest.TestCase):
    """Test input parsing."""
    
    def test_parse_example(self):
        """Test parsing the example input file."""
        ranges, available_ids = parse_input("day05/example.txt")
        
        expected_ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        expected_ids = [1, 5, 8, 11, 17, 32]
        
        self.assertEqual(ranges, expected_ranges)
        self.assertEqual(available_ids, expected_ids)


class TestIsFresh(unittest.TestCase):
    """Test the is_fresh function."""
    
    def setUp(self):
        """Set up test ranges."""
        self.ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
    
    def test_fresh_in_first_range(self):
        """Test ID that falls in first range."""
        self.assertTrue(is_fresh(5, self.ranges))
    
    def test_fresh_in_middle_range(self):
        """Test ID that falls in middle range."""
        self.assertTrue(is_fresh(11, self.ranges))
    
    def test_fresh_in_overlapping_ranges(self):
        """Test ID that falls in multiple overlapping ranges."""
        self.assertTrue(is_fresh(17, self.ranges))
    
    def test_spoiled_below_all_ranges(self):
        """Test ID below all ranges."""
        self.assertFalse(is_fresh(1, self.ranges))
    
    def test_spoiled_between_ranges(self):
        """Test ID between ranges."""
        self.assertFalse(is_fresh(8, self.ranges))
    
    def test_spoiled_above_all_ranges(self):
        """Test ID above all ranges."""
        self.assertFalse(is_fresh(32, self.ranges))
    
    def test_fresh_at_range_boundaries(self):
        """Test IDs at exact range boundaries."""
        self.assertTrue(is_fresh(3, self.ranges))  # Start of first range
        self.assertTrue(is_fresh(5, self.ranges))  # End of first range
        self.assertTrue(is_fresh(10, self.ranges)) # Start of second range
        self.assertTrue(is_fresh(14, self.ranges)) # End of second range


class TestSolvePartOne(unittest.TestCase):
    """Test part one solution."""
    
    def test_example_input(self):
        """Test with the example input."""
        data = parse_input("day05/example.txt")
        result = solve_part_one(data)
        expected = 3  # IDs 5, 11, and 17 are fresh
        self.assertEqual(result, expected)
    
    def test_all_fresh(self):
        """Test when all IDs are fresh."""
        ranges = [(1, 100)]
        available_ids = [5, 10, 50, 99]
        result = solve_part_one((ranges, available_ids))
        self.assertEqual(result, 4)
    
    def test_none_fresh(self):
        """Test when no IDs are fresh."""
        ranges = [(10, 20)]
        available_ids = [1, 2, 3, 25, 30]
        result = solve_part_one((ranges, available_ids))
        self.assertEqual(result, 0)
    
    def test_single_range_single_id(self):
        """Test with single range and single ID."""
        ranges = [(5, 10)]
        available_ids = [7]
        result = solve_part_one((ranges, available_ids))
        self.assertEqual(result, 1)


class TestMergeRanges(unittest.TestCase):
    """Test range merging logic."""
    
    def test_no_overlap(self):
        """Test ranges with no overlap."""
        ranges = [(1, 3), (5, 7), (10, 12)]
        result = solve_part_two((ranges, []))
        # 3 + 3 + 3 = 9
        self.assertEqual(result, 9)
    
    def test_complete_overlap(self):
        """Test ranges that completely overlap."""
        ranges = [(1, 10), (3, 7)]
        result = solve_part_two((ranges, []))
        # Should count 1-10 only once = 10
        self.assertEqual(result, 10)
    
    def test_partial_overlap(self):
        """Test ranges with partial overlap."""
        ranges = [(1, 5), (3, 8)]
        result = solve_part_two((ranges, []))
        # Merged to 1-8 = 8
        self.assertEqual(result, 8)
    
    def test_adjacent_ranges(self):
        """Test adjacent ranges that should merge."""
        ranges = [(1, 5), (6, 10)]
        result = solve_part_two((ranges, []))
        # Adjacent ranges merge to 1-10 = 10
        self.assertEqual(result, 10)
    
    def test_multiple_overlaps(self):
        """Test multiple overlapping ranges."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        result = solve_part_two((ranges, []))
        # 3-5 (3 IDs) + 10-20 merged (11 IDs) = 14
        self.assertEqual(result, 14)


class TestSolvePartTwo(unittest.TestCase):
    """Test part two solution."""
    
    def test_example_input(self):
        """Test part two with the example input."""
        data = parse_input("day05/example.txt")
        result = solve_part_two(data)
        # Example expects 14 unique fresh IDs
        expected = 14
        self.assertEqual(result, expected)
    
    def test_single_range(self):
        """Test with a single range."""
        ranges = [(5, 10)]
        result = solve_part_two((ranges, []))
        self.assertEqual(result, 6)  # 5, 6, 7, 8, 9, 10


if __name__ == "__main__":
    unittest.main()
