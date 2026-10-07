import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os
import hashlib


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER_DB = os.path.join(
    BASE_DIR,
    "databases",
    "user.db"
)


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
INPUT_COLOR = "#334155"
ACCENT_COLOR = "#3B82F6"
ACCENT_HOVER = "#2563EB"
TEXT_COLOR = "#F8FAFC"
SECONDARY_TEXT = "#94A3B8"
BORDER_COLOR = "#475569"


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# LOGIN
# ============================================================

def login():

    id_number = id_entry.get().strip()
    password = password_entry.get()

    # --------------------------------------------------------
    # Validate ID
    # --------------------------------------------------------

    if not id_number:

        messagebox.showwarning(
            "Missing ID Number",
            "Please enter your ID number."
        )

        id_entry.focus()

        return

    if len(id_number) != 8 or not id_number.isdigit():

        messagebox.showerror(
            "Invalid ID Number",
            "ID number must contain exactly 8 digits."
        )

        id_entry.focus()

        return

    # --------------------------------------------------------
    # Validate password
    # --------------------------------------------------------

    if not password:

        messagebox.showwarning(
            "Missing Password",
            "Please enter your password."
        )

        password_entry.focus()

        return

    # --------------------------------------------------------
    # Hash entered password
    # --------------------------------------------------------

    password_hash = hash_password(password)

    # --------------------------------------------------------
    # Connect to user.db
    # --------------------------------------------------------

    try:

        conn = sqlite3.connect(USER_DB)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM users
            WHERE id_number = ?
            AND password = ?
        """, (
            id_number,
            password_hash
        ))

        user = cursor.fetchone()

        conn.close()

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not access the user database.\n\n{error}"
        )

        return

    # --------------------------------------------------------
    # Authentication result
    # --------------------------------------------------------

    if user:

        open_dashboard(id_number)

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid ID number or password."
        )

        password_entry.delete(
            0,
            tk.END
        )

        password_entry.focus()


# ============================================================
# OPEN SIGNUP
# ============================================================

def open_signup():

    login_window.destroy()

    subprocess.Popen([
        "python",
        os.path.join(
            BASE_DIR,
            "signup.py"
        )
    ])


# ============================================================
# OPEN DASHBOARD
# ============================================================

def open_dashboard(user_id):

    login_window.destroy()

    subprocess.Popen([
        "python",
        os.path.join(
            BASE_DIR,
            "dashboard.py"
        ),
        str(user_id)
    ])


# ============================================================
# PASSWORD VISIBILITY
# ============================================================

password_visible = False


def toggle_password():

    global password_visible

    password_visible = not password_visible

    if password_visible:

        password_entry.configure(
            show=""
        )

        password_toggle.configure(
            text="Hide"
        )

    else:

        password_entry.configure(
            show="●"
        )

        password_toggle.configure(
            text="Show"
        )


# ============================================================
# ID VALIDATION
# ============================================================

def validate_id(P):

    if P == "":
        return True

    return P.isdigit() and len(P) <= 8


# ============================================================
# MAIN WINDOW
# ============================================================

login_window = tk.Tk()

login_window.title(
    "Voter Login"
)

login_window.geometry(
    "520x620"
)

login_window.minsize(
    450,
    550
)

login_window.configure(
    bg=BG_COLOR
)


# ============================================================
# CENTER WINDOW
# ============================================================

login_window.update_idletasks()

screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

window_width = 520
window_height = 620

x = (
    screen_width -
    window_width
) // 2

y = (
    screen_height -
    window_height
) // 2

login_window.geometry(
    f"{window_width}x{window_height}+{x}+{y}"
)


# ============================================================
# MAIN CONTAINER
# ============================================================

main_frame = tk.Frame(
    login_window,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=45
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

header.pack(
    fill="x",
    pady=(55, 25)
)


# Logo

logo = tk.Label(
    header,
    text="✓",
    font=(
        "Helvetica",
        30,
        "bold"
    ),
    fg="white",
    bg=ACCENT_COLOR,
    width=3,
    height=1
)

logo.pack(
    pady=(0, 18)
)


# Title

title = tk.Label(
    header,
    text="Welcome Back",
    font=(
        "Helvetica",
        26,
        "bold"
    ),
    fg=TEXT_COLOR,
    bg=BG_COLOR
)

title.pack()


# Subtitle

subtitle = tk.Label(
    header,
    text="Sign in to your voter account",
    font=(
        "Helvetica",
        11
    ),
    fg=SECONDARY_TEXT,
    bg=BG_COLOR
)

subtitle.pack(
    pady=(6, 0)
)


# ============================================================
# LOGIN CARD
# ============================================================

card = tk.Frame(
    main_frame,
    bg=CARD_COLOR
)

card.pack(
    fill="x"
)


# ============================================================
# CARD CONTENT
# ============================================================

content = tk.Frame(
    card,
    bg=CARD_COLOR
)

content.pack(
    fill="x",
    padx=30,
    pady=30
)


# ============================================================
# ID LABEL
# ============================================================

id_label = tk.Label(
    content,
    text="ID NUMBER",
    font=(
        "Helvetica",
        10,
        "bold"
    ),
    fg=SECONDARY_TEXT,
    bg=CARD_COLOR,
    anchor="w"
)

id_label.pack(
    fill="x",
    pady=(0, 7)
)


# ============================================================
# ID ENTRY
# ============================================================

id_entry = tk.Entry(
    content,
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    bd=0,
    font=(
        "Helvetica",
        12
    ),
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_COLOR
)

id_entry.pack(
    fill="x",
    ipady=11
)


# ID validation

id_validation = (
    login_window.register(
        validate_id
    ),
    "%P"
)

id_entry.configure(
    validate="key",
    validatecommand=id_validation
)


# ============================================================
# PASSWORD LABEL
# ============================================================

password_label = tk.Label(
    content,
    text="PASSWORD",
    font=(
        "Helvetica",
        10,
        "bold"
    ),
    fg=SECONDARY_TEXT,
    bg=CARD_COLOR,
    anchor="w"
)

password_label.pack(
    fill="x",
    pady=(22, 7)
)


# ============================================================
# PASSWORD CONTAINER
# ============================================================

password_frame = tk.Frame(
    content,
    bg=INPUT_COLOR
)

password_frame.pack(
    fill="x"
)

password_frame.columnconfigure(
    0,
    weight=1
)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password_entry = tk.Entry(
    password_frame,
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    bd=0,
    font=(
        "Helvetica",
        12
    ),
    show="●"
)

password_entry.grid(
    row=0,
    column=0,
    sticky="ew",
    ipady=11,
    padx=(12, 0)
)


# ============================================================
# PASSWORD TOGGLE
# ============================================================

password_toggle = tk.Button(
    password_frame,
    text="Show",
    command=toggle_password,
    bg=INPUT_COLOR,
    fg=ACCENT_COLOR,
    activebackground=INPUT_COLOR,
    activeforeground=ACCENT_HOVER,
    relief="flat",
    bd=0,
    font=(
        "Helvetica",
        9,
        "bold"
    ),
    cursor="hand2"
)

password_toggle.grid(
    row=0,
    column=1,
    padx=12
)


# ============================================================
# LOGIN BUTTON
# ============================================================

def login_hover(event):

    login_button.configure(
        bg=ACCENT_HOVER
    )


def login_leave(event):

    login_button.configure(
        bg=ACCENT_COLOR
    )


login_button = tk.Button(
    content,
    text="SIGN IN",
    command=login,
    bg=ACCENT_COLOR,
    fg="white",
    activebackground=ACCENT_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    font=(
        "Helvetica",
        11,
        "bold"
    ),
    cursor="hand2"
)

login_button.pack(
    fill="x",
    pady=(28, 0),
    ipady=12
)

login_button.bind(
    "<Enter>",
    login_hover
)

login_button.bind(
    "<Leave>",
    login_leave
)


# ============================================================
# SIGNUP AREA
# ============================================================

signup_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

signup_frame.pack(
    fill="x",
    pady=25
)


signup_text = tk.Label(
    signup_frame,
    text="Don't have an account?",
    font=(
        "Helvetica",
        10
    ),
    fg=SECONDARY_TEXT,
    bg=BG_COLOR
)

signup_text.pack(
    side="left"
)


signup_button = tk.Button(
    signup_frame,
    text=" Register",
    command=open_signup,
    bg=BG_COLOR,
    fg=ACCENT_COLOR,
    activebackground=BG_COLOR,
    activeforeground=ACCENT_HOVER,
    relief="flat",
    bd=0,
    font=(
        "Helvetica",
        10,
        "bold"
    ),
    cursor="hand2"
)

signup_button.pack(
    side="left"
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    main_frame,
    text="Secure Voter Authentication",
    font=(
        "Helvetica",
        9
    ),
    fg="#64748B",
    bg=BG_COLOR
)

footer.pack(
    pady=(5, 25)
)


# ============================================================
# ENTER KEY
# ============================================================

login_window.bind(
    "<Return>",
    lambda event: login()
)


# ============================================================
# INITIAL FOCUS
# ============================================================

id_entry.focus()


# ============================================================
# START APPLICATION
# ============================================================

login_window.mainloop()
