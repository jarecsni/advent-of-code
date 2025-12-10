#!/usr/bin/env python3
"""
Tests for Day 10: Factory solution
"""

import pytest
from factory import parse_machine, solve_gf2_system, part1, parse_input


def test_parse_machine():
    """Test parsing of machine specifications."""
    line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    target, buttons = parse_machine(line)
    
    assert target == [0, 1, 1, 0]
    assert buttons == [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]


def test_solve_gf2_system_example1():
    """Test first example machine."""
    target = [0, 1, 1, 0]  # [.##.]
    buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    
    result = solve_gf2_system(target, buttons)
    assert result == 2


def test_solve_gf2_system_example2():
    """Test second example machine."""
    target = [0, 0, 0, 1, 0]  # [...#.]
    buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
    
    result = solve_gf2_system(target, buttons)
    assert result == 3


def test_solve_gf2_system_example3():
    """Test third example machine."""
    target = [0, 1, 1, 1, 0, 1]  # [.###.#]
    buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
    
    result = solve_gf2_system(target, buttons)
    assert result == 2


def test_solve_factory_example():
    """Test complete example solution."""
    data = parse_input('example.txt')
    result = part1(data)
    assert result == 7


def test_impossible_case():
    """Test case where no solution exists."""
    target = [1, 0]  # Need first light on, second off
    buttons = [[1]]   # Only button toggles second light
    
    result = solve_gf2_system(target, buttons)
    assert result == -1


def test_trivial_case():
    """Test case where target is already achieved."""
    target = [0, 0, 0]  # All lights off (initial state)
    buttons = [[0], [1], [2]]
    
    result = solve_gf2_system(target, buttons)
    assert result == 0


if __name__ == "__main__":
    # Run tests manually if pytest not available
    test_parse_machine()
    test_solve_gf2_system_example1()
    test_solve_gf2_system_example2()
    test_solve_gf2_system_example3()
    test_solve_factory_example()
    test_impossible_case()
    test_trivial_case()
    print("All tests passed!")