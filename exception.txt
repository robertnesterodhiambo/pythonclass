# Declaring and initializing variables
first_name = "John"
last_name = "Doe"

try:
    # Prompt the user to enter their age
    age = int(input("Please enter your age: "))
    
    if age < 0:
        raise ValueError("Age cannot be negative.")
except ValueError as ve:
    print("Error:", ve)
else:
    # Writing to the screen (printing)
    print("Welcome, " + first_name + " " + last_name + "!")
    print("You are " + str(age) + " years old.")

# Declaring and initializing more variables
try:
    num1 = 10
    num2 = 20

    # Check if num1 and num2 are integers
    if not isinstance(num1, int) or not isinstance(num2, int):
        raise ValueError("Both num1 and num2 must be integers.")
except ValueError as ve:
    print("Error:", ve)
else:
    # Using variables to perform a calculation
    sum_result = num1 + num2

    # Writing the result to the screen
    print("The sum of " + str(num1) + " and " + str(num2) + " is: " + str(sum_result))
