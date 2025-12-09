# Day 9: Movie Theater Tiles

## Problem Description

The movie theater has a tile floor with red tiles at specific coordinates. We need to find the largest rectangle that can be formed using two red tiles as opposite corners.

## Approach

This is a maximum rectangle problem with constraints:
1. Parse red tile coordinates from input
2. For each pair of red tiles, check if they can form opposite corners of a rectangle
3. Calculate the area of valid rectangles
4. Return the maximum area found

### Key Insight

For two tiles at positions (x1, y1) and (x2, y2) to be opposite corners of a rectangle, we simply need them to be different points. The rectangle area is:
```
area = |x2 - x1| × |y2 - y1|
```

The challenge is efficiently checking all pairs - with n red tiles, there are n(n-1)/2 pairs to check.

## Solution

- Part 1: Find largest rectangle area using any two red tiles as opposite corners
- Part 2: TBD

## Usage

```
python theater.py example.txt  # Test with example
python theater.py input.txt    # Solve puzzle
```
