# Dictioneries are used to store data values in key:value pairs.

user = {"Name": "Robert", "Age": 30, "Occupation": "Engineer"}
print(user["Name"])  # Output: Robert
print(user)  # Output: {'Name': 'Robert', 'Age': 30, 'Occupation': 'Engineer'}

print(user.get("Age"))  # Output: 30

# Adding a new key-value pair to the dictionary
user["Age"] = 56
user["Name"] = "John"
user["Occupation"] = "Doctor"
print(user)  # Output: {'Name': 'John', 'Age': 56, 'Occupation': 'Doctor'}

# Updaing and Merging Dictioneries
profile = {"Name": "Alice", "Age": 25,}
profile.update({"Occupation": "Designer"})
print(profile)  # Output: {'Name': 'Alice', 'Age': 25, 'Occupation': 'Designer'}

d1 = {"A": 1, "B": 2}
d2 = {"B": 99, "C": 3}

merged_dict = {**d1, **d2}
print(merged_dict)  # Output: {'A': 1, 'B': 99, 'C': 3}
merged_dict = d1|d2
print(merged_dict)  # Output: {'A': 1, 'B': 99, 'C': 3}