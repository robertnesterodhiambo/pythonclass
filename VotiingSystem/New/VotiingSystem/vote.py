import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER_DB = os.path.join(BASE_DIR, "databases", "user.db")
VOTING_DB = os.path.join(BASE_DIR, "databases", "voting.db")
VOTE_DB = os.path.join(BASE_DIR, "databases", "vote.db")


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
# DATABASE INITIALIZATION
# ============================================================

def initialize_vote_database():

    """
    Make sure vote.db exists and contains the votes table.
    """

    try:

        conn = sqlite3.connect(VOTE_DB)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                id_number TEXT NOT NULL UNIQUE
                    CHECK (
                        length(id_number) = 8
                        AND id_number GLOB '[0-9]*'
                        AND id_number NOT GLOB '*[^0-9]*'
                    ),

                president_vote TEXT NOT NULL,
                governor_vote TEXT NOT NULL,
                senator_vote TEXT NOT NULL,
                women_rep_vote TEXT NOT NULL,
                mp_vote TEXT NOT NULL,
                mca_vote TEXT NOT NULL,

                province INTEGER NOT NULL,
                county INTEGER NOT NULL,
                constituency INTEGER NOT NULL,
                ward INTEGER NOT NULL,

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Unable to initialize vote database.\n\n{error}"
        )


# ============================================================
# GET USER
# ============================================================

def get_user(user_id):

    """
    Get voter information from user.db.
    """

    try:

        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id_number,
                first_name,
                second_name,
                last_name,
                province,
                county,
                constituency,
                ward
            FROM users
            WHERE id_number = ?
        """, (str(user_id),))

        user = cursor.fetchone()

        conn.close()

        return user

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Unable to retrieve voter information.\n\n{error}"
        )

        return None


# ============================================================
# GET LOCATION NAMES
# ============================================================

def get_location_names(
    province_id,
    county_id,
    constituency_id,
    ward_id
):

    """
    Convert geographic IDs stored in user.db
    into names from voting.db.
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
            """
            SELECT constituency_name
            FROM constituencies
            WHERE id=?
            """,
            (constituency_id,)
        )

        constituency = cursor.fetchone()

        cursor.execute(
            """
            SELECT ward_name
            FROM wards
            WHERE id=?
            """,
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


# ============================================================
# CHECK IF ALREADY VOTED
# ============================================================

def has_voted(user_id):

    try:

        conn = sqlite3.connect(VOTE_DB)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM votes
            WHERE id_number=?
            LIMIT 1
            """,
            (str(user_id),)
        )

        result = cursor.fetchone()

        conn.close()

        return result is not None

    except sqlite3.Error:

        return False


# ============================================================
# FETCH ASPIRANTS
# ============================================================

def fetch_aspirants(
    position,
    location_column=None,
    location_value=None
):

    """
    Fetch candidate names from voting.db.

    Aspirant geographic columns contain the corresponding
    geographic IDs.
    """

    try:

        conn = sqlite3.connect(VOTING_DB)
        cursor = conn.cursor()

        if location_column:

            query = f"""
                SELECT
                    id,
                    first_name || ' ' || last_name
                FROM aspirant
                WHERE aspirant_position=?
                AND {location_column}=?
                ORDER BY first_name, last_name
            """

            cursor.execute(
                query,
                (
                    position,
                    location_value
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    first_name || ' ' || last_name
                FROM aspirant
                WHERE aspirant_position=?
                ORDER BY first_name, last_name
                """,
                (position,)
            )

        candidates = cursor.fetchall()

        conn.close()

        return candidates

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Unable to load candidates.\n\n{error}"
        )

        return []


# ============================================================
# MAIN VOTING PANEL
# ============================================================

def open_vote_panel(user_id):

    # --------------------------------------------------------
    # Initialize vote database
    # --------------------------------------------------------

    initialize_vote_database()

    # --------------------------------------------------------
    # Check user
    # --------------------------------------------------------

    user = get_user(user_id)

    if not user:

        messagebox.showerror(
            "Voter Not Found",
            "Your voter information could not be found."
        )

        return

    (
        id_number,
        first_name,
        second_name,
        last_name,
        province_id,
        county_id,
        constituency_id,
        ward_id
    ) = user

    # --------------------------------------------------------
    # Check whether already voted
    # --------------------------------------------------------

    if has_voted(id_number):

        messagebox.showinfo(
            "Already Voted",
            "Your vote has already been recorded.\n\n"
            "A voter can only submit one ballot."
        )

        return

    # --------------------------------------------------------
    # Get location names
    # --------------------------------------------------------

    (
        province_name,
        county_name,
        constituency_name,
        ward_name
    ) = get_location_names(
        province_id,
        county_id,
        constituency_id,
        ward_id
    )

    # ========================================================
    # WINDOW
    # ========================================================

    vote_panel = tk.Toplevel()

    vote_panel.title("Votiing System — Cast Your Vote")
    vote_panel.geometry("850x720")
    vote_panel.minsize(750, 650)
    vote_panel.configure(bg=BG)

    vote_panel.transient()
    vote_panel.grab_set()

    # ========================================================
    # STYLE
    # ========================================================

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Vote.TCombobox",
        fieldbackground=INPUT,
        background=INPUT,
        foreground=TEXT,
        borderwidth=0,
        arrowsize=14,
        padding=8
    )

    style.map(
        "Vote.TCombobox",
        fieldbackground=[
            ("readonly", INPUT)
        ],
        foreground=[
            ("readonly", TEXT)
        ]
    )

    # ========================================================
    # HEADER
    # ========================================================

    header = tk.Frame(
        vote_panel,
        bg=BG
    )

    header.pack(
        fill="x",
        padx=35,
        pady=(25, 15)
    )

    tk.Label(
        header,
        text="Cast Your Vote",
        font=("Helvetica", 25, "bold"),
        fg=TEXT,
        bg=BG
    ).pack(anchor="w")

    tk.Label(
        header,
        text=(
            f"Welcome, {first_name}. "
            "Select one candidate for each position."
        ),
        font=("Helvetica", 10),
        fg=SECONDARY_TEXT,
        bg=BG
    ).pack(anchor="w", pady=(5, 0))

    # ========================================================
    # VOTER INFORMATION
    # ========================================================

    voter_card = tk.Frame(
        vote_panel,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    voter_card.pack(
        fill="x",
        padx=35,
        pady=(0, 15)
    )

    voter_left = tk.Frame(
        voter_card,
        bg=CARD
    )

    voter_left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    tk.Label(
        voter_left,
        text=f"{first_name} {second_name} {last_name}",
        font=("Helvetica", 12, "bold"),
        fg=TEXT,
        bg=CARD
    ).pack(anchor="w")

    tk.Label(
        voter_left,
        text=f"Voter ID: {id_number}",
        font=("Helvetica", 9),
        fg=SECONDARY_TEXT,
        bg=CARD
    ).pack(anchor="w", pady=(3, 0))

    voter_location = tk.Frame(
        voter_card,
        bg=CARD
    )

    voter_location.pack(
        side="right",
        padx=20,
        pady=15
    )

    tk.Label(
        voter_location,
        text=ward_name,
        font=("Helvetica", 10, "bold"),
        fg=ACCENT,
        bg=CARD
    ).pack(anchor="e")

    tk.Label(
        voter_location,
        text=f"{constituency_name} • {county_name}",
        font=("Helvetica", 8),
        fg=SECONDARY_TEXT,
        bg=CARD
    ).pack(anchor="e")

    # ========================================================
    # SCROLLABLE VOTING AREA
    # ========================================================

    container = tk.Frame(
        vote_panel,
        bg=BG
    )

    container.pack(
        fill="both",
        expand=True,
        padx=35
    )

    canvas = tk.Canvas(
        container,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview
    )

    voting_frame = tk.Frame(
        canvas,
        bg=BG
    )

    voting_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=voting_frame,
        anchor="nw"
    )

    def resize_voting_frame(event):

        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        resize_voting_frame
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ========================================================
    # POSITIONS
    # ========================================================

    positions = [
        (
            "President",
            None,
            None
        ),

        (
            "Governor",
            "province",
            province_id
        ),

        (
            "Senator",
            "county",
            county_id
        ),

        (
            "Women Rep",
            "county",
            county_id
        ),

        (
            "Member of Parliament (MP)",
            "constituency",
            constituency_id
        ),

        (
            "Member of County Assembly (MCA)",
            "ward",
            ward_id
        )
    ]

    comboboxes = {}

    candidate_maps = {}

    for index, (
        position,
        location_column,
        location_value
    ) in enumerate(positions):

        # --------------------------------------------
        # Position card
        # --------------------------------------------

        card = tk.Frame(
            voting_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=6
        )

        # --------------------------------------------
        # Position header
        # --------------------------------------------

        header_frame = tk.Frame(
            card,
            bg=CARD
        )

        header_frame.pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        tk.Label(
            header_frame,
            text=f"{index + 1:02d}",
            font=("Helvetica", 10, "bold"),
            fg=ACCENT,
            bg=INPUT,
            width=3,
            pady=5
        ).pack(side="left")

        tk.Label(
            header_frame,
            text=position,
            font=("Helvetica", 11, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(
            side="left",
            padx=12
        )

        # --------------------------------------------
        # Candidate dropdown
        # --------------------------------------------

        candidates = fetch_aspirants(
            position,
            location_column,
            location_value
        )

        candidate_maps[position] = {
            name: candidate_id
            for candidate_id, name in candidates
        }

        candidate_names = [
            name
            for candidate_id, name in candidates
        ]

        combobox = ttk.Combobox(
            card,
            values=candidate_names,
            state="readonly",
            style="Vote.TCombobox",
            font=("Helvetica", 10)
        )

        combobox.pack(
            fill="x",
            padx=18,
            pady=(5, 18)
        )

        comboboxes[position] = combobox

        if not candidate_names:

            combobox.set(
                "No candidates available"
            )

            combobox.configure(
                state="disabled"
            )

    # ========================================================
    # BOTTOM ACTION AREA
    # ========================================================

    action_frame = tk.Frame(
        vote_panel,
        bg=BG
    )

    action_frame.pack(
        fill="x",
        padx=35,
        pady=20
    )

    # --------------------------------------------------------
    # Warning
    # --------------------------------------------------------

    tk.Label(
        action_frame,
        text="⚠  Your ballot can only be submitted once.",
        font=("Helvetica", 9),
        fg=WARNING,
        bg=BG
    ).pack(
        side="left"
    )

    # --------------------------------------------------------
    # Submit
    # --------------------------------------------------------

    def submit_votes():

        selected_names = {}

        # --------------------------------------------
        # Validate selections
        # --------------------------------------------

        for position, combobox in comboboxes.items():

            if str(combobox["state"]) == "disabled":

                messagebox.showerror(
                    "Candidate Unavailable",
                    f"No candidate is available for {position}.",
                    parent=vote_panel
                )

                return

            selected = combobox.get().strip()

            if not selected:

                messagebox.showerror(
                    "Incomplete Ballot",
                    f"Please select a candidate for {position}.",
                    parent=vote_panel
                )

                combobox.focus_set()

                return

            selected_names[position] = selected

        # --------------------------------------------
        # Confirmation
        # --------------------------------------------

        confirmation = messagebox.askyesno(
            "Confirm Your Ballot",
            "Are you sure you want to submit your ballot?\n\n"
            "Once submitted, your vote cannot be changed.",
            parent=vote_panel
        )

        if not confirmation:
            return

        # --------------------------------------------
        # Insert ballot
        # --------------------------------------------

        conn = None

        try:

            conn = sqlite3.connect(VOTE_DB)

            cursor = conn.cursor()

            # Check again immediately before insertion
            cursor.execute(
                """
                SELECT id
                FROM votes
                WHERE id_number=?
                LIMIT 1
                """,
                (id_number,)
            )

            if cursor.fetchone():

                messagebox.showinfo(
                    "Already Voted",
                    "Your ballot has already been recorded.",
                    parent=vote_panel
                )

                vote_panel.destroy()

                return

            cursor.execute(
                """
                INSERT INTO votes (
                    id_number,
                    president_vote,
                    governor_vote,
                    senator_vote,
                    women_rep_vote,
                    mp_vote,
                    mca_vote,
                    province,
                    county,
                    constituency,
                    ward
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    id_number,

                    selected_names["President"],

                    selected_names["Governor"],

                    selected_names["Senator"],

                    selected_names["Women Rep"],

                    selected_names[
                        "Member of Parliament (MP)"
                    ],

                    selected_names[
                        "Member of County Assembly (MCA)"
                    ],

                    province_id,

                    county_id,

                    constituency_id,

                    ward_id
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Vote Submitted",
                "Your ballot has been submitted successfully.\n\n"
                "Thank you for participating in the election.",
                parent=vote_panel
            )

            vote_panel.destroy()

        except sqlite3.IntegrityError:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Vote Already Submitted",
                "This voter already has a recorded ballot.",
                parent=vote_panel
            )

        except sqlite3.Error as error:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Your ballot could not be submitted.\n\n{error}",
                parent=vote_panel
            )

        finally:

            if conn:
                conn.close()

    submit_button = tk.Button(
        action_frame,
        text="SUBMIT BALLOT  →",
        command=submit_votes,
        font=("Helvetica", 10, "bold"),
        fg="white",
        bg=ACCENT,
        activebackground=ACCENT_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=25,
        pady=12
    )

    submit_button.pack(
        side="right"
    )

    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def mousewheel(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mousewheel
    )

    # ========================================================
    # CLOSE
    # ========================================================

    def close_vote_panel():

        canvas.unbind_all("<MouseWheel>")
        vote_panel.destroy()

    vote_panel.protocol(
        "WM_DELETE_WINDOW",
        close_vote_panel
    )

    # ========================================================
    # START
    # ========================================================

    vote_panel.focus_force()