# Day 6: Trash Compactor

## Problem Description

After jumping into a garbage chute, you find yourself in a garbage smasher with a magnetically sealed door. While waiting for a family of cephalopods to open it, you help the youngest with her math homework.

## The Challenge

Cephalopod math worksheets present problems in a unique horizontal format where:
- Problems are arranged side-by-side in columns
- Each problem has numbers stacked vertically
- The operation (* or +) appears at the bottom of each column
- Problems are separated by full columns of spaces
- Number alignment within columns can vary

### Example

```
123 328  51 64   45 64  387 23    6 98  215 314 *   +   *   +   
```

This represents four problems:
- `123 * 45 * 6 = 33210`
- `328 + 64 + 98 = 490`
- `51 * 387 * 215 = 4243455`
- `64 + 23 + 314 = 401`

Grand total: `33210 + 490 + 4243455 + 401 = 4277556`

## Task

Parse the worksheet, solve each problem, and calculate the grand total by summing all individual problem results.

## Approach

1. Parse input into a 2D grid
2. Identify problem boundaries (columns of spaces)
3. For each problem column:
   - Extract all numbers (ignoring alignment)
   - Find the operator at the bottom
   - Compute the result
4. Sum all results for the grand total
