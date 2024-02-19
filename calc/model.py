class CalculatorModel:
    def __init__(self):
        # Initialize the result to 0
        self._result = 0

    def add(self, num):
        # Add the given number to the result
        self._result += num

    def subtract(self, num):
        # Subtract the given number from the result
        self._result -= num

    def multiply(self, num):
        # Multiply the result by the given number
        self._result *= num

    def divide(self, num):
        # Check if the given number is not zero
        if num != 0:
            # Divide the result by the given number
            self._result /= num

    def get_result(self):
        # Return the current result
        return self._result
