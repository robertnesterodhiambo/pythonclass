def count_strings(string_list):
    # Initialize an empty dictionary to store counts
    string_counts = {}
    
    # Iterate over each string in the list
    for string in string_list:
        # Increment the count for each string
        if string in string_counts:
            string_counts[string] += 1
        else:
            string_counts[string] = 1

    return string_counts

# Sample input
sample_list = ["apple", "banana", "apple", "orange", "banana", "apple"]

# Get the output
output = count_strings(sample_list)

# Print the output
print(output)
