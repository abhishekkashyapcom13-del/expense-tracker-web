import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# HELPERS
# ============================================================

def today():
    return datetime.now().strftime("%Y-%m-%d")


def money(value):
    return f"₹{value:,.2f}"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("1200x750")
root.minsize(950, 650)
root.configure(bg="#f4f6f8")

try:
    root.state("zoomed")
except:
    pass


# ============================================================
# COLORS
# ============================================================

BG = "#f4f6f8"
CARD = "#ffffff"
PRIMARY = "#2563eb"
SUCCESS = "#16a34a"
DANGER = "#dc2626"
WARNING = "#d97706"
TEXT = "#1f2937"
SUBTEXT = "#6b7280"
BORDER = "#e5e7eb"


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass

style.configure(
    "TButton",
    font=("Segoe UI", 10),
    padding=(12, 7)
)

style.configure(
    "Treeview",
    font=("Segoe UI", 10),
    rowheight=32,
    background="white",
    fieldbackground="white"
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold")
)

style.configure(
    "TEntry",
    padding=7,
    font=("Segoe UI", 10)
)

style.configure(
    "TCombobox",
    padding=7,
    font=("Segoe UI", 10)
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=PRIMARY,
    height=70
)

header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="PERSONAL EXPENSE TRACKER",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 20, "bold")
).pack(
    side="left",
    padx=25
)

tk.Label(
    header,
    text=datetime.now().strftime("%d %B %Y"),
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 10)
).pack(
    side="right",
    padx=25
)


# ============================================================
# MAIN
# ============================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)


# ============================================================
# DASHBOARD
# ============================================================

dashboard = tk.Frame(
    main,
    bg=BG
)

dashboard.pack(
    fill="x",
    pady=(0, 15)
)


def create_card(parent, title, value, color):

    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=SUBTEXT,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 3)
    )

    value_label = tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=color,
        font=("Segoe UI", 18, "bold")
    )

    value_label.pack(
        anchor="w",
        padx=15,
        pady=(0, 12)
    )

    return value_label


income_card = create_card(
    dashboard,
    "TOTAL INCOME",
    "₹0.00",
    SUCCESS
)

expense_card = create_card(
    dashboard,
    "TOTAL EXPENSE",
    "₹0.00",
    DANGER
)

transaction_card = create_card(
    dashboard,
    "TRANSACTIONS",
    "0",
    PRIMARY
)

today_card = create_card(
    dashboard,
    "TODAY'S EXPENSE",
    "₹0.00",
    WARNING
)

balance_card = create_card(
    dashboard,
    "BALANCE",
    "₹0.00",
    SUCCESS
)


# ============================================================
# INPUT SECTION
# ============================================================

input_frame = tk.Frame(
    main,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

input_frame.pack(
    fill="x",
    pady=(0, 12)
)


# ---------------- INCOME ----------------

tk.Label(
    input_frame,
    text="ADD INCOME",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 11, "bold")
).grid(
    row=0,
    column=0,
    padx=15,
    pady=(12, 5),
    sticky="w"
)

income_amount_entry = ttk.Entry(
    input_frame,
    width=18
)

income_amount_entry.grid(
    row=1,
    column=0,
    padx=15,
    pady=(0, 12)
)

income_button = ttk.Button(
    input_frame,
    text="Add Income",
    command=lambda: add_income()
)

income_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=(0, 12)
)

edit_income_button = ttk.Button(
    input_frame,
    text="Edit Income",
    command=lambda: edit_income()
)

edit_income_button.grid(
    row=1,
    column=2,
    padx=5,
    pady=(0, 12)
)

delete_income_button = ttk.Button(
    input_frame,
    text="Delete Income",
    command=lambda: delete_income()
)

delete_income_button.grid(
    row=1,
    column=3,
    padx=5,
    pady=(0, 12)
)

income_history_button = ttk.Button(
    input_frame,
    text="Income History",
    command=lambda: income_history()
)

income_history_button.grid(
    row=1,
    column=4,
    padx=5,
    pady=(0, 12)
)


# Separator

separator = ttk.Separator(
    input_frame,
    orient="vertical"
)

separator.grid(
    row=0,
    column=5,
    rowspan=2,
    sticky="ns",
    padx=20
)


# ---------------- EXPENSE ----------------

tk.Label(
    input_frame,
    text="ADD EXPENSE",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 11, "bold")
).grid(
    row=0,
    column=6,
    padx=10,
    pady=(12, 5),
    sticky="w"
)

amount_entry = ttk.Entry(
    input_frame,
    width=16
)

amount_entry.grid(
    row=1,
    column=6,
    padx=10,
    pady=(0, 12)
)

category_combo = ttk.Combobox(
    input_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Education",
        "Entertainment",
        "Health",
        "Mobile",
        "Internet",
        "Other"
    ],
    width=16,
    state="readonly"
)

category_combo.grid(
    row=1,
    column=7,
    padx=10,
    pady=(0, 12)
)

category_combo.set("Food")

description_entry = ttk.Entry(
    input_frame,
    width=25
)

description_entry.grid(
    row=1,
    column=8,
    padx=10,
    pady=(0, 12)
)

add_expense_button = ttk.Button(
    input_frame,
    text="Add Expense",
    command=lambda: add_expense()
)

add_expense_button.grid(
    row=1,
    column=9,
    padx=10,
    pady=(0, 12)
)


# ============================================================
# SEARCH / ACTIONS
# ============================================================

action_frame = tk.Frame(
    main,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

action_frame.pack(
    fill="x",
    pady=(0, 12)
)

tk.Label(
    action_frame,
    text="Search:",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=(15, 5),
    pady=10
)

search_entry = ttk.Entry(
    action_frame,
    width=28
)

search_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=10
)

search_button = ttk.Button(
    action_frame,
    text="Search",
    command=lambda: search_expenses()
)

search_button.grid(
    row=0,
    column=2,
    padx=5,
    pady=10
)

refresh_button = ttk.Button(
    action_frame,
    text="Refresh",
    command=lambda: refresh_table()
)

refresh_button.grid(
    row=0,
    column=3,
    padx=5,
    pady=10
)

analytics_button = ttk.Button(
    action_frame,
    text="Analytics",
    command=lambda: show_analytics()
)

analytics_button.grid(
    row=0,
    column=4,
    padx=5,
    pady=10
)

edit_button = ttk.Button(
    action_frame,
    text="Edit Selected",
    command=lambda: edit_selected()
)

edit_button.grid(
    row=0,
    column=5,
    padx=5,
    pady=10
)

delete_button = ttk.Button(
    action_frame,
    text="Delete Selected",
    command=lambda: delete_selected()
)

delete_button.grid(
    row=0,
    column=6,
    padx=5,
    pady=10
)

total_button = ttk.Button(
    action_frame,
    text="Show Total",
    command=lambda: show_total()
)

total_button.grid(
    row=0,
    column=7,
    padx=5,
    pady=10
)


# ============================================================
# EXPENSE TABLE
# ============================================================

table_frame = tk.Frame(
    main,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

table_frame.pack(
    fill="both",
    expand=True
)

columns = (
    "ID",
    "Amount",
    "Category",
    "Description",
    "Date"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Description", text="Description")
tree.heading("Date", text="Date")

tree.column(
    "ID",
    width=60,
    anchor="center"
)

tree.column(
    "Amount",
    width=130,
    anchor="center"
)

tree.column(
    "Category",
    width=150,
    anchor="center"
)

tree.column(
    "Description",
    width=400
)

tree.column(
    "Date",
    width=130,
    anchor="center"
)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scrollbar.set
)

tree.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ============================================================
# STATUS BAR
# ============================================================

status_var = tk.StringVar(
    value="Ready"
)

status_bar = tk.Label(
    root,
    textvariable=status_var,
    bg="#e5e7eb",
    fg=TEXT,
    anchor="w",
    padx=15,
    font=("Segoe UI", 9)
)

status_bar.pack(
    fill="x"
)


# ============================================================
# DASHBOARD UPDATE
# ============================================================

def update_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM income"
    )

    total_income = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )

    total_expense = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM expenses"
    )

    transaction_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) "
        "FROM expenses WHERE date = ?",
        (today(),)
    )

    today_expense = cursor.fetchone()[0]

    conn.close()

    balance = total_income - total_expense

    income_card.config(
        text=money(total_income)
    )

    expense_card.config(
        text=money(total_expense)
    )

    transaction_card.config(
        text=str(transaction_count)
    )

    today_card.config(
        text=money(today_expense)
    )

    balance_card.config(
        text=money(balance),
        fg=SUCCESS if balance >= 0 else DANGER
    )


# ============================================================
# REFRESH EXPENSE TABLE
# ============================================================

def refresh_table(search_text=""):

    for item in tree.get_children():
        tree.delete(item)

    conn = get_connection()
    cursor = conn.cursor()

    if search_text.strip():

        value = f"%{search_text}%"

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
            WHERE category LIKE ?
               OR description LIKE ?
            ORDER BY date DESC, id DESC
        """, (value, value))

    else:

        cursor.execute("""
            SELECT id, amount, category, description, date
            FROM expenses
            ORDER BY date DESC, id DESC
        """)

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        tree.insert(
            "",
            "end",
            values=(
                row[0],
                money(row[1]),
                row[2],
                row[3] if row[3] else "",
                row[4]
            )
        )

    update_dashboard()

    status_var.set(
        f"{len(rows)} expense record(s) displayed"
    )


# ============================================================
# ADD INCOME
# ============================================================

def add_income():

    value = income_amount_entry.get().strip()

    if not value:

        messagebox.showwarning(
            "Missing Amount",
            "Please enter income amount."
        )

        income_amount_entry.focus()
        return

    try:

        amount = float(value)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )

        income_amount_entry.focus()
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO income (amount, date) VALUES (?, ?)",
        (amount, today())
    )

    conn.commit()
    conn.close()

    income_amount_entry.delete(
        0,
        tk.END
    )

    update_dashboard()

    status_var.set(
        f"Income {money(amount)} added successfully."
    )

    income_amount_entry.focus()


# ============================================================
# INCOME HISTORY
# ============================================================

def income_history():

    window = tk.Toplevel(root)
    window.title("Income History")
    window.geometry("650x500")
    window.minsize(550, 400)
    window.configure(bg=BG)
    window.transient(root)

    tk.Label(
        window,
        text="INCOME HISTORY",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 16, "bold")
    ).pack(
        pady=15
    )

    frame = tk.Frame(
        window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=5
    )

    columns = (
        "ID",
        "Amount",
        "Date"
    )

    income_tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    income_tree.heading(
        "ID",
        text="ID"
    )

    income_tree.heading(
        "Amount",
        text="Amount"
    )

    income_tree.heading(
        "Date",
        text="Date"
    )

    income_tree.column(
        "ID",
        width=80,
        anchor="center"
    )

    income_tree.column(
        "Amount",
        width=200,
        anchor="center"
    )

    income_tree.column(
        "Date",
        width=180,
        anchor="center"
    )

    income_scroll = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=income_tree.yview
    )

    income_tree.configure(
        yscrollcommand=income_scroll.set
    )

    income_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    income_scroll.pack(
        side="right",
        fill="y"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, date
        FROM income
        ORDER BY date DESC, id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        income_tree.insert(
            "",
            "end",
            values=(
                row[0],
                money(row[1]),
                row[2]
            )
        )

    total = sum(row[1] for row in rows)

    tk.Label(
        window,
        text=f"Total Income: {money(total)}",
        bg=BG,
        fg=SUCCESS,
        font=("Segoe UI", 12, "bold")
    ).pack(
        pady=15
    )

    income_tree.bind(
        "<Escape>",
        lambda event: window.destroy()
    )


# ============================================================
# DELETE INCOME
# ============================================================

def delete_income():

    window = tk.Toplevel(root)
    window.title("Delete Income")
    window.geometry("600x450")
    window.minsize(500, 350)
    window.configure(bg=BG)
    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text="DELETE INCOME",
        bg=BG,
        fg=DANGER,
        font=("Segoe UI", 16, "bold")
    ).pack(
        pady=15
    )

    frame = tk.Frame(
        window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=5
    )

    columns = (
        "ID",
        "Amount",
        "Date"
    )

    income_tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    income_tree.heading(
        "ID",
        text="ID"
    )

    income_tree.heading(
        "Amount",
        text="Amount"
    )

    income_tree.heading(
        "Date",
        text="Date"
    )

    income_tree.column(
        "ID",
        width=80,
        anchor="center"
    )

    income_tree.column(
        "Amount",
        width=180,
        anchor="center"
    )

    income_tree.column(
        "Date",
        width=160,
        anchor="center"
    )

    income_tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, date
        FROM income
        ORDER BY date DESC, id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        income_tree.insert(
            "",
            "end",
            values=(
                row[0],
                money(row[1]),
                row[2]
            )
        )

    def remove_income():

        selected = income_tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Income",
                "Please select an income record.",
                parent=window
            )

            income_tree.focus_set()
            return

        values = income_tree.item(
            selected[0],
            "values"
        )

        income_id = int(values[0])

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n"
            f"Amount: {values[1]}\n"
            f"Date: {values[2]}",
            parent=window
        )

        if not confirm:
            income_tree.focus_set()
            return

        conn2 = get_connection()
        cursor2 = conn2.cursor()

        cursor2.execute(
            "DELETE FROM income WHERE id = ?",
            (income_id,)
        )

        conn2.commit()
        conn2.close()

        window.destroy()

        update_dashboard()

        status_var.set(
            "Income deleted successfully."
        )

    ttk.Button(
        window,
        text="Delete Selected Income",
        command=remove_income
    ).pack(
        pady=15
    )

    # ========================================================
    # IMPORTANT:
    # ENTER KEY = DELETE SELECTED INCOME
    # ========================================================

    income_tree.bind(
        "<Return>",
        lambda event: remove_income()
    )

    # DELETE KEY = DELETE SELECTED INCOME

    income_tree.bind(
        "<Delete>",
        lambda event: remove_income()
    )

    # ESC KEY = CLOSE WINDOW

    income_tree.bind(
        "<Escape>",
        lambda event: window.destroy()
    )

    income_tree.focus_set()


# ============================================================
# EDIT INCOME
# ============================================================

def edit_income():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, date
        FROM income
        ORDER BY date DESC, id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        messagebox.showinfo(
            "No Income",
            "No income record available."
        )

        return

    window = tk.Toplevel(root)
    window.title("Edit Income")
    window.geometry("600x500")
    window.minsize(500, 400)
    window.configure(bg=BG)
    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text="EDIT INCOME",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 16, "bold")
    ).pack(
        pady=15
    )

    listbox = tk.Listbox(
        window,
        font=("Segoe UI", 11),
        height=8
    )

    listbox.pack(
        fill="both",
        expand=True,
        padx=20
    )

    for row in rows:

        listbox.insert(
            tk.END,
            f"ID {row[0]}     {money(row[1])}     {row[2]}"
        )

    tk.Label(
        window,
        text="New Amount:",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(
        pady=(15, 5)
    )

    new_amount_entry = ttk.Entry(
        window,
        width=25
    )

    new_amount_entry.pack()

    def save_income():

        selected = listbox.curselection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select an income record.",
                parent=window
            )

            return

        value = new_amount_entry.get().strip()

        try:

            new_amount = float(value)

            if new_amount <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid positive amount.",
                parent=window
            )

            return

        income_id = rows[selected[0]][0]

        conn2 = get_connection()
        cursor2 = conn2.cursor()

        cursor2.execute(
            "UPDATE income SET amount = ? WHERE id = ?",
            (new_amount, income_id)
        )

        conn2.commit()
        conn2.close()

        window.destroy()

        update_dashboard()

        status_var.set(
            "Income updated successfully."
        )

    ttk.Button(
        window,
        text="Save Changes",
        command=save_income
    ).pack(
        pady=15
    )

    listbox.bind(
        "<Return>",
        lambda event: new_amount_entry.focus()
    )

    new_amount_entry.bind(
        "<Return>",
        lambda event: save_income()
    )

    window.bind(
        "<Escape>",
        lambda event: window.destroy()
    )


# ============================================================
# ADD EXPENSE
# ============================================================

def add_expense():

    amount_value = amount_entry.get().strip()
    category = category_combo.get().strip()
    description = description_entry.get().strip()

    if not amount_value:

        messagebox.showwarning(
            "Missing Amount",
            "Please enter expense amount."
        )

        amount_entry.focus()
        return

    try:

        amount = float(amount_value)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )

        amount_entry.focus()
        return

    if not category:

        messagebox.showwarning(
            "Missing Category",
            "Please select a category."
        )

        category_combo.focus()
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (
        amount,
        category,
        description,
        today()
    ))

    conn.commit()
    conn.close()

    amount_entry.delete(
        0,
        tk.END
    )

    description_entry.delete(
        0,
        tk.END
    )

    refresh_table()

    status_var.set(
        f"Expense {money(amount)} added successfully."
    )

    amount_entry.focus()


# ============================================================
# SELECTED EXPENSE ID
# ============================================================

def get_selected_id():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense record first."
        )

        return None

    values = tree.item(
        selected[0],
        "values"
    )

    return int(values[0])


# ============================================================
# EDIT EXPENSE
# ============================================================

def edit_selected():

    expense_id = get_selected_id()

    if expense_id is None:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount, category, description, date
        FROM expenses
        WHERE id = ?
    """, (expense_id,))

    row = cursor.fetchone()

    conn.close()

    if not row:

        messagebox.showerror(
            "Error",
            "Expense record not found."
        )

        return

    window = tk.Toplevel(root)
    window.title("Edit Expense")
    window.geometry("550x450")
    window.configure(bg=BG)
    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text="EDIT EXPENSE",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 16, "bold")
    ).pack(
        pady=15
    )

    form = tk.Frame(
        window,
        bg=BG
    )

    form.pack(
        padx=30
    )

    tk.Label(
        form,
        text="Amount:",
        bg=BG,
        fg=TEXT
    ).grid(
        row=0,
        column=0,
        sticky="w",
        pady=8
    )

    edit_amount = ttk.Entry(
        form,
        width=30
    )

    edit_amount.grid(
        row=0,
        column=1,
        pady=8
    )

    edit_amount.insert(
        0,
        str(row[0])
    )

    tk.Label(
        form,
        text="Category:",
        bg=BG,
        fg=TEXT
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=8
    )

    edit_category = ttk.Combobox(
        form,
        values=[
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Education",
            "Entertainment",
            "Health",
            "Mobile",
            "Internet",
            "Other"
        ],
        width=27,
        state="readonly"
    )

    edit_category.grid(
        row=1,
        column=1,
        pady=8
    )

    edit_category.set(row[1])

    tk.Label(
        form,
        text="Description:",
        bg=BG,
        fg=TEXT
    ).grid(
        row=2,
        column=0,
        sticky="w",
        pady=8
    )

    edit_description = ttk.Entry(
        form,
        width=30
    )

    edit_description.grid(
        row=2,
        column=1,
        pady=8
    )

    edit_description.insert(
        0,
        row[2] if row[2] else ""
    )

    tk.Label(
        form,
        text="Date:",
        bg=BG,
        fg=TEXT
    ).grid(
        row=3,
        column=0,
        sticky="w",
        pady=8
    )

    edit_date = ttk.Entry(
        form,
        width=30
    )

    edit_date.grid(
        row=3,
        column=1,
        pady=8
    )

    edit_date.insert(
        0,
        row[3]
    )

    def save_changes():

        try:

            amount = float(
                edit_amount.get().strip()
            )

            if amount <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid positive amount.",
                parent=window
            )

            return

        category = edit_category.get().strip()
        description = edit_description.get().strip()
        date_value = edit_date.get().strip()

        if not category or not date_value:

            messagebox.showwarning(
                "Missing Information",
                "Category and Date are required.",
                parent=window
            )

            return

        conn2 = get_connection()
        cursor2 = conn2.cursor()

        cursor2.execute("""
            UPDATE expenses
            SET amount = ?,
                category = ?,
                description = ?,
                date = ?
            WHERE id = ?
        """, (
            amount,
            category,
            description,
            date_value,
            expense_id
        ))

        conn2.commit()
        conn2.close()

        window.destroy()

        refresh_table()

        status_var.set(
            "Expense updated successfully."
        )

    ttk.Button(
        window,
        text="Save Changes",
        command=save_changes
    ).pack(
        pady=20
    )

    edit_amount.bind(
        "<Return>",
        lambda event: edit_category.focus()
    )

    edit_category.bind(
        "<Return>",
        lambda event: edit_description.focus()
    )

    edit_description.bind(
        "<Return>",
        lambda event: edit_date.focus()
    )

    edit_date.bind(
        "<Return>",
        lambda event: save_changes()
    )

    window.bind(
        "<Escape>",
        lambda event: window.destroy()
    )


# ============================================================
# DELETE EXPENSE
# ============================================================

def delete_selected():

    expense_id = get_selected_id()

    if expense_id is None:
        return

    selected = tree.selection()[0]

    values = tree.item(
        selected,
        "values"
    )

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete this expense?\n\n"
        f"Amount: {values[1]}\n"
        f"Category: {values[2]}\n"
        f"Description: {values[3]}"
    )

    if not confirm:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    refresh_table()

    status_var.set(
        "Expense deleted successfully."
    )


# ============================================================
# SEARCH
# ============================================================

def search_expenses():

    text = search_entry.get().strip()

    refresh_table(text)

    if text:

        status_var.set(
            f"Search results for: {text}"
        )


# ============================================================
# TOTAL
# ============================================================

def show_total():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )

    total_expense = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM income"
    )

    total_income = cursor.fetchone()[0]

    conn.close()

    balance = total_income - total_expense

    messagebox.showinfo(
        "Financial Summary",
        f"Total Income: {money(total_income)}\n\n"
        f"Total Expense: {money(total_expense)}\n\n"
        f"Balance: {money(balance)}"
    )


# ============================================================
# ANALYTICS
# ============================================================

def show_analytics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    category_data = cursor.fetchall()

    cursor.execute("""
        SELECT substr(date, 1, 7), SUM(amount)
        FROM expenses
        GROUP BY substr(date, 1, 7)
        ORDER BY substr(date, 1, 7)
    """)

    monthly_data = cursor.fetchall()

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )

    total_expense = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM income"
    )

    total_income = cursor.fetchone()[0]

    conn.close()

    if not category_data:

        messagebox.showinfo(
            "Analytics",
            "No expense data available yet."
        )

        return

    window = tk.Toplevel(root)
    window.title("Expense Analytics")
    window.geometry("1000x700")
    window.minsize(800, 600)
    window.configure(bg=BG)

    header2 = tk.Frame(
        window,
        bg=PRIMARY,
        height=65
    )

    header2.pack(fill="x")
    header2.pack_propagate(False)

    tk.Label(
        header2,
        text="EXPENSE ANALYTICS",
        bg=PRIMARY,
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(
        side="left",
        padx=20,
        pady=15
    )

    summary = tk.Frame(
        window,
        bg=BG
    )

    summary.pack(
        fill="x",
        padx=20,
        pady=15
    )

    balance = total_income - total_expense

    data = [
        ("Total Income", money(total_income), SUCCESS),
        ("Total Expense", money(total_expense), DANGER),
        (
            "Balance",
            money(balance),
            SUCCESS if balance >= 0 else DANGER
        )
    ]

    for title, value, color in data:

        card = tk.Frame(
            summary,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            card,
            text=title,
            bg=CARD,
            fg=SUBTEXT
        ).pack(
            pady=(10, 2)
        )

        tk.Label(
            card,
            text=value,
            bg=CARD,
            fg=color,
            font=("Segoe UI", 15, "bold")
        ).pack(
            pady=(0, 10)
        )

    content = tk.Frame(
        window,
        bg=BG
    )

    content.pack(
        fill="both",
        expand=True,
        padx=20
    )

    # CATEGORY

    category_frame = tk.Frame(
        content,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    category_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 7)
    )

    tk.Label(
        category_frame,
        text="CATEGORY-WISE SPENDING",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 12, "bold")
    ).pack(
        pady=12
    )

    category_tree = ttk.Treeview(
        category_frame,
        columns=("Category", "Amount", "Percent"),
        show="headings"
    )

    category_tree.heading(
        "Category",
        text="Category"
    )

    category_tree.heading(
        "Amount",
        text="Amount"
    )

    category_tree.heading(
        "Percent",
        text="%"
    )

    category_tree.column(
        "Category",
        width=150,
        anchor="center"
    )

    category_tree.column(
        "Amount",
        width=120,
        anchor="center"
    )

    category_tree.column(
        "Percent",
        width=80,
        anchor="center"
    )

    category_tree.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )

    for category, amount in category_data:

        percent = (
            amount / total_expense * 100
            if total_expense > 0
            else 0
        )

        category_tree.insert(
            "",
            "end",
            values=(
                category,
                money(amount),
                f"{percent:.1f}%"
            )
        )

    # MONTHLY

    monthly_frame = tk.Frame(
        content,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    monthly_frame.pack(
        side="right",
        fill="both",
        expand=True,
        padx=(7, 0)
    )

    tk.Label(
        monthly_frame,
        text="MONTHLY SPENDING",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 12, "bold")
    ).pack(
        pady=12
    )

    monthly_tree = ttk.Treeview(
        monthly_frame,
        columns=("Month", "Amount"),
        show="headings"
    )

    monthly_tree.heading(
        "Month",
        text="Month"
    )

    monthly_tree.heading(
        "Amount",
        text="Amount"
    )

    monthly_tree.column(
        "Month",
        width=150,
        anchor="center"
    )

    monthly_tree.column(
        "Amount",
        width=150,
        anchor="center"
    )

    monthly_tree.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )

    for month, amount in monthly_data:

        monthly_tree.insert(
            "",
            "end",
            values=(
                month,
                money(amount)
            )
        )

    # INSIGHTS

    insights_frame = tk.Frame(
        window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    insights_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )

    top_category = category_data[0]

    highest_month = None

    if monthly_data:

        highest_month = max(
            monthly_data,
            key=lambda x: x[1]
        )

    insight = (
        f"• Highest spending category: "
        f"{top_category[0]} ({money(top_category[1])})\n"
    )

    if highest_month:

        insight += (
            f"• Highest spending month: "
            f"{highest_month[0]} ({money(highest_month[1])})\n"
        )

    if total_income > 0:

        saving_percent = (
            balance / total_income
        ) * 100

        insight += (
            f"• Balance percentage: "
            f"{saving_percent:.1f}%"
        )

    tk.Label(
        insights_frame,
        text="SMART INSIGHTS",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 12, "bold")
    ).pack(
        anchor="w",
        padx=15,
        pady=(10, 5)
    )

    tk.Label(
        insights_frame,
        text=insight,
        bg=CARD,
        fg=SUBTEXT,
        justify="left",
        anchor="w",
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        padx=15,
        pady=(0, 12)
    )

    window.bind(
        "<Escape>",
        lambda event: window.destroy()
    )


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

income_amount_entry.bind(
    "<Return>",
    lambda event: add_income()
)

amount_entry.bind(
    "<Return>",
    lambda event: category_combo.focus()
)

category_combo.bind(
    "<Return>",
    lambda event: description_entry.focus()
)

description_entry.bind(
    "<Return>",
    lambda event: add_expense()
)

search_entry.bind(
    "<Return>",
    lambda event: search_expenses()
)

tree.bind(
    "<Double-1>",
    lambda event: edit_selected()
)

tree.bind(
    "<Return>",
    lambda event: edit_selected()
)

root.bind(
    "<Delete>",
    lambda event: delete_selected()
)

root.bind(
    "<Control-f>",
    lambda event: search_entry.focus()
)

root.bind(
    "<F5>",
    lambda event: refresh_table()
)


# ============================================================
# START APPLICATION
# ============================================================

create_database()
refresh_table()

income_amount_entry.focus()

root.mainloop()