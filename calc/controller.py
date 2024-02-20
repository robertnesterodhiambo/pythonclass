from model import TodoModel
from view import TodoView
import tkinter as tk

class TodoController:
    def __init__(self):
        self.model = TodoModel()
        self.view = TodoView(tk.Tk(), self)
        self.view.mainloop()

    def add_task(self, task):
        self.model.add_task(task)

    def remove_task(self, task):
        self.model.remove_task(task)

    def get_tasks(self):
        return self.model.get_tasks()

def main():
    controller = TodoController()

if __name__ == "__main__":
    main()
