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

# Main App Window
root = tk.Tk()
root.title("Final Project")
root.geometry("700x500")
# Create the Notebook (tab container)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# -----------------------
# Tab 1 - UDF7 Interface
# -----------------------
tab1 = tk.Frame(notebook, bg="#e0f7fa")
notebook.add(tab1, text='User-Defined Function 7')

tk.Label(tab1, text="Search EERDBS-3 Items by Price Range", bg="#e0f7fa", font=("Arial", 14)).pack(pady=10)

form_frame = tk.Frame(tab1, bg="#e0f7fa")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Min Price:").grid(row=0, column=0, padx=5, pady=5)
min_price_entry = tk.Entry(form_frame)
min_price_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Max Price:").grid(row=1, column=0, padx=5, pady=5)
max_price_entry = tk.Entry(form_frame)
max_price_entry.grid(row=1, column=1, padx=5, pady=5)

udf_table = ttk.Treeview(tab1, columns=("Item_Description", "Unit_Price", "I_D"), show="headings")
udf_table.heading("Item_Description", text="Item Description")
udf_table.heading("Unit_Price", text="Unit Price")
udf_table.heading("I_D", text="Item ID")
udf_table.pack(fill="both", expand=True, padx=10, pady=10)

def call_udf7():
    try:
        min_price = float(min_price_entry.get())
        max_price = float(max_price_entry.get())

        for i in udf_table.get_children():
            udf_table.delete(i)

        cursor.execute("SELECT * FROM dbo.udf7(?, ?)", min_price, max_price)
        rows = cursor.fetchall()

        for row in rows:
            udf_table.insert("", "end", values=(row[1], f"${row[2]:.2f}", row[3]))

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for price range.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(tab1, text="Search", command=call_udf7, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

# -----------------------
# Tab 2 - SP2 Procedure
# -----------------------
tab2 = tk.Frame(notebook, bg="#f3e5f5")
notebook.add(tab2, text='Stored Procedure 2')

sp2_table = ttk.Treeview(tab2, show="headings")
sp2_table.pack(fill='both', expand=True, padx=10, pady=10)

def call_sp2():
    try:
        for i in sp2_table.get_children():
            sp2_table.delete(i)

        sql = """
        DECLARE @total INT, @avg MONEY;
        EXEC sp2 @total OUTPUT, @avg OUTPUT;
        SELECT @total AS TotalReceipts, @avg AS AvgAmount;
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        if rows:
            columns = [column[0] for column in cursor.description]
            sp2_table['columns'] = columns
            for col in columns:
                sp2_table.heading(col, text=col)
            for row in rows:
                formatted_row = (row[0], f"${float(row[1]):.2f}")
                sp2_table.insert("", "end", values=formatted_row)

            if cursor.nextset():
                out_params = cursor.fetchall()
                if out_params:
                    total, avg = out_params[0]
                    messagebox.showinfo("SP2 Output", f"Total Receipts: {total}\nAverage Amount: ${avg:.2f}")
        else:
            messagebox.showinfo("No Data", "Stored procedure returned no results.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(tab2, text="Run Stored Procedure", command=call_sp2, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()