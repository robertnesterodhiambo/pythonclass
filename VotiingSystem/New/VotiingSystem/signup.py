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
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ============================================================
# SUBMIT FORM
# ============================================================

def submit_form():

    # Get data from form
    first_name = entries['First Name'].get().strip()
    second_name = entries['Second Name'].get().strip()
    last_name = entries['Last Name'].get().strip()
    date_of_birth = entries['Date of Birth'].get().strip()
    id_number = entries['ID Number'].get().strip()
    place_of_birth = entries['Place of Birth'].get().strip()
    password = entries['Password'].get()

    province_name = province_var.get().strip()
    county_name = county_var.get().strip()
    constituency_name = constituency_var.get().strip()
    ward_name = ward_var.get().strip()

    # ========================================================
    # CHECK EMPTY FIELDS
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
            "Please fill in all fields."
        )
        return

    # ========================================================
    # VALIDATE ID NUMBER
    # ========================================================

    if len(id_number) != 8 or not id_number.isdigit():
        messagebox.showerror(
            "Invalid ID Number",
            "ID Number must contain exactly 8 digits."
        )
        return

    # ========================================================
    # GET SELECTED LOCATION IDs
    # ========================================================

    province_id = province_ids.get(province_name)
    county_id = county_ids.get(county_name)
    constituency_id = constituency_ids.get(constituency_name)
    ward_id = ward_ids.get(ward_name)

    if not province_id:
        messagebox.showerror(
            "Error",
            "Please select a valid province."
        )
        return

    if not county_id:
        messagebox.showerror(
            "Error",
            "Please select a valid county."
        )
        return

    if not constituency_id:
        messagebox.showerror(
            "Error",
            "Please select a valid constituency."
        )
        return

    if not ward_id:
        messagebox.showerror(
            "Error",
            "Please select a valid ward."
        )
        return

    # ========================================================
    # CONNECT TO USER DATABASE
    # ========================================================

    try:
        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()

        # ====================================================
        # CHECK WHETHER ID ALREADY EXISTS
        # ====================================================

        cursor.execute("""
            SELECT id
            FROM users
            WHERE id_number = ?
        """, (id_number,))

        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror(
                "Registration Error",
                "This ID number is already registered."
            )
            conn.close()
            return

        # ====================================================
        # HASH PASSWORD
        # ====================================================

        password_hash = hash_password(password)

        # ====================================================
        # INSERT USER
        # ====================================================

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

        # ====================================================
        # SUCCESS
        # ====================================================

        messagebox.showinfo(
            "Registration Successful",
            "Your information has been saved successfully!"
        )

        # ====================================================
        # CLEAR FORM
        # ====================================================

        for entry in entries.values():
            entry.delete(0, tk.END)

        province_var.set("")
        county_var.set("")
        constituency_var.set("")
        ward_var.set("")

        county_ids.clear()
        constituency_ids.clear()
        ward_ids.clear()

        county_dropdown['values'] = []
        constituency_dropdown['values'] = []
        ward_dropdown['values'] = []

    except sqlite3.IntegrityError as error:

        messagebox.showerror(
            "Database Error",
            f"Could not save user information.\n\n{error}"
        )

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Database error occurred.\n\n{error}"
        )


# ============================================================
# OPEN LOGIN
# ============================================================

def open_login_and_close_signup():

    root.destroy()

    subprocess.Popen([
        "python",
        os.path.join(BASE_DIR, "login.py")
    ])


# ============================================================
# LOAD COUNTIES
# ============================================================

def update_counties(event=None):

    province_name = province_var.get()

    province_id = province_ids.get(province_name)

    if not province_id:
        return

    try:

        conn = sqlite3.connect(VOTING_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name
            FROM Counties
            WHERE province_id = ?
            ORDER BY name
        """, (province_id,))

        counties = cursor.fetchall()

        conn.close()

        # Clear old mappings
        county_ids.clear()
        constituency_ids.clear()
        ward_ids.clear()

        # Clear lower dropdowns
        county_var.set("")
        constituency_var.set("")
        ward_var.set("")

        county_dropdown['values'] = [
            county[1] for county in counties
        ]

        constituency_dropdown['values'] = []
        ward_dropdown['values'] = []

        # Store county name -> county ID
        for county_id, county_name in counties:
            county_ids[county_name] = county_id

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not load counties.\n\n{error}"
        )


# ============================================================
# LOAD CONSTITUENCIES
# ============================================================

def update_constituencies(event=None):

    county_name = county_var.get()

    county_id = county_ids.get(county_name)

    if not county_id:
        return

    try:

        conn = sqlite3.connect(VOTING_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, constituency_name
            FROM constituencies
            WHERE county_id = ?
            ORDER BY constituency_name
        """, (county_id,))

        constituencies = cursor.fetchall()

        conn.close()

        # Clear old mappings
        constituency_ids.clear()
        ward_ids.clear()

        # Clear lower dropdowns
        constituency_var.set("")
        ward_var.set("")

        constituency_dropdown['values'] = [
            constituency[1]
            for constituency in constituencies
        ]

        ward_dropdown['values'] = []

        # Store constituency name -> ID
        for constituency_id, constituency_name in constituencies:
            constituency_ids[constituency_name] = constituency_id

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not load constituencies.\n\n{error}"
        )


# ============================================================
# LOAD WARDS
# ============================================================

def update_wards(event=None):

    constituency_name = constituency_var.get()

    constituency_id = constituency_ids.get(constituency_name)

    if not constituency_id:
        return

    try:

        conn = sqlite3.connect(VOTING_DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, ward_name
            FROM wards
            WHERE constituency_id = ?
            ORDER BY ward_name
        """, (constituency_id,))

        wards = cursor.fetchall()

        conn.close()

        # Clear old mapping
        ward_ids.clear()

        ward_var.set("")

        ward_dropdown['values'] = [
            ward[1]
            for ward in wards
        ]

        # Store ward name -> ID
        for ward_id, ward_name in wards:
            ward_ids[ward_name] = ward_id

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not load wards.\n\n{error}"
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Voter Registration")

root.geometry("500x600")

root.configure(bg="#282c34")


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TLabel",
    background="#f0f0f0",
    foreground="#333",
    padding=6,
    font=("Helvetica", 12)
)

style.configure(
    "TEntry",
    padding=6,
    font=("Helvetica", 12)
)

style.configure(
    "TButton",
    background="#61afef",
    foreground="white",
    padding=6,
    font=("Helvetica", 12, "bold")
)

style.configure(
    "TCombobox",
    padding=6,
    font=("Helvetica", 12)
)


# ============================================================
# FRAME
# ============================================================

shadow_frame = tk.Frame(
    root,
    bg="#61afef",
    bd=0
)

shadow_frame.place(
    relwidth=0.98,
    relheight=0.98,
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ============================================================
# CANVAS + SCROLLBAR
# ============================================================

canvas = tk.Canvas(
    shadow_frame,
    bg="#f0f0f0"
)

scrollbar = tk.Scrollbar(
    shadow_frame,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = tk.Frame(
    canvas,
    bg="#f0f0f0"
)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# USER INFORMATION FIELDS
# ============================================================

fields = [
    "First Name",
    "Second Name",
    "Last Name",
    "Date of Birth",
    "ID Number",
    "Place of Birth",
    "Password"
]

entries = {}


for i, field in enumerate(fields):

    label = ttk.Label(
        scrollable_frame,
        text=field
    )

    label.grid(
        row=i,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    if field == "Password":

        entry = ttk.Entry(
            scrollable_frame,
            show="*"
        )

    elif field == "Date of Birth":

        entry = DateEntry(
            scrollable_frame,
            width=19,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            year=2000
        )

    else:

        entry = ttk.Entry(
            scrollable_frame
        )

    entry.grid(
        row=i,
        column=1,
        sticky="ew",
        padx=10,
        pady=10
    )

    entries[field] = entry


# ============================================================
# LOCATION DATA
# ============================================================

try:

    conn = sqlite3.connect(VOTING_DB)

    cursor = conn.cursor()

    # --------------------------------------------------------
    # PROVINCES
    # --------------------------------------------------------

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
        f"Could not open voting database.\n\n{error}"
    )

    root.destroy()

    raise SystemExit


# ============================================================
# LOCATION VARIABLES
# ============================================================

province_var = tk.StringVar()
county_var = tk.StringVar()
constituency_var = tk.StringVar()
ward_var = tk.StringVar()


# ============================================================
# LOCATION ID MAPPINGS
# ============================================================

province_ids = {
    province[1]: province[0]
    for province in provinces
}

county_ids = {}
constituency_ids = {}
ward_ids = {}


# ============================================================
# LOCATION FRAME
# ============================================================

options_frame = tk.Frame(
    scrollable_frame,
    bg="#f0f0f0"
)

options_frame.grid(
    row=len(fields),
    column=0,
    columnspan=2,
    pady=10
)


# ============================================================
# PROVINCE
# ============================================================

ttk.Label(
    options_frame,
    text="Province"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=10,
    pady=10
)

province_dropdown = ttk.Combobox(
    options_frame,
    textvariable=province_var,
    state="readonly"
)

province_dropdown["values"] = [
    province[1]
    for province in provinces
]

province_dropdown.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=10,
    pady=10
)

province_dropdown.bind(
    "<<ComboboxSelected>>",
    update_counties
)


# ============================================================
# COUNTY
# ============================================================

ttk.Label(
    options_frame,
    text="County"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=10,
    pady=10
)

county_dropdown = ttk.Combobox(
    options_frame,
    textvariable=county_var,
    state="readonly"
)

county_dropdown.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=10,
    pady=10
)

county_dropdown.bind(
    "<<ComboboxSelected>>",
    update_constituencies
)


# ============================================================
# CONSTITUENCY
# ============================================================

ttk.Label(
    options_frame,
    text="Constituency"
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=10,
    pady=10
)

constituency_dropdown = ttk.Combobox(
    options_frame,
    textvariable=constituency_var,
    state="readonly"
)

constituency_dropdown.grid(
    row=2,
    column=1,
    sticky="ew",
    padx=10,
    pady=10
)

constituency_dropdown.bind(
    "<<ComboboxSelected>>",
    update_wards
)


# ============================================================
# WARD
# ============================================================

ttk.Label(
    options_frame,
    text="Ward"
).grid(
    row=3,
    column=0,
    sticky="w",
    padx=10,
    pady=10
)

ward_dropdown = ttk.Combobox(
    options_frame,
    textvariable=ward_var,
    state="readonly"
)

ward_dropdown.grid(
    row=3,
    column=1,
    sticky="ew",
    padx=10,
    pady=10
)


# ============================================================
# SUBMIT BUTTON
# ============================================================

submit_button = ttk.Button(
    scrollable_frame,
    text="Submit",
    command=submit_form
)

submit_button.grid(
    row=len(fields) + 1,
    column=0,
    columnspan=2,
    pady=10
)


# ============================================================
# LOGIN BUTTON
# ============================================================

login_button = ttk.Button(
    scrollable_frame,
    text="Go to Login",
    command=open_login_and_close_signup
)

login_button.grid(
    row=len(fields) + 2,
    column=0,
    columnspan=2,
    pady=10
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()