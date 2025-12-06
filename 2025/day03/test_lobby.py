#!/usr/bin/env python3
"""
Unit tests for Day 3: Lobby
"""

import unittest
import os
from lobby import max_joltage, solve


class TestMaxJoltage(unittest.TestCase):
    """Test cases for max_joltage function"""
    
    def test_example_bank_1(self):
        """Test first example bank: 987654321111111 -> 98"""
        self.assertEqual(max_joltage("987654321111111"), 98)
    
    def test_example_bank_2(self):
        """Test second example bank: 811111111111119 -> 89"""
        self.assertEqual(max_joltage("811111111111119"), 89)
    
    def test_example_bank_3(self):
        """Test third example bank: 234234234234278 -> 78"""
        self.assertEqual(max_joltage("234234234234278"), 78)
    
    def test_example_bank_4(self):
        """Test fourth example bank: 818181911112111 -> 92"""
        self.assertEqual(max_joltage("818181911112111"), 92)
    
    def test_simple_ascending(self):
        """Test simple ascending sequence: 123 -> 23"""
        self.assertEqual(max_joltage("123"), 23)
    
    def test_simple_descending(self):
        """Test simple descending sequence: 321 -> 32"""
        self.assertEqual(max_joltage("321"), 32)
    
    def test_all_same(self):
        """Test all same digits: 5555 -> 55"""
        self.assertEqual(max_joltage("5555"), 55)
    
    def test_two_digits_only(self):
        """Test minimum case with two digits: 42 -> 42"""
        self.assertEqual(max_joltage("42"), 42)
    
    def test_nine_and_one(self):
        """Test 91 -> 91"""
        self.assertEqual(max_joltage("91"), 91)
    
    def test_distant_digits(self):
        """Test digits far apart: 9000001 -> 91"""
        self.assertEqual(max_joltage("9000001"), 91)


class TestMaxJoltageTwelve(unittest.TestCase):
    """Test cases for max_joltage with 12 batteries (Part Two)"""
    
    def test_example_bank_1_twelve(self):
        """Test first example bank with 12 batteries: 987654321111111 -> 987654321111"""
        self.assertEqual(max_joltage("987654321111111", 12), 987654321111)
    
    def test_example_bank_2_twelve(self):
        """Test second example bank with 12 batteries: 811111111111119 -> 811111111119"""
        self.assertEqual(max_joltage("811111111111119", 12), 811111111119)
    
    def test_example_bank_3_twelve(self):
        """Test third example bank with 12 batteries: 234234234234278 -> 434234234278"""
        self.assertEqual(max_joltage("234234234234278", 12), 434234234278)
    
    def test_example_bank_4_twelve(self):
        """Test fourth example bank with 12 batteries: 818181911112111 -> 888911112111"""
        self.assertEqual(max_joltage("818181911112111", 12), 888911112111)


class TestSolve(unittest.TestCase):
    """Test cases for solve function"""
    
    def test_example_file_part_one(self):
        """Test Part One with example.txt -> 357"""
        test_dir = os.path.dirname(__file__)
        example_path = os.path.join(test_dir, "example.txt")
        result = solve(example_path, num_batteries=2)
        self.assertEqual(result, 357)
    
    def test_example_file_part_two(self):
        """Test Part Two with example.txt -> 3121910778619"""
        test_dir = os.path.dirname(__file__)
        example_path = os.path.join(test_dir, "example.txt")
        result = solve(example_path, num_batteries=12)
        self.assertEqual(result, 3121910778619)


if __name__ == "__main__":
    unittest.main()
