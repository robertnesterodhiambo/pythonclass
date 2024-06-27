import tkinter as tk
from tkinter import ttk

def open_dashboard(user_id):
    # Create the dashboard window
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("500x400")
    
    # Set background color for the dashboard window
    dashboard_window.configure(bg='#f0f8ff')
    
    # Define styles for labels
    style = ttk.Style()
    style.configure('TLabel', font=('Helvetica', 12), background='#f0f8ff')
    style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground='#4b0082', background='#f0f8ff')
    
    # Display user ID at the top
    user_label = ttk.Label(dashboard_window, text=f"Current User ID: {user_id}", style='Title.TLabel')
    user_label.pack(pady=20)
    
    # Placeholder for dashboard content
    blank_label = ttk.Label(dashboard_window, text="Welcome! This is the dashboard page.", style='TLabel')
    blank_label.pack(pady=50)
    
    dashboard_window.mainloop()

if __name__ == "__main__":
    import sys
    user_id = sys.argv[1]
    open_dashboard(user_id)
