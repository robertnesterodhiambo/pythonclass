# vote.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Import messagebox explicitly

import sqlite3

def open_vote_panel(user_id):
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    
    # Fetch user details from the database based on user_id
    cursor.execute("SELECT province, county, constituency, ward FROM citizen WHERE id_number=?", (user_id,))
    user_details = cursor.fetchone()
    conn.close()  # Close connection after fetching data
    
    if user_details is None:
        # If user_details is None, handle the error gracefully (e.g., show an error message)
        error_message = "User details not found"
        messagebox.showerror("Error", error_message)  # Use messagebox from tkinter module
        return
    
    vote_panel = tk.Toplevel()
    vote_panel.title("Vote Panel")
    vote_panel.geometry("400x300")
    vote_panel.configure(bg='#f0f8ff')
    
    ttk.Label(vote_panel, text=f"Vote Panel for User ID: {user_id}", background='#f0f8ff', foreground='#4b0082', font=('Helvetica', 16, 'bold')).pack(pady=10)
    
    ttk.Label(vote_panel, text=f"Province: {user_details[0]}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ttk.Label(vote_panel, text=f"County: {user_details[1]}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ttk.Label(vote_panel, text=f"Constituency: {user_details[2]}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ttk.Label(vote_panel, text=f"Ward: {user_details[3]}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    
    # You can add voting components here
    
    vote_panel.mainloop()
