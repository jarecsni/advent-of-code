#!/usr/bin/env python3
"""
Day 5: Cafeteria
Determine which ingredient IDs are fresh based on range specifications.

Part 1: Count how many available IDs are fresh
Part 2: Count total unique IDs covered by all ranges
"""

import argparse


def parse_input(filename):
    """Parse the input file and return ranges and available IDs."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    # Split on blank line
    parts = content.split('\n\n')
    
    # Parse ranges from first part
    ranges = []
    for range_spec in parts[0].split():
        start, end = map(int, range_spec.split('-'))
        ranges.append((start, end))
    
    # Parse available IDs from second part
    available_ids = list(map(int, parts[1].split()))
    
    return ranges, available_ids


def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID falls within any fresh range."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def solve_part_one(data, debug=False):
    """Count how many available ingredient IDs are fresh."""
    ranges, available_ids = data
    
    if debug:
        print(f"Fresh ranges: {ranges}")
        print(f"Available IDs: {available_ids}")
    
    fresh_count = 0
    for ingredient_id in available_ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1
            if debug:
                print(f"  ID {ingredient_id}: fresh")
        elif debug:
            print(f"  ID {ingredient_id}: spoiled")
    
    return fresh_count


def merge_ranges(ranges):
    """Merge overlapping ranges and return total count of unique IDs."""
    if not ranges:
        return 0
    
    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    
    # Merge overlapping ranges
    merged = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        # If current range overlaps or is adjacent to last merged range
        if start <= last_end + 1:
            # Extend the last merged range
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap, add as new range
            merged.append((start, end))
    
    # Count total IDs in merged ranges
    total = sum(end - start + 1 for start, end in merged)
    return total


def solve_part_two(data, debug=False):
    """Count total unique ingredient IDs considered fresh by the ranges."""
    ranges, available_ids = data
    
    if debug:
        print(f"Processing {len(ranges)} ranges...")
        print(f"Sample ranges: {ranges[:3]}")
    
    total_fresh = merge_ranges(ranges)
    
    if debug:
        print(f"Total unique fresh IDs: {total_fresh}")
    
    return total_fresh


def main():
    parser = argparse.ArgumentParser(
        description="Day 5: Cafeteria - Determine fresh ingredient IDs"
    )
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("-d", "--debug", action="store_true", 
                       help="Print debug information")
    parser.add_argument("--part-two", action="store_true",
                       help="Solve part two instead of part one")
    args = parser.parse_args()
    
    data = parse_input(args.input_file)
    
    if args.part_two:
        result = solve_part_two(data, args.debug)
        print(f"\nPart Two Result: {result}")
    else:
        result = solve_part_one(data, args.debug)
        print(f"\nPart One Result: {result}")


if __name__ == "__main__":
    main()
