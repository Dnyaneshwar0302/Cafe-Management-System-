import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# -----------------------------
# Sample Menu (in-memory dataset)
# -----------------------------
MENU = [
    {"id": 1, "name": "Espresso", "category": "Beverage", "price": 60},
    {"id": 2, "name": "Cappuccino", "category": "Beverage", "price": 80},
    {"id": 3, "name": "Latte", "category": "Beverage", "price": 90},
    {"id": 4, "name": "Cold Coffee", "category": "Beverage", "price": 100},
    {"id": 5, "name": "Sandwich", "category": "Food", "price": 120},
    {"id": 6, "name": "Burger", "category": "Food", "price": 150},
    {"id": 7, "name": "French Fries", "category": "Food", "price": 70},
    {"id": 8, "name": "Pasta", "category": "Food", "price": 140},
    {"id": 9, "name": "Chocolate Cake", "category": "Dessert", "price": 110},
    {"id": 10, "name": "Ice Cream", "category": "Dessert", "price": 80},
    {"id": 11, "name": "Americano", "category": "Beverage", "price": 70},
    {"id": 12, "name": "Mocha", "category": "Beverage", "price": 100},
    {"id": 13, "name": "Green Tea", "category": "Beverage", "price": 60},
    {"id": 14, "name": "Hot Chocolate", "category": "Beverage", "price": 90},
    {"id": 15, "name": "Veg Pizza", "category": "Food", "price": 180},
    {"id": 16, "name": "Paneer Roll", "category": "Food", "price": 120},
    {"id": 17, "name": "Brownie", "category": "Dessert", "price": 120},
    {"id": 18, "name": "Donut", "category": "Dessert", "price": 80},
    {"id": 19, "name": "Mango Smoothie", "category": "Cold Beverage", "price": 120},
    {"id": 20, "name": "Oreo Shake", "category": "Cold Beverage", "price": 130},

]

TAX_RATE = 0.05  # 5% GST

# -----------------------------
# Main Application
# -----------------------------
class CafeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cafe Management System (Mini Project)")
        self.geometry("1050x600")

        self.cart = []
        self.discount = 0.0
        self.payment_method = tk.StringVar(value="Cash")

        self.create_widgets()
        self.load_menu()

    def create_widgets(self):
        # Top Frame
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        ttk.Label(top, text="Payment:").pack(side="left", padx=5)
        ttk.Combobox(
            top,
            textvariable=self.payment_method,
            values=["Cash", "UPI", "Card"],
            width=10,
            state="readonly"
        ).pack(side="left")

        # Paned Window
        mid = ttk.Panedwindow(self, orient="horizontal")
        mid.pack(fill="both", expand=True, pady=4, padx=8)

        # Left (Menu)
        left = ttk.Frame(mid, padding=6)
        mid.add(left, weight=1)

        ttk.Label(left, text="Menu").pack(anchor="w")
        self.menu_tree = ttk.Treeview(
            left, columns=("name", "category", "price"), show="headings", height=15
        )
        self.menu_tree.heading("name", text="Item")
        self.menu_tree.heading("category", text="Category")
        self.menu_tree.heading("price", text="Price")
        self.menu_tree.pack(fill="both", expand=True, pady=5)

        add_frame = ttk.Frame(left)
        add_frame.pack(fill="x", pady=5)
        ttk.Label(add_frame, text="Qty:").pack(side="left")
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(add_frame, from_=1, to=50, textvariable=self.qty_var, width=5).pack(side="left", padx=4)
        ttk.Button(add_frame, text="Add to Cart", command=self.add_to_cart).pack(side="left", padx=5)

        # Middle (Cart)
        middle = ttk.Frame(mid, padding=6)
        mid.add(middle, weight=1)

        ttk.Label(middle, text="Cart").pack(anchor="w")
        self.cart_tree = ttk.Treeview(
            middle, columns=("name", "qty", "unit", "line"), show="headings", height=15
        )
        self.cart_tree.heading("name", text="Item")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("unit", text="Unit Price")
        self.cart_tree.heading("line", text="Line Total")
        self.cart_tree.pack(fill="both", expand=True, pady=5)

        cart_btns = ttk.Frame(middle)
        cart_btns.pack(fill="x", pady=5)
        ttk.Button(cart_btns, text="Remove Selected", command=self.remove_from_cart).pack(side="left")
        ttk.Button(cart_btns, text="Clear Cart", command=self.clear_cart).pack(side="left", padx=5)

        # Right (Bill Area)
        right = ttk.Frame(mid, padding=6)
        mid.add(right, weight=1)

        ttk.Label(right, text="Bill").pack(anchor="w")
        self.bill_text = tk.Text(right, width=40, height=25, state="disabled", font=("Courier New", 10))
        self.bill_text.pack(fill="both", expand=True, pady=5)

        # Bottom (Totals)
        bottom = ttk.Frame(self, padding=8)
        bottom.pack(fill="x")

        self.subtotal_var = tk.StringVar(value="0.00")
        self.tax_var = tk.StringVar(value="0.00")
        self.total_var = tk.StringVar(value="0.00")
        self.discount_var = tk.StringVar(value="0.00")

        ttk.Label(bottom, text="Subtotal:").pack(side="left")
        ttk.Label(bottom, textvariable=self.subtotal_var, width=10).pack(side="left", padx=4)
        ttk.Label(bottom, text="Tax (5%):").pack(side="left")
        ttk.Label(bottom, textvariable=self.tax_var, width=10).pack(side="left", padx=4)
        ttk.Label(bottom, text="Discount:").pack(side="left")
        ttk.Entry(bottom, textvariable=self.discount_var, width=8).pack(side="left", padx=4)
        ttk.Button(bottom, text="Apply", command=self.recalc_totals).pack(side="left", padx=4)

        ttk.Button(bottom, text="Generate Bill", command=self.generate_bill).pack(side="right")

    def load_menu(self):
        for item in MENU:
            self.menu_tree.insert("", "end", iid=item["id"], values=(item["name"], item["category"], item["price"]))

    def add_to_cart(self):
        sel = self.menu_tree.selection()
        if not sel:
            return
        mid = int(sel[0])
        qty = self.qty_var.get()
        item = next((i for i in MENU if i["id"] == mid), None)
        if item:
            for c in self.cart:
                if c["id"] == mid:
                    c["qty"] += qty
                    break
            else:
                self.cart.append({"id": mid, "name": item["name"], "qty": qty, "price": item["price"]})
        self.render_cart()
        self.recalc_totals()

    def render_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)
        for idx, item in enumerate(self.cart):
            line = item["qty"] * item["price"]
            self.cart_tree.insert("", "end", iid=str(idx),
                                  values=(item["name"], item["qty"], f"{item['price']:.2f}", f"{line:.2f}"))

    def remove_from_cart(self):
        sel = self.cart_tree.selection()
        if not sel: return
        idx = int(sel[0])
        self.cart.pop(idx)
        self.render_cart()
        self.recalc_totals()

    def clear_cart(self):
        self.cart.clear()
        self.render_cart()
        self.recalc_totals()

    def recalc_totals(self):
        subtotal = sum(i["qty"] * i["price"] for i in self.cart)
        try:
            self.discount = float(self.discount_var.get())
        except ValueError:
            self.discount = 0.0
            self.discount_var.set("0.00")
        tax = round(subtotal * TAX_RATE, 2)
        total = round(subtotal + tax - self.discount, 2)
        self.subtotal_var.set(f"{subtotal:.2f}")
        self.tax_var.set(f"{tax:.2f}")
        self.total_var.set(f"{total:.2f}")

    def generate_bill(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items before generating bill!")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        bill_lines = []
        bill_lines.append("   CAFE MANAGEMENT SYSTEM BILL   ")
        bill_lines.append("="*36)
        bill_lines.append(f"Time: {now}")
        bill_lines.append(f"Payment: {self.payment_method.get()}")
        bill_lines.append("-"*36)
        bill_lines.append(f"{'Item':<15}{'Qty':<5}{'Price':<8}{'Total':<8}")
        bill_lines.append("-"*36)

        for item in self.cart:
            line_total = item['qty'] * item['price']
            bill_lines.append(f"{item['name']:<15}{item['qty']:<5}{item['price']:<8}{line_total:<8}")

        bill_lines.append("-"*36)
        bill_lines.append(f"Subtotal: {self.subtotal_var.get()}")
        bill_lines.append(f"Tax (5%): {self.tax_var.get()}")
        bill_lines.append(f"Discount: {self.discount_var.get()}")
        bill_lines.append(f"Grand Total: {self.total_var.get()}")
        bill_lines.append("="*36)
        bill_lines.append("  Thank you! Visit again :)  ")

        self.bill_text.config(state="normal")
        self.bill_text.delete(1.0, "end")
        self.bill_text.insert("end", "\n".join(bill_lines))
        self.bill_text.config(state="disabled")

# -----------------------------
# Run the App
# -----------------------------
if __name__ == "__main__":
    app = CafeApp()
    app.mainloop()
