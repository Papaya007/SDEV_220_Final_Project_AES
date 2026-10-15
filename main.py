
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime


# Employee information
class Employee:
    def __init__(self, employee_id, name):
        self.employee_id = employee_id
        self.name = name


# FR clothing information
class ClothingItem:
    def __init__(self, item_name, size, price):
        self.item_name = item_name
        self.size = size
        self.price = price


# Employee clothing order
class Order:
    def __init__(self, employee):
        self.employee = employee
        self.items = []

    def add_item(self, clothing_item, quantity):
        self.items.append({
            "item": clothing_item,
            "quantity": quantity
        })

    def calculate_total(self):
        return sum(
            entry["item"].price * entry["quantity"]
            for entry in self.items
        )

    def display_summary(self):
        summary = "AES Indiana FR Clothing Order\n"
        summary += "--------------------------------\n"
        summary += f"Employee: {self.employee.name}\n"
        summary += f"Employee ID: {self.employee.employee_id}\n\n"

        for entry in self.items:
            item = entry["item"]
            quantity = entry["quantity"]
            subtotal = item.price * quantity

            summary += (
                f"{item.item_name} | Size: {item.size}\n"
                f"Quantity: {quantity} | Subtotal: ${subtotal:.2f}\n\n"
            )

        summary += f"TOTAL: ${self.calculate_total():.2f}"
        return summary


# Sample FR clothing catalog and prices
catalog = {
    "FR Long Sleeve Shirt": 65.00,
    "FR Work Pants": 85.00,
    "FR Jacket": 145.00,
    "FR Hoodie": 110.00,
    "FR Coveralls": 175.00,
    "FR Short Sleeve Shirt": 55.00
}


class ClothingOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Indiana - FR Clothing Ordering System")
        self.root.geometry("750x700")

        self.order = None

        title = ttk.Label(
            root,
            text="AES Indiana FR Clothing Ordering System",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=15)

        # Employee information section
        employee_frame = ttk.LabelFrame(
            root,
            text="Employee Information",
            padding=15
        )
        employee_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(
            employee_frame,
            text="Employee Name:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.name_entry = ttk.Entry(employee_frame, width=30)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(
            employee_frame,
            text="Employee ID:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.id_entry = ttk.Entry(employee_frame, width=30)
        self.id_entry.grid(row=1, column=1)

        # Clothing selection section
        clothing_frame = ttk.LabelFrame(
            root,
            text="Select FR Clothing",
            padding=15
        )
        clothing_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(
            clothing_frame,
            text="Clothing Item:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.item_combo = ttk.Combobox(
            clothing_frame,
            values=list(catalog.keys()),
            state="readonly",
            width=28
        )
        self.item_combo.grid(row=0, column=1)
        self.item_combo.current(0)

        ttk.Label(
            clothing_frame,
            text="Size:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.size_combo = ttk.Combobox(
            clothing_frame,
            values=[
                "S", "M", "L", "XL", "2XL", "3XL",
                "30x30", "32x32", "34x32"
            ],
            state="readonly",
            width=28
        )
        self.size_combo.grid(row=1, column=1)
        self.size_combo.current(1)

        ttk.Label(
            clothing_frame,
            text="Quantity:"
        ).grid(row=2, column=0, padx=5, pady=5)

        self.quantity_spin = ttk.Spinbox(
            clothing_frame,
            from_=1,
            to=20,
            width=10
        )
        self.quantity_spin.grid(row=2, column=1, sticky="w")
        self.quantity_spin.set(1)

        ttk.Button(
            clothing_frame,
            text="Add to Order",
            command=self.add_to_order
        ).grid(row=3, column=1, pady=10)

        # Order summary section
        summary_frame = ttk.LabelFrame(
            root,
            text="Order Summary",
            padding=15
        )
        summary_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.summary_text = tk.Text(
            summary_frame,
            height=12,
            width=70
        )
        self.summary_text.pack(fill="both", expand=True)

        # Submit order button
        tk.Button(
            root,
            text="Submit Order",
            command=self.submit_order,
            font=("Arial", 12, "bold"),
            bg="#176B45",
            fg="white",
            activebackground="#125536",
            activeforeground="white",
            padx=25,
            pady=10
        ).pack(pady=15)

    def add_to_order(self):
        name = self.name_entry.get().strip()
        employee_id = self.id_entry.get().strip()

        if not name or not employee_id:
            messagebox.showerror(
                "Missing Information",
                "Please enter employee name and ID."
            )
            return

        # Prevent changing employee during an active order
        if self.order is not None:
            if (
                self.order.employee.name != name
                or self.order.employee.employee_id != employee_id
            ):
                messagebox.showerror(
                    "Employee Changed",
                    "Finish the current order before changing employee information."
                )
                return

        try:
            quantity = int(self.quantity_spin.get())

            if not 1 <= quantity <= 20:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Please enter a quantity between 1 and 20."
            )
            return

        item_name = self.item_combo.get()
        size = self.size_combo.get()
        price = catalog[item_name]

        if self.order is None:
            employee = Employee(employee_id, name)
            self.order = Order(employee)

        clothing_item = ClothingItem(item_name, size, price)
        self.order.add_item(clothing_item, quantity)

        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(
            tk.END,
            self.order.display_summary()
        )

    def submit_order(self):
        if self.order is None or not self.order.items:
            messagebox.showwarning(
                "Empty Order",
                "Please add clothing before submitting."
            )
            return

        try:
            # Create orders folder if it does not exist
            orders_folder = (
                Path(__file__).resolve().parent / "orders"
            )
            orders_folder.mkdir(exist_ok=True)

            # Create a unique filename
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S_%f"
            )

            filename = (
                orders_folder / f"order_{timestamp}.txt"
            )

            # Generate receipt
            receipt = self.order.display_summary()
            receipt += (
                f"\n\nSubmitted: "
                f"{datetime.now():%Y-%m-%d %I:%M %p}"
            )

            # Save receipt to file
            filename.write_text(
                receipt,
                encoding="utf-8"
            )

        except OSError as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the order:\n{error}"
            )
            return

        messagebox.showinfo(
            "Order Saved",
            f"Order saved successfully!\n\n"
            f"Receipt: {filename.name}"
        )

        # Reset order
        self.order = None
        self.summary_text.delete("1.0", tk.END)


# Start application
if __name__ == "__main__":
    root = tk.Tk()
    app = ClothingOrderApp(root)
    root.mainloop()

