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


def part1(data: List[str], debug: bool = False) -> int:
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
    parser.add_argument("part", type=int, nargs="?", default=1, 
                        choices=[1, 2], help="Puzzle part (1 or 2, default: 1)")
    parser.add_argument("-d", "--debug", action="store_true", 
                        help="Print debug information")
    
    args = parser.parse_args()
    
    try:
        data = parse_input(args.input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    if args.part == 1:
        result = part1(data, debug=args.debug)
        print(f"Part 1: {result}")
    else:
        result = part2(data, debug=args.debug)
        print(f"Part 2: {result}")


if __name__ == "__main__":
    main()