def is_invalid_id(num, repeating_pattern=False):
    """
    Check if a number is an invalid ID.
    
    Args:
        num: Integer to check
        repeating_pattern: If True, check for pattern repeated at least twice (Part Two)
                          If False, check for pattern repeated exactly twice (Part One)
    
    Returns:
        True if invalid (repeated pattern), False otherwise
    """
    s = str(num)
    length = len(s)
    
    if repeating_pattern:
        # Check if string is made of a pattern repeated at least twice
        # Try all possible pattern lengths from 1 to length//2
        for pattern_len in range(1, length // 2 + 1):
            if length % pattern_len == 0:
                pattern = s[:pattern_len]
                repetitions = length // pattern_len
                if repetitions >= 2 and pattern * repetitions == s:
                    return True
        return False
    else:
        # Part One: must be even length and first half equals second half
        if length % 2 != 0:
            return False
        mid = length // 2
        return s[:mid] == s[mid:]


def solve_gift_shop(filename, verbose=False, debug=False, repeating_pattern=False):
    """
    Find sum of all invalid product IDs in given ranges.
    
    Args:
        filename: Path to file containing comma-separated ranges
        verbose: If True, print count of invalid IDs found
        debug: If True, print all invalid IDs found
        repeating_pattern: If True, use Part Two rules (pattern repeated at least twice)
    
    Returns:
        Sum of all invalid IDs
    """
    with open(filename) as f:
        line = f.read().strip()
    
    ranges = line.split(',')
    total = 0
    invalid_ids = []
    
    for range_str in ranges:
        start, end = map(int, range_str.split('-'))
        
        for num in range(start, end + 1):
            if is_invalid_id(num, repeating_pattern=repeating_pattern):
                total += num
                invalid_ids.append(num)
    
    if verbose:
        print(f"Found {len(invalid_ids)} invalid IDs")
    
    if debug:
        if repeating_pattern:
            # Separate into half-half patterns and other repeating patterns
            half_half = []
            other_patterns = []
            
            for id_num in invalid_ids:
                s = str(id_num)
                length = len(s)
                # Check if it's a half-half pattern
                if length % 2 == 0:
                    mid = length // 2
                    if s[:mid] == s[mid:]:
                        half_half.append(id_num)
                        continue
                other_patterns.append(id_num)
            
            print("Half-half patterns: " + ", ".join(f"[{i+1}] {id}" for i, id in enumerate(half_half)))
            print("Other repeating patterns: " + ", ".join(f"[{i+1}] {id}" for i, id in enumerate(other_patterns)))
        else:
            print(", ".join(f"[{i+1}] {id}" for i, id in enumerate(invalid_ids)))
    
    return total


if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Find invalid product IDs in gift shop')
    parser.add_argument('input_file', help='Input file containing ranges')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print count of invalid IDs')
    parser.add_argument('-d', '--debug', action='store_true', help='List all invalid IDs')
    parser.add_argument('--repeating-pattern', action='store_true', 
                       help='Use Part Two rules: pattern repeated at least twice')
    
    args = parser.parse_args()
    
    result = solve_gift_shop(args.input_file, verbose=args.verbose, debug=args.debug,
                            repeating_pattern=args.repeating_pattern)
    print(f"Sum of invalid IDs: {result}")
