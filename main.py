import tkinter as tk
from tkinter import ttk, messagebox
import random

# Catalog Dataset
PRODUCTS = [
    {
        "id": 1,
        "name": "Apple iPhone 15 (Black, 128 GB)",
        "category": "Mobiles",
        "price": 65999,
        "original": 79900,
        "discount": "17% off",
        "rating": 4.6,
        "reviews": 1420,
    },
    {
        "id": 2,
        "name": "Sony WH-1000XM5 Wireless ANC Headphones",
        "category": "Electronics",
        "price": 26990,
        "original": 34990,
        "discount": "22% off",
        "rating": 4.7,
        "reviews": 890,
    },
    {
        "id": 3,
        "name": "Smart Fitness Watch Series 9 GPS",
        "category": "Electronics",
        "price": 38900,
        "original": 41900,
        "discount": "7% off",
        "rating": 4.5,
        "reviews": 520,
    },
    {
        "id": 4,
        "name": "Men's Slim Fit 100% Cotton Casual Shirt",
        "category": "Fashion",
        "price": 799,
        "original": 1999,
        "discount": "60% off",
        "rating": 3.9,
        "reviews": 230,
    },
    {
        "id": 5,
        "name": '55" Ultra HD 4K Smart QLED Television',
        "category": "Appliances",
        "price": 42999,
        "original": 69990,
        "discount": "38% off",
        "rating": 4.4,
        "reviews": 1120,
    },
    {
        "id": 6,
        "name": "High-Back Ergonomic Office Desk Chair",
        "category": "Home",
        "price": 5499,
        "original": 11999,
        "discount": "54% off",
        "rating": 3.8,
        "reviews": 95,
    },
    {
        "id": 7,
        "name": "Fast 65W GaN Dual USB-C Charger",
        "category": "Electronics",
        "price": 1299,
        "original": 2499,
        "discount": "48% off",
        "rating": 4.5,
        "reviews": 640,
    },
    {
        "id": 8,
        "name": "Samsung Galaxy S24 Ultra (Titanium Gray)",
        "category": "Mobiles",
        "price": 119999,
        "original": 134999,
        "discount": "11% off",
        "rating": 4.8,
        "reviews": 2040,
    },
    {
        "id": 9,
        "name": "Mechanical RGB Gaming Keyboard",
        "category": "Electronics",
        "price": 3499,
        "original": 6999,
        "discount": "50% off",
        "rating": 4.3,
        "reviews": 410,
    },
    {
        "id": 10,
        "name": "Inverter Split AC 1.5 Ton 5-Star",
        "category": "Appliances",
        "price": 37990,
        "original": 54990,
        "discount": "30% off",
        "rating": 4.6,
        "reviews": 890,
    },
]

CATEGORIES = ["All", "Mobiles", "Electronics", "Appliances", "Fashion", "Home"]


class FlipkartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flipkart - Online Shopping Simulator")
        self.root.geometry("1180x780")
        self.root.minsize(980, 640)
        self.root.configure(bg="#f1f3f6")

        # Application State
        self.cart = {}  # { product_id: {"product": ..., "qty": ...} }
        self.category_var = tk.StringVar(value="All")
        self.rating_var = tk.IntVar(value=0)
        self.sort_var = tk.StringVar(value="Relevance")
        self.search_var = tk.StringVar()
        self.max_price_var = tk.IntVar(value=140000)

        # Style Config
        self.setup_styles()

        # Build GUI
        self.create_navbar()
        self.create_main_layout()

        # Initial Render
        self.render_products()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TCombobox", padding=4)
        self.style.configure("Horizontal.TScale", background="#ffffff")

    # ------------------ TOP NAVBAR ------------------
    def create_navbar(self):
        nav = tk.Frame(self.root, bg="#2874f0", height=60, padx=20, pady=8)
        nav.pack(side=tk.TOP, fill=tk.X)

        # Brand Title
        brand_frame = tk.Frame(nav, bg="#2874f0", cursor="hand2")
        brand_frame.pack(side=tk.LEFT, padx=(0, 25))
        brand_frame.bind("<Button-1>", lambda e: self.reset_filters())

        logo = tk.Label(
            brand_frame,
            text="Flipkart",
            font=("Arial", 18, "bold italic"),
            fg="#ffffff",
            bg="#2874f0",
        )
        logo.pack(anchor="w")
        sublogo = tk.Label(
            brand_frame,
            text="Explore Plus ✨",
            font=("Arial", 9, "italic bold"),
            fg="#ffe500",
            bg="#2874f0",
        )
        sublogo.pack(anchor="w", pady=(0, 0))

        # Search Bar
        search_frame = tk.Frame(nav, bg="#ffffff", bd=0, relief=tk.FLAT)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))

        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 11),
            bd=0,
            bg="#ffffff",
            fg="#212121",
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=12, pady=7)
        self.search_entry.bind("<KeyRelease>", lambda e: self.render_products())

        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            font=("Arial", 9, "bold"),
            bg="#2874f0",
            fg="#ffffff",
            activebackground="#1c5ec4",
            activeforeground="#ffffff",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.render_products,
        )
        search_btn.pack(side=tk.RIGHT, padx=4, pady=3)

        # Cart Button
        self.cart_btn = tk.Button(
            nav,
            text="🛒 Cart (0)",
            font=("Arial", 11, "bold"),
            bg="#fb641b",
            fg="#ffffff",
            activebackground="#e05613",
            activeforeground="#ffffff",
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.open_cart_window,
        )
        self.cart_btn.pack(side=tk.RIGHT)

    # ------------------ MAIN LAYOUT ------------------
    def create_main_layout(self):
        container = tk.Frame(self.root, bg="#f1f3f6")
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # Sidebar Filters (Left)
        sidebar = tk.Frame(container, bg="#ffffff", width=250, bd=1, relief=tk.SOLID)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)

        # Sidebar Header
        sb_header = tk.Frame(sidebar, bg="#ffffff", padx=12, pady=10)
        sb_header.pack(fill=tk.X)
        tk.Label(
            sb_header, text="FILTERS", font=("Arial", 12, "bold"), fg="#212121", bg="#ffffff"
        ).pack(side=tk.LEFT)

        clear_btn = tk.Button(
            sb_header,
            text="CLEAR ALL",
            font=("Arial", 8, "bold"),
            fg="#2874f0",
            bg="#ffffff",
            bd=0,
            cursor="hand2",
            command=self.reset_filters,
        )
        clear_btn.pack(side=tk.RIGHT)

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X)

        # Category Filter
        cat_box = tk.Frame(sidebar, bg="#ffffff", padx=12, pady=10)
        cat_box.pack(fill=tk.X)
        tk.Label(
            cat_box, text="CATEGORIES", font=("Arial", 9, "bold"), fg="#878787", bg="#ffffff"
        ).pack(anchor="w", pady=(0, 6))

        for cat in CATEGORIES:
            rb = tk.Radiobutton(
                cat_box,
                text=cat,
                value=cat,
                variable=self.category_var,
                bg="#ffffff",
                activebackground="#ffffff",
                font=("Arial", 9),
                command=self.render_products,
            )
            rb.pack(anchor="w", pady=1)

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X)

        # Price Slider
        price_box = tk.Frame(sidebar, bg="#ffffff", padx=12, pady=10)
        price_box.pack(fill=tk.X)
        tk.Label(
            price_box, text="PRICE (UP TO)", font=("Arial", 9, "bold"), fg="#878787", bg="#ffffff"
        ).pack(anchor="w")

        self.price_label = tk.Label(
            price_box,
            text="₹1,40,000",
            font=("Arial", 10, "bold"),
            fg="#2874f0",
            bg="#ffffff",
        )
        self.price_label.pack(anchor="w", pady=(2, 4))

        price_scale = ttk.Scale(
            price_box,
            from_=1000,
            to=140000,
            orient="horizontal",
            variable=self.max_price_var,
            command=self.on_price_scale_change,
        )
        price_scale.pack(fill=tk.X)

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, pady=(10, 0))

        # Rating Filter
        rating_box = tk.Frame(sidebar, bg="#ffffff", padx=12, pady=10)
        rating_box.pack(fill=tk.X)
        tk.Label(
            rating_box, text="CUSTOMER RATINGS", font=("Arial", 9, "bold"), fg="#878787", bg="#ffffff"
        ).pack(anchor="w", pady=(0, 6))

        ratings = [("4★ & above", 4), ("3★ & above", 3), ("All Ratings", 0)]
        for label, val in ratings:
            rb = tk.Radiobutton(
                rating_box,
                text=label,
                value=val,
                variable=self.rating_var,
                bg="#ffffff",
                activebackground="#ffffff",
                font=("Arial", 9),
                command=self.render_products,
            )
            rb.pack(anchor="w", pady=1)

        # Product Content Area (Right)
        right_panel = tk.Frame(container, bg="#ffffff", bd=1, relief=tk.SOLID)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Sort Bar
        sort_bar = tk.Frame(right_panel, bg="#ffffff", padx=15, pady=8)
        sort_bar.pack(fill=tk.X)

        tk.Label(
            sort_bar, text="Sort By:", font=("Arial", 10, "bold"), fg="#212121", bg="#ffffff"
        ).pack(side=tk.LEFT, padx=(0, 10))

        sort_options = [
            "Relevance",
            "Price -- Low to High",
            "Price -- High to Low",
            "Customer Rating",
        ]
        self.sort_combo = ttk.Combobox(
            sort_bar,
            values=sort_options,
            textvariable=self.sort_var,
            state="readonly",
            width=22,
        )
        self.sort_combo.pack(side=tk.LEFT)
        self.sort_combo.bind("<<ComboboxSelected>>", lambda e: self.render_products())

        self.count_label = tk.Label(
            sort_bar, text="", font=("Arial", 9), fg="#878787", bg="#ffffff"
        )
        self.count_label.pack(side=tk.RIGHT)

        ttk.Separator(right_panel, orient="horizontal").pack(fill=tk.X)

        # Scrollable Product Canvas
        self.canvas = tk.Canvas(right_panel, bg="#ffffff", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            right_panel, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ffffff", padx=10, pady=10)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.configure(xscrollcommand=None, yscrollcommand=self.scrollbar.set)

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        # Mouse wheel support
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_price_scale_change(self, val):
        price = int(float(val))
        self.price_label.config(text=f"₹{price:,}")
        self.render_products()

    def reset_filters(self):
        self.search_var.set("")
        self.category_var.set("All")
        self.rating_var.set(0)
        self.max_price_var.set(140000)
        self.price_label.config(text="₹1,40,000")
        self.sort_var.set("Relevance")
        self.render_products()

    # ------------------ PRODUCT RENDERING ------------------
    def get_filtered_products(self):
        query = self.search_var.get().strip().lower()
        selected_cat = self.category_var.get()
        min_rate = self.rating_var.get()
        max_p = self.max_price_var.get()

        filtered = []
        for p in PRODUCTS:
            matches_query = (
                query in p["name"].lower() or query in p["category"].lower()
            )
            matches_cat = selected_cat == "All" or p["category"] == selected_cat
            matches_rate = p["rating"] >= min_rate
            matches_price = p["price"] <= max_p

            if matches_query and matches_cat and matches_rate and matches_price:
                filtered.append(p)

        # Sorting
        sort_by = self.sort_var.get()
        if sort_by == "Price -- Low to High":
            filtered.sort(key=lambda x: x["price"])
        elif sort_by == "Price -- High to Low":
            filtered.sort(key=lambda x: x["price"], reverse=True)
        elif sort_by == "Customer Rating":
            filtered.sort(key=lambda x: x["rating"], reverse=True)

        return filtered

    def render_products(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        items = self.get_filtered_products()
        self.count_label.config(text=f"Showing {len(items)} items")

        if not items:
            empty_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", pady=60)
            empty_frame.pack(fill=tk.BOTH, expand=True)
            tk.Label(
                empty_frame, text="🔍", font=("Arial", 36), bg="#ffffff"
            ).pack()
            tk.Label(
                empty_frame,
                text="No matching products found",
                font=("Arial", 13, "bold"),
                fg="#333333",
                bg="#ffffff",
            ).pack(pady=4)
            tk.Label(
                empty_frame,
                text="Try adjusting your search terms or filters.",
                font=("Arial", 10),
                fg="#878787",
                bg="#ffffff",
            ).pack()
            return

        # Render list of product cards
        for prod in items:
            self.create_product_card(prod)

    def create_product_card(self, product):
        card = tk.Frame(
            self.scrollable_frame,
            bg="#ffffff",
            bd=1,
            relief=tk.GROOVE,
            padx=14,
            pady=12,
        )
        card.pack(fill=tk.X, expand=True, pady=4)

        # Left Info
        left = tk.Frame(card, bg="#ffffff")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Category chip
        tk.Label(
            left,
            text=product["category"].upper(),
            font=("Arial", 8, "bold"),
            fg="#878787",
            bg="#ffffff",
        ).pack(anchor="w")

        # Name
        tk.Label(
            left,
            text=product["name"],
            font=("Arial", 12, "bold"),
            fg="#212121",
            bg="#ffffff",
            anchor="w",
        ).pack(anchor="w", pady=(1, 4))

        # Rating pill
        rate_frame = tk.Frame(left, bg="#ffffff")
        rate_frame.pack(anchor="w", pady=(0, 4))

        badge = tk.Label(
            rate_frame,
            text=f" {product['rating']} ★ ",
            font=("Arial", 9, "bold"),
            fg="#ffffff",
            bg="#388e3c",
            padx=3,
            pady=1,
        )
        badge.pack(side=tk.LEFT)

        tk.Label(
            rate_frame,
            text=f" ({product['reviews']:,} ratings)",
            font=("Arial", 9),
            fg="#878787",
            bg="#ffffff",
        ).pack(side=tk.LEFT, padx=5)

        # Price row
        price_row = tk.Frame(left, bg="#ffffff")
        price_row.pack(anchor="w", pady=(2, 0))

        tk.Label(
            price_row,
            text=f"₹{product['price']:,}",
            font=("Arial", 14, "bold"),
            fg="#212121",
            bg="#ffffff",
        ).pack(side=tk.LEFT)

        tk.Label(
            price_row,
            text=f"₹{product['original']:,}",
            font=("Arial", 10, "overstrike"),
            fg="#878787",
            bg="#ffffff",
        ).pack(side=tk.LEFT, padx=6)

        tk.Label(
            price_row,
            text=product["discount"],
            font=("Arial", 10, "bold"),
            fg="#388e3c",
            bg="#ffffff",
        ).pack(side=tk.LEFT)

        # Right Actions
        right = tk.Frame(card, bg="#ffffff")
        right.pack(side=tk.RIGHT, padx=10)

        add_btn = tk.Button(
            right,
            text="ADD TO CART",
            font=("Arial", 10, "bold"),
            bg="#ff9f00",
            fg="#ffffff",
            activebackground="#e08b00",
            activeforeground="#ffffff",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=lambda p=product: self.add_to_cart(p),
        )
        add_btn.pack()

    # ------------------ CART OPERATIONS ------------------
    def add_to_cart(self, product):
        pid = product["id"]
        if pid in self.cart:
            self.cart[pid]["qty"] += 1
        else:
            self.cart[pid] = {"product": product, "qty": 1}

        self.update_cart_badge()
        messagebox.showinfo(
            "Cart Updated", f"Added '{product['name']}' to your cart!"
        )

    def update_cart_badge(self):
        total_items = sum(item["qty"] for item in self.cart.values())
        self.cart_btn.config(text=f"🛒 Cart ({total_items})")

    def open_cart_window(self):
        CartWindow(self.root, self.cart, self.on_cart_update, self.open_checkout)

    def on_cart_update(self):
        self.update_cart_badge()

    # ------------------ CHECKOUT FLOW ------------------
    def open_checkout(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "Your cart is empty!")
            return
        CheckoutWindow(self.root, self.cart, self.on_order_placed)

    def on_order_placed(self):
        self.cart.clear()
        self.update_cart_badge()


# ------------------ CART WINDOW ------------------
class CartWindow(tk.Toplevel):
    def __init__(self, parent, cart, on_update, on_checkout):
        super().__init__(parent)
        self.title("My Shopping Cart - Flipkart")
        self.geometry("640x540")
        self.cart = cart
        self.on_update = on_update
        self.on_checkout = on_checkout
        self.configure(bg="#f1f3f6")
        self.grab_set()

        self.render()

    def render(self):
        for w in self.winfo_children():
            w.destroy()

        # Header
        hdr = tk.Frame(self, bg="#2874f0", pady=12, padx=16)
        hdr.pack(fill=tk.X)
        total_count = sum(item["qty"] for item in self.cart.values())
        tk.Label(
            hdr,
            text=f"My Cart ({total_count} Items)",
            font=("Arial", 13, "bold"),
            fg="#ffffff",
            bg="#2874f0",
        ).pack(side=tk.LEFT)

        if not self.cart:
            body = tk.Frame(self, bg="#ffffff", pady=60)
            body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
            tk.Label(body, text="🛒", font=("Arial", 40), bg="#ffffff").pack()
            tk.Label(
                body,
                text="Your cart is currently empty!",
                font=("Arial", 12, "bold"),
                fg="#555555",
                bg="#ffffff",
            ).pack(pady=6)
            return

        # Items List
        content = tk.Frame(self, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        canvas = tk.Canvas(content, bg="#ffffff", highlightthickness=0)
        scroll = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        list_frame = tk.Frame(canvas, bg="#ffffff", padx=8, pady=8)

        list_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        cw = canvas.create_window((0, 0), window=list_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        total_price = 0
        total_mrp = 0

        for pid, data in list(self.cart.items()):
            p = data["product"]
            qty = data["qty"]
            item_total = p["price"] * qty
            total_price += item_total
            total_mrp += p["original"] * qty

            item_row = tk.Frame(list_frame, bg="#ffffff", pady=8)
            item_row.pack(fill=tk.X, expand=True)

            # Details
            info = tk.Frame(item_row, bg="#ffffff")
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            tk.Label(
                info,
                text=p["name"],
                font=("Arial", 10, "bold"),
                fg="#212121",
                bg="#ffffff",
                anchor="w",
            ).pack(anchor="w")

            tk.Label(
                info,
                text=f"₹{p['price']:,} each | Subtotal: ₹{item_total:,}",
                font=("Arial", 9),
                fg="#878787",
                bg="#ffffff",
            ).pack(anchor="w")

            # Quantity Controller
            controls = tk.Frame(item_row, bg="#ffffff")
            controls.pack(side=tk.RIGHT, padx=10)

            tk.Button(
                controls,
                text="-",
                width=2,
                font=("Arial", 9, "bold"),
                command=lambda id=pid: self.change_qty(id, -1),
            ).pack(side=tk.LEFT)

            tk.Label(
                controls,
                text=f" {qty} ",
                font=("Arial", 10, "bold"),
                bg="#ffffff",
            ).pack(side=tk.LEFT, padx=4)

            tk.Button(
                controls,
                text="+",
                width=2,
                font=("Arial", 9, "bold"),
                command=lambda id=pid: self.change_qty(id, 1),
            ).pack(side=tk.LEFT)

            tk.Button(
                controls,
                text="🗑️",
                bd=0,
                bg="#ffffff",
                fg="red",
                font=("Arial", 10),
                cursor="hand2",
                command=lambda id=pid: self.remove_item(id),
            ).pack(side=tk.LEFT, padx=(10, 0))

            ttk.Separator(list_frame, orient="horizontal").pack(fill=tk.X, pady=4)

        # Footer Checkout Bar
        footer = tk.Frame(self, bg="#ffffff", padx=16, pady=12, bd=1, relief=tk.SOLID)
        footer.pack(fill=tk.X)

        savings = total_mrp - total_price
        price_summary = tk.Frame(footer, bg="#ffffff")
        price_summary.pack(side=tk.LEFT)

        tk.Label(
            price_summary,
            text=f"Total: ₹{total_price:,}",
            font=("Arial", 13, "bold"),
            fg="#212121",
            bg="#ffffff",
        ).pack(anchor="w")

        tk.Label(
            price_summary,
            text=f"You save ₹{savings:,} on this order!",
            font=("Arial", 9, "bold"),
            fg="#388e3c",
            bg="#ffffff",
        ).pack(anchor="w")

        checkout_btn = tk.Button(
            footer,
            text="PLACE ORDER",
            font=("Arial", 11, "bold"),
            bg="#fb641b",
            fg="#ffffff",
            activebackground="#e05613",
            activeforeground="#ffffff",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.start_checkout,
        )
        checkout_btn.pack(side=tk.RIGHT)

    def change_qty(self, pid, delta):
        if pid in self.cart:
            self.cart[pid]["qty"] += delta
            if self.cart[pid]["qty"] <= 0:
                del self.cart[pid]
            self.on_update()
            self.render()

    def remove_item(self, pid):
        if pid in self.cart:
            del self.cart[pid]
            self.on_update()
            self.render()

    def start_checkout(self):
        self.destroy()
        self.on_checkout()


# ------------------ CHECKOUT & PAYMENT WINDOW ------------------
class CheckoutWindow(tk.Toplevel):
    def __init__(self, parent, cart, on_success):
        super().__init__(parent)
        self.title("Flipkart Secure Checkout")
        self.geometry("600x620")
        self.cart = cart
        self.on_success = on_success
        self.configure(bg="#f1f3f6")
        self.grab_set()

        self.pay_method = tk.StringVar(value="UPI")

        self.total_amount = sum(
            item["product"]["price"] * item["qty"] for item in self.cart.values()
        )

        self.build_form()

    def build_form(self):
        # Header
        hdr = tk.Frame(self, bg="#2874f0", pady=12, padx=16)
        hdr.pack(fill=tk.X)
        tk.Label(
            hdr,
            text="Order Checkout & Payment",
            font=("Arial", 13, "bold"),
            fg="#ffffff",
            bg="#2874f0",
        ).pack(side=tk.LEFT)

        main_box = tk.Frame(self, bg="#ffffff", padx=20, pady=16)
        main_box.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # 1. Delivery Details
        tk.Label(
            main_box,
            text="1. Delivery Address",
            font=("Arial", 11, "bold"),
            fg="#2874f0",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 6))

        addr_form = tk.Frame(main_box, bg="#ffffff")
        addr_form.pack(fill=tk.X, pady=(0, 12))

        tk.Label(addr_form, text="Full Name:", font=("Arial", 9), bg="#ffffff").grid(
            row=0, column=0, sticky="w", pady=3
        )
        self.name_entry = tk.Entry(addr_form, font=("Arial", 9), width=28)
        self.name_entry.insert(0, "Patel Happy")
        self.name_entry.grid(row=0, column=1, padx=8, pady=3)

        tk.Label(addr_form, text="Mobile No:", font=("Arial", 9), bg="#ffffff").grid(
            row=0, column=2, sticky="w", pady=3
        )
        self.phone_entry = tk.Entry(addr_form, font=("Arial", 9), width=18)
        self.phone_entry.insert(0, "9876543210")
        self.phone_entry.grid(row=0, column=3, padx=8, pady=3)

        tk.Label(addr_form, text="Street Address:", font=("Arial", 9), bg="#ffffff").grid(
            row=1, column=0, sticky="w", pady=3
        )
        self.addr_entry = tk.Entry(addr_form, font=("Arial", 9), width=28)
        self.addr_entry.insert(0, "Flat 402, Sea View Apartments")
        self.addr_entry.grid(row=1, column=1, padx=8, pady=3)

        tk.Label(addr_form, text="Pincode:", font=("Arial", 9), bg="#ffffff").grid(
            row=1, column=2, sticky="w", pady=3
        )
        self.pin_entry = tk.Entry(addr_form, font=("Arial", 9), width=18)
        self.pin_entry.insert(0, "400001")
        self.pin_entry.grid(row=1, column=3, padx=8, pady=3)

        ttk.Separator(main_box, orient="horizontal").pack(fill=tk.X, pady=8)

        # 2. Payment Options
        tk.Label(
            main_box,
            text="2. Select Payment Option",
            font=("Arial", 11, "bold"),
            fg="#2874f0",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 6))

        methods = [
            ("UPI (Google Pay, PhonePe, Paytm, BHIM)", "UPI"),
            ("Credit / Debit / ATM Card", "CARD"),
            ("Net Banking", "NETBANKING"),
            ("Cash on Delivery (COD)", "COD"),
        ]

        for text, val in methods:
            tk.Radiobutton(
                main_box,
                text=text,
                value=val,
                variable=self.pay_method,
                font=("Arial", 9),
                bg="#ffffff",
                activebackground="#ffffff",
            ).pack(anchor="w", pady=2)

        ttk.Separator(main_box, orient="horizontal").pack(fill=tk.X, pady=12)

        # Order Total Summary
        tk.Label(
            main_box,
            text=f"Total Payable Amount: ₹{self.total_amount:,}",
            font=("Arial", 13, "bold"),
            fg="#212121",
            bg="#ffffff",
        ).pack(anchor="w")

        tk.Label(
            main_box,
            text="🛡️ Safe and Secure Payments. 100% Authentic Products.",
            font=("Arial", 9),
            fg="#388e3c",
            bg="#ffffff",
        ).pack(anchor="w", pady=(2, 16))

        # Confirm & Pay CTA
        pay_btn = tk.Button(
            main_box,
            text=f"CONFIRM & PAY ₹{self.total_amount:,}",
            font=("Arial", 11, "bold"),
            bg="#fb641b",
            fg="#ffffff",
            activebackground="#e05613",
            activeforeground="#ffffff",
            bd=0,
            pady=10,
            cursor="hand2",
            command=self.process_payment,
        )
        pay_btn.pack(fill=tk.X)

    def process_payment(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        addr = self.addr_entry.get().strip()

        if not name or not phone or not addr:
            messagebox.showerror("Error", "Please fill in all address details!")
            return

        order_id = f"OD{random.randint(1000000000, 9999999999)}"
        method = self.pay_method.get()

        messagebox.showinfo(
            "Order Placed Successfully! 🎉",
            f"Thank you, {name}!\n\n"
            f"Order ID: {order_id}\n"
            f"Payment Method: {method}\n"
            f"Amount Paid: ₹{self.total_amount:,}\n\n"
            "Your items will be delivered within 2-3 business days.",
        )

        self.on_success()
        self.destroy()


# ------------------ APP ENTRY POINT ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FlipkartApp(root)
    root.mainloop()