import sqlite3
import pandas as pd
import numpy as np
import datetime
import re

# ================= DATABASE SETUP =================
def create_tables():
    conn = sqlite3.connect("eb_system.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        meter_no TEXT UNIQUE,
        address TEXT,
        phone TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS readings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date TEXT,
        reading REAL,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        units REAL,
        amount REAL,
        status TEXT,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)

    conn.commit()
    conn.close()


# ================= VALIDATION FUNCTION =================
def validate_phone(phone):
    """Checks if a phone number has exactly 10 digits."""
    return re.fullmatch(r"\d{10}", phone) is not None


# ================= CLIENT FUNCTIONS =================
def add_client():
    print("\n--- Add New Client ---")
    name = input("Enter client name: ").strip()
    meter = input("Enter meter number: ").strip()
    address = input("Enter address: ").strip()

    while True:
        phone = input("Enter 10-digit phone number: ").strip()
        if validate_phone(phone):
            break
        else:
            print(" Invalid phone number! Please enter exactly 10 digits.")

    
    client_data = (name, meter, address, phone)

    conn = sqlite3.connect("eb_system.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO clients(name, meter_no, address, phone) VALUES (?, ?, ?, ?)", client_data)
        conn.commit()
        print(" Client added successfully!\n")
    except sqlite3.IntegrityError:
        print(" Meter number already exists! Try a different one.\n")
    conn.close()


def view_clients():
    conn = sqlite3.connect("eb_system.db")
    df = pd.read_sql_query("SELECT * FROM clients", conn)
    if df.empty:
        print("No clients found.\n")
    else:
        print("\n--- CLIENT LIST ---")
        print(df)
    conn.close()


def remove_client():
    view_clients()
    try:
        client_id = int(input("Enter Client ID to remove: "))
    except ValueError:
        print("Invalid input. Please enter a valid numeric ID.")
        return

    conn = sqlite3.connect("eb_system.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE id=?", (client_id,))
    row = cur.fetchone()

    if not row:
        print(" No client found with that ID.")
    else:
        confirm = input(f"Are you sure you want to delete client '{row[1]}'? (y/n): ").lower()
        if confirm == 'y':
            cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
            conn.commit()
            print(" Client removed successfully!")
        else:
            print(" Deletion cancelled.")
    conn.close()


# ================= READING FUNCTIONS =================
def add_reading():
    view_clients()
    client_id = input("Enter Client ID: ")
    date = input("Enter reading date (YYYY-MM-DD): ")
    reading = float(input("Enter reading in kWh: "))

    conn = sqlite3.connect("eb_system.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO readings(client_id, date, reading) VALUES (?, ?, ?)",
                (client_id, date, reading))
    conn.commit()
    conn.close()
    print(" Reading added successfully!\n")


def view_readings():
    conn = sqlite3.connect("eb_system.db")
    df = pd.read_sql_query("""SELECT r.id, c.name, r.date, r.reading
                              FROM readings r JOIN clients c ON r.client_id=c.id
                              ORDER BY r.date""", conn)
    if df.empty:
        print("No readings found.\n")
    else:
        print("\n--- METER READINGS ---")
        print(df)
    conn.close()


# ================= BILLING FUNCTIONS =================
def generate_bill():
    view_clients()
    client_id = input("Enter Client ID: ")
    start = input("Enter start date (YYYY-MM-DD): ")
    end = input("Enter end date (YYYY-MM-DD): ")

    conn = sqlite3.connect("eb_system.db")
    cur = conn.cursor()
    cur.execute("""SELECT reading FROM readings 
                   WHERE client_id=? AND date BETWEEN ? AND ?
                   ORDER BY date ASC""", (client_id, start, end))
    readings = [r[0] for r in cur.fetchall()]
    conn.close()

    if len(readings) < 2:
        print("⚠️ Not enough readings to generate bill.\n")
        return

    
    units = np.round(readings[-1] - readings[0], 2)
    rate = 5.0
    amount = np.round(units * rate, 2)

    conn = sqlite3.connect("eb_system.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO bills(client_id, start_date, end_date, units, amount, status) VALUES (?, ?, ?, ?, ?, ?)",
                (client_id, start, end, units, amount, "Unpaid"))
    conn.commit()
    conn.close()

    
    bill_summary = {
        "Client ID": client_id,
        "Units": units,
        "Rate": rate,
        "Amount": amount,
        "Status": "Unpaid"
    }

    print("\n Bill generated successfully!")
    for key, value in bill_summary.items():
        print(f"{key}: {value}")
    print()


def view_bills():
    conn = sqlite3.connect("eb_system.db")
    df = pd.read_sql_query("""SELECT b.id, c.name, b.start_date, b.end_date, b.units, b.amount, b.status
                              FROM bills b JOIN clients c ON b.client_id=c.id""", conn)
    if df.empty:
        print("No bills found.\n")
    else:
        print("\n--- BILL DETAILS ---")
        print(df)
    conn.close()


# ================= ANALYSIS USING PANDAS, NUMPY, LIST =================
def show_analysis():
    conn = sqlite3.connect("eb_system.db")
    df_bills = pd.read_sql_query("""SELECT c.name, b.units, b.amount
                                    FROM bills b JOIN clients c ON b.client_id=c.id""", conn)
    conn.close()

    if df_bills.empty:
        print("No billing data to analyze.\n")
        return

    print("\n--- ELECTRICITY CONSUMPTION ANALYSIS ---")

    total_units = np.sum(df_bills['units'])
    total_amount = np.sum(df_bills['amount'])
    avg_units = np.mean(df_bills['units'])
    max_units = np.max(df_bills['units'])

    print(f"🔹 Total Units Consumed: {total_units} kWh")
    print(f"🔹 Total Revenue Collected: ₹{total_amount}")
    print(f"🔹 Average Units per Bill: {avg_units:.2f}")
    print(f"🔹 Highest Consumption in a Bill: {max_units} kWh\n")

    
    top_consumers = df_bills.groupby("name")["units"].sum().sort_values(ascending=False).head(5)
    top_list = list(zip(top_consumers.index, top_consumers.values))

    print("--- Top 5 Consumers (Name, Units) ---")
    for name, units in top_list:
        print(f"{name} → {units} kWh")


# ================= MAIN MENU =================
def main_menu():
    create_tables()

    while True:
        print("\n===== ELECTRICITY BOARD MANAGEMENT SYSTEM =====")
        print("1. Add Client")
        print("2. View Clients")
        print("3. Remove Client")
        print("4. Add Reading")
        print("5. View Readings")
        print("6. Generate Bill")
        print("7. View Bills")
        print("8. Show Analysis (Pandas + NumPy + Lists)")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_client()
        elif choice == '2':
            view_clients()
        elif choice == '3':
            remove_client()
        elif choice == '4':
            add_reading()
        elif choice == '5':
            view_readings()
        elif choice == '6':
            generate_bill()
        elif choice == '7':
            view_bills()
        elif choice == '8':
            show_analysis()
        elif choice == '0':
            print("Thank you for using the system! 👋")
            break
        else:
            print("Invalid choice. Try again!")

# ================= RUN PROGRAM =================
if __name__ == "__main__":
    main_menu()
