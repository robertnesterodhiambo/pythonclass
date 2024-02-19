from model import CalculatorModel
from view import CalculatorView

class CalculatorController:
    def __init__(self):
        # Initialize the model and view
        self.model = CalculatorModel()
        self.view = CalculatorView(self)

    def add(self):
        # Get the number from the input field
        num = float(self.view.num_entry.get())
        # Call the add method of the model
        self.model.add(num)
        # Update the result label
        self.update_result_label()

    def subtract(self):
        # Get the number from the input field
        num = float(self.view.num_entry.get())
        # Call the subtract method of the model
        self.model.subtract(num)
        # Update the result label
        self.update_result_label()

    def multiply(self):
        # Get the number from the input field
        num = float(self.view.num_entry.get())
        # Call the multiply method of the model
        self.model.multiply(num)
        # Update the result label
        self.update_result_label()

    def divide(self):
        # Get the number from the input field
        num = float(self.view.num_entry.get())
        # Call the divide method of the model
        self.model.divide(num)
        # Update the result label
        self.update_result_label()

    def update_result_label(self):
        # Get the current result from the model
        result = self.model.get_result()
        # Update the result label in the view
        self.view.result_label.config(text=f"Result: {result}")
