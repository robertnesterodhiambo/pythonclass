# vote.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def open_vote_panel(user_id):
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    
    # Fetch user details from the database based on user_id
    cursor.execute("SELECT province, county, constituency, ward FROM citizen WHERE id_number=?", (user_id,))
    user_details = cursor.fetchone()
    
    if user_details is None:
        error_message = "User details not found"
        messagebox.showerror("Error", error_message)
        conn.close()
        return

    province, county, constituency, ward = user_details

    # Check if the user has already voted
    cursor.execute("SELECT * FROM votes WHERE id_number=?", (user_id,))
    if cursor.fetchone() is not None:
        error_message = "You have already voted"
        messagebox.showinfo("Info", error_message)
        conn.close()
        return

    def fetch_aspirants(position, location_column=None, location_value=None):
        if location_column:
            cursor.execute(f"SELECT first_name || ' ' || last_name FROM aspirant WHERE aspirant_position=? AND {location_column}=?", (position, location_value))
        else:
            cursor.execute("SELECT first_name || ' ' || last_name FROM aspirant WHERE aspirant_position=?", (position,))
        return [row[0] for row in cursor.fetchall()]

    vote_panel = tk.Toplevel()
    vote_panel.title("Vote Panel")
    vote_panel.geometry("400x600")
    vote_panel.configure(bg='#f0f8ff')
    
    ttk.Label(vote_panel, text=f"Vote Panel for User ID: {user_id}", background='#f0f8ff', foreground='#4b0082', font=('Helvetica', 16, 'bold')).pack(pady=10)
    
    ttk.Label(vote_panel, text=f"Province: {province}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ttk.Label(vote_panel, text=f"County: {county}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ttk.Label(vote_panel, text=f"Constituency: {constituency}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    ttk.Label(vote_panel, text=f"Ward: {ward}", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
    
    positions = [
        'President',
        'Governor',
        'Senator',
        'Women Rep',
        'Member of Parliament (MP)',
        'Member of County Assembly (MCA)'
    ]
    
    comboboxes = {}
    for position in positions:
        ttk.Label(vote_panel, text=f"{position}:", background='#f0f8ff', foreground='#4b0082').pack(pady=5)
        
        if position == 'President':
            candidates = fetch_aspirants(position)
        elif position == 'Governor':
            candidates = fetch_aspirants(position, 'province', province)
        elif position == 'Senator' or position == 'Women Rep':
            candidates = fetch_aspirants(position, 'county', county)
        elif position == 'Member of Parliament (MP)':
            candidates = fetch_aspirants(position, 'constituency', constituency)
        elif position == 'Member of County Assembly (MCA)':
            candidates = fetch_aspirants(position, 'ward', ward)

        combobox = ttk.Combobox(vote_panel, values=candidates)
        combobox.pack(pady=5)
        comboboxes[position] = combobox
    
    def submit_votes():
        votes = {position: combobox.get() for position, combobox in comboboxes.items()}
        if any(not vote for vote in votes.values()):
            messagebox.showerror("Error", "Please select a candidate for each position.")
            return
        
        try:
            conn = sqlite3.connect('voting.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO votes (id_number, president_vote, governor_vote, senator_vote, women_rep_vote, mp_vote, mca_vote, province, county, constituency, ward)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, votes['President'], votes['Governor'], votes['Senator'], votes['Women Rep'], votes['Member of Parliament (MP)'], votes['Member of County Assembly (MCA)'], province, county, constituency, ward))
            
            conn.commit()
            messagebox.showinfo("Success", "Your votes have been submitted successfully!")
            vote_panel.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
    
    ttk.Button(vote_panel, text="Submit Votes", command=submit_votes).pack(pady=20)
    
    vote_panel.mainloop()
