def parse_grid(text):
    """Parse input text into a 2D grid."""
    return [list(line) for line in text.strip().split('\n')]


def count_neighbors(grid, row, col):
    """Count how many of the 8 adjacent positions contain '@'."""
    rows, cols = len(grid), len(grid[0])
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # NW, N, NE
        (0, -1),           (0, 1),    # W, E
        (1, -1),  (1, 0),  (1, 1)     # SW, S, SE
    ]
    
    count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '@':
            count += 1
    
    return count


def count_accessible_rolls(grid):
    """Count rolls with fewer than 4 neighbors."""
    accessible = 0
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                neighbors = count_neighbors(grid, row, col)
                if neighbors < 4:
                    accessible += 1
    
    return accessible


def find_accessible_rolls(grid):
    """
    Find all rolls that are currently accessible (< 4 neighbors).
    
    Returns:
        List of (row, col) tuples for accessible rolls
    """
    accessible = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                neighbors = count_neighbors(grid, row, col)
                if neighbors < 4:
                    accessible.append((row, col))
    return accessible


def remove_accessible_rolls(grid, debug=False):
    """
    Repeatedly remove accessible rolls until no more can be removed.
    
    Args:
        grid: 2D grid (will be modified in place)
        debug: Whether to print debug information
        
    Returns:
        Total number of rolls removed
    """
    total_removed = 0
    iteration = 0
    
    while True:
        accessible = find_accessible_rolls(grid)
        
        if not accessible:
            break
        
        iteration += 1
        count = len(accessible)
        total_removed += count
        
        if debug:
            print(f"Iteration {iteration}: Removing {count} rolls")
        
        # Remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'
    
    return total_removed


def solve(input_file, remove_all=False, debug=False):
    """
    Solve the puzzle for the given input file.
    
    Args:
        input_file: Path to input file
        remove_all: If True, repeatedly remove accessible rolls (Part Two)
        debug: Whether to print debug information
        
    Returns:
        Number of accessible rolls (Part One) or total removed (Part Two)
    """
    with open(input_file) as f:
        text = f.read()
    
    grid = parse_grid(text)
    
    if debug:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
    
    if remove_all:
        if debug:
            print("Part Two: Removing all accessible rolls iteratively...")
        return remove_accessible_rolls(grid, debug)
    else:
        if debug:
            print("Part One: Counting accessible rolls...")
        return count_accessible_rolls(grid)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Day 4: Printing Department - Accessible Roll Counter")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
    parser.add_argument("--remove-all", action="store_true", help="Part Two: Repeatedly remove accessible rolls")
    
    args = parser.parse_args()
    
    result = solve(args.input_file, args.remove_all, args.debug)
    
    if args.remove_all:
        print(f"\nTotal rolls removed: {result}")
    else:
        print(f"\nAccessible rolls: {result}")


if __name__ == '__main__':
    main()
