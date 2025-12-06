#!/usr/bin/env python3
"""
Visual demonstration of the greedy battery selection algorithm
"""

def visualize_selection(bank: str, num_batteries: int):
    """Show step-by-step how the algorithm picks batteries"""
    n = len(bank)
    result = []
    start = 0
    
    print(f"\nBank: {bank}")
    print(f"Need to pick: {num_batteries} batteries")
    print(f"Total batteries: {n}")
    print("=" * 60)
    
    for position in range(num_batteries):
        remaining_needed = num_batteries - position - 1
        latest_pos = n - remaining_needed - 1
        
        print(f"\n--- Picking battery #{position + 1} ---")
        print(f"Remaining needed after this: {remaining_needed}")
        print(f"Must leave at least {remaining_needed} batteries for later")
        print(f"Can search from index {start} to {latest_pos}")
        
        # Visual representation
        search_range = bank[start:latest_pos + 1]
        reserved = bank[latest_pos + 1:] if latest_pos + 1 < n else ""
        
        print(f"\nBank visualization:")
        print(f"  Already used: {bank[:start]}")
        print(f"  Search range: [{search_range}]  <- looking here")
        print(f"  Reserved:     ({reserved})  <- must keep for later")
        
        max_digit = max(search_range)
        idx = bank.index(max_digit, start)
        
        print(f"\nBest digit in search range: '{max_digit}' at index {idx}")
        print(f"Picking: {max_digit}")
        
        result.append(max_digit)
        start = idx + 1
        
        print(f"Result so far: {''.join(result)}")
    
    print("\n" + "=" * 60)
    print(f"FINAL RESULT: {''.join(result)}")
    print(f"As number: {int(''.join(result))}")
    return int(''.join(result))


# Example 1: Simple case
print("\n" + "#" * 60)
print("EXAMPLE 1: Pick 3 from '987654321'")
print("#" * 60)
visualize_selection("987654321", 3)

# Example 2: More interesting
print("\n\n" + "#" * 60)
print("EXAMPLE 2: Pick 3 from '132456'")
print("#" * 60)
visualize_selection("132456", 3)

# Example 3: From the problem
print("\n\n" + "#" * 60)
print("EXAMPLE 3: Pick 2 from '234234234234278'")
print("#" * 60)
visualize_selection("234234234234278", 2)

# Example 4: Tricky case
print("\n\n" + "#" * 60)
print("EXAMPLE 4: Pick 4 from '918273645'")
print("#" * 60)
visualize_selection("918273645", 4)
