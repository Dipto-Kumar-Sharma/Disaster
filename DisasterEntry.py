import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, messagebox
from tkcalendar import DateEntry
import psycopg2

class ReliefDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Relief Distribution Management")
        self.root.geometry("1300x800")  # Larger window size for better layout

        # Variable initializations
        self.selected_distributor = tk.StringVar()
        self.dislocation = tk.StringVar()
        self.relief_amount = tk.StringVar()
        self.distribution_date = tk.StringVar()
        self.selected_item = None

        # Create frames for the form and table view
        self.create_frames()

        # Populate the distributor dropdown and table view
        self.populate_distributor_dropdown()
        self.populate_table()

    def create_frames(self):
        # Frame for the form
        self.formFrame = Frame(self.root, bg="#f5f5f5", padx=20, pady=20)
        self.formFrame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        self.Student_frame_title = Label(self.formFrame, text="Disaster Relief Control Panel",
                                          font=("Goudy old style", 35),
                                          bg="#f5f5f5",
                                          fg="#333333")
        self.Student_frame_title.grid(row=0, columnspan=2, pady=20, sticky="w")

        # Form Fields
        self.create_form_fields()

        # Frame for the table view
        self.tableFrame = Frame(self.root, bg="#ffffff", bd=2, relief="flat")
        self.tableFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=20, pady=20, expand=True)

        # Style for the Treeview
        style = ttk.Style()
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#333333",
                        fieldbackground="#f5f5f5",
                        borderwidth=0,
                        highlightthickness=0,
                        font=("Arial", 11))
        style.configure("Treeview.Heading",
                        background="#4CAF50",
                        foreground="#ffffff",
                        font=("Arial", 12, "bold"))
        style.map("Treeview.Heading", background=[('active', '#45a049')])

        # Treeview columns
        self.table = ttk.Treeview(self.tableFrame, columns=("ID", "Distributor", "Location", "Amount", "Date"), show='headings', style="Treeview")
        self.table.heading("ID", text="ID")
        self.table.heading("Distributor", text="Distributor")
        self.table.heading("Location", text="Location")
        self.table.heading("Amount", text="Amount (kg)")
        self.table.heading("Date", text="Date")

        # Set column widths
        self.table.column("ID", width=60, anchor=tk.CENTER)
        self.table.column("Distributor", width=180, anchor=tk.W)
        self.table.column("Location", width=250, anchor=tk.W)
        self.table.column("Amount", width=120, anchor=tk.CENTER)
        self.table.column("Date", width=140, anchor=tk.CENTER)

        # Add Scrollbars
        self.v_scroll = tk.Scrollbar(self.tableFrame, orient="vertical", command=self.table.yview)
        self.v_scroll.pack(side="right", fill="y")

        self.h_scroll = tk.Scrollbar(self.tableFrame, orient="horizontal", command=self.table.xview)
        self.h_scroll.pack(side="bottom", fill="x")

        self.table.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Pack the table
        self.table.pack(fill=tk.BOTH, expand=True)

        # Bind selection event
        self.table.bind("<ButtonRelease-1>", self.on_table_select)

        # Apply row color alternation
        self.table.tag_configure('evenrow', background='#f9f9f9')
        self.table.tag_configure('oddrow', background='#ffffff')

    def create_form_fields(self):
        # Distributor Label and Dropdown
        self.labelFName = Label(self.formFrame, text="Distributor Name :", font=("Arial", 14),
                                bg="#f5f5f5",
                                fg="#333333")
        self.labelFName.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.distributor_dropdown = ttk.Combobox(self.formFrame, textvariable=self.selected_distributor,
                                                font=("Arial", 12), width=30)
        self.distributor_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Location Label and Entry
        self.labelLocation = Label(self.formFrame, text="Location :", font=("Arial", 14),
                                   bg="#f5f5f5",
                                   fg="#333333")
        self.labelLocation.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.location_entry = Entry(self.formFrame, textvariable=self.dislocation, font=("Arial", 12), width=30)
        self.location_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Amount Label and Entry
        self.labelAmount = Label(self.formFrame, text="Relief Amount (kg) :", font=("Arial", 14),
                                 bg="#f5f5f5",
                                 fg="#333333")
        self.labelAmount.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.amount_entry = Entry(self.formFrame, textvariable=self.relief_amount, font=("Arial", 12), width=30)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Date Label and Entry
        self.labelDate = Label(self.formFrame, text="Distribution Date :", font=("Arial", 14),
                               bg="#f5f5f5",
                               fg="#333333")
        self.labelDate.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.date_entry = DateEntry(self.formFrame, textvariable=self.distribution_date, font=("Arial", 12), width=27, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Buttons
        self.submit_button = Button(self.formFrame, text="Submit", command=self.submit_form, font=("Arial", 14), bg="#4CAF50", fg="white", width=15)
        self.submit_button.grid(row=5, column=0, padx=10, pady=20, sticky="w")

        self.update_button = Button(self.formFrame, text="Update", command=self.update_record, font=("Arial", 14), bg="#2196F3", fg="white", width=15)
        self.update_button.grid(row=5, column=1, padx=10, pady=20, sticky="w")

        self.delete_button = Button(self.formFrame, text="Delete", command=self.delete_record, font=("Arial", 14), bg="#F44336", fg="white", width=15)
        self.delete_button.grid(row=6, column=0, padx=10, pady=20, sticky="w")

        self.clear_button = Button(self.formFrame, text="Clear", command=self.clear_form, font=("Arial", 14), bg="#9E9E9E", fg="white", width=15)
        self.clear_button.grid(row=6, column=1, padx=10, pady=20, sticky="w")

    def populate_distributor_dropdown(self):
        try:
            connection = self.create_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT firstName FROM students")
            rows = cursor.fetchall()
            names = [row[0] for row in rows]
            self.distributor_dropdown['values'] = names
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def populate_table(self):
        try:
            connection = self.create_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM relief_distribution")
            rows = cursor.fetchall()
            self.table.delete(*self.table.get_children())

            for index, row in enumerate(rows):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.table.insert("", tk.END, values=row, tags=(tag,))
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def submit_form(self):
        if not self.selected_distributor.get() or not self.dislocation.get() or not self.relief_amount.get() or not self.distribution_date.get():
            messagebox.showwarning("Validation Error", "All fields must be filled out.")
            return

        try:
            amount = float(self.relief_amount.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            messagebox.showwarning("Validation Error", "Amount must be a positive number.")
            return

        try:
            connection = self.create_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO relief_distribution (distributor_name, location, amount, distribution_date)
                VALUES (%s, %s, %s, %s)
            """, (self.selected_distributor.get(), self.dislocation.get(), self.relief_amount.get(), self.distribution_date.get()))
            connection.commit()
            cursor.close()
            connection.close()
            self.populate_table()
            self.clear_form()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def update_record(self):
        if not self.selected_item:
            messagebox.showwarning("Selection Error", "No record selected for update.")
            return

        if not self.selected_distributor.get() or not self.dislocation.get() or not self.relief_amount.get() or not self.distribution_date.get():
            messagebox.showwarning("Validation Error", "All fields must be filled out.")
            return

        try:
            amount = float(self.relief_amount.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            messagebox.showwarning("Validation Error", "Amount must be a positive number.")
            return

        try:
            connection = self.create_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE relief_distribution
                SET distributor_name = %s, location = %s, amount = %s, distribution_date = %s
                WHERE distributionID = %s
            """, (self.selected_distributor.get(), self.dislocation.get(), self.relief_amount.get(), self.distribution_date.get(), self.selected_item))
            connection.commit()
            cursor.close()
            connection.close()
            self.populate_table()
            self.clear_form()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def delete_record(self):
        if not self.selected_item:
            messagebox.showwarning("Selection Error", "No record selected for deletion.")
            return

        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
            try:
                connection = self.create_db_connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM relief_distribution WHERE distributionID = %s", (self.selected_item,))
                connection.commit()
                cursor.close()
                connection.close()
                self.populate_table()
                self.clear_form()
            except Exception as e:
                print(f"Error connecting to the database: {e}")

    def on_table_select(self, event):
        try:
            selected = self.table.selection()[0]
            values = self.table.item(selected, 'values')
            self.selected_item = values[0]
            self.selected_distributor.set(values[1])
            self.dislocation.set(values[2])
            self.relief_amount.set(values[3])
            self.distribution_date.set(values[4])
        except IndexError:
            self.selected_item = None

    def clear_form(self):
        self.selected_distributor.set('')
        self.dislocation.set('')
        self.relief_amount.set('')
        self.distribution_date.set('')
        self.selected_item = None

    def create_db_connection(self):
        return psycopg2.connect(
            dbname='ds',
            user='postgres',
            password='dipto@123456'
        )

# Creating the main window
root = tk.Tk()
app = ReliefDistributionApp(root)
root.mainloop()
