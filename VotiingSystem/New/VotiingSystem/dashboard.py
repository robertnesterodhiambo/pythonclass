import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import os
import sys

from vote import open_vote_panel


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER_DB = os.path.join(BASE_DIR, "databases", "user.db")
VOTING_DB = os.path.join(BASE_DIR, "databases", "voting.db")


# ============================================================
# COLORS
# ============================================================

BG = "#0F172A"
SIDEBAR = "#111827"
CARD = "#1E293B"
CARD_HOVER = "#263449"

INPUT = "#334155"
BORDER = "#475569"

ACCENT = "#3B82F6"
ACCENT_HOVER = "#2563EB"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"

TEXT = "#F8FAFC"
SECONDARY_TEXT = "#94A3B8"
MUTED_TEXT = "#64748B"


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_user(user_id):
    """
    Fetch the logged-in user's information from user.db.
    """

    try:
        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                first_name,
                second_name,
                last_name,
                date_of_birth,
                id_number,
                place_of_birth,
                province,
                county,
                constituency,
                ward,
                created_at
            FROM users
            WHERE id_number = ?
        """, (str(user_id),))

        user = cursor.fetchone()

        conn.close()

        return user

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to load user information.\n\n{error}"
        )
        return None


def get_location_names(province_id, county_id, constituency_id, ward_id):
    """
    Convert the geographic IDs stored in user.db into readable names
    using voting.db.
    """

    try:
        conn = sqlite3.connect(VOTING_DB)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM Provinces WHERE id=?",
            (province_id,)
        )
        province = cursor.fetchone()

        cursor.execute(
            "SELECT name FROM Counties WHERE id=?",
            (county_id,)
        )
        county = cursor.fetchone()

        cursor.execute(
            "SELECT constituency_name FROM constituencies WHERE id=?",
            (constituency_id,)
        )
        constituency = cursor.fetchone()

        cursor.execute(
            "SELECT ward_name FROM wards WHERE id=?",
            (ward_id,)
        )
        ward = cursor.fetchone()

        conn.close()

        return (
            province[0] if province else "Unknown",
            county[0] if county else "Unknown",
            constituency[0] if constituency else "Unknown",
            ward[0] if ward else "Unknown"
        )

    except sqlite3.Error:
        return (
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown"
        )


def check_vote_status(user_id):
    """
    Check whether the current user has already voted.

    vote.db is optional at this stage. If it does not exist yet,
    the dashboard simply reports that voting status is unavailable.
    """

    vote_db = os.path.join(BASE_DIR, "databases", "vote.db")

    if not os.path.exists(vote_db):
        return False

    try:
        conn = sqlite3.connect(vote_db)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM votes
            WHERE id_number = ?
            LIMIT 1
        """, (str(user_id),))

        result = cursor.fetchone()

        conn.close()

        return result is not None

    except sqlite3.Error:
        return False


# ============================================================
# DASHBOARD
# ============================================================

def open_dashboard(user_id):

    # --------------------------------------------------------
    # Get user information
    # --------------------------------------------------------

    user = get_user(user_id)

    if not user:
        messagebox.showerror(
            "Login Error",
            "Unable to find the logged-in user."
        )
        return

    (
        database_id,
        first_name,
        second_name,
        last_name,
        date_of_birth,
        id_number,
        place_of_birth,
        province_id,
        county_id,
        constituency_id,
        ward_id,
        created_at
    ) = user

    # --------------------------------------------------------
    # Geographic names
    # --------------------------------------------------------

    province_name, county_name, constituency_name, ward_name = \
        get_location_names(
            province_id,
            county_id,
            constituency_id,
            ward_id
        )

    # --------------------------------------------------------
    # Voting status
    # --------------------------------------------------------

    already_voted = check_vote_status(id_number)

    # --------------------------------------------------------
    # Main window
    # --------------------------------------------------------

    dashboard = tk.Tk()

    dashboard.title("Votiing System — Dashboard")
    dashboard.geometry("1180x720")
    dashboard.minsize(1000, 650)
    dashboard.configure(bg=BG)

    # --------------------------------------------------------
    # Window icon / close handling
    # --------------------------------------------------------

    def on_close():
        dashboard.destroy()

    dashboard.protocol("WM_DELETE_WINDOW", on_close)

    # ========================================================
    # STYLE
    # ========================================================

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Modern.TButton",
        font=("Helvetica", 10, "bold"),
        foreground=TEXT,
        background=CARD,
        borderwidth=0,
        padding=(15, 10)
    )

    style.map(
        "Modern.TButton",
        background=[
            ("active", CARD_HOVER)
        ]
    )

    style.configure(
        "Accent.TButton",
        font=("Helvetica", 11, "bold"),
        foreground="white",
        background=ACCENT,
        borderwidth=0,
        padding=(18, 12)
    )

    style.map(
        "Accent.TButton",
        background=[
            ("active", ACCENT_HOVER)
        ]
    )

    # ========================================================
    # HELPER FUNCTIONS
    # ========================================================

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    def create_card(parent, **kwargs):
        return tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            **kwargs
        )

    def show_home():
        clear_content()

        # --------------------------------------------
        # Header
        # --------------------------------------------

        header = tk.Frame(content_area, bg=BG)
        header.pack(fill="x", pady=(0, 25))

        tk.Label(
            header,
            text=f"Good to see you, {first_name}!",
            font=("Helvetica", 25, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Welcome to your secure election dashboard.",
            font=("Helvetica", 11),
            fg=SECONDARY_TEXT,
            bg=BG
        ).pack(anchor="w", pady=(5, 0))

        # --------------------------------------------
        # Status banner
        # --------------------------------------------

        status_card = create_card(content_area)
        status_card.pack(fill="x", pady=(0, 20))

        status_left = tk.Frame(status_card, bg=CARD)
        status_left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=18
        )

        status_icon = "✓" if already_voted else "●"

        status_color = SUCCESS if already_voted else WARNING

        tk.Label(
            status_left,
            text=status_icon,
            font=("Helvetica", 22, "bold"),
            fg=status_color,
            bg=CARD
        ).pack(side="left", padx=(0, 15))

        status_text_frame = tk.Frame(status_left, bg=CARD)
        status_text_frame.pack(side="left")

        if already_voted:
            status_title = "Your vote has been recorded"
            status_description = (
                "Your ballot is already present in the voting database."
            )
        else:
            status_title = "You have not voted yet"
            status_description = (
                "You are eligible to proceed to the voting panel."
            )

        tk.Label(
            status_text_frame,
            text=status_title,
            font=("Helvetica", 12, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w")

        tk.Label(
            status_text_frame,
            text=status_description,
            font=("Helvetica", 9),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", pady=(4, 0))

        # --------------------------------------------
        # Information cards
        # --------------------------------------------

        stats_frame = tk.Frame(content_area, bg=BG)
        stats_frame.pack(fill="x", pady=(0, 20))

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)

        # Location card
        location_card = create_card(stats_frame)
        location_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        tk.Label(
            location_card,
            text="LOCATION",
            font=("Helvetica", 9, "bold"),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(16, 5))

        tk.Label(
            location_card,
            text=ward_name,
            font=("Helvetica", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=18)

        tk.Label(
            location_card,
            text=f"{constituency_name}\n{county_name}",
            font=("Helvetica", 9),
            fg=SECONDARY_TEXT,
            bg=CARD,
            justify="left"
        ).pack(anchor="w", padx=18, pady=(4, 16))

        # Voter card
        voter_card = create_card(stats_frame)
        voter_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8
        )

        tk.Label(
            voter_card,
            text="VOTER ID",
            font=("Helvetica", 9, "bold"),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(16, 5))

        tk.Label(
            voter_card,
            text=id_number,
            font=("Helvetica", 18, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=18)

        tk.Label(
            voter_card,
            text="Registered voter",
            font=("Helvetica", 9),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(4, 16))

        # Election card
        election_card = create_card(stats_frame)
        election_card.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(8, 0)
        )

        tk.Label(
            election_card,
            text="ELECTION STATUS",
            font=("Helvetica", 9, "bold"),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(16, 5))

        election_status = "VOTED" if already_voted else "READY"

        tk.Label(
            election_card,
            text=election_status,
            font=("Helvetica", 18, "bold"),
            fg=SUCCESS if already_voted else ACCENT,
            bg=CARD
        ).pack(anchor="w", padx=18)

        tk.Label(
            election_card,
            text="Ballot status",
            font=("Helvetica", 9),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", padx=18, pady=(4, 16))

        # --------------------------------------------
        # Quick actions
        # --------------------------------------------

        actions_card = create_card(content_area)
        actions_card.pack(fill="both", expand=True)

        tk.Label(
            actions_card,
            text="Quick Actions",
            font=("Helvetica", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=20, pady=(18, 4))

        tk.Label(
            actions_card,
            text="Access the main election services.",
            font=("Helvetica", 9),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", padx=20)

        actions = tk.Frame(actions_card, bg=CARD)
        actions.pack(fill="x", padx=20, pady=20)

        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)
        actions.columnconfigure(2, weight=1)

        # Vote
        vote_btn = tk.Button(
            actions,
            text="🗳  CAST YOUR VOTE",
            command=lambda: open_vote_panel(id_number),
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg=ACCENT,
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=14
        )
        vote_btn.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 6)
        )

        # Aspirant
        aspirant_btn = tk.Button(
            actions,
            text="👤  APPLY AS ASPIRANT",
            command=lambda: open_apply_popup(id_number),
            font=("Helvetica", 10, "bold"),
            fg=TEXT,
            bg=INPUT,
            activebackground=CARD_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=14
        )
        aspirant_btn.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=6
        )

        # Results
        results_btn = tk.Button(
            actions,
            text="📊  VIEW RESULTS",
            command=run_results_script,
            font=("Helvetica", 10, "bold"),
            fg=TEXT,
            bg=INPUT,
            activebackground=CARD_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=14
        )
        results_btn.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(6, 0)
        )

    # ========================================================
    # PROFILE PAGE
    # ========================================================

    def show_profile():
        clear_content()

        tk.Label(
            content_area,
            text="My Profile",
            font=("Helvetica", 25, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            content_area,
            text="Your registered voter information.",
            font=("Helvetica", 11),
            fg=SECONDARY_TEXT,
            bg=BG
        ).pack(anchor="w", pady=(5, 20))

        profile_card = create_card(content_area)
        profile_card.pack(fill="x")

        # Avatar
        avatar = tk.Label(
            profile_card,
            text=first_name[0].upper() if first_name else "?",
            font=("Helvetica", 28, "bold"),
            fg="white",
            bg=ACCENT,
            width=3,
            height=2
        )
        avatar.pack(side="left", padx=25, pady=25)

        profile_name = tk.Frame(profile_card, bg=CARD)
        profile_name.pack(side="left", pady=25)

        tk.Label(
            profile_name,
            text=f"{first_name} {second_name} {last_name}",
            font=("Helvetica", 18, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w")

        tk.Label(
            profile_name,
            text=f"Voter ID: {id_number}",
            font=("Helvetica", 10),
            fg=SECONDARY_TEXT,
            bg=CARD
        ).pack(anchor="w", pady=(5, 0))

        # Details
        details = create_card(content_area)
        details.pack(fill="x", pady=20)

        profile_rows = [
            ("Date of Birth", date_of_birth),
            ("Place of Birth", place_of_birth),
            ("Province", province_name),
            ("County", county_name),
            ("Constituency", constituency_name),
            ("Ward", ward_name),
            ("Registered", created_at)
        ]

        for label, value in profile_rows:

            row = tk.Frame(details, bg=CARD)
            row.pack(fill="x", padx=25, pady=8)

            tk.Label(
                row,
                text=label,
                font=("Helvetica", 10),
                fg=SECONDARY_TEXT,
                bg=CARD,
                width=18,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                font=("Helvetica", 10, "bold"),
                fg=TEXT,
                bg=CARD,
                anchor="w"
            ).pack(side="left")

    # ========================================================
    # VOTING PAGE
    # ========================================================

    def show_voting():

        if already_voted:
            messagebox.showinfo(
                "Already Voted",
                "Your vote has already been recorded."
            )
            return

        open_vote_panel(id_number)

    # ========================================================
    # RESULTS
    # ========================================================

    def run_results_script():

        results_script = os.path.join(
            BASE_DIR,
            "results.py"
        )

        if not os.path.exists(results_script):
            messagebox.showerror(
                "Results",
                "results.py could not be found."
            )
            return

        try:
            subprocess.Popen(
                [sys.executable, results_script]
            )

        except Exception as error:
            messagebox.showerror(
                "Results Error",
                f"Unable to open results.\n\n{error}"
            )

    # ========================================================
    # ASPIRANT APPLICATION
    # ========================================================

    def open_apply_popup(user_id):

        popup = tk.Toplevel(dashboard)
        popup.title("Aspirant Application")
        popup.geometry("520x650")
        popup.minsize(500, 600)
        popup.configure(bg=BG)

        popup.transient(dashboard)
        popup.grab_set()

        # --------------------------------------------
        # Header
        # --------------------------------------------

        header = tk.Frame(popup, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text="♟",
            font=("Helvetica", 30),
            fg=ACCENT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Aspirant Application",
            font=("Helvetica", 21, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            header,
            text="Submit your application for consideration.",
            font=("Helvetica", 9),
            fg=SECONDARY_TEXT,
            bg=BG
        ).pack(anchor="w")

        # --------------------------------------------
        # Form
        # --------------------------------------------

        form = tk.Frame(
            popup,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        form.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        def field_label(text, row, column):
            tk.Label(
                form,
                text=text,
                font=("Helvetica", 9, "bold"),
                fg=SECONDARY_TEXT,
                bg=CARD
            ).grid(
                row=row,
                column=column,
                sticky="w",
                padx=15,
                pady=(15, 5)
            )

        def entry_widget(row, column):
            entry = tk.Entry(
                form,
                font=("Helvetica", 10),
                fg=TEXT,
                bg=INPUT,
                insertbackground=TEXT,
                relief="flat",
                bd=0
            )

            entry.grid(
                row=row + 1,
                column=column,
                sticky="ew",
                padx=15,
                pady=(0, 5),
                ipady=8
            )

            return entry

        field_label("First Name", 0, 0)
        first_name_entry = entry_widget(0, 0)

        field_label("Last Name", 0, 1)
        last_name_entry = entry_widget(0, 1)

        # Position
        field_label("Position", 2, 0)

        position_combobox = ttk.Combobox(
            form,
            state="readonly",
            font=("Helvetica", 10)
        )

        position_combobox.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 5)
        )

        # Age
        field_label("Age", 4, 0)
        age_entry = entry_widget(4, 0)

        # Gender
        field_label("Gender", 4, 1)

        gender_combobox = ttk.Combobox(
            form,
            state="readonly",
            values=["Male", "Female"],
            font=("Helvetica", 10)
        )

        gender_combobox.grid(
            row=5,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 5)
        )

        # Province
        field_label("Province", 6, 0)

        province_combobox = ttk.Combobox(
            form,
            state="readonly",
            font=("Helvetica", 10)
        )

        province_combobox.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 5)
        )

        # County
        field_label("County", 8, 0)

        county_combobox = ttk.Combobox(
            form,
            state="disabled",
            font=("Helvetica", 10)
        )

        county_combobox.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 5)
        )

        # Constituency
        field_label("Constituency", 10, 0)

        constituency_combobox = ttk.Combobox(
            form,
            state="disabled",
            font=("Helvetica", 10)
        )

        constituency_combobox.grid(
            row=11,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 5)
        )

        # Ward
        field_label("Ward", 12, 0)

        ward_combobox = ttk.Combobox(
            form,
            state="disabled",
            font=("Helvetica", 10)
        )

        ward_combobox.grid(
            row=13,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 5)
        )

        # --------------------------------------------
        # Database functions for application
        # --------------------------------------------

        def fetch_positions():

            try:
                conn = sqlite3.connect(VOTING_DB)
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT position_name FROM positions"
                )

                positions = [
                    row[0]
                    for row in cursor.fetchall()
                ]

                conn.close()

                return positions

            except sqlite3.Error:
                return []

        def fetch_provinces():

            try:
                conn = sqlite3.connect(VOTING_DB)
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT name FROM Provinces"
                )

                provinces = [
                    row[0]
                    for row in cursor.fetchall()
                ]

                conn.close()

                return provinces

            except sqlite3.Error:
                return []

        def fetch_counties(province_name):

            conn = sqlite3.connect(VOTING_DB)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM Provinces WHERE name=?",
                (province_name,)
            )

            result = cursor.fetchone()

            if not result:
                conn.close()
                return []

            province_id = result[0]

            cursor.execute(
                "SELECT name FROM Counties WHERE province_id=?",
                (province_id,)
            )

            counties = [
                row[0]
                for row in cursor.fetchall()
            ]

            conn.close()

            return counties

        def fetch_constituencies(county_name):

            conn = sqlite3.connect(VOTING_DB)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM Counties WHERE name=?",
                (county_name,)
            )

            result = cursor.fetchone()

            if not result:
                conn.close()
                return []

            county_id = result[0]

            cursor.execute(
                """
                SELECT constituency_name
                FROM constituencies
                WHERE county_id=?
                """,
                (county_id,)
            )

            constituencies = [
                row[0]
                for row in cursor.fetchall()
            ]

            conn.close()

            return constituencies

        def fetch_wards(constituency_name):

            conn = sqlite3.connect(VOTING_DB)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id
                FROM constituencies
                WHERE constituency_name=?
                """,
                (constituency_name,)
            )

            result = cursor.fetchone()

            if not result:
                conn.close()
                return []

            constituency_id = result[0]

            cursor.execute(
                """
                SELECT ward_name
                FROM wards
                WHERE constituency_id=?
                """,
                (constituency_id,)
            )

            wards = [
                row[0]
                for row in cursor.fetchall()
            ]

            conn.close()

            return wards

        # --------------------------------------------
        # Load dropdowns
        # --------------------------------------------

        position_combobox["values"] = fetch_positions()
        province_combobox["values"] = fetch_provinces()

        # --------------------------------------------
        # Cascading dropdowns
        # --------------------------------------------

        def update_counties(event=None):

            selected = province_combobox.get()

            counties = fetch_counties(selected)

            county_combobox["values"] = counties
            county_combobox.config(state="readonly")
            county_combobox.set("")

            constituency_combobox.set("")
            constituency_combobox.config(state="disabled")

            ward_combobox.set("")
            ward_combobox.config(state="disabled")

        def update_constituencies(event=None):

            selected = county_combobox.get()

            constituencies = fetch_constituencies(selected)

            constituency_combobox["values"] = constituencies
            constituency_combobox.config(state="readonly")
            constituency_combobox.set("")

            ward_combobox.set("")
            ward_combobox.config(state="disabled")

        def update_wards(event=None):

            selected = constituency_combobox.get()

            wards = fetch_wards(selected)

            ward_combobox["values"] = wards
            ward_combobox.config(state="readonly")
            ward_combobox.set("")

        province_combobox.bind(
            "<<ComboboxSelected>>",
            update_counties
        )

        county_combobox.bind(
            "<<ComboboxSelected>>",
            update_constituencies
        )

        constituency_combobox.bind(
            "<<ComboboxSelected>>",
            update_wards
        )

        # --------------------------------------------
        # Submit
        # --------------------------------------------

        def submit():

            first_name_value = first_name_entry.get().strip()
            last_name_value = last_name_entry.get().strip()
            position_value = position_combobox.get().strip()
            age_value = age_entry.get().strip()
            gender_value = gender_combobox.get().strip()
            province_value = province_combobox.get().strip()
            county_value = county_combobox.get().strip()
            constituency_value = constituency_combobox.get().strip()
            ward_value = ward_combobox.get().strip()

            if not all([
                first_name_value,
                last_name_value,
                position_value,
                age_value,
                gender_value,
                province_value,
                county_value,
                constituency_value,
                ward_value
            ]):
                messagebox.showwarning(
                    "Incomplete Application",
                    "Please complete all fields.",
                    parent=popup
                )
                return

            try:
                age = int(age_value)

            except ValueError:
                messagebox.showerror(
                    "Invalid Age",
                    "Age must be a number.",
                    parent=popup
                )
                return

            try:
                conn = sqlite3.connect(VOTING_DB)
                cursor = conn.cursor()

                # Get geographic IDs
                cursor.execute(
                    "SELECT id FROM Provinces WHERE name=?",
                    (province_value,)
                )
                province_id_value = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT id FROM Counties WHERE name=?",
                    (county_value,)
                )
                county_id_value = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT id
                    FROM constituencies
                    WHERE constituency_name=?
                    """,
                    (constituency_value,)
                )
                constituency_id_value = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT id
                    FROM wards
                    WHERE ward_name=?
                    AND constituency_id=?
                    """,
                    (
                        ward_value,
                        constituency_id_value
                    )
                )

                ward_result = cursor.fetchone()

                if not ward_result:
                    raise ValueError(
                        "Selected ward could not be found."
                    )

                ward_id_value = ward_result[0]

                # Insert application
                cursor.execute(
                    """
                    INSERT INTO aspirant (
                        citizen_id,
                        first_name,
                        last_name,
                        aspirant_position,
                        age,
                        gender,
                        province,
                        county,
                        constituency,
                        ward
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        first_name_value,
                        last_name_value,
                        position_value,
                        age,
                        gender_value,
                        province_id_value,
                        county_id_value,
                        constituency_id_value,
                        ward_id_value
                    )
                )

                conn.commit()
                conn.close()

                messagebox.showinfo(
                    "Application Submitted",
                    "Your aspirant application has been submitted successfully.",
                    parent=popup
                )

                popup.destroy()

            except sqlite3.Error as error:

                messagebox.showerror(
                    "Database Error",
                    f"Unable to submit application.\n\n{error}",
                    parent=popup
                )

            except Exception as error:

                messagebox.showerror(
                    "Application Error",
                    str(error),
                    parent=popup
                )

        submit_button = tk.Button(
            form,
            text="SUBMIT APPLICATION",
            command=submit,
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg=ACCENT,
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=12
        )

        submit_button.grid(
            row=14,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=20
        )

    # ========================================================
    # SIDEBAR
    # ========================================================

    sidebar = tk.Frame(
        dashboard,
        bg=SIDEBAR,
        width=250
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    # Logo
    logo_frame = tk.Frame(
        sidebar,
        bg=SIDEBAR
    )
    logo_frame.pack(
        fill="x",
        padx=22,
        pady=(25, 25)
    )

    tk.Label(
        logo_frame,
        text="✓",
        font=("Helvetica", 27, "bold"),
        fg="white",
        bg=ACCENT,
        width=2,
        height=1
    ).pack(side="left")

    logo_text = tk.Frame(
        logo_frame,
        bg=SIDEBAR
    )
    logo_text.pack(side="left", padx=10)

    tk.Label(
        logo_text,
        text="VOTIING",
        font=("Helvetica", 15, "bold"),
        fg=TEXT,
        bg=SIDEBAR
    ).pack(anchor="w")

    tk.Label(
        logo_text,
        text="ELECTION SYSTEM",
        font=("Helvetica", 7, "bold"),
        fg=SECONDARY_TEXT,
        bg=SIDEBAR
    ).pack(anchor="w")

    # User mini-profile
    user_card = tk.Frame(
        sidebar,
        bg=CARD
    )
    user_card.pack(
        fill="x",
        padx=15,
        pady=(0, 25)
    )

    avatar = tk.Label(
        user_card,
        text=first_name[0].upper() if first_name else "?",
        font=("Helvetica", 17, "bold"),
        fg="white",
        bg=ACCENT,
        width=2,
        height=1
    )
    avatar.pack(
        side="left",
        padx=12,
        pady=12
    )

    user_info = tk.Frame(
        user_card,
        bg=CARD
    )
    user_info.pack(
        side="left",
        fill="x",
        expand=True
    )

    tk.Label(
        user_info,
        text=first_name,
        font=("Helvetica", 10, "bold"),
        fg=TEXT,
        bg=CARD
    ).pack(anchor="w")

    tk.Label(
        user_info,
        text="Registered voter",
        font=("Helvetica", 8),
        fg=SECONDARY_TEXT,
        bg=CARD
    ).pack(anchor="w")

    # --------------------------------------------------------
    # Sidebar buttons
    # --------------------------------------------------------

    def sidebar_button(text, command, active=False):

        button = tk.Button(
            sidebar,
            text=text,
            command=command,
            font=("Helvetica", 10, "bold"),
            fg=TEXT if active else SECONDARY_TEXT,
            bg=ACCENT if active else SIDEBAR,
            activebackground=CARD_HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            anchor="w",
            cursor="hand2",
            padx=25,
            pady=13
        )

        button.pack(
            fill="x",
            padx=10,
            pady=2
        )

        return button

    home_button = sidebar_button(
        "⌂    Dashboard",
        show_home,
        active=True
    )

    sidebar_button(
        "◉    My Profile",
        show_profile
    )

    sidebar_button(
        "☑    Vote",
        show_voting
    )

    sidebar_button(
        "♟    Aspirant",
        lambda: open_apply_popup(id_number)
    )

    sidebar_button(
        "▣    Election Results",
        run_results_script
    )

    # Spacer
    spacer = tk.Frame(
        sidebar,
        bg=SIDEBAR
    )
    spacer.pack(
        fill="both",
        expand=True
    )

    # Logout
    def logout():

        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if result:
            dashboard.destroy()

            login_script = os.path.join(
                BASE_DIR,
                "login.py"
            )

            subprocess.Popen(
                [sys.executable, login_script]
            )

    logout_button = tk.Button(
        sidebar,
        text="↪    Logout",
        command=logout,
        font=("Helvetica", 10, "bold"),
        fg="#FCA5A5",
        bg=SIDEBAR,
        activebackground=CARD_HOVER,
        activeforeground=DANGER,
        relief="flat",
        bd=0,
        anchor="w",
        cursor="hand2",
        padx=25,
        pady=15
    )

    logout_button.pack(
        fill="x",
        padx=10,
        pady=(5, 15)
    )

    # ========================================================
    # MAIN CONTENT
    # ========================================================

    main = tk.Frame(
        dashboard,
        bg=BG
    )

    main.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Top bar
    topbar = tk.Frame(
        main,
        bg=BG,
        height=65
    )

    topbar.pack(
        fill="x",
        padx=35,
        pady=(20, 0)
    )

    topbar.pack_propagate(False)

    tk.Label(
        topbar,
        text="Secure Election Portal",
        font=("Helvetica", 10),
        fg=SECONDARY_TEXT,
        bg=BG
    ).pack(side="left")

    tk.Label(
        topbar,
        text="●  ONLINE",
        font=("Helvetica", 9, "bold"),
        fg=SUCCESS,
        bg=BG
    ).pack(side="right")

    # Scrollable content
    canvas = tk.Canvas(
        main,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        main,
        orient="vertical",
        command=canvas.yview
    )

    content_area = tk.Frame(
        canvas,
        bg=BG
    )

    content_area.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=content_area,
        anchor="nw"
    )

    def resize_content(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        resize_content
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(35, 0),
        pady=(0, 25)
    )

    scrollbar.pack(
        side="right",
        fill="y",
        padx=(0, 15),
        pady=(0, 25)
    )

    # Mouse wheel
    def mousewheel(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mousewheel
    )

    # Display home page
    show_home()

    dashboard.mainloop()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python dashboard.py <id_number>")
        sys.exit(1)

    user_id = sys.argv[1]

    open_dashboard(user_id)