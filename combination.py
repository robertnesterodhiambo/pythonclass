def calculate_sum(numbers):
    sum_total = 0
    for number in numbers:
        sum_total += number
    return sum_total

def calculate_average(numbers):
    if len(numbers) == 0:
        raise ValueError("The array is empty. Cannot compute the average.")
    sum_total = sum(numbers)
    average = sum_total / len(numbers)
    return average

def main():
    # Taking input from the user
    input_str = input("Enter floating-point numbers separated by spaces: ")
    numbers = list(map(float, input_str.split()))

    # Asking user for the desired operation
    choice = input("Enter 'sum' to calculate the sum or 'average' to calculate the average: ").strip().lower()

    if choice == 'sum':
        result = calculate_sum(numbers)
        print("Sum:", result)
    elif choice == 'average':
        try:
            result = calculate_average(numbers)
            print("Average:", result)
        except ValueError as e:
            print(e)
    else:
        print("Invalid choice. Please enter 'sum' or 'average'.")

# Running the main function
if __name__ == "__main__":
    main()
