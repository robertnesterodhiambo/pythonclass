def calculate_average(numbers):
    if len(numbers) == 0:
        raise ValueError("The array is empty. Cannot compute the average.")
    sum_total = sum(numbers)
    average = sum_total / len(numbers)
    return average

# Taking input from the user
input_str = input("Enter floating-point numbers separated by spaces: ")
numbers = list(map(float, input_str.split()))

# Calculating and printing the average
print("Average:", calculate_average(numbers))
