import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import subprocess
import os
import hashlib


# ============================================================
# DATABASE PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VOTING_DB = os.path.join(BASE_DIR, "databases", "voting.db")
USER_DB = os.path.join(BASE_DIR, "databases", "user.db")


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
SUCCESS_COLOR = "#22C55E"
ERROR_COLOR = "#EF4444"


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_user_db():
    return sqlite3.connect(USER_DB)


def connect_voting_db():
    return sqlite3.connect(VOTING_DB)


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

password_visible = False


def toggle_password():
    global password_visible

    password_visible = not password_visible

    if password_visible:
        password_entry.configure(show="")
        password_toggle.configure(text="Hide")
    else:
        password_entry.configure(show="●")
        password_toggle.configure(text="Show")


# ============================================================
# VALIDATE ID NUMBER
# ============================================================

def validate_id_number(value):

    if value == "":
        return True

    return value.isdigit() and len(value) <= 8


def validate_id_keypress(P):
    return validate_id_number(P)


# ============================================================
# UPDATE COUNTIES
# ============================================================

def update_counties(event=None):

    province_name = province_var.get()

    province_id = province_ids.get(province_name)

    if not province_id:
        return

    try:

        conn = connect_voting_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name
            FROM Counties
            WHERE province_id = ?
            ORDER BY name
        """, (province_id,))

        counties = cursor.fetchall()

        conn.close()

        county_ids.clear()
        constituency_ids.clear()
        ward_ids.clear()

        county_var.set("")
        constituency_var.set("")
        ward_var.set("")

        county_dropdown["values"] = [
            county[1]
            for county in counties
        ]

        constituency_dropdown["values"] = []
        ward_dropdown["values"] = []

        for county_id, county_name in counties:
            county_ids[county_name] = county_id

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not load counties.\n\n{error}"
        )


# ============================================================
# UPDATE CONSTITUENCIES
# ============================================================

def update_constituencies(event=None):

    county_name = county_var.get()

    county_id = county_ids.get(county_name)

    if not county_id:
        return

    try:

        conn = connect_voting_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, constituency_name
            FROM constituencies
            WHERE county_id = ?
            ORDER BY constituency_name
        """, (county_id,))

        constituencies = cursor.fetchall()

        conn.close()

        constituency_ids.clear()
        ward_ids.clear()

        constituency_var.set("")
        ward_var.set("")

        constituency_dropdown["values"] = [
            constituency[1]
            for constituency in constituencies
        ]

        ward_dropdown["values"] = []

        for constituency_id, constituency_name in constituencies:
            constituency_ids[constituency_name] = constituency_id

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not load constituencies.\n\n{error}"
        )


# ============================================================
# UPDATE WARDS
# ============================================================

def update_wards(event=None):

    constituency_name = constituency_var.get()

    constituency_id = constituency_ids.get(
        constituency_name
    )

    if not constituency_id:
        return

    try:

        conn = connect_voting_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, ward_name
            FROM wards
            WHERE constituency_id = ?
            ORDER BY ward_name
        """, (constituency_id,))

        wards = cursor.fetchall()

        conn.close()

        ward_ids.clear()

        ward_var.set("")

        ward_dropdown["values"] = [
            ward[1]
            for ward in wards
        ]

        for ward_id, ward_name in wards:
            ward_ids[ward_name] = ward_id

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not load wards.\n\n{error}"
        )


# ============================================================
# SUBMIT FORM
# ============================================================

def submit_form():

    first_name = first_name_entry.get().strip()
    second_name = second_name_entry.get().strip()
    last_name = last_name_entry.get().strip()

    date_of_birth = dob_entry.get().strip()

    id_number = id_entry.get().strip()

    place_of_birth = pob_entry.get().strip()

    password = password_entry.get()

    province_name = province_var.get().strip()
    county_name = county_var.get().strip()
    constituency_name = constituency_var.get().strip()
    ward_name = ward_var.get().strip()

    # ========================================================
    # REQUIRED FIELDS
    # ========================================================

    if not all([
        first_name,
        second_name,
        last_name,
        date_of_birth,
        id_number,
        place_of_birth,
        password,
        province_name,
        county_name,
        constituency_name,
        ward_name
    ]):

        messagebox.showwarning(
            "Incomplete Form",
            "Please complete all required fields."
        )

        return

    # ========================================================
    # ID VALIDATION
    # ========================================================

    if len(id_number) != 8 or not id_number.isdigit():

        messagebox.showerror(
            "Invalid ID Number",
            "The ID number must contain exactly 8 digits."
        )

        id_entry.focus()

        return

    # ========================================================
    # PASSWORD VALIDATION
    # ========================================================

    if len(password) < 6:

        messagebox.showerror(
            "Weak Password",
            "Password must contain at least 6 characters."
        )

        password_entry.focus()

        return

    # ========================================================
    # GET LOCATION IDS
    # ========================================================

    province_id = province_ids.get(province_name)

    county_id = county_ids.get(county_name)

    constituency_id = constituency_ids.get(
        constituency_name
    )

    ward_id = ward_ids.get(ward_name)

    if not all([
        province_id,
        county_id,
        constituency_id,
        ward_id
    ]):

        messagebox.showerror(
            "Invalid Location",
            "Please select a valid Province, County, "
            "Constituency and Ward."
        )

        return

    # ========================================================
    # SAVE USER
    # ========================================================

    try:

        conn = connect_user_db()
        cursor = conn.cursor()

        # Check duplicate ID

        cursor.execute("""
            SELECT id
            FROM users
            WHERE id_number = ?
        """, (id_number,))

        if cursor.fetchone():

            conn.close()

            messagebox.showerror(
                "Already Registered",
                "This ID number is already registered."
            )

            return

        # Hash password

        password_hash = hash_password(password)

        # Insert user

        cursor.execute("""
            INSERT INTO users (
                first_name,
                second_name,
                last_name,
                date_of_birth,
                id_number,
                place_of_birth,
                password,
                province,
                county,
                constituency,
                ward
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name,
            second_name,
            last_name,
            date_of_birth,
            id_number,
            place_of_birth,
            password_hash,
            province_id,
            county_id,
            constituency_id,
            ward_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Registration Successful",
            "Your account has been created successfully."
        )

        clear_form()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Registration Error",
            "This ID number is already registered."
        )

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not create account.\n\n{error}"
        )


# ============================================================
# CLEAR FORM
# ============================================================

def clear_form():

    first_name_entry.delete(0, tk.END)
    second_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    pob_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    province_var.set("")
    county_var.set("")
    constituency_var.set("")
    ward_var.set("")

    county_dropdown["values"] = []
    constituency_dropdown["values"] = []
    ward_dropdown["values"] = []

    county_ids.clear()
    constituency_ids.clear()
    ward_ids.clear()

    first_name_entry.focus()


# ============================================================
# OPEN LOGIN
# ============================================================

def open_login():

    root.destroy()

    subprocess.Popen([
        "python",
        os.path.join(BASE_DIR, "login.py")
    ])


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Voter Registration")

root.geometry("720x850")

root.minsize(650, 700)

root.configure(
    bg=BG_COLOR
)


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Modern.TCombobox",
    fieldbackground=INPUT_COLOR,
    background=INPUT_COLOR,
    foreground=TEXT_COLOR,
    borderwidth=0,
    arrowsize=18,
    padding=10,
    font=("Helvetica", 11)
)

style.map(
    "Modern.TCombobox",
    fieldbackground=[
        ("readonly", INPUT_COLOR)
    ],
    foreground=[
        ("readonly", TEXT_COLOR)
    ]
)


# ============================================================
# SCROLLABLE AREA
# ============================================================

outer_canvas = tk.Canvas(
    root,
    bg=BG_COLOR,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    root,
    orient="vertical",
    command=outer_canvas.yview
)

outer_canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

outer_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


main_frame = tk.Frame(
    outer_canvas,
    bg=BG_COLOR
)

canvas_window = outer_canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="n"
)


def update_scroll_region(event=None):

    outer_canvas.configure(
        scrollregion=outer_canvas.bbox("all")
    )

    outer_canvas.itemconfigure(
        canvas_window,
        width=outer_canvas.winfo_width()
    )


main_frame.bind(
    "<Configure>",
    update_scroll_region
)

outer_canvas.bind(
    "<Configure>",
    update_scroll_region
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
    padx=45,
    pady=(35, 20)
)


# Logo / icon

logo = tk.Label(
    header,
    text="✓",
    font=("Helvetica", 28, "bold"),
    fg="white",
    bg=ACCENT_COLOR,
    width=3,
    height=1
)

logo.pack(
    pady=(0, 15)
)


title = tk.Label(
    header,
    text="Voter Registration",
    font=("Helvetica", 25, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
)

title.pack()


subtitle = tk.Label(
    header,
    text="Create your voter account",
    font=("Helvetica", 11),
    fg=SECONDARY_TEXT,
    bg=BG_COLOR
)

subtitle.pack(
    pady=(5, 0)
)


# ============================================================
# PERSONAL INFORMATION CARD
# ============================================================

personal_card = tk.Frame(
    main_frame,
    bg=CARD_COLOR
)

personal_card.pack(
    fill="x",
    padx=45,
    pady=10
)


personal_title = tk.Label(
    personal_card,
    text="  Personal Information",
    font=("Helvetica", 15, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR,
    anchor="w"
)

personal_title.pack(
    fill="x",
    padx=20,
    pady=(20, 15)
)


def create_label(parent, text):

    return tk.Label(
        parent,
        text=text,
        font=("Helvetica", 10, "bold"),
        fg=SECONDARY_TEXT,
        bg=CARD_COLOR,
        anchor="w"
    )


def create_entry(parent):

    return tk.Entry(
        parent,
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        relief="flat",
        bd=0,
        font=("Helvetica", 11),
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        highlightcolor=ACCENT_COLOR
    )


# Grid

personal_grid = tk.Frame(
    personal_card,
    bg=CARD_COLOR
)

personal_grid.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

personal_grid.columnconfigure(0, weight=1)
personal_grid.columnconfigure(1, weight=1)


# First name

create_label(
    personal_grid,
    "FIRST NAME"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=(0, 10),
    pady=(5, 5)
)

first_name_entry = create_entry(personal_grid)

first_name_entry.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=(0, 10),
    pady=(0, 15),
    ipady=9
)


# Second name

create_label(
    personal_grid,
    "SECOND NAME"
).grid(
    row=0,
    column=1,
    sticky="w",
    padx=(10, 0),
    pady=(5, 5)
)

second_name_entry = create_entry(personal_grid)

second_name_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=(10, 0),
    pady=(0, 15),
    ipady=9
)


# Last name

create_label(
    personal_grid,
    "LAST NAME"
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=(0, 10),
    pady=(5, 5)
)

last_name_entry = create_entry(personal_grid)

last_name_entry.grid(
    row=3,
    column=0,
    sticky="ew",
    padx=(0, 10),
    pady=(0, 15),
    ipady=9
)


# Date of birth

create_label(
    personal_grid,
    "DATE OF BIRTH"
).grid(
    row=2,
    column=1,
    sticky="w",
    padx=(10, 0),
    pady=(5, 5)
)

dob_entry = DateEntry(
    personal_grid,
    width=18,
    background=ACCENT_COLOR,
    foreground="white",
    borderwidth=0,
    date_pattern="yyyy-mm-dd",
    font=("Helvetica", 11)
)

dob_entry.grid(
    row=3,
    column=1,
    sticky="ew",
    padx=(10, 0),
    pady=(0, 15),
    ipady=7
)


# ID Number

create_label(
    personal_grid,
    "8-DIGIT ID NUMBER"
).grid(
    row=4,
    column=0,
    sticky="w",
    padx=(0, 10),
    pady=(5, 5)
)

vcmd = (
    root.register(validate_id_keypress),
    "%P"
)

id_entry = tk.Entry(
    personal_grid,
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    bd=0,
    font=("Helvetica", 11),
    validate="key",
    validatecommand=vcmd,
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_COLOR
)

id_entry.grid(
    row=5,
    column=0,
    sticky="ew",
    padx=(0, 10),
    pady=(0, 15),
    ipady=9
)


# Place of birth

create_label(
    personal_grid,
    "PLACE OF BIRTH"
).grid(
    row=4,
    column=1,
    sticky="w",
    padx=(10, 0),
    pady=(5, 5)
)

pob_entry = create_entry(personal_grid)

pob_entry.grid(
    row=5,
    column=1,
    sticky="ew",
    padx=(10, 0),
    pady=(0, 15),
    ipady=9
)


# Password

create_label(
    personal_grid,
    "PASSWORD"
).grid(
    row=6,
    column=0,
    sticky="w",
    padx=(0, 10),
    pady=(5, 5)
)


password_frame = tk.Frame(
    personal_grid,
    bg=INPUT_COLOR
)

password_frame.grid(
    row=7,
    column=0,
    sticky="ew",
    padx=(0, 10),
    pady=(0, 5)
)

password_frame.columnconfigure(0, weight=1)


password_entry = tk.Entry(
    password_frame,
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    bd=0,
    font=("Helvetica", 11),
    show="●"
)

password_entry.grid(
    row=0,
    column=0,
    sticky="ew",
    ipady=9,
    padx=(10, 0)
)


password_toggle = tk.Button(
    password_frame,
    text="Show",
    command=toggle_password,
    bg=INPUT_COLOR,
    fg=ACCENT_COLOR,
    activebackground=INPUT_COLOR,
    activeforeground=ACCENT_COLOR,
    relief="flat",
    bd=0,
    font=("Helvetica", 9, "bold"),
    cursor="hand2"
)

password_toggle.grid(
    row=0,
    column=1,
    padx=10
)


# ============================================================
# LOCATION CARD
# ============================================================

location_card = tk.Frame(
    main_frame,
    bg=CARD_COLOR
)

location_card.pack(
    fill="x",
    padx=45,
    pady=10
)


location_title = tk.Label(
    location_card,
    text="  Location",
    font=("Helvetica", 15, "bold"),
    fg=TEXT_COLOR,
    bg=CARD_COLOR,
    anchor="w"
)

location_title.pack(
    fill="x",
    padx=20,
    pady=(20, 5)
)


location_subtitle = tk.Label(
    location_card,
    text="Select your location from Province down to Ward",
    font=("Helvetica", 10),
    fg=SECONDARY_TEXT,
    bg=CARD_COLOR,
    anchor="w"
)

location_subtitle.pack(
    fill="x",
    padx=20,
    pady=(0, 15)
)


location_grid = tk.Frame(
    location_card,
    bg=CARD_COLOR
)

location_grid.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

location_grid.columnconfigure(1, weight=1)


# ============================================================
# LOAD PROVINCES
# ============================================================

try:

    conn = connect_voting_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM Provinces
        ORDER BY name
    """)

    provinces = cursor.fetchall()

    conn.close()

except sqlite3.Error as error:

    messagebox.showerror(
        "Database Error",
        f"Could not load provinces.\n\n{error}"
    )

    root.destroy()

    raise SystemExit


province_ids = {
    province[1]: province[0]
    for province in provinces
}

county_ids = {}
constituency_ids = {}
ward_ids = {}


province_var = tk.StringVar()
county_var = tk.StringVar()
constituency_var = tk.StringVar()
ward_var = tk.StringVar()


def create_location_label(text, row):

    label = tk.Label(
        location_grid,
        text=text,
        font=("Helvetica", 10, "bold"),
        fg=SECONDARY_TEXT,
        bg=CARD_COLOR,
        anchor="w"
    )

    label.grid(
        row=row,
        column=0,
        sticky="w",
        padx=(0, 20),
        pady=9
    )


# Province

create_location_label(
    "PROVINCE",
    0
)

province_dropdown = ttk.Combobox(
    location_grid,
    textvariable=province_var,
    state="readonly",
    style="Modern.TCombobox"
)

province_dropdown["values"] = [
    province[1]
    for province in provinces
]

province_dropdown.grid(
    row=0,
    column=1,
    sticky="ew",
    pady=5
)

province_dropdown.bind(
    "<<ComboboxSelected>>",
    update_counties
)


# County

create_location_label(
    "COUNTY",
    1
)

county_dropdown = ttk.Combobox(
    location_grid,
    textvariable=county_var,
    state="readonly",
    style="Modern.TCombobox"
)

county_dropdown.grid(
    row=1,
    column=1,
    sticky="ew",
    pady=5
)

county_dropdown.bind(
    "<<ComboboxSelected>>",
    update_constituencies
)


# Constituency

create_location_label(
    "CONSTITUENCY",
    2
)

constituency_dropdown = ttk.Combobox(
    location_grid,
    textvariable=constituency_var,
    state="readonly",
    style="Modern.TCombobox"
)

constituency_dropdown.grid(
    row=2,
    column=1,
    sticky="ew",
    pady=5
)

constituency_dropdown.bind(
    "<<ComboboxSelected>>",
    update_wards
)


# Ward

create_location_label(
    "WARD",
    3
)

ward_dropdown = ttk.Combobox(
    location_grid,
    textvariable=ward_var,
    state="readonly",
    style="Modern.TCombobox"
)

ward_dropdown.grid(
    row=3,
    column=1,
    sticky="ew",
    pady=5
)


# ============================================================
# BUTTON AREA
# ============================================================

button_frame = tk.Frame(
    main_frame,
    bg=BG_COLOR
)

button_frame.pack(
    fill="x",
    padx=45,
    pady=(15, 40)
)


def submit_hover(event):

    submit_button.configure(
        bg=ACCENT_HOVER
    )


def submit_leave(event):

    submit_button.configure(
        bg=ACCENT_COLOR
    )


submit_button = tk.Button(
    button_frame,
    text="CREATE ACCOUNT",
    command=submit_form,
    bg=ACCENT_COLOR,
    fg="white",
    activebackground=ACCENT_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    font=("Helvetica", 11, "bold"),
    cursor="hand2"
)

submit_button.pack(
    fill="x",
    ipady=13
)

submit_button.bind(
    "<Enter>",
    submit_hover
)

submit_button.bind(
    "<Leave>",
    submit_leave
)


login_button = tk.Button(
    button_frame,
    text="Already have an account?  Sign in",
    command=open_login,
    bg=BG_COLOR,
    fg=ACCENT_COLOR,
    activebackground=BG_COLOR,
    activeforeground=ACCENT_HOVER,
    relief="flat",
    bd=0,
    font=("Helvetica", 10, "bold"),
    cursor="hand2"
)

login_button.pack(
    pady=(18, 0)
)


# ============================================================
# START
# ============================================================

first_name_entry.focus()

root.mainloop()