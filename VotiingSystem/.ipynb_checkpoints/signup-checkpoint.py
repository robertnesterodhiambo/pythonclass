import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import subprocess

def submit_form():
    # Get the data from the form
    first_name = entries['First Name'].get()
    second_name = entries['Second Name'].get()
    last_name = entries['Last Name'].get()
    date_of_birth = entries['Date of Birth'].get()
    id_number = entries['ID Number'].get()
    place_of_birth = entries['Place of Birth'].get()
    password = entries['Password'].get()
    province = province_var.get()
    county = county_var.get()
    constituency = constituency_var.get()
    ward = ward_var.get()

    # Check if any field is empty
    if any([not first_name, not second_name, not last_name, not date_of_birth, not id_number, not place_of_birth, not password, not province, not county, not constituency, not ward]):
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
        INSERT INTO citizen (first_name, second_name, last_name, date_of_birth, id_number, place_of_birth, password, province, county, constituency, ward)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, second_name, last_name, date_of_birth, id_number, place_of_birth, password, province, county, constituency, ward))

        # Commit and close the connection
        conn.commit()
        messagebox.showinfo("Success", "Information saved successfully!")

        # Clear the form
        for entry in entries.values():
            entry.delete(0, tk.END)
        province_var.set('')
        county_var.set('')
        constituency_var.set('')
        ward_var.set('')

    conn.close()

def open_login_and_close_signup():
    # Close the current signup window
    root.destroy()

    # Open the login.py script
    subprocess.Popen(['python', 'login.py'])

def update_counties(event):
    province_id = province_ids.get(province_var.get())
    if not province_id:
        return
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM Counties WHERE province_id=?', (province_id,))
    counties = cursor.fetchall()
    county_ids.clear()
    county_var.set('')
    county_dropdown['values'] = [county[1] for county in counties]
    for county in counties:
        county_ids[county[1]] = county[0]
    conn.close()
    constituency_dropdown.set('')
    ward_dropdown.set('')
    constituency_dropdown['values'] = []
    ward_dropdown['values'] = []

def update_constituencies(event):
    county_id = county_ids.get(county_var.get())
    if not county_id:
        return
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, constituency_name FROM constituencies WHERE county_id=?', (county_id,))
    constituencies = cursor.fetchall()
    constituency_ids.clear()
    constituency_var.set('')
    constituency_dropdown['values'] = [constituency[1] for constituency in constituencies]
    for constituency in constituencies:
        constituency_ids[constituency[1]] = constituency[0]
    conn.close()
    ward_dropdown.set('')
    ward_dropdown['values'] = []

def update_wards(event):
    constituency_id = constituency_ids.get(constituency_var.get())
    if not constituency_id:
        return
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ward_name FROM wards WHERE constituency_id=?', (constituency_id,))
    wards = cursor.fetchall()
    ward_var.set('')
    ward_dropdown['values'] = [ward[0] for ward in wards]
    conn.close()

root = tk.Tk()
root.title("Beautiful Responsive Form")
root.geometry("500x600")
root.configure(bg="#282c34")

# Create a style
style = ttk.Style()
style.theme_use("clam")

# Style configuration
style.configure("TLabel", background="#f0f0f0", foreground="#333", padding=6, font=('Helvetica', 12))
style.configure("TEntry", padding=6, font=('Helvetica', 12))
style.configure("TButton", background="#61afef", foreground="white", padding=6, font=('Helvetica', 12, 'bold'))
style.configure("TCombobox", padding=6, font=('Helvetica', 12))

# Create a frame with a box shadow effect
shadow_frame = tk.Frame(root, bg="#61afef", bd=0)
shadow_frame.place(relwidth=0.98, relheight=0.98, relx=0.5, rely=0.5, anchor='center')

# Create a canvas and a scrollbar
canvas = tk.Canvas(shadow_frame, bg="#f0f0f0")
scrollbar = tk.Scrollbar(shadow_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Create and place the form widgets
fields = ['First Name', 'Second Name', 'Last Name', 'Date of Birth', 'ID Number', 'Place of Birth', 'Password']
entries = {}

for i, field in enumerate(fields):
    label = ttk.Label(scrollable_frame, text=field)
    label.grid(row=i, column=0, sticky='w', padx=10, pady=10)
    
    if field == 'Password':
        entry = ttk.Entry(scrollable_frame, show='*')
    elif field == 'Date of Birth':
        entry = DateEntry(scrollable_frame, width=19, background='darkblue', foreground='white', borderwidth=2, year=2000)
    else:
        entry = ttk.Entry(scrollable_frame)
    
    entry.grid(row=i, column=1, sticky='ew', padx=10, pady=10)
    entries[field] = entry

# Database connection to get province, county, constituency, and ward details
conn = sqlite3.connect('voting.db')
cursor = conn.cursor()

# Dropdown options for new fields
options_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
options_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

# Dropdown for province
ttk.Label(options_frame, text="Province").grid(row=0, column=0, sticky='w', padx=10, pady=10)
province_var = tk.StringVar()
province_dropdown = ttk.Combobox(options_frame, textvariable=province_var)
cursor.execute('SELECT id, name FROM Provinces')
provinces = cursor.fetchall()
province_ids = {province[1]: province[0] for province in provinces}
province_dropdown['values'] = [province[1] for province in provinces]
province_dropdown.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
province_dropdown.bind("<<ComboboxSelected>>", update_counties)

# Dropdown for county
ttk.Label(options_frame, text="County").grid(row=1, column=0, sticky='w', padx=10, pady=10)
county_var = tk.StringVar()
county_dropdown = ttk.Combobox(options_frame, textvariable=county_var)
county_ids = {}
county_dropdown.grid(row=1, column=1, sticky='ew', padx=10, pady=10)
county_dropdown.bind("<<ComboboxSelected>>", update_constituencies)

# Dropdown for constituency
ttk.Label(options_frame, text="Constituency").grid(row=2, column=0, sticky='w', padx=10, pady=10)
constituency_var = tk.StringVar()
constituency_dropdown = ttk.Combobox(options_frame, textvariable=constituency_var)
constituency_ids = {}
constituency_dropdown.grid(row=2, column=1, sticky='ew', padx=10, pady=10)
constituency_dropdown.bind("<<ComboboxSelected>>", update_wards)

# Dropdown for ward
ttk.Label(options_frame, text="Ward").grid(row=3, column=0, sticky='w', padx=10, pady=10)
ward_var = tk.StringVar()
ward_dropdown = ttk.Combobox(options_frame, textvariable=ward_var)
ward_dropdown.grid(row=3, column=1, sticky='ew', padx=10, pady=10)

# Add a submit button
submit_button = ttk.Button(scrollable_frame, text="Submit", command=submit_form)
submit_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

# Button to open login.py and close the signup form
login_button = ttk.Button(scrollable_frame, text="Go to Login", command=open_login_and_close_signup)
login_button.grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

conn.close()
root.mainloop()
