import sqlite3
from datetime import datetime

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT,
    note TEXT
)
""")
conn.commit()

def add_expense():
    amount = float(input("Enter amount: ₹"))
    category = input("Enter category (e.g., Food, Travel, Bills): ")
    note = input("Enter a note (optional): ")
    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
                   (amount, category, date, note))
    conn.commit()
    print("✅ Expense added successfully!\n")

def view_expenses():
    print("\n--- All Expenses ---")
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    for row in rows:
        print(f"₹{row[1]} | {row[2]} | {row[3]} | {row[4]}")
    print()

def monthly_summary():
    print("\n--- Monthly Summary ---")
    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount)
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """)
    for row in cursor.fetchall():
        print(f"{row[0]} → ₹{row[1]}")
    print()

def category_summary():
    print("\n--- Category-wise Summary ---")
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    for row in cursor.fetchall():
        print(f"{row[0]} → ₹{row[1]}")
    print()

def menu():
    while True:
        print("========== Expense Tracker ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary")
        print("4. Category-wise Summary")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            print("👋 Exiting... Have a great day!")
            break
        else:
            print("❌ Invalid choice. Try again.")

menu()
conn.close()
