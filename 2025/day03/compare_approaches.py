#!/usr/bin/env python3
"""
Compare different approaches to the battery selection problem
"""

def greedy_leftmost(bank: str, num_batteries: int) -> str:
    """Current approach: greedily pick best digit for each position left-to-right"""
    n = len(bank)
    result = []
    start = 0
    
    for position in range(num_batteries):
        remaining_needed = num_batteries - position - 1
        latest_pos = n - remaining_needed - 1
        max_digit = max(bank[start:latest_pos + 1])
        idx = bank.index(max_digit, start)
        result.append(max_digit)
        start = idx + 1
    
    return ''.join(result)


def pick_n_largest(bank: str, num_batteries: int) -> str:
    """Alternative: pick the n largest digits, maintaining their order"""
    # Create list of (digit, original_index)
    indexed = [(digit, i) for i, digit in enumerate(bank)]
    # Sort by digit descending, then by index ascending (to break ties)
    indexed.sort(key=lambda x: (-ord(x[0]), x[1]))
    # Take the n largest
    selected = indexed[:num_batteries]
    # Sort by original index to maintain order
    selected.sort(key=lambda x: x[1])
    # Extract just the digits
    return ''.join(d for d, _ in selected)


# Test cases
test_cases = [
    ("987654321111111", 12, "987654321111"),
    ("811111111111119", 12, "811111111119"),
    ("234234234234278", 12, "434234234278"),
    ("818181911112111", 12, "888911112111"),
    ("234234234234278", 2, "78"),
    ("543219876", 4, None),  # Don't know expected
    ("918273645", 4, None),
]

print("Comparing approaches:\n")
print("=" * 80)

for bank, n, expected in test_cases:
    greedy = greedy_leftmost(bank, n)
    largest = pick_n_largest(bank, n)
    
    print(f"\nBank: {bank}")
    print(f"Pick: {n} digits")
    if expected:
        print(f"Expected:        {expected}")
    print(f"Greedy leftmost: {greedy}")
    print(f"Pick n largest:  {largest}")
    
    if greedy != largest:
        print(f"  ⚠️  DIFFERENT! Greedy: {int(greedy)}, Largest: {int(largest)}")
        if int(greedy) > int(largest):
            print(f"  ✓ Greedy wins")
        else:
            print(f"  ✗ Largest wins")
    else:
        print(f"  ✓ Same result")
    
    if expected and greedy != expected:
        print(f"  ❌ Greedy doesn't match expected!")
    if expected and largest != expected:
        print(f"  ❌ Largest doesn't match expected!")

print("\n" + "=" * 80)
