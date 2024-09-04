def calculate_sum(numbers):
    sum_total = 0
    for number in numbers:
        sum_total += number
    return sum_total

# Taking input from the user
input_str = input("Enter floating-point numbers separated by spaces: ")
numbers = list(map(float, input_str.split()))

# Calculating and printing the sum
print("Sum:", calculate_sum(numbers))
