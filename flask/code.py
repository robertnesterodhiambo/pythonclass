# 1. Declaring three variables:

first_name = "Zamarie"
last_name = "Baker"
full_name = first_name + " " + last_name


# 2. Conditional Statement:

favorite_color = "blue"  # Replace with your actual favorite color
if favorite_color == "blue":
    print("Zamarie's favorite color is blue!")
else:
    print("Zamarie's favorite color is not blue.")


### 3. Lists, Tuples, and Dictionaries:

# List: A mutable ordered collection of items.
my_list = ["Zamarie", "Python", "Air Force"]

# Tuple: An immutable ordered collection of items.
my_tuple = ("Zamarie", "Python", "Air Force")

# Dictionary: An unordered collection of key-value pairs.
my_dict = {"name": "Zamarie", "language": "Python", "occupation": "Air Force"}


### 4. Function Definition and Calling:

def greet_Zamarie():
    return "Hello Zamarie!"

# Calling the function
greeting = greet_Zamarie()
print(greeting)


### 5. Handling Exceptions:

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero.")


### 6. Loops in Python:

# For loop
name = "Zamarie Baker"
for char in name:
    print(char)

# While loop
i = 0
while i < len(name):
    print(name[i])
    i += 1


### 7. Reading Data from a File:

with open('file.txt', 'r') as file:
    content = file.read()
    print(content)


### 8. Object-Oriented Programming - Classes and Objects:

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Creating an object of the class
person1 = Person("Zamarie", 21)
print(person1.name)  # Output: Zamarie

