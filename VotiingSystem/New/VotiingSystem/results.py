import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VOTE_DB = os.path.join(BASE_DIR, "databases", "vote.db")
VOTING_DB = os.path.join(BASE_DIR, "databases", "voting.db")


# ============================================================
# UI COLORS
# ============================================================

BG = "#0F172A"
CARD = "#1E293B"
CARD_LIGHT = "#263449"
INPUT = "#334155"

ACCENT = "#3B82F6"
ACCENT_HOVER = "#2563EB"

TEXT = "#F8FAFC"
SECONDARY_TEXT = "#94A3B8"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"

BORDER = "#475569"


# ============================================================
# VOTE TYPES
# ============================================================

VOTE_TYPES = {
    "President": "president_vote",
    "Governor": "governor_vote",
    "Senator": "senator_vote",
    "Women Representative": "women_rep_vote",
    "Member of Parliament": "mp_vote",
    "MCA": "mca_vote",
}


GROUP_TYPES = {
    "Province": "province",
    "County": "county",
    "Constituency": "constituency",
    "Ward": "ward",
}


# ============================================================
# DATABASE CONNECTIONS
# ============================================================

def get_vote_connection():
    return sqlite3.connect(VOTE_DB)


def get_voting_connection():
    return sqlite3.connect(VOTING_DB)


# ============================================================
# GEOGRAPHY LOOKUP
# ============================================================

def get_geography_name(table, geography_id):
    """
    Convert a geography ID stored in vote.db into a human-readable
    name from voting.db.
    """

    table_config = {
        "province": ("Provinces", "name"),
        "county": ("Counties", "name"),
        "constituency": ("constituencies", "constituency_name"),
        "ward": ("wards", "ward_name"),
    }

    if table not in table_config:
        return str(geography_id)

    table_name, name_column = table_config[table]

    try:
        conn = get_voting_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT {name_column}
            FROM {table_name}
            WHERE id = ?
        """

        cursor.execute(query, (geography_id,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]

    except sqlite3.Error:
        pass

    return str(geography_id)


# ============================================================
# GET RESULTS
# ============================================================

def get_unique_counts(column, group_by):
    """
    Get vote totals grouped by the selected geographical area
    and candidate.

    Ballots are read from vote.db.
    Geography names are resolved using voting.db.
    """

    try:
        conn = get_vote_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT {group_by}, {column}, COUNT(*)
            FROM votes
            WHERE {column} IS NOT NULL
              AND TRIM({column}) != ''
            GROUP BY {group_by}, {column}
            ORDER BY {group_by}, COUNT(*) DESC
        """

        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()

        formatted_data = []

        for group_id, candidate, count in data:
            group_name = get_geography_name(group_by, group_id)

            formatted_data.append(
                (
                    group_name,
                    candidate,
                    count
                )
            )

        return formatted_data

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not load election results.\n\n{e}"
        )
        return []


# ============================================================
# CREATE BAR CHART
# ============================================================

def plot_bar_chart(data, group_by):
    """
    Create a grouped bar chart.

    data format:
        [
            (group_name, candidate, count),
            ...
        ]
    """

    fig, ax = plt.subplots(
        figsize=(10, 5),
        dpi=100
    )

    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    if not data:
        ax.text(
            0.5,
            0.5,
            "No voting results available",
            ha="center",
            va="center",
            color=TEXT,
            fontsize=14,
            transform=ax.transAxes
        )

        ax.set_xticks([])
        ax.set_yticks([])

        for spine in ax.spines.values():
            spine.set_visible(False)

        return fig

    categories = sorted(
        list(set(row[1] for row in data))
    )

    groups = sorted(
        list(set(row[0] for row in data))
    )

    # --------------------------------------------------------
    # Build count dictionary
    # --------------------------------------------------------

    counts = {
        group: {
            category: 0
            for category in categories
        }
        for group in groups
    }

    for group, category, count in data:
        counts[group][category] = count

    # --------------------------------------------------------
    # Bar positioning
    # --------------------------------------------------------

    number_of_groups = len(groups)

    bar_width = 0.8 / max(number_of_groups, 1)

    x_positions = list(range(len(categories)))

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    for index, group in enumerate(groups):

        values = [
            counts[group][category]
            for category in categories
        ]

        positions = [
            x + (index - (number_of_groups - 1) / 2) * bar_width
            for x in x_positions
        ]

        bars = ax.bar(
            positions,
            values,
            width=bar_width,
            label=group
        )

        # Value labels
        for bar in bars:
            height = bar.get_height()

            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    str(int(height)),
                    ha="center",
                    va="bottom",
                    color=TEXT,
                    fontsize=8
                )

    # --------------------------------------------------------
    # Styling
    # --------------------------------------------------------

    ax.set_xticks(x_positions)
    ax.set_xticklabels(
        categories,
        rotation=25,
        ha="right",
        color=TEXT
    )

    ax.set_ylabel(
        "Number of Votes",
        color=SECONDARY_TEXT
    )

    ax.set_xlabel(
        "Candidate",
        color=SECONDARY_TEXT
    )

    ax.set_title(
        f"Election Results by {group_by.title()}",
        color=TEXT,
        fontsize=14,
        fontweight="bold",
        pad=15
    )

    ax.tick_params(
        axis="y",
        colors=SECONDARY_TEXT
    )

    ax.tick_params(
        axis="x",
        colors=TEXT
    )

    # Grid
    ax.grid(
        axis="y",
        alpha=0.15
    )

    # Remove borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Legend
    legend = ax.legend(
        title=group_by.title(),
        facecolor=CARD_LIGHT,
        edgecolor=BORDER,
        labelcolor=TEXT
    )

    if legend:
        legend.get_title().set_color(TEXT)

    fig.tight_layout()

    return fig


# ============================================================
# UPDATE CHART
# ============================================================

def update_chart():
    vote_column = vote_type.get()
    group_column = filter_type.get()

    data = get_unique_counts(
        vote_column,
        group_column
    )

    # Clear previous chart
    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig = plot_bar_chart(
        data,
        group_column
    )

    canvas = FigureCanvasTkAgg(
        fig,
        master=chart_frame
    )

    canvas.draw()

    canvas_widget = canvas.get_tk_widget()

    canvas_widget.configure(
        bg=CARD,
        highlightthickness=0
    )

    canvas_widget.pack(
        expand=True,
        fill=tk.BOTH,
        padx=15,
        pady=15
    )

    # Update summary
    total_votes = sum(
        row[2]
        for row in data
    )

    candidate_count = len(
        set(row[1] for row in data)
    )

    group_count = len(
        set(row[0] for row in data)
    )

    total_votes_label.config(
        text=f"{total_votes:,}"
    )

    candidates_label.config(
        text=str(candidate_count)
    )

    groups_label.config(
        text=str(group_count)
    )


# ============================================================
# RESET / REFRESH
# ============================================================

def refresh_results():
    update_chart()


# ============================================================
# MAIN DASHBOARD
# ============================================================

def open_dashboard(parent=None):

    global vote_type
    global filter_type
    global chart_frame

    global total_votes_label
    global candidates_label
    global groups_label

    # --------------------------------------------------------
    # Window
    # --------------------------------------------------------

    if parent:
        dashboard_window = tk.Toplevel(parent)
    else:
        dashboard_window = tk.Toplevel()

    dashboard_window.title(
        "Election Results Dashboard"
    )

    dashboard_window.geometry(
        "1200x760"
    )

    dashboard_window.minsize(
        950,
        650
    )

    dashboard_window.configure(
        bg=BG
    )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    header = tk.Frame(
        dashboard_window,
        bg=BG
    )

    header.pack(
        fill="x",
        padx=30,
        pady=(25, 10)
    )

    title = tk.Label(
        header,
        text="Election Results",
        bg=BG,
        fg=TEXT,
        font=("Helvetica", 24, "bold")
    )

    title.pack(
        anchor="w"
    )

    subtitle = tk.Label(
        header,
        text="View and analyse voting results by geographical area",
        bg=BG,
        fg=SECONDARY_TEXT,
        font=("Helvetica", 11)
    )

    subtitle.pack(
        anchor="w",
        pady=(5, 0)
    )

    # --------------------------------------------------------
    # Control Card
    # --------------------------------------------------------

    controls = tk.Frame(
        dashboard_window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    controls.pack(
        fill="x",
        padx=30,
        pady=15
    )

    controls_inner = tk.Frame(
        controls,
        bg=CARD
    )

    controls_inner.pack(
        fill="x",
        padx=20,
        pady=18
    )

    # Vote type
    tk.Label(
        controls_inner,
        text="Election Position",
        bg=CARD,
        fg=SECONDARY_TEXT,
        font=("Helvetica", 10, "bold")
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 10)
    )

    vote_type = tk.StringVar(
        value="president_vote"
    )

    vote_menu = ttk.Combobox(
        controls_inner,
        textvariable=vote_type,
        values=list(VOTE_TYPES.values()),
        state="readonly",
        width=25
    )

    # Display friendly names instead
    vote_menu["values"] = list(
        VOTE_TYPES.keys()
    )

    vote_menu.set("President")

    vote_menu.grid(
        row=1,
        column=0,
        padx=(0, 20),
        pady=(7, 0)
    )

    # Group by
    tk.Label(
        controls_inner,
        text="Group Results By",
        bg=CARD,
        fg=SECONDARY_TEXT,
        font=("Helvetica", 10, "bold")
    ).grid(
        row=0,
        column=1,
        sticky="w",
        padx=10
    )

    filter_type = tk.StringVar(
        value="county"
    )

    filter_menu = ttk.Combobox(
        controls_inner,
        textvariable=filter_type,
        values=list(GROUP_TYPES.keys()),
        state="readonly",
        width=25
    )

    filter_menu.set("County")

    filter_menu.grid(
        row=1,
        column=1,
        padx=10,
        pady=(7, 0)
    )

    # --------------------------------------------------------
    # Convert friendly values to DB columns
    # --------------------------------------------------------

    def update_from_dropdown():

        selected_vote = vote_type.get()
        selected_group = filter_type.get()

        vote_column = VOTE_TYPES.get(
            selected_vote,
            "president_vote"
        )

        group_column = GROUP_TYPES.get(
            selected_group,
            "county"
        )

        # Temporarily replace values with database values
        old_vote = vote_type.get()
        old_group = filter_type.get()

        vote_type.set(vote_column)
        filter_type.set(group_column)

        update_chart()

        vote_type.set(old_vote)
        filter_type.set(old_group)

    # --------------------------------------------------------
    # Update button
    # --------------------------------------------------------

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Modern.TButton",
        background=ACCENT,
        foreground=TEXT,
        borderwidth=0,
        padding=(18, 10),
        font=("Helvetica", 10, "bold")
    )

    style.map(
        "Modern.TButton",
        background=[
            ("active", ACCENT_HOVER)
        ]
    )

    update_button = ttk.Button(
        controls_inner,
        text="↻  Update Results",
        style="Modern.TButton",
        command=update_from_dropdown
    )

    update_button.grid(
        row=1,
        column=2,
        padx=(20, 0),
        pady=(7, 0)
    )

    # --------------------------------------------------------
    # Summary Cards
    # --------------------------------------------------------

    summary = tk.Frame(
        dashboard_window,
        bg=BG
    )

    summary.pack(
        fill="x",
        padx=30,
        pady=5
    )

    def create_summary_card(
        parent,
        title_text,
        value_text,
        column
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        tk.Label(
            card,
            text=title_text,
            bg=CARD,
            fg=SECONDARY_TEXT,
            font=("Helvetica", 9, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        label = tk.Label(
            card,
            text=value_text,
            bg=CARD,
            fg=TEXT,
            font=("Helvetica", 20, "bold")
        )

        label.pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        return label

    total_votes_label = create_summary_card(
        summary,
        "TOTAL VOTES",
        "0",
        0
    )

    candidates_label = create_summary_card(
        summary,
        "CANDIDATES",
        "0",
        1
    )

    groups_label = create_summary_card(
        summary,
        "AREAS",
        "0",
        2
    )

    # --------------------------------------------------------
    # Chart Card
    # --------------------------------------------------------

    chart_card = tk.Frame(
        dashboard_window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    chart_card.pack(
        expand=True,
        fill="both",
        padx=30,
        pady=(15, 25)
    )

    chart_frame = tk.Frame(
        chart_card,
        bg=CARD
    )

    chart_frame.pack(
        expand=True,
        fill="both"
    )

    # --------------------------------------------------------
    # Initial chart
    # --------------------------------------------------------

    update_from_dropdown()


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    open_dashboard(root)

    root.mainloop()