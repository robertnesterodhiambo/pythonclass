# Creating sets

fruits = {"apple", "banana", "cherry"}

# REpetetive vlaues in sets are automatically removed

numbers = {1, 2, 3, 4, 4, 5, 5}

# Empty set

empty_set = set()  # Use set() to create an empty set, not {}

print(fruits)  # Output: {'banana', 'cherry', 'apple'}
print(numbers)  # Output: {1, 2, 3, 4, 5}
print(empty_set)  # Output: set()

# Set operations

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union

union_set = a.union(b)
print(union_set)  # Output: {1, 2, 3, 4, 5, 6}

# Intersection  

intersection_set = a.intersection(b)
print(intersection_set)  # Output: {3, 4}

# Difference

difference_set = a.difference(b)
print(difference_set)  # Output: {1, 2}

# Symmetric Difference
systematic_diff_set = a.symmetric_difference(b)
print(systematic_diff_set)  # Output: {1, 2, 5, 6}

# Adding and removing elements

fruits.add("orange")
print(fruits)  # Output: {'banana', 'cherry', 'apple', 'orange'}    

fruits.remove("banana")
print(fruits)  # Output: {'cherry', 'apple', 'orange'}    

# Discarding an element (does not raise an error if the element is not present)
fruits.discard("grape")  # No error, even though "grape" is not in the set

# Clearing a set
fruits.clear()
print(fruits)  # Output: set()