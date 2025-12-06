#!/usr/bin/env python3
"""
Day 3: Lobby - Maximum Joltage Calculator

Finds the maximum two-digit joltage from each battery bank.
"""

import argparse
from itertools import combinations


def max_joltage(bank: str, num_batteries: int = 2) -> int:
    """
    Find the maximum joltage by selecting num_batteries from the bank.
    
    Strategy: To maximize the number, we want the largest possible digits
    in the leftmost positions. We greedily select digits from left to right,
    always choosing the largest available digit that still leaves enough
    digits remaining to complete our selection.
    
    Args:
        bank: String of digits representing battery joltages
        num_batteries: Number of batteries to turn on (default: 2)
        
    Returns:
        Maximum joltage possible
    """
    n = len(bank)
    result = []
    start = 0
    
    for position in range(num_batteries):
        # How many more digits do we need after this one?
        remaining_needed = num_batteries - position - 1
        # Latest position we can pick from (must leave enough digits after)
        latest_pos = n - remaining_needed - 1
        
        # Find the maximum digit in the valid range
        max_digit = max(bank[start:latest_pos + 1])
        # Find the first occurrence of this max digit
        idx = bank.index(max_digit, start)
        
        result.append(max_digit)
        start = idx + 1
    
    return int(''.join(result))


def solve(input_file: str, num_batteries: int = 2, debug: bool = False) -> int:
    """
    Calculate total output joltage from all battery banks.
    
    Args:
        input_file: Path to input file
        num_batteries: Number of batteries to turn on per bank (default: 2)
        debug: Whether to print debug information
        
    Returns:
        Total output joltage
    """
    total = 0
    
    with open(input_file) as f:
        lines = [line.strip() for line in f if line.strip()]
        
    print(f"Processing {len(lines)} battery banks (selecting {num_batteries} batteries each)...")
    
    for idx, bank in enumerate(lines, 1):
        max_jolts = max_joltage(bank, num_batteries)
        total += max_jolts
        
        if debug:
            print(f"Bank {idx}/{len(lines)}: {bank} -> {max_jolts}")
        else:
            print(f"Bank {idx}/{len(lines)}: {max_jolts}")
    
    return total


def main():
    parser = argparse.ArgumentParser(description="Day 3: Lobby - Maximum Joltage Calculator")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    parser.add_argument("--twelve", action="store_true", help="Part Two: Use 12 batteries instead of 2")
    
    args = parser.parse_args()
    
    num_batteries = 12 if args.twelve else 2
    result = solve(args.input_file, num_batteries, args.debug)
    print(f"\nTotal output joltage: {result}")


if __name__ == "__main__":
    main()
