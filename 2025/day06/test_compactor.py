#!/usr/bin/env python3
"""
Tests for Day 6: Trash Compactor
"""

import unittest
from compactor import parse_worksheet, parse_worksheet_part2, solve_problem, calculate_grand_total


class TestParseWorksheet(unittest.TestCase):
    """Test worksheet parsing"""
    
    def test_parse_simple_worksheet(self):
        """Test parsing a simple worksheet"""
        lines = [
            "123 328  51 64",
            " 45  64 387 23",
            "  6  98 215 314",
            "  *   +   *   +"
        ]
        problems = parse_worksheet(lines)
        
        self.assertEqual(len(problems), 4)
        self.assertEqual(problems[0], ([123, 45, 6], '*'))
        self.assertEqual(problems[1], ([328, 64, 98], '+'))
        self.assertEqual(problems[2], ([51, 387, 215], '*'))
        self.assertEqual(problems[3], ([64, 23, 314], '+'))
    
    def test_parse_single_problem(self):
        """Test parsing a worksheet with one problem"""
        lines = [
            "10",
            "20",
            "30",
            "+"
        ]
        problems = parse_worksheet(lines)
        
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0], ([10, 20, 30], '+'))
    
    def test_parse_varying_widths(self):
        """Test parsing numbers with varying digit widths"""
        lines = [
            "1 9999",
            "2 1",
            "3 1",
            "* +"
        ]
        problems = parse_worksheet(lines)
        
        self.assertEqual(problems[0], ([1, 2, 3], '*'))
        self.assertEqual(problems[1], ([9999, 1, 1], '+'))


class TestSolveProblem(unittest.TestCase):
    """Test individual problem solving"""
    
    def test_multiply_three_numbers(self):
        """Test multiplication of three numbers"""
        result = solve_problem([123, 45, 6], '*')
        self.assertEqual(result, 33210)
    
    def test_add_three_numbers(self):
        """Test addition of three numbers"""
        result = solve_problem([328, 64, 98], '+')
        self.assertEqual(result, 490)
    
    def test_multiply_large_numbers(self):
        """Test multiplication with large result"""
        result = solve_problem([51, 387, 215], '*')
        self.assertEqual(result, 4243455)
    
    def test_add_two_numbers(self):
        """Test addition of two numbers"""
        result = solve_problem([100, 200], '+')
        self.assertEqual(result, 300)
    
    def test_multiply_single_number(self):
        """Test multiplication with single number"""
        result = solve_problem([42], '*')
        self.assertEqual(result, 42)
    
    def test_multiply_with_zero(self):
        """Test multiplication including zero"""
        result = solve_problem([5, 0, 10], '*')
        self.assertEqual(result, 0)


class TestCalculateGrandTotal(unittest.TestCase):
    """Test grand total calculation"""
    
    def test_example_worksheet_part1(self):
        """Test Part 1 with the example"""
        result = calculate_grand_total('day06/example.txt')
        self.assertEqual(result, 4277556)
    
    def test_example_worksheet_part2(self):
        """Test Part 2 with the example (cephalopod column reading)"""
        result = calculate_grand_total('day06/example.txt', part2=True)
        self.assertEqual(result, 3263827)


class TestParseWorksheetPart2(unittest.TestCase):
    """Test Part 2 worksheet parsing"""
    
    def test_parse_example_part2(self):
        """Test Part 2 parsing produces correct numbers"""
        with open('day06/example.txt', 'r') as f:
            lines = f.readlines()
        
        problems = parse_worksheet_part2(lines)
        
        self.assertEqual(len(problems), 4)
        # Problem 0 (leftmost): 356 * 24 * 1 = 8544
        self.assertEqual(set(problems[0][0]), {1, 24, 356})
        self.assertEqual(problems[0][1], '*')
        # Problem 1: 8 + 248 + 369 = 625
        self.assertEqual(set(problems[1][0]), {8, 248, 369})
        self.assertEqual(problems[1][1], '+')
        # Problem 2: 175 * 581 * 32 = 3253600
        self.assertEqual(set(problems[2][0]), {32, 175, 581})
        self.assertEqual(problems[2][1], '*')
        # Problem 3 (rightmost): 4 + 431 + 623 = 1058
        self.assertEqual(set(problems[3][0]), {4, 431, 623})
        self.assertEqual(problems[3][1], '+')


if __name__ == "__main__":
    unittest.main()
