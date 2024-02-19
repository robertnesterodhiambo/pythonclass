import tkinter as tk

class CalculatorView:
    def __init__(self, controller):
        # Initialize the view with the controller
        self.controller = controller
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Calculator")

        # Create an entry widget for input
        self.num_entry = tk.Entry(self.root)
        self.num_entry.pack()

        # Create buttons for basic operations
        self.add_button = tk.Button(self.root, text="+", command=self.controller.add)
        self.add_button.pack()

        self.subtract_button = tk.Button(self.root, text="-", command=self.controller.subtract)
        self.subtract_button.pack()

        self.multiply_button = tk.Button(self.root, text="*", command=self.controller.multiply)
        self.multiply_button.pack()

        self.divide_button = tk.Button(self.root, text="/", command=self.controller.divide)
        self.divide_button.pack()

        # Create a label to display the result
        self.result_label = tk.Label(self.root, text="Result:")
        self.result_label.pack()

        # Start the main event loop
        self.root.mainloop()
