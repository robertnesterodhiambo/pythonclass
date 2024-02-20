import tkinter as tk

class TodoView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.master.title("Todo List")

        self.task_entry = tk.Entry(self.master)
        self.task_entry.pack()

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(self.master)
        self.task_listbox.pack()

        self.refresh_tasks()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.controller.add_task(task)
            self.refresh_tasks()

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.controller.get_tasks()
        for task in tasks:
            self.task_listbox.insert(tk.END, task)
