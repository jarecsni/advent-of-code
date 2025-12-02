def solve_safe(filename, count_clicks=False):
    """
    Solve the safe dial puzzle.
    
    Args:
        filename: Path to file containing rotations (one per line, e.g., "L68" or "R48")
        count_clicks: If True, count every click through 0 during rotation (method 0x434C49434B)
                     If False, only count when dial ends on 0 after rotation
    
    Returns:
        Number of times the dial points at 0
    """
    position = 50
    count = 0
    
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            direction = line[0]
            distance = int(line[1:])
            step = -1 if direction == 'L' else 1
            
            # Always loop through each click
            for i in range(distance):
                position = (position + step) % 100
                # In click mode: count every zero
                # In normal mode: only count if this is the final position
                if position == 0:
                    if count_clicks or i == distance - 1:
                        count += 1
    
    return count


if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Solve the safe dial puzzle')
    parser.add_argument('input_file', help='Input file containing rotations')
    parser.add_argument('-countClickOverZero', action='store_true',
                       help='Use method 0x434C49434B: count every click through 0')
    
    args = parser.parse_args()
    
    password = solve_safe(args.input_file, count_clicks=args.countClickOverZero)
    print(f"Password: {password}")
