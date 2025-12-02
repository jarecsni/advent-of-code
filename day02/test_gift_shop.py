import unittest
from gift_shop import is_invalid_id, solve_gift_shop
import tempfile
import os


class TestIsInvalidId(unittest.TestCase):
    """Test the is_invalid_id function for both Part One and Part Two rules."""
    
    def test_part_one_valid_ids(self):
        """Test that valid IDs are not flagged in Part One."""
        valid_ids = [12, 123, 1234, 101, 1001, 12345]
        for id_num in valid_ids:
            with self.subTest(id=id_num):
                self.assertFalse(is_invalid_id(id_num, repeating_pattern=False))
    
    def test_part_one_invalid_ids_two_digit(self):
        """Test two-digit repeating patterns."""
        invalid_ids = [11, 22, 33, 44, 55, 66, 77, 88, 99]
        for id_num in invalid_ids:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=False))
    
    def test_part_one_invalid_ids_four_digit(self):
        """Test four-digit repeating patterns."""
        invalid_ids = [1010, 6464, 1212, 9999]
        for id_num in invalid_ids:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=False))
    
    def test_part_one_invalid_ids_six_digit(self):
        """Test six-digit repeating patterns."""
        invalid_ids = [123123, 456456, 999999]
        for id_num in invalid_ids:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=False))
    
    def test_part_one_invalid_ids_from_spec(self):
        """Test specific examples from the problem specification."""
        spec_examples = [11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859]
        for id_num in spec_examples:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=False))
    
    def test_part_one_odd_length_always_valid(self):
        """Test that odd-length numbers are always valid in Part One."""
        odd_length_ids = [111, 123, 12345, 999, 1234567]
        for id_num in odd_length_ids:
            with self.subTest(id=id_num):
                self.assertFalse(is_invalid_id(id_num, repeating_pattern=False))
    
    def test_part_two_triple_repeats(self):
        """Test patterns repeated three times."""
        triple_repeats = [111, 222, 333, 999, 123123123]
        for id_num in triple_repeats:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=True))
    
    def test_part_two_five_repeats(self):
        """Test patterns repeated five times."""
        five_repeats = [11111, 55555, 1212121212]
        for id_num in five_repeats:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=True))
    
    def test_part_two_seven_repeats(self):
        """Test patterns repeated seven times."""
        self.assertTrue(is_invalid_id(1111111, repeating_pattern=True))
        self.assertTrue(is_invalid_id(7777777, repeating_pattern=True))
    
    def test_part_two_includes_part_one_patterns(self):
        """Test that Part Two rules include all Part One patterns."""
        part_one_patterns = [11, 22, 6464, 123123, 1010, 446446]
        for id_num in part_one_patterns:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=True))
    
    def test_part_two_from_spec(self):
        """Test specific examples from Part Two specification."""
        spec_examples = [
            111, 999, 565656, 824824824, 2121212121,
            12341234, 123123123, 1212121212, 1111111
        ]
        for id_num in spec_examples:
            with self.subTest(id=id_num):
                self.assertTrue(is_invalid_id(id_num, repeating_pattern=True))
    
    def test_part_two_valid_ids(self):
        """Test that non-repeating patterns are valid in Part Two."""
        valid_ids = [12, 123, 1234, 12345, 123456, 1234567]
        for id_num in valid_ids:
            with self.subTest(id=id_num):
                self.assertFalse(is_invalid_id(id_num, repeating_pattern=True))
    
    def test_edge_case_single_digit(self):
        """Test single-digit numbers (should be valid)."""
        for i in range(10):
            with self.subTest(id=i):
                self.assertFalse(is_invalid_id(i, repeating_pattern=False))
                self.assertFalse(is_invalid_id(i, repeating_pattern=True))


class TestSolveGiftShop(unittest.TestCase):
    """Test the solve_gift_shop function with example data."""
    
    def setUp(self):
        """Create temporary test files."""
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary test files."""
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def create_test_file(self, content):
        """Helper to create a temporary test file."""
        fd, path = tempfile.mkstemp(dir=self.test_dir, text=True)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    def test_part_one_example(self):
        """Test Part One with the example from the specification."""
        example_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
        test_file = self.create_test_file(example_input)
        
        result = solve_gift_shop(test_file, repeating_pattern=False)
        self.assertEqual(result, 1227775554)
    
    def test_part_two_example(self):
        """Test Part Two with the example from the specification."""
        example_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
        test_file = self.create_test_file(example_input)
        
        result = solve_gift_shop(test_file, repeating_pattern=True)
        self.assertEqual(result, 4174379265)
    
    def test_single_range_part_one(self):
        """Test with a single range."""
        test_file = self.create_test_file("11-22")
        result = solve_gift_shop(test_file, repeating_pattern=False)
        self.assertEqual(result, 11 + 22)
    
    def test_single_range_part_two(self):
        """Test with a single range in Part Two mode."""
        test_file = self.create_test_file("95-115")
        result = solve_gift_shop(test_file, repeating_pattern=True)
        self.assertEqual(result, 99 + 111)
    
    def test_range_with_no_invalid_ids(self):
        """Test a range that contains no invalid IDs."""
        test_file = self.create_test_file("1698522-1698528")
        result = solve_gift_shop(test_file, repeating_pattern=False)
        self.assertEqual(result, 0)
    
    def test_multiple_ranges(self):
        """Test with multiple ranges."""
        test_file = self.create_test_file("11-22,95-115")
        result = solve_gift_shop(test_file, repeating_pattern=False)
        self.assertEqual(result, 11 + 22 + 99)
    
    def test_range_boundaries(self):
        """Test that range boundaries are inclusive."""
        test_file = self.create_test_file("11-11")
        result = solve_gift_shop(test_file, repeating_pattern=False)
        self.assertEqual(result, 11)


class TestPatternRecognition(unittest.TestCase):
    """Test specific pattern recognition edge cases."""
    
    def test_six_digit_patterns(self):
        """Test 6-digit patterns that can be interpreted multiple ways."""
        # 565656 can be seen as 56 repeated 3 times OR 565 repeated 2 times
        self.assertTrue(is_invalid_id(565656, repeating_pattern=True))
        # In Part One, it's not a half-half pattern
        self.assertFalse(is_invalid_id(565656, repeating_pattern=False))
    
    def test_ten_digit_patterns(self):
        """Test 10-digit patterns."""
        # 5757575757 is 57 repeated 5 times
        self.assertTrue(is_invalid_id(5757575757, repeating_pattern=True))
        # Not a half-half pattern
        self.assertFalse(is_invalid_id(5757575757, repeating_pattern=False))
    
    def test_nine_digit_triple_patterns(self):
        """Test 9-digit patterns repeated 3 times."""
        self.assertTrue(is_invalid_id(714714714, repeating_pattern=True))
        self.assertTrue(is_invalid_id(531531531, repeating_pattern=True))
        # Not half-half patterns
        self.assertFalse(is_invalid_id(714714714, repeating_pattern=False))
        self.assertFalse(is_invalid_id(531531531, repeating_pattern=False))


if __name__ == '__main__':
    unittest.main()
