import random
from collections import Counter

rows = 25
cols = 40
total_numbers = rows * cols  # 1000

numbers = [random.randint(1, 45) for _ in range(total_numbers)]  # Generate 1000 numbers

# Print the numbers in a grid format
for i in range(rows):
    print(", ".join(f"{num:2}" for num in numbers[i * cols: (i + 1) * cols]))

print('\n\n')


# Count occurrences of each number
counter = Counter(numbers)

# Sort numbers by frequency (highest to lowest)
sorted_counts = sorted(counter.items(), key=lambda x: x[1], reverse=True)

# Print the sorted numbers with their frequencies
print("Number | Frequency")
print("-----------------")
for num, freq in sorted_counts:
    print(f"  {num:2}   |    {freq}")


print('\n\n')


print("Top 6 Most Frequent Numbers:")
print("----------------------------")

# Extract and print the top 6 most common numbers
top_6 = counter.most_common(6)
for num, freq in top_6:
    print(f"  {num:2}   |    {freq}")
