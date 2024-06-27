import tkinter as tk
from tkinter import ttk
import sqlite3

def submit_aspirant_details(citizen_id, first_name, last_name, position, age, gender, province, county, constituency, ward):
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO aspirant (citizen_id, first_name, last_name, aspirant_position, age, gender, province, county, constituency, ward)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (citizen_id, first_name, last_name, position, age, gender, province, county, constituency, ward))
    
    conn.commit()
    conn.close()

def open_apply_popup(user_id):
    popup = tk.Toplevel()
    popup.title("Apply as Aspirant")
    popup.geometry("400x550")
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
    
    ttk.Label(popup, text="Province:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    province_entry = ttk.Entry(popup)
    province_entry.pack(pady=5, fill=tk.X, padx=20)
    
    ttk.Label(popup, text="County:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    county_entry = ttk.Entry(popup)
    county_entry.pack(pady=5, fill=tk.X, padx=20)
    
    ttk.Label(popup, text="Constituency:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    constituency_entry = ttk.Entry(popup)
    constituency_entry.pack(pady=5, fill=tk.X, padx=20)
    
    ttk.Label(popup, text="Ward:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ward_entry = ttk.Entry(popup)
    ward_entry.pack(pady=5, fill=tk.X, padx=20)
    
    def submit():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        position = position_entry.get()
        age = int(age_entry.get())
        gender = gender_entry.get()
        province = province_entry.get()
        county = county_entry.get()
        constituency = constituency_entry.get()
        ward = ward_entry.get()
        
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

if __name__ == "__main__":
    import sys
    user_id = sys.argv[1]
    open_dashboard(user_id)
