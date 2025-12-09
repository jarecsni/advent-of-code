---
inclusion: always
---

# Advent of Code Project Standards

## Workflow for New Day Solutions

### Phase 1: Setup and Discussion
When receiving a new day's problem:
1. Create the day folder structure
2. **CRITICAL: Update the master README (`2025/README.md`) with the new day** - DO NOT SKIP THIS
3. Create the day's README with the problem description
4. Create placeholder files (example.txt, input.txt, solution.py, test_solution.py)
5. **STOP and discuss the problem with Cooper before implementing**
   - Analyse the problem structure
   - Discuss potential approaches
   - Consider edge cases and complexity
   - Agree on the solution strategy

**REMINDER:** Always update the master README in step 2. This is mandatory and must not be forgotten.

### Phase 2: Implementation
After discussing and agreeing on the approach, proceed with implementation.

## When Creating New Day Solutions

Every new day solution MUST include:

### 1. Update Master README
- Add the new day to the structure section in `README.md`
- Include a brief one-line description of the puzzle

### 2. CLI Interface with sys.argv or argparse
- **REQUIRED:** Support part selection via command-line argument
- **REQUIRED:** Include `-d` or `--debug` flag for verbose debugging output
- Accept `input_file` as first positional argument
- Accept `part` (1 or 2) as second positional argument, defaulting to 1
- Separate `part1()` and `part2()` functions for each puzzle part
- **Simple scripts:** Use `sys.argv` for straightforward input file + part selection
- **Complex scripts:** Use `argparse` for multiple flags and options (recommended when debug flag is needed)
- Provide clear usage message when arguments are missing

Debug output should include:
- Intermediate calculation steps
- Key data structure states
- Algorithm progress for long-running operations
- Validation of assumptions or constraints
- Timing information for performance analysis

Simple example (sys.argv) - STANDARD PATTERN:
```
def part1(data):
    """Solve part 1."""
    # Implementation
    return result

def part2(data):
    """Solve part 2."""
    # Implementation
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python solution.py <input_file> [part]")
        print("  part: 1 or 2 (default: 1)")
        sys.exit(1)
    
    filename = sys.argv[1]
    part = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    data = parse_input(filename)
    
    if part == 1:
        result = part1(data)
        print(f"Part 1: {result}")
    elif part == 2:
        result = part2(data)
        print(f"Part 2: {result}")
    else:
        print(f"Invalid part: {part}")
        sys.exit(1)
```

Complex example (argparse) - RECOMMENDED PATTERN:
```
def main():
    parser = argparse.ArgumentParser(description="Day X: Title - Description")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("part", type=int, nargs="?", default=1, 
                        choices=[1, 2], help="Puzzle part (1 or 2, default: 1)")
    parser.add_argument("-d", "--debug", action="store_true", 
                        help="Print debug information")
    args = parser.parse_args()
    
    data = parse_input(args.input_file)
    
    if args.part == 1:
        result = part1(data, debug=args.debug)
        print(f"Part 1: {result}")
    else:
        result = part2(data, debug=args.debug)
        print(f"Part 2: {result}")
```

### 3. Comprehensive Test Suite
- Create `test_<module>.py` with unittest
- Test individual functions with multiple cases
- Test edge cases and boundary conditions
- Test with the example input file
- Aim for thorough coverage of the logic

Test structure:
- One test class per function
- Descriptive test method names
- Include docstrings explaining what's being tested
- Test the example file result as integration test

### 4. File Structure
Each day directory should contain:
- `README.md` - Problem description and examples
- `<solution>.py` - Main solution with CLI interface
- `test_<solution>.py` - Comprehensive test suite
- `example.txt` - Example input from puzzle
- `input.txt` - Actual puzzle input (or placeholder)

## Running Solutions

Solutions should be runnable with input file as argument:
```
python dayXX/<solution>.py example.txt
python dayXX/<solution>.py input.txt
python dayXX/<solution>.py example.txt 10  # with optional parameter
```

Or from parent directory:
```
python dayXX/<solution>.py dayXX/example.txt
```

Tests should be runnable as:
```
python -m pytest dayXX/test_<solution>.py -v
```
