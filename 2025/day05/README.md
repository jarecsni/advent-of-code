# Day 5: Cafeteria

## Part One

The cafeteria's new inventory management system tracks ingredient freshness using ID ranges. Given a list of fresh ingredient ID ranges and a list of available ingredient IDs, determine how many available ingredients are fresh.

Fresh ID ranges are inclusive and can overlap. An ingredient ID is fresh if it falls within any range.

### Example

```
3-5 10-14 16-20 12-18

1 5 8 11 17 32
```

- ID 1: spoiled (not in any range)
- ID 5: fresh (in range 3-5)
- ID 8: spoiled
- ID 11: fresh (in range 10-14)
- ID 17: fresh (in ranges 16-20 and 12-18)
- ID 32: spoiled

Expected output: `3` fresh ingredients

## Part Two

[Part two description will go here]

## Solution

Run with:
```
python day05/cafeteria.py day05/example.txt
python day05/cafeteria.py day05/input.txt
```

Run tests:
```
python -m pytest day05/test_cafeteria.py -v
```
