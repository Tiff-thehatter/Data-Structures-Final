import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Final Project")
root.geometry("700x500")

# Create the Notebook (tab container)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create individual frames for each tab
udf_frame = tk.Frame(notebook, bg="#e0f7fa")   # UDF7 tab
sp2_frame = tk.Frame(notebook, bg="#f3e5f5")   # SP2 tab

# Add tabs to the notebook
notebook.add(udf_frame, text="UDF7 Search")
notebook.add(sp2_frame, text="SP2 Action")

# Add your widgets to the correct frame
# For example:
tk.Label(udf_frame, text="This is UDF7 tab", bg="#e0f7fa").pack(pady=20)
tk.Label(sp2_frame, text="This is SP2 tab", bg="#f3e5f5").pack(pady=20)

root.mainloop()