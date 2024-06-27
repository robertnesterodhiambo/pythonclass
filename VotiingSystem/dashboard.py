import tkinter as tk
from tkinter import ttk
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('voting.db')
cursor = conn.cursor()

# Function to fetch all provinces from the database
def fetch_provinces():
    cursor.execute("SELECT name FROM Provinces")
    provinces = cursor.fetchall()
    return [province[0] for province in provinces]

# Function to fetch counties based on selected province
def fetch_counties(province_name):
    cursor.execute("SELECT id FROM Provinces WHERE name=?", (province_name,))
    province_id = cursor.fetchone()[0]
    cursor.execute("SELECT name FROM Counties WHERE province_id=?", (province_id,))
    counties = cursor.fetchall()
    return [county[0] for county in counties]

# Function to fetch constituencies based on selected county
def fetch_constituencies(county_name):
    cursor.execute("SELECT id FROM Counties WHERE name=?", (county_name,))
    county_id = cursor.fetchone()[0]
    cursor.execute("SELECT constituency_name FROM constituencies WHERE county_id=?", (county_id,))
    constituencies = cursor.fetchall()
    return [constituency[0] for constituency in constituencies]

# Function to fetch wards based on selected constituency
def fetch_wards(constituency_name):
    cursor.execute("SELECT id FROM constituencies WHERE constituency_name=?", (constituency_name,))
    constituency_id = cursor.fetchone()[0]
    cursor.execute("SELECT ward_name FROM wards WHERE constituency_id=?", (constituency_id,))
    wards = cursor.fetchall()
    return [ward[0] for ward in wards]

def submit_aspirant_details(citizen_id, first_name, last_name, position, age, gender, province, county, constituency, ward):
    cursor.execute('''
    INSERT INTO aspirant (citizen_id, first_name, last_name, aspirant_position, age, gender, province, county, constituency, ward)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (citizen_id, first_name, last_name, position, age, gender, province, county, constituency, ward))
    conn.commit()

def open_apply_popup(user_id):
    popup = tk.Toplevel()
    popup.title("Apply as Aspirant")
    popup.geometry("400x600")
    popup.configure(bg='#f0f8ff')
    
    ttk.Label(popup, text="Aspirant Application", background='#f0f8ff', foreground='#4b0082', font=('Helvetica', 16, 'bold')).pack(pady=10)
    
    ttk.Label(popup, text="First Name:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    first_name_entry = ttk.Entry(popup)
    first_name_entry.pack(pady=5, fill=tk.X, padx=20)
    
    ttk.Label(popup, text="Last Name:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    last_name_entry = ttk.Entry(popup)
    last_name_entry.pack(pady=5, fill=tk.X, padx=20)
    
    ttk.Label(popup, text="Position:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    position_entry = ttk.Entry(popup)
    position_entry.pack(pady=5, fill=tk.X, padx=20)
    
    ttk.Label(popup, text="Age:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    age_entry = ttk.Entry(popup)
    age_entry.pack(pady=5, fill=tk.X, padx=20)
    
    ttk.Label(popup, text="Gender:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    gender_entry = ttk.Entry(popup)
    gender_entry.pack(pady=5, fill=tk.X, padx=20)
    
    # Province dropdown
    ttk.Label(popup, text="Province:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    province_combobox = ttk.Combobox(popup, values=fetch_provinces())
    province_combobox.pack(pady=5, fill=tk.X, padx=20)
    
    # County dropdown
    ttk.Label(popup, text="County:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    county_combobox = ttk.Combobox(popup, state='disabled')
    county_combobox.pack(pady=5, fill=tk.X, padx=20)
    
    # Constituency dropdown
    ttk.Label(popup, text="Constituency:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    constituency_combobox = ttk.Combobox(popup, state='disabled')
    constituency_combobox.pack(pady=5, fill=tk.X, padx=20)
    
    # Ward dropdown
    ttk.Label(popup, text="Ward:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ward_combobox = ttk.Combobox(popup, state='disabled')
    ward_combobox.pack(pady=5, fill=tk.X, padx=20)
    
    def update_counties(event):
        selected_province = province_combobox.get()
        counties = fetch_counties(selected_province)
        county_combobox['values'] = counties
        county_combobox.config(state='readonly')
        county_combobox.set('')
        constituency_combobox.set('')
        ward_combobox.set('')
        constituency_combobox.config(state='disabled')
        ward_combobox.config(state='disabled')
    
    def update_constituencies(event):
        selected_county = county_combobox.get()
        constituencies = fetch_constituencies(selected_county)
        constituency_combobox['values'] = constituencies
        constituency_combobox.config(state='readonly')
        constituency_combobox.set('')
        ward_combobox.set('')
        ward_combobox.config(state='disabled')
    
    def update_wards(event):
        selected_constituency = constituency_combobox.get()
        wards = fetch_wards(selected_constituency)
        ward_combobox['values'] = wards
        ward_combobox.config(state='readonly')
        ward_combobox.set('')
    
    province_combobox.bind('<<ComboboxSelected>>', update_counties)
    county_combobox.bind('<<ComboboxSelected>>', update_constituencies)
    constituency_combobox.bind('<<ComboboxSelected>>', update_wards)
    
    def submit():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        position = position_entry.get()
        age = int(age_entry.get())
        gender = gender_entry.get()
        province = province_combobox.get()
        county = county_combobox.get()
        constituency = constituency_combobox.get()
        ward = ward_combobox.get()
        
        submit_aspirant_details(user_id, first_name, last_name, position, age, gender, province, county, constituency, ward)
        popup.destroy()

    submit_button = ttk.Button(popup, text="Submit", command=submit)
    submit_button.pack(pady=20)
    
    popup.mainloop()
    
def open_dashboard(user_id):
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("500x400")
    
    # Configure window to expand and fill available space
    dashboard_window.grid_rowconfigure(0, weight=1)
    dashboard_window.grid_columnconfigure(0, weight=1)
    
    content_frame = ttk.Frame(dashboard_window, padding="10", style='Dashboard.TFrame')
    content_frame.grid(row=0, column=0, sticky="nsew")
    content_frame.rowconfigure(2, weight=1)
    
    # Configure frame to expand and fill available space
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    
    style = ttk.Style()
    style.configure('Dashboard.TFrame', background='#f0f8ff')
    style.configure('TLabel', font=('Helvetica', 12), background='#f0f8ff', foreground='#4b0082')
    style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground='#4b0082', background='#f0f8ff')
    
    user_label = ttk.Label(content_frame, text=f"Current User ID: {user_id}", style='Title.TLabel')
    user_label.grid(row=0, column=0, pady=20, sticky="n")
    
    blank_label = ttk.Label(content_frame, text="Welcome! This is the dashboard page.", style='TLabel')
    blank_label.grid(row=1, column=0, pady=50, sticky="n")
    
    apply_button = ttk.Button(content_frame, text="Aspirant Application", command=lambda: open_apply_popup(user_id))
    apply_button.grid(row=2, column=0, pady=20, sticky="s")

    dashboard_window.mainloop()

# Test the open_dashboard function
open_dashboard(1)

# Don't forget to close the database connection
conn.close()
