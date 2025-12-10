# Day 10: Factory

## Problem Summary

Factory machines need initialization by configuring indicator lights to match specific patterns. Each machine has:
- Indicator light diagram showing target state (`.` = off, `#` = on)
- Button wiring schematics showing which lights each button toggles
- Joltage requirements (ignored for this problem)

Goal: Find minimum button presses to configure all machines correctly.

## Approach

This is a system of linear equations over GF(2) (binary field):
- Each light state is binary (0/1)
- Each button press toggles specific lights (XOR operation)
- Need to solve for minimum number of button presses

## Examples

```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```
- 4 lights, target: [0,1,1,0]
- Buttons toggle: [3], [1,3], [2], [2,3], [0,2], [0,1]
- Minimum presses: 2

## Solution Strategy

1. Parse input to extract light patterns and button mappings
2. Set up system of linear equations in GF(2)
3. Use Gaussian elimination to find solution
4. Sum minimum presses across all machines