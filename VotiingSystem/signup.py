import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import subprocess

def adjust_window_size(event):
    content_frame.place(relwidth=0.95, relheight=0.95, relx=0.5, rely=0.5, anchor='center')

def submit_form():
    # Get the data from the form
    first_name = entries['First Name'].get()
    second_name = entries['Second Name'].get()
    last_name = entries['Last Name'].get()
    date_of_birth = entries['Date of Birth'].get()
    id_number = entries['ID Number'].get()
    place_of_birth = entries['Place of Birth'].get()
    password = entries['Password'].get()

    # Check if any field is empty
    if any([not first_name, not second_name, not last_name, not date_of_birth, not id_number, not place_of_birth, not password]):
        messagebox.showwarning("Incomplete Form", "Please fill in all fields.")
        return

    # Connect to SQLite database
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()

    # Check if the ID number already exists
    cursor.execute('''
    SELECT * FROM citizen WHERE id_number=?
    ''', (id_number,))
    row = cursor.fetchone()

    if row:
        messagebox.showerror("Error", "ID number already exists!")
    else:
        # Insert data into 'citizen' table
        cursor.execute('''
        INSERT INTO citizen (first_name, second_name, last_name, date_of_birth, id_number, place_of_birth, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, second_name, last_name, date_of_birth, id_number, place_of_birth, password))

        # Commit and close the connection
        conn.commit()
        messagebox.showinfo("Success", "Information saved successfully!")

        # Clear the form
        for entry in entries.values():
            entry.delete(0, tk.END)

    conn.close()

def open_login_and_close_signup():
    # Close the current signup window
    root.destroy()

    # Open the login.py script
    subprocess.Popen(['python', 'login.py'])

root = tk.Tk()
root.title("Beautiful Responsive Form")
root.geometry("500x600")
root.configure(bg="#282c34")
root.bind('<Configure>', adjust_window_size)

# Create a style
style = ttk.Style()
style.theme_use("clam")

# Style configuration
style.configure("TLabel", background="#f0f0f0", foreground="#333", padding=6, font=('Helvetica', 12))
style.configure("TEntry", padding=6, font=('Helvetica', 12))
style.configure("TButton", background="#61afef", foreground="white", padding=6, font=('Helvetica', 12, 'bold'))

# Create a frame with a box shadow effect
shadow_frame = tk.Frame(root, bg="#61afef", bd=0)
shadow_frame.place(relwidth=0.98, relheight=0.98, relx=0.5, rely=0.5, anchor='center')

content_frame = tk.Frame(shadow_frame, bg="#f0f0f0", bd=0)
content_frame.place(relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor='center')

# Create and place the form widgets
fields = ['First Name', 'Second Name', 'Last Name', 'Date of Birth', 'ID Number', 'Place of Birth', 'Password']
entries = {}

for i, field in enumerate(fields):
    label = ttk.Label(content_frame, text=field)
    label.grid(row=i, column=0, sticky='w', padx=10, pady=10)
    
    if field == 'Password':
        entry = ttk.Entry(content_frame, show='*')
    elif field == 'Date of Birth':
        entry = DateEntry(content_frame, width=19, background='darkblue', foreground='white', borderwidth=2, year=2000)
    else:
        entry = ttk.Entry(content_frame)
    
    entry.grid(row=i, column=1, sticky='ew', padx=10, pady=10)
    entries[field] = entry

# Add a submit button
submit_button = ttk.Button(content_frame, text="Submit", command=submit_form)
submit_button.grid(row=len(fields), column=0, pady=20)

# Add a login button
login_button = ttk.Button(content_frame, text="Login", command=open_login_and_close_signup)
login_button.grid(row=len(fields), column=1, pady=20)

# Configure grid to make the content_frame responsive
content_frame.columnconfigure(1, weight=1)
content_frame.rowconfigure(len(fields), weight=1)

root.mainloop()
