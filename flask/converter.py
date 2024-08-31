def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9/5 + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def main():
    """Main function to handle user input and conversion."""
    print("Temperature Conversion Program")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")

    while True:
        try:
            choice = int(input("Enter the number of your choice (1 or 2): "))
            if choice not in [1, 2]:
                raise ValueError("Invalid choice. Please select 1 or 2.")

            if choice == 1:
                temp_celsius = float(input("Enter temperature in Celsius: "))
                temp_fahrenheit = celsius_to_fahrenheit(temp_celsius)
                print(f"{temp_celsius}°C is equal to {temp_fahrenheit:.2f}°F")

            elif choice == 2:
                temp_fahrenheit = float(input("Enter temperature in Fahrenheit: "))
                temp_celsius = fahrenheit_to_celsius(temp_fahrenheit)
                print(f"{temp_fahrenheit}°F is equal to {temp_celsius:.2f}°C")

            break  # Exit the loop after successful conversion

        except ValueError as e:
            print(f"Error: {e}. Please enter a valid number.")

if __name__ == "__main__":
    main()
