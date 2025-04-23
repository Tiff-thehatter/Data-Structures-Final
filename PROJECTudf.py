import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# Database connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=Tiffanys_lenovo\\SQLEXPRESS;'
    'DATABASE=EERDBS-3;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Call udf7 with min and max price
def call_udf7():
    try:
        min_price = float(min_price_entry.get())
        max_price = float(max_price_entry.get())

        # Clear previous results
        for i in udf_table.get_children():
            udf_table.delete(i)

        # Call UDF7 with input parameters
        cursor.execute("SELECT * FROM dbo.udf7(?, ?)", min_price, max_price)
        rows = cursor.fetchall()

        for row in rows:
            udf_table.insert("", "end", values=(
                row[1],  # itemdescription
                f"${row[2]:.2f}",  # price
                row[3]  # ItemID
            ))

              # Check the structure of the returned row
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for price range.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("UDF7 - Items by Unit Price Range")
root.geometry("600x400")
root.configure(bg="#e0f7fa")

tk.Label(root, text="Search EERDBS-3 Items by Price Range",bg="#e0f7fa", font=("Arial", 14)).pack(pady=10)

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="Min Price:").grid(row=0, column=0, padx=5, pady=5)
min_price_entry = tk.Entry(form_frame)
min_price_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Max Price:").grid(row=1, column=0, padx=5, pady=5)
max_price_entry = tk.Entry(form_frame)
max_price_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Search", command=call_udf7, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

# Result table
udf_table = ttk.Treeview(root, columns=("Item_Description", "Unit_Price", "I_D"), show="headings")
udf_table.heading("Item_Description", text="Item Description")
udf_table.heading("Unit_Price", text="Unit Price")
udf_table.heading("I_D", text="Item ID")
udf_table.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
