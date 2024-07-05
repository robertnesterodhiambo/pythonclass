import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_unique_counts(column, group_by):
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    query = f'''
    SELECT {group_by}, {column}, COUNT(*)
    FROM votes
    GROUP BY {group_by}, {column}
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def plot_bar_chart(data, group_by):
    fig, ax = plt.subplots()
    categories = list(set([row[1] for row in data]))
    groups = list(set([row[0] for row in data]))
    
    counts = {group: [0] * len(categories) for group in groups}
    for row in data:
        group, category, count = row
        counts[group][categories.index(category)] = count
    
    for group in groups:
        ax.bar(categories, counts[group], label=group)
    
    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.legend(title=group_by)
    ax.set_title(f'Counts of {group_by}')
    
    return fig

def update_chart():
    column = vote_type.get()
    group_by = filter_type.get()
    data = get_unique_counts(column, group_by)
    fig = plot_bar_chart(data, group_by)
    
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def open_dashboard():
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Election Results Dashboard")
    dashboard_window.geometry("800x600")
    dashboard_window.configure(bg='#f0f8ff')

    global vote_type, filter_type, chart_frame
    vote_type = tk.StringVar(value="president_vote")
    filter_type = tk.StringVar(value="county")

    ttk.Label(dashboard_window, text="Election Results Dashboard", background='#f0f8ff', foreground='#4b0082', font=('Helvetica', 16, 'bold')).pack(pady=10)

    filter_frame = ttk.Frame(dashboard_window)
    filter_frame.pack(pady=10)

    ttk.Label(filter_frame, text="Vote Type:").grid(row=0, column=0, padx=5)
    ttk.OptionMenu(filter_frame, vote_type, "president_vote", "president_vote", "governor_vote", "senator_vote", "women_rep_vote", "mp_vote", "mca_vote").grid(row=0, column=1, padx=5)

    ttk.Label(filter_frame, text="Group By:").grid(row=1, column=0, padx=5)
    ttk.OptionMenu(filter_frame, filter_type, "county", "province", "county", "constituency", "ward").grid(row=1, column=1, padx=5)

    ttk.Button(filter_frame, text="Update Chart", command=update_chart).grid(row=2, columnspan=2, pady=10)

    chart_frame = ttk.Frame(dashboard_window)
    chart_frame.pack(expand=True, fill=tk.BOTH)

    update_chart()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Voting System Dashboard")
    root.geometry("400x300")
    root.configure(bg='#f0f8ff')

    ttk.Button(root, text="Open Dashboard", command=open_dashboard).pack(pady=20)

    root.mainloop()
