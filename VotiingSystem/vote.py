# vote.py

import tkinter as tk
from tkinter import ttk

def open_vote_panel(user_id):
    vote_panel = tk.Toplevel()
    vote_panel.title("Vote Panel")
    vote_panel.geometry("400x300")
    vote_panel.configure(bg='#f0f8ff')
    
    ttk.Label(vote_panel, text=f"Vote Panel for User ID: {user_id}", background='#f0f8ff', foreground='#4b0082', font=('Helvetica', 16, 'bold')).pack(pady=10)
    
    # You can add voting components here
    
    vote_panel.mainloop()
