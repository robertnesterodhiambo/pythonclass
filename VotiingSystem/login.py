import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess

def login():
    # Get login credentials
    id_number = id_entry.get()
    password = password_entry.get()

    # Connect to SQLite database
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute('''
    SELECT * FROM citizen WHERE id_number=? AND password=?
    ''', (id_number, password))
    row = cursor.fetchone()

    # Close the connection
    conn.close()

    if row:
        # Open main application window (dashboard)
        open_dashboard(id_number)
    else:
        messagebox.showerror("Error", "Invalid ID number or password!")

def open_signup():
    # Open the signup panel
    signup_window = tk.Toplevel(login_window)
    signup_window.title("Signup")
    signup_window.geometry("300x200")

    # Add signup UI elements here
    # Example: ttk.Label(signup_window, text="Signup Form").pack()

def open_dashboard(user_id):
    # Close the current login window
    login_window.destroy()

    # Open the dashboard window
    subprocess.Popen(['python', 'dashboard.py', str(user_id)])

# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x200")
login_window.configure(bg="#282c34")

# Create a style
style = ttk.Style()
style.theme_use("clam")

# Style configuration
style.configure("TLabel", background="#282c34", foreground="#ffffff", font=('Helvetica', 12))
style.configure("TEntry", padding=6, font=('Helvetica', 12))
style.configure("TButton", background="#61afef", foreground="white", padding=6, font=('Helvetica', 12, 'bold'))

# Create and place login widgets
id_label = ttk.Label(login_window, text="ID Number:")
id_label.grid(row=0, column=0, padx=10, pady=10)

id_entry = ttk.Entry(login_window)
id_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ttk.Label(login_window, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)

password_entry = ttk.Entry(login_window, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = ttk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, column=0, padx=10, pady=20)

# Signup button
signup_button = ttk.Button(login_window, text="Signup", command=open_signup)
signup_button.grid(row=2, column=1, padx=10, pady=20)

# Configure grid to make the login window responsive
login_window.grid_columnconfigure(1, weight=1)
login_window.grid_rowconfigure(2, weight=1)

login_window.mainloop()
