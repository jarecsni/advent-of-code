#!/usr/bin/env python3
"""Day 9: Movie Theater Tiles - Find largest rectangle between red tiles."""

import argparse
from itertools import combinations


def parse_tiles(filename):
    """Parse red tile coordinates from input file."""
    tiles = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                x, y = map(int, line.split(','))
                tiles.append((x, y))
    return tiles


def find_largest_rectangle(tiles, debug=False):
    """Find the largest rectangle area using any two tiles as opposite corners."""
    max_area = 0
    best_pair = None
    total_pairs = len(tiles) * (len(tiles) - 1) // 2
    
    if debug:
        print(f"\nChecking {total_pairs} tile pairs...")
        print(f"Tile coordinate ranges: x=[{min(t[0] for t in tiles)}, {max(t[0] for t in tiles)}], "
              f"y=[{min(t[1] for t in tiles)}, {max(t[1] for t in tiles)}]")
    
    # Check all pairs of tiles
    # Area includes both corner tiles, so add 1 to each dimension
    for i, ((x1, y1), (x2, y2)) in enumerate(combinations(tiles, 2)):
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        area = width * height
        
        if area > max_area:
            max_area = area
            best_pair = ((x1, y1), (x2, y2))
            if debug:
                print(f"  New max at pair {i+1}: ({x1},{y1}) to ({x2},{y2}) = {width}×{height} = {area}")
    
    if debug and best_pair:
        (x1, y1), (x2, y2) = best_pair
        print(f"\nBest rectangle: ({x1},{y1}) to ({x2},{y2})")
        print(f"  Width: {abs(x2-x1)+1}, Height: {abs(y2-y1)+1}, Area: {max_area}")
    
    return max_area


def part1(tiles, debug=False):
    """Solve part 1: Find largest rectangle area."""
    return find_largest_rectangle(tiles, debug=debug)


def build_polygon_boundary(tiles):
    """Build set of all tiles on the polygon boundary (red tiles + green connecting tiles)."""
    boundary = set(tiles)
    
    # Connect consecutive red tiles with straight lines of green tiles
    for i in range(len(tiles)):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % len(tiles)]  # Wrap around to first tile
        
        # Add all tiles between these two red tiles
        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                boundary.add((x1, y))
        elif y1 == y2:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                boundary.add((x, y1))
    
    return boundary


def point_in_polygon(x, y, polygon_vertices):
    """Check if point (x, y) is inside polygon using ray casting algorithm."""
    n = len(polygon_vertices)
    inside = False
    
    p1x, p1y = polygon_vertices[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def find_interior_point(tiles, boundary):
    """Find a point that's definitely inside the polygon."""
    # Use centroid of red tiles as starting point
    cx = sum(t[0] for t in tiles) // len(tiles)
    cy = sum(t[1] for t in tiles) // len(tiles)
    
    # If centroid is not on boundary, it's likely inside
    if (cx, cy) not in boundary and point_in_polygon(cx, cy, tiles):
        return (cx, cy)
    
    # Otherwise, search near centroid
    for dx in range(-100, 101):
        for dy in range(-100, 101):
            x, y = cx + dx, cy + dy
            if (x, y) not in boundary and point_in_polygon(x, y, tiles):
                return (x, y)
    
    return None


def flood_fill_interior(start, boundary, tiles):
    """Flood fill from interior point to find all interior tiles."""
    interior = set()
    queue = [start]
    visited = {start}
    
    while queue:
        x, y = queue.pop(0)
        interior.add((x, y))
        
        # Check 4 neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and (nx, ny) not in boundary:
                # Verify it's actually inside (boundary check might miss some)
                if point_in_polygon(nx, ny, tiles):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    
    return interior


def build_valid_tiles(tiles, debug=False):
    """Build set of all valid tiles (red + green boundary + green interior)."""
    # Start with boundary tiles
    boundary = build_polygon_boundary(tiles)
    
    if debug:
        print(f"Boundary has {len(boundary)} tiles")
    
    # Find an interior point and flood fill from it
    if debug:
        print(f"Finding interior point...")
    
    interior_start = find_interior_point(tiles, boundary)
    
    if interior_start is None:
        if debug:
            print(f"No interior found - polygon might be just the boundary")
        return boundary
    
    if debug:
        print(f"Starting flood fill from {interior_start}...")
    
    interior = flood_fill_interior(interior_start, boundary, tiles)
    
    if debug:
        print(f"Found {len(interior)} interior tiles")
    
    valid_tiles = boundary | interior
    
    if debug:
        print(f"Total valid tiles (red + green): {len(valid_tiles)}")
    
    return valid_tiles


def is_rectangle_valid(x1, y1, x2, y2, valid_tiles):
    """Check if all tiles in rectangle are valid (optimized)."""
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    
    # For small rectangles, check every tile
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    
    if width * height <= 10000:  # Threshold for full check
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) not in valid_tiles:
                    return False
        return True
    
    # For large rectangles, check perimeter first (fast rejection)
    # Check top and bottom edges
    for x in range(min_x, max_x + 1):
        if (x, min_y) not in valid_tiles or (x, max_y) not in valid_tiles:
            return False
    
    # Check left and right edges
    for y in range(min_y + 1, max_y):
        if (min_x, y) not in valid_tiles or (max_x, y) not in valid_tiles:
            return False
    
    # Sample interior points (if perimeter is valid, sample to verify interior)
    sample_rate = max(1, min(width, height) // 20)  # Sample every N tiles
    for x in range(min_x + sample_rate, max_x, sample_rate):
        for y in range(min_y + sample_rate, max_y, sample_rate):
            if (x, y) not in valid_tiles:
                return False
    
    return True


def find_largest_valid_rectangle(tiles, valid_tiles, debug=False):
    """Find largest rectangle using only red/green tiles."""
    max_area = 0
    best_pair = None
    total_pairs = len(tiles) * (len(tiles) - 1) // 2
    
    if debug:
        print(f"\nChecking {total_pairs} tile pairs for valid rectangles...")
    
    checked = 0
    valid_count = 0
    skipped = 0
    
    for i, ((x1, y1), (x2, y2)) in enumerate(combinations(tiles, 2)):
        checked += 1
        
        # Calculate potential area
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        area = width * height
        
        # Skip if this can't beat current max
        if area <= max_area:
            skipped += 1
            continue
        
        # Check if rectangle is valid
        if is_rectangle_valid(x1, y1, x2, y2, valid_tiles):
            valid_count += 1
            
            if area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2))
                if debug:
                    print(f"  New max at pair {i+1}: ({x1},{y1}) to ({x2},{y2}) = {width}×{height} = {area}")
    
    if debug:
        print(f"\nChecked {checked} pairs, skipped {skipped}, {valid_count} were valid")
        if best_pair:
            (x1, y1), (x2, y2) = best_pair
            print(f"Best valid rectangle: ({x1},{y1}) to ({x2},{y2})")
            print(f"  Width: {abs(x2-x1)+1}, Height: {abs(y2-y1)+1}, Area: {max_area}")
    
    return max_area


def is_rectangle_valid_lazy(x1, y1, x2, y2, boundary, tiles):
    """Check if rectangle is valid without precomputing all interior tiles."""
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    
    # Sample points in the rectangle
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    
    # For small rectangles, check every point
    if width * height <= 1000:
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) not in boundary and not point_in_polygon(x, y, tiles):
                    return False
        return True
    
    # For large rectangles, sample strategically
    # Check corners
    for x in [min_x, max_x]:
        for y in [min_y, max_y]:
            if (x, y) not in boundary and not point_in_polygon(x, y, tiles):
                return False
    
    # Check edges
    step = max(1, min(width, height) // 50)
    for x in range(min_x, max_x + 1, step):
        for y in [min_y, max_y]:
            if (x, y) not in boundary and not point_in_polygon(x, y, tiles):
                return False
    
    for y in range(min_y, max_y + 1, step):
        for x in [min_x, max_x]:
            if (x, y) not in boundary and not point_in_polygon(x, y, tiles):
                return False
    
    # Sample interior
    for x in range(min_x, max_x + 1, step):
        for y in range(min_y, max_y + 1, step):
            if (x, y) not in boundary and not point_in_polygon(x, y, tiles):
                return False
    
    return True


def find_largest_valid_rectangle_lazy(tiles, boundary, debug=False):
    """Find largest rectangle without precomputing all interior tiles."""
    max_area = 0
    best_pair = None
    total_pairs = len(tiles) * (len(tiles) - 1) // 2
    
    if debug:
        print(f"\nChecking {total_pairs} tile pairs for valid rectangles...")
    
    checked = 0
    valid_count = 0
    skipped = 0
    
    for i, ((x1, y1), (x2, y2)) in enumerate(combinations(tiles, 2)):
        checked += 1
        
        if debug and checked % 10000 == 0:
            print(f"  Progress: {checked}/{total_pairs} pairs checked...")
        
        # Calculate potential area
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        area = width * height
        
        # Skip if this can't beat current max
        if area <= max_area:
            skipped += 1
            continue
        
        # Check if rectangle is valid
        if is_rectangle_valid_lazy(x1, y1, x2, y2, boundary, tiles):
            valid_count += 1
            
            if area > max_area:
                max_area = area
                best_pair = ((x1, y1), (x2, y2))
                if debug:
                    print(f"  New max at pair {i+1}: ({x1},{y1}) to ({x2},{y2}) = {width}×{height} = {area}")
    
    if debug:
        print(f"\nChecked {checked} pairs, skipped {skipped}, {valid_count} were valid")
        if best_pair:
            (x1, y1), (x2, y2) = best_pair
            print(f"Best valid rectangle: ({x1},{y1}) to ({x2},{y2})")
            print(f"  Width: {abs(x2-x1)+1}, Height: {abs(y2-y1)+1}, Area: {max_area}")
    
    return max_area


def part2(tiles, debug=False):
    """Solve part 2: Find largest rectangle using only red and green tiles."""
    boundary = build_polygon_boundary(tiles)
    if debug:
        print(f"Boundary has {len(boundary)} tiles")
    return find_largest_valid_rectangle_lazy(tiles, boundary, debug=debug)


def main():
    parser = argparse.ArgumentParser(
        description="Day 9: Movie Theater Tiles - Find largest rectangle between red tiles"
    )
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument(
        "part",
        type=int,
        nargs="?",
        default=1,
        choices=[1, 2],
        help="Puzzle part (1 or 2, default: 1)",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Print debug information"
    )
    args = parser.parse_args()
    
    tiles = parse_tiles(args.input_file)
    print(f"Found {len(tiles)} red tiles")
    
    if args.part == 1:
        result = part1(tiles, debug=args.debug)
        print(f"\nPart 1: Largest rectangle area = {result}")
    else:
        result = part2(tiles, debug=args.debug)
        print(f"\nPart 2: {result}")


if __name__ == "__main__":
    main()
