---
inclusion: always
---

# Advent of Code Project Standards

## Workflow for New Day Solutions

### Phase 1: Setup and Discussion
When receiving a new day's problem:
1. Create the day folder structure
2. Update the master README with the new day
3. Create the day's README with the problem description
4. Create placeholder files (example.txt, input.txt, solution.py, test_solution.py)
5. **STOP and discuss the problem with Cooper before implementing**
   - Analyse the problem structure
   - Discuss potential approaches
   - Consider edge cases and complexity
   - Agree on the solution strategy

### Phase 2: Implementation
After discussing and agreeing on the approach, proceed with implementation.

## When Creating New Day Solutions

Every new day solution MUST include:

### 1. Update Master README
- Add the new day to the structure section in `README.md`
- Include a brief one-line description of the puzzle

### 2. CLI Interface with argparse
- Use `argparse` for command-line argument parsing
- Accept `input_file` as a positional argument
- Include `-d/--debug` flag for verbose output
- Add any puzzle-specific flags (e.g., `--twelve` for part two variations)
- Follow the pattern from day03/lobby.py

Example structure:
```
def main():
    parser = argparse.ArgumentParser(description="Day X: Title - Description")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    args = parser.parse_args()
    
    result = solve(args.input_file, args.debug)
    print(f"\nResult: {result}")
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

Solutions should be runnable as:
```
python dayXX/<solution>.py dayXX/example.txt
python dayXX/<solution>.py dayXX/input.txt -d
```

Tests should be runnable as:
```
python -m pytest dayXX/test_<solution>.py -v
```
