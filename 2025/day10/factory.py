#!/usr/bin/env python3
"""
Day 10: Factory - Indicator Light Configuration

This problem is a system of linear equations over GF(2) (binary field).
Each button press toggles specific lights, and we need to find the minimum
number of presses to achieve the target configuration.
"""

import re
from typing import List, Tuple, Set
import numpy as np


def parse_machine(line: str) -> Tuple[List[int], List[List[int]]]:
    """
    Parse a machine specification line.
    
    Returns:
        target_state: List of 0s and 1s representing target light configuration
        buttons: List of button configurations, each being a list of light indices
    """
    # Extract indicator pattern [.##.]
    pattern_match = re.search(r'\[([.#]+)\]', line)
    if not pattern_match:
        raise ValueError(f"No indicator pattern found in line: {line}")
    
    pattern = pattern_match.group(1)
    target_state = [1 if c == '#' else 0 for c in pattern]
    
    # Extract button configurations (1,3) (2) etc.
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        if button_str.strip():  # Handle empty parentheses
            button_lights = [int(x) for x in button_str.split(',')]
            buttons.append(button_lights)
    
    return target_state, buttons


def solve_gf2_gaussian(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Solve using Gaussian elimination over GF(2).
    
    This is much faster for large systems but finds A solution, not necessarily 
    the minimum weight solution. For minimum weight, you'd need to enumerate
    the null space and find the minimum among all solutions.
    """
    num_lights = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return float('inf') if any(target) else 0
    
    # Create augmented matrix [A|b]
    augmented = np.zeros((num_lights, num_buttons + 1), dtype=int)
    
    # Fill coefficient matrix
    for button_idx, button_lights in enumerate(buttons):
        for light_idx in button_lights:
            if light_idx < num_lights:
                augmented[light_idx, button_idx] = 1
    
    # Fill target vector
    for i, val in enumerate(target):
        augmented[i, num_buttons] = val
    
    if debug:
        print("Initial augmented matrix:")
        print(augmented)
    
    # Gaussian elimination in GF(2)
    pivot_row = 0
    for col in range(num_buttons):
        # Find pivot
        pivot_found = False
        for row in range(pivot_row, num_lights):
            if augmented[row, col] == 1:
                # Swap rows if needed
                if row != pivot_row:
                    augmented[[pivot_row, row]] = augmented[[row, pivot_row]]
                pivot_found = True
                break
        
        if not pivot_found:
            continue
        
        # Eliminate column
        for row in range(num_lights):
            if row != pivot_row and augmented[row, col] == 1:
                # XOR rows (addition in GF(2))
                augmented[row] ^= augmented[pivot_row]
        
        pivot_row += 1
    
    if debug:
        print("After Gaussian elimination:")
        print(augmented)
    
    # Check for inconsistency
    for row in range(pivot_row, num_lights):
        if augmented[row, num_buttons] == 1:
            return -1  # No solution
    
    # Find pivot columns (basic variables)
    pivot_cols = []
    for row in range(min(pivot_row, num_buttons)):
        for col in range(num_buttons):
            if augmented[row, col] == 1:
                pivot_cols.append(col)
                break
    
    # Free variables are non-pivot columns
    free_vars = [col for col in range(num_buttons) if col not in pivot_cols]
    
    if debug:
        print(f"Pivot columns (basic variables): {pivot_cols}")
        print(f"Free variables: {free_vars}")
    
    # If no free variables, we have a unique solution
    if not free_vars:
        solution = np.zeros(num_buttons, dtype=int)
        for row in range(len(pivot_cols) - 1, -1, -1):
            pivot_col = pivot_cols[row]
            val = augmented[row, num_buttons]
            for col in range(pivot_col + 1, num_buttons):
                val ^= augmented[row, col] * solution[col]
            solution[pivot_col] = val
        
        if debug:
            print(f"Unique solution: {solution}")
        return sum(solution)
    
    # Multiple solutions exist - find minimum weight solution
    min_weight = float('inf')
    best_solution = None
    
    # Try all combinations of free variables (2^|free_vars|)
    for free_combo in range(2 ** len(free_vars)):
        solution = np.zeros(num_buttons, dtype=int)
        
        # Set free variables according to current combination
        for i, free_var in enumerate(free_vars):
            solution[free_var] = (free_combo >> i) & 1
        
        # Back substitute to find basic variables
        for row in range(len(pivot_cols) - 1, -1, -1):
            pivot_col = pivot_cols[row]
            val = augmented[row, num_buttons]
            for col in range(pivot_col + 1, num_buttons):
                val ^= augmented[row, col] * solution[col]
            solution[pivot_col] = val
        
        # Check weight of this solution
        weight = sum(solution)
        if weight < min_weight:
            min_weight = weight
            best_solution = solution.copy()
    
    if debug:
        print(f"Minimum weight solution: {best_solution} (weight: {min_weight})")
    
    return min_weight


def solve_gf2_system(target: List[int], buttons: List[List[int]]) -> int:
    """
    Solve the system of linear equations over GF(2) to find minimum button presses.
    
    This creates a matrix where:
    - Each row represents a light
    - Each column represents a button
    - Entry (i,j) is 1 if button j toggles light i
    
    We solve: A * x = target (mod 2)
    where x is the vector of button press counts (0 or 1 each)
    """
    num_lights = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        # No buttons available
        return float('inf') if any(target) else 0
    
    # Create the coefficient matrix
    matrix = np.zeros((num_lights, num_buttons), dtype=int)
    
    for button_idx, button_lights in enumerate(buttons):
        for light_idx in button_lights:
            if light_idx < num_lights:  # Bounds check
                matrix[light_idx, button_idx] = 1
    
    # Try all possible combinations of button presses (brute force for small cases)
    # Since we're in GF(2), each button is pressed either 0 or 1 times
    min_presses = float('inf')
    
    for combination in range(2 ** num_buttons):
        button_presses = [(combination >> i) & 1 for i in range(num_buttons)]
        
        # Calculate resulting light state
        result_state = np.zeros(num_lights, dtype=int)
        for button_idx, press_count in enumerate(button_presses):
            if press_count:
                for light_idx in buttons[button_idx]:
                    if light_idx < num_lights:
                        result_state[light_idx] ^= 1  # XOR toggle
        
        # Check if this matches target
        if np.array_equal(result_state, target):
            total_presses = sum(button_presses)
            min_presses = min(min_presses, total_presses)
    
    return min_presses if min_presses != float('inf') else -1





def parse_input(filename: str) -> List[str]:
    """Parse input file and return list of machine specifications."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def part1(data: List[str], debug: bool = False, use_gaussian: bool = False) -> int:
    """
    Solve part 1: Find minimum button presses for all machines.
    
    Args:
        data: List of machine specification strings
        debug: Whether to print debug information
        
    Returns:
        Total minimum button presses needed for all machines
    """
    total_presses = 0
    
    for i, line in enumerate(data):
        try:
            target_state, buttons = parse_machine(line)
            if use_gaussian:
                min_presses = solve_gf2_gaussian(target_state, buttons, debug)
            else:
                min_presses = solve_gf2_system(target_state, buttons)
            
            if min_presses == -1:
                if debug:
                    print(f"Machine {i+1}: No solution possible")
                return -1
            
            if debug:
                target_str = ''.join('#' if x else '.' for x in target_state)
                print(f"Machine {i+1}: {min_presses} presses (target: {target_str})")
            
            total_presses += min_presses
            
        except Exception as e:
            if debug:
                print(f"Error processing machine {i+1}: {e}")
            return -1
    
    return total_presses


def part2(data: List[str], debug: bool = False) -> int:
    """
    Solve part 2: (Not yet available - placeholder)
    
    Args:
        data: List of machine specification strings
        debug: Whether to print debug information
        
    Returns:
        Result for part 2
    """
    # Part 2 not yet available
    return 0


def main():
    """Main function with proper CLI interface."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Day 10: Factory - Configure indicator lights using minimum button presses")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("--part2", action="store_true",
                        help="Solve part 2 instead of part 1")
    parser.add_argument("-d", "--debug", action="store_true", 
                        help="Print debug information")
    parser.add_argument("-g", "--gaussian", action="store_true",
                        help="Use Gaussian elimination instead of brute force")
    
    args = parser.parse_args()
    
    try:
        data = parse_input(args.input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    if args.part2:
        result = part2(data, debug=args.debug)
        print(f"Part 2: {result}")
    else:
        result = part1(data, debug=args.debug, use_gaussian=args.gaussian)
        print(f"Part 1: {result}")


if __name__ == "__main__":
    main()