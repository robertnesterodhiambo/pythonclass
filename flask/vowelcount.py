def count_vowels(input_string):
    # Initialize a dictionary with vowels as keys and zero counts
    vowels = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}

    # Convert the input string to lowercase to ensure case-insensitivity
    input_string = input_string.lower()

    # Iterate through each character in the input string
    for char in input_string:
        # If the character is a vowel, increment its count
        if char in vowels:
            vowels[char] += 1

    return vowels

# Request input from the user
user_input = input("Please enter a string: ")

# Get the vowel counts
result = count_vowels(user_input)

# Print the result
print("Vowel counts:", result)
