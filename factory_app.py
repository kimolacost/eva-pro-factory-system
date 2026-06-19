import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from openpyxl import Workbook

# ================= DATABASE =================
conn = sqlite3.connect("factory.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS production (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    machine TEXT,
    worker TEXT,
    type1 TEXT, prod1 INT, scrap1 INT, reason1 TEXT,
    type2 TEXT, prod2 INT, scrap2 INT, reason2 TEXT,
    type3 TEXT, prod3 INT, scrap3 INT, reason3 TEXT,
    type4 TEXT, prod4 INT, scrap4 INT, reason4 TEXT
)
""")
conn.commit()

# ================= APP =================
root = Tk()
root.title("Factory Production System - V2")
root.geometry("1300x750")
root.configure(bg="#1e1e2f")

# ================= HEADER =================
header = Frame(root, bg="#2c2f48", height=60)
header.pack(fill=X)

Label(
    header,
    text="FACTORY PRODUCTION DASHBOARD",
    bg="#2c2f48",
    fg="white",
    font=("Arial", 16, "bold")
).pack(pady=15)

# ================= LEFT PANEL =================
left = Frame(root, bg="#2b2d42", width=400)
left.pack(side=LEFT, fill=Y)

right = Frame(root, bg="#f5f6fa")
right.pack(side=RIGHT, fill=BOTH, expand=True)

# ================= VARIABLES =================
machine = StringVar()
worker = StringVar()

types, prods, scraps, reasons = [], [], [], []

# ================= INPUTS =================
Label(left, text="Machine", bg="#2b2d42", fg="white").pack(pady=5)
Entry(left, textvariable=machine).pack(pady=5)

Label(left, text="Worker", bg="#2b2d42", fg="white").pack(pady=5)
Entry(left, textvariable=worker).pack(pady=5)

for i in range(4):
    t = StringVar()
    p = StringVar()
    s = StringVar()
    r = StringVar()

    types.append(t)
    prods.append(p)
    scraps.append(s)
    reasons.append(r)

    Frame(left, bg="#2b2d42").pack(pady=5)

    Label(left, text=f"Type {i+1}", bg="#2b2d42", fg="#00d4ff").pack()

    Entry(left, textvariable=t).pack(pady=2)
    Entry(left, textvariable=p).pack(pady=2)
    Entry(left, textvariable=s).pack(pady=2)
    Entry(left, textvariable=r).pack(pady=2)

# ================= FUNCTIONS =================
def save():
    date = datetime.now().strftime("%Y-%m-%d")

    def to_int(x):
        try:
            return int(x.get() or 0)
        except:
            return 0

    c.execute("""
    INSERT INTO production VALUES (
        NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
    )
    """, (
        date, machine.get(), worker.get(),
        types[0].get(), to_int(prods[0]), to_int(scraps[0]), reasons[0].get(),
        types[1].get(), to_int(prods[1]), to_int(scraps[1]), reasons[1].get(),
        types[2].get(), to_int(prods[2]), to_int(scraps[2]), reasons[2].get(),
        types[3].get(), to_int(prods[3]), to_int(scraps[3]), reasons[3].get()
    ))

    conn.commit()
    load_data()

    messagebox.showinfo("Success", "Data saved successfully")

# ================= BUTTONS =================
Button(left, text="SAVE", command=save, bg="#00c853", fg="white").pack(pady=10, fill=X)

# ================= TABLE =================
style = ttk.Style()
style.configure("Treeview", font=("Arial", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

table = ttk.Treeview(right, columns=("date","machine","worker"), show="headings")
table.heading("date", text="Date")
table.heading("machine", text="Machine")
table.heading("worker", text="Worker")

table.pack(fill=BOTH, expand=True, padx=10, pady=10)

# ================= LOAD DATA =================
def load_data():
    table.delete(*table.get_children())

    rows = c.execute("""
        SELECT date, machine, worker
        FROM production
        ORDER BY id DESC
    """).fetchall()

    for r in rows:
        table.insert("", END, values=r)

load_data()

root.mainloop()