#!/usr/bin/env python3
"""
Day 6: Trash Compactor - Cephalopod Math Worksheet Solver
"""

import argparse
import re
from functools import reduce
from operator import add, mul


def parse_worksheet(lines):
    """
    Parse the cephalopod math worksheet into problems.
    
    Args:
        lines: List of strings representing the worksheet rows
        
    Returns:
        List of tuples (numbers, operator) where numbers is a list of ints
    """
    # Split each line into tokens
    rows = [line.split() for line in lines]
    
    # The last row contains operators, previous rows contain numbers
    operator_row = rows[-1]
    number_rows = rows[:-1]
    
    # Transpose: group nth element from each row
    problems = []
    for i in range(len(operator_row)):
        numbers = [int(row[i]) for row in number_rows]
        operator = operator_row[i]
        problems.append((numbers, operator))
    
    return problems


def parse_worksheet_part2(lines):
    """
    Parse the cephalopod math worksheet for Part 2 (right-to-left column reading).
    
    Each number occupies a column, with most significant digit at top.
    We read digit columns top-to-bottom to form new numbers.
    
    Args:
        lines: List of strings representing the worksheet rows
        
    Returns:
        List of tuples (numbers, operator) where numbers is a list of ints
    """
    # Filter empty lines and strip newlines but preserve spaces
    rows = [line.rstrip('\n') for line in lines if line.strip()]
    
    # Pad all rows to same length
    max_len = max(len(r) for r in rows)
    rows_padded = [r.ljust(max_len) for r in rows]
    
    num_rows = rows[:-1]
    num_rows_padded = rows_padded[:-1]
    op_row = rows[-1]
    
    # Get tokens per row to identify problem boundaries
    tokens_per_row = [row.split() for row in num_rows]
    num_problems = len(tokens_per_row[0])
    
    # Find problem bounds (min start, max end across all rows for each problem)
    problem_bounds = []
    for prob_idx in range(num_problems):
        min_start = float('inf')
        max_end = 0
        
        for row_idx, row in enumerate(num_rows):
            token = tokens_per_row[row_idx][prob_idx]
            # Find position by skipping previous tokens
            pos = 0
            for t in tokens_per_row[row_idx][:prob_idx]:
                pos = row.find(t, pos) + len(t)
            token_start = row.find(token, pos)
            token_end = token_start + len(token)
            min_start = min(min_start, token_start)
            max_end = max(max_end, token_end)
        
        problem_bounds.append((min_start, max_end))
    
    # Find operators
    op_matches = [m.group() for m in re.finditer(r'[+*]', op_row)]
    
    # Process each problem
    problems = []
    for prob_idx, (start, end) in enumerate(problem_bounds):
        # Extract character matrix for this problem
        matrix = [row[start:end] for row in num_rows_padded]
        
        # Read digit columns top-to-bottom
        width = end - start
        new_numbers = []
        for c in range(width):
            digits = ''
            for row_chunk in matrix:
                char = row_chunk[c] if c < len(row_chunk) else ' '
                if char.isdigit():
                    digits += char
            if digits:
                new_numbers.append(int(digits))
        
        operator = op_matches[prob_idx]
        problems.append((new_numbers, operator))
    
    return problems


def solve_problem(numbers, operator):
    """
    Solve a single problem by applying the operator to all numbers.
    
    Args:
        numbers: List of integers
        operator: String ('+' or '*')
        
    Returns:
        Integer result of the operation
    """
    op_func = mul if operator == '*' else add
    return reduce(op_func, numbers)


def calculate_grand_total(input_file, debug=False, part2=False):
    """
    Calculate the grand total from the worksheet.
    
    Args:
        input_file: Path to the input file
        debug: Whether to print debug information
        part2: Whether to use Part 2 parsing (cephalopod column reading)
        
    Returns:
        Integer grand total
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    if part2:
        problems = parse_worksheet_part2(lines)
    else:
        # Part 1: strip lines for simple parsing
        lines = [line.rstrip('\n') for line in lines]
        problems = parse_worksheet(lines)
    
    results = []
    for numbers, operator in problems:
        result = solve_problem(numbers, operator)
        results.append(result)
        if debug:
            op_str = ' {} '.format(operator).join(map(str, numbers))
            print(f"{op_str} = {result}")
    
    grand_total = sum(results)
    
    if debug:
        print(f"\nGrand total: {' + '.join(map(str, results))} = {grand_total}")
    
    return grand_total


def main():
    parser = argparse.ArgumentParser(
        description="Day 6: Trash Compactor - Solve cephalopod math worksheets"
    )
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    parser.add_argument("-2", "--part2", action="store_true", help="Use Part 2 parsing (cephalopod column reading)")
    args = parser.parse_args()
    
    result = calculate_grand_total(args.input_file, args.debug, args.part2)
    print(f"\nGrand total: {result}")


if __name__ == "__main__":
    main()
