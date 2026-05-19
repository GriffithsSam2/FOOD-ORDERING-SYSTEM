#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║         FOOD ORDERING SYSTEM  —  Python Edition v2.0         ║
║              Developed by: Griffiths Samuel Yankson           ║
╠══════════════════════════════════════════════════════════════╣
║  Improvements over C version:                                 ║
║   ✓ Graphical User Interface (Tkinter)                        ║
║   ✓ SQLite database  (replaces raw binary FOS.DAT)            ║
║   ✓ Shopping cart  (multiple items per session)               ║
║   ✓ Admin panel with PIN authentication                       ║
║   ✓ Order history with timestamps                             ║
║   ✓ Editable dish prices through admin panel                  ║
║   ✓ Cross-platform  (Windows · macOS · Linux)                 ║
╠══════════════════════════════════════════════════════════════╣
║  Requirements : Python 3.6+  (standard library only)          ║
║  Run with     : python FoodOrderingSystem.py                   ║
║  Admin PIN    : 1234  (change ADMIN_PIN below)                 ║
╚══════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import datetime
import os

# ── CONFIGURATION ──────────────────────────────────────────────────────────────
ADMIN_PIN  = "1234"
DB_FILE    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fos.db")
APP_TITLE  = "Food Ordering System  ·  FOS v2.0"
CURRENCY   = "GH₵"

# ── COLOUR PALETTE ─────────────────────────────────────────────────────────────
C = {
    "bg":         "#F0F4F8",
    "header":     "#1A252F",
    "sidebar":    "#2C3E50",
    "card":       "#FFFFFF",
    "border":     "#DDE3EA",
    "text":       "#2C3E50",
    "muted":      "#7F8C8D",
    "white":      "#FFFFFF",
    "Breakfast":  "#E67E22",
    "Lunch":      "#27AE60",
    "Dinner":     "#8E44AD",
    "primary":    "#2980B9",
    "danger":     "#E74C3C",
    "success":    "#27AE60",
    "cart_bg":    "#EBF5FB",
    "price":      "#E74C3C",
    "tab_active": "#2980B9",
    "tab_hover":  "#34495E",
    "checkout":   "#27AE60",
    "receipt_bg": "#FDFEFE",
}

# ── MENU DATA ──────────────────────────────────────────────────────────────────
# (name, category, price_ghc, ingredients)
MENU_DATA = [
    # BREAKFAST
    ("Pancakes",                              "Breakfast", 210, "Flour, Sugar, Baking Powder, Salt, Nutmeg, Eggs, Butter"),
    ("Avocado Toasts",                        "Breakfast", 299, "Avocado, Salt, Pepper, Whole Grain Bread, Garlic, Olive Oil"),
    ("Granola",                               "Breakfast", 185, "Oats, Almonds, Cashews, Coconut, Brown Sugar, Raisins"),
    ("Sausage Gravy Breakfast Lasagna",       "Breakfast", 379, "Lasagna Noodles, Sausage, Flour, Milk, Cheese, Spinach, Parsley"),
    ("Instant Pot Mini Frittatas",            "Breakfast", 185, "Bacon, Mushrooms, Baby Spinach, Cheddar, Eggs, Cream, Nutmeg"),
    ("Scrambled Eggs with Herbs",             "Breakfast", 145, "Eggs, Milk, Heavy Cream, Chives, Parsley, Tarragon, Butter"),
    ("Breakfast Bread Pudding",               "Breakfast", 155, "Eggs, Honey, Vanilla, Orange Zest, Brioche, Raisins, Maple Syrup"),
    ("Blueberry Scones with Lemon Glaze",     "Breakfast", 465, "Flour, Butter, Blueberries, Heavy Cream, Lemon Juice, Lemon Zest"),
    ("Sheet-Pan Bacon Egg Sandwiches",        "Breakfast", 500, "Bacon, Eggs, Scallions, Tomatoes, Cheddar, Potato Rolls, Hot Sauce"),
    ("Burritos with Chorizo",                 "Breakfast", 410, "Chorizo, Eggs, Hash Browns, Refried Beans, Tortillas, Mozzarella"),
    # LUNCH
    ("Lemon-Herb Rice Salad",                 "Lunch", 300, "Rice, Red Onion, Carrot, Cucumber, Peanuts, Mint, Basil, Cilantro"),
    ("Lightened-Up Stuffed Peppers",          "Lunch", 365, "Bell Peppers, Beef, Lentils, Rice, Tomato Paste, Broth, Oregano"),
    ("Tex-Mex Chicken Quinoa",                "Lunch", 320, "Chicken, Quinoa, Black Beans, Avocado, Cheese, Lime Juice"),
    ("Veggie Lover's Club Sandwich",          "Lunch", 300, "Avocado, Arugula, Tofu, Red Onion, Whole Wheat Bread, Yogurt"),
    ("Nordic Shrimp Toast",                   "Lunch", 340, "Shrimp, Cream Cheese, Greek Yogurt, Pumpernickel Bread, Radishes"),
    ("Chicken Tacos with Avocado Salad",      "Lunch", 420, "Chicken, Avocado, Cilantro, Salsa, Sour Cream, Corn Tortillas"),
    ("Pizza with Cauliflower Crust",          "Lunch", 480, "Cauliflower, Mozzarella, Parmesan, Eggs, Marinara, Bell Peppers"),
    ("Pork and Broccoli Grain Bowl",          "Lunch", 520, "Pork, Sweet Potato, Broccoli, Quinoa, Orange Juice, Red Wine Vinegar"),
    ("Monte Cristo Crepes",                   "Lunch", 320, "Ham, Turkey, Muenster Cheese, Crepes, Dijon Mustard, Raspberry Jam"),
    ("Antipasti Penne",                       "Lunch", 320, "Whole-Grain Penne, Salami, Spanish Olives, Tomatoes, Mozzarella"),
    ("Grilled Spiced Chicken and Plums",      "Lunch", 490, "Chicken Drumsticks, Plums, Honey, Broccoli, Almonds, Lemon Juice"),
    ("Shrimp Fajita Salad",                   "Lunch", 490, "Shrimp, Bell Peppers, Onion, Lime Juice, Honey, Cilantro, Lettuce"),
    ("Veggie-Stacked Pita Pockets",           "Lunch", 400, "White Beans, Avocado, Cucumber, Pita, Pecorino Romano, Olive Oil"),
    ("Creamy Hummus & Smoked Turkey Sandwich","Lunch", 590, "Smoked Turkey, Hummus, Whole Wheat Bagel, Spinach, Tomato, Cucumber"),
    ("Turkey Frittata",                       "Lunch", 640, "Turkey, Eggs, Bell Pepper, Potatoes, Cream, Cheddar, Mozzarella"),
    # DINNER
    ("Ground Turkey Enchilada Stir-Fry",      "Dinner", 610, "Turkey, Couscous, Squash, Broccoli, Black Beans, Enchilada Sauce"),
    ("Chili Chicken with Hominy Hash",        "Dinner", 460, "Chicken Thighs, Chili Powder, Cumin, Acorn Squash, Bell Pepper"),
    ("Chicken Katsu with Ginger Rice",        "Dinner", 475, "Chicken Cutlets, Flour, Eggs, Ginger, White Rice, Katsu Sauce"),
    ("Ribbony Shrimp and Pasta Scampi",       "Dinner", 420, "Shrimp, Wheat Spaghetti, Squash, Tomatoes, Garlic, Chicken Broth"),
    ("Coconut-Crusted Shrimp & Pineapple",    "Dinner", 460, "Shrimp, Coconut, Egg Whites, Lime Juice, Cilantro, Pineapple"),
    ("Whole-Wheat Fettuccine & Zucchini",     "Dinner", 440, "Fettuccini, Green Zucchini, Yellow Zucchini, Parmesan, Garlic, Basil"),
    ("Honey-Soy Grilled Salmon & Edamame",    "Dinner", 535, "Salmon, Soy Sauce, Honey, Ginger, Sesame Seeds, Lime, Edamame"),
    ("Thai Curry Veggie Noodles",             "Dinner", 410, "Coconut Milk, Red Curry Paste, Chicken, Carrot, Cabbage, Cashews"),
    ("Sheet Pan Chicken Fajitas",             "Dinner", 490, "Chicken Breast, Bell Peppers, Onion, Tortillas, Cheese, Salsa"),
    ("Pork Tenderloin with Seasoned Rub",     "Dinner", 500, "Pork, Garlic Powder, Oregano, Cumin, Coriander, Salt, Olive Oil"),
    ("Spicy Kale & Corn Stuffed Chicken",     "Dinner", 440, "Chicken Breast, Corn, Cheese, Garlic, Broth, Kale, Lemon Juice"),
    ("Vietnamese Pork Chops & Ginger Rice",   "Dinner", 520, "Pork, Brown Sugar, Fish Sauce, Lemongrass, Jasmine Rice, Ginger"),
    ("Chicken Thighs & Couscous with Dill",   "Dinner", 465, "Chicken Thighs, Couscous, Tomatoes, Lemon Juice, Greek Yogurt"),
    ("Tricolore Penne Pasta with Chicken",    "Dinner", 410, "Penne, Chicken, Arugula, Tomatoes, Parmesan, Basil, Olive Oil"),
    ("Tricolor Salad Pizzas",                 "Dinner", 470, "Pizza Dough, Ricotta, Mozzarella, Radicchio, Arugula, Tomatoes"),
    ("Bacon and Kimchi Noodle Stir-Fry",      "Dinner", 480, "Bacon, Kimchi, Chinese Egg Noodles, Broccolini, Sesame Oil"),
]

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════════════════════
class Database:
    def __init__(self, path):
        self.path = path
        self._init()

    def _conn(self):
        return sqlite3.connect(self.path)

    def _init(self):
        with self._conn() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS dishes (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT    NOT NULL,
                    category    TEXT    NOT NULL,
                    price       INTEGER NOT NULL,
                    ingredients TEXT    NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp  TEXT NOT NULL,
                    items_json TEXT NOT NULL,
                    total      INTEGER NOT NULL
                )
            """)
            # Seed dishes if table is empty
            if cur.execute("SELECT COUNT(*) FROM dishes").fetchone()[0] == 0:
                cur.executemany(
                    "INSERT INTO dishes (name, category, price, ingredients) VALUES (?,?,?,?)",
                    MENU_DATA
                )
            con.commit()

    def get_dishes(self, category=None):
        with self._conn() as con:
            if category:
                return con.execute(
                    "SELECT id, name, category, price, ingredients FROM dishes WHERE category=? ORDER BY name",
                    (category,)
                ).fetchall()
            return con.execute(
                "SELECT id, name, category, price, ingredients FROM dishes ORDER BY category, name"
            ).fetchall()

    def add_dish(self, name, category, price, ingredients):
        with self._conn() as con:
            con.execute(
                "INSERT INTO dishes (name, category, price, ingredients) VALUES (?,?,?,?)",
                (name, category, price, ingredients)
            )
            con.commit()

    def update_price(self, dish_id, new_price):
        with self._conn() as con:
            con.execute("UPDATE dishes SET price=? WHERE id=?", (new_price, dish_id))
            con.commit()

    def delete_dish(self, dish_id):
        with self._conn() as con:
            con.execute("DELETE FROM dishes WHERE id=?", (dish_id,))
            con.commit()

    def save_order(self, items, total):
        import json
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._conn() as con:
            con.execute(
                "INSERT INTO orders (timestamp, items_json, total) VALUES (?,?,?)",
                (ts, json.dumps(items), total)
            )
            con.commit()

    def get_orders(self):
        import json
        with self._conn() as con:
            rows = con.execute(
                "SELECT id, timestamp, items_json, total FROM orders ORDER BY id DESC"
            ).fetchall()
        result = []
        for r in rows:
            result.append((r[0], r[1], json.loads(r[2]), r[3]))
        return result


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════
class FoodOrderingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db      = Database(DB_FILE)
        self.cart    = []   # list of {"id","name","price","qty"}
        self.current = tk.StringVar(value="Breakfast")

        self.title(APP_TITLE)
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(bg=C["bg"])
        self._build_ui()
        self._clock()

    # ── UI CONSTRUCTION ───────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_body()

    def _build_header(self):
        hdr = tk.Frame(self, bg=C["header"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="🍽  Food Ordering System", bg=C["header"],
                 fg=C["white"], font=("Segoe UI", 16, "bold")).pack(side="left", padx=20)

        self._clock_lbl = tk.Label(hdr, bg=C["header"], fg="#AAB7C4",
                                   font=("Segoe UI", 10))
        self._clock_lbl.pack(side="left", padx=10)

        for txt, cmd in [("📋 History", self._show_history),
                         ("🔐 Admin",   self._show_admin)]:
            tk.Button(hdr, text=txt, command=cmd,
                      bg=C["sidebar"], fg=C["white"],
                      relief="flat", font=("Segoe UI", 10),
                      padx=14, pady=4, cursor="hand2",
                      activebackground=C["tab_hover"],
                      activeforeground=C["white"]).pack(side="right", padx=6, pady=10)

    def _build_body(self):
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True)

        # ── Category tabs ──
        tab_bar = tk.Frame(body, bg=C["sidebar"], height=46)
        tab_bar.pack(fill="x")
        tab_bar.pack_propagate(False)

        self._tab_btns = {}
        for cat in ("Breakfast", "Lunch", "Dinner"):
            emoji = {"Breakfast": "🌅", "Lunch": "☀️", "Dinner": "🌙"}[cat]
            b = tk.Button(tab_bar,
                          text=f"  {emoji}  {cat}  ",
                          command=lambda c=cat: self._select_category(c),
                          bg=C["sidebar"], fg="#AAB7C4",
                          relief="flat", font=("Segoe UI", 11),
                          activebackground=C[cat],
                          activeforeground=C["white"],
                          cursor="hand2", pady=6)
            b.pack(side="left", padx=2, pady=4, ipady=2)
            self._tab_btns[cat] = b

        # ── Main split: menu list | cart ──
        split = tk.Frame(body, bg=C["bg"])
        split.pack(fill="both", expand=True)

        # Menu panel (left + center)
        self._menu_outer = tk.Frame(split, bg=C["bg"])
        self._menu_outer.pack(side="left", fill="both", expand=True)

        # Cart panel (right, fixed width)
        self._build_cart_panel(split)

        # Load initial category
        self._select_category("Breakfast")

    def _build_cart_panel(self, parent):
        panel = tk.Frame(parent, bg=C["cart_bg"], width=280)
        panel.pack(side="right", fill="y")
        panel.pack_propagate(False)

        tk.Label(panel, text="🛒  Your Cart", bg=C["cart_bg"],
                 fg=C["text"], font=("Segoe UI", 13, "bold")).pack(pady=(16, 4), padx=16, anchor="w")

        sep = tk.Frame(panel, bg=C["border"], height=1)
        sep.pack(fill="x", padx=16, pady=4)

        # Scrollable cart items
        cart_scroll_frame = tk.Frame(panel, bg=C["cart_bg"])
        cart_scroll_frame.pack(fill="both", expand=True, padx=8)

        self._cart_canvas = tk.Canvas(cart_scroll_frame, bg=C["cart_bg"],
                                      highlightthickness=0)
        sb = tk.Scrollbar(cart_scroll_frame, orient="vertical",
                          command=self._cart_canvas.yview)
        self._cart_inner = tk.Frame(self._cart_canvas, bg=C["cart_bg"])

        self._cart_inner.bind("<Configure>",
            lambda e: self._cart_canvas.configure(
                scrollregion=self._cart_canvas.bbox("all")))

        self._cart_canvas.create_window((0, 0), window=self._cart_inner, anchor="nw")
        self._cart_canvas.configure(yscrollcommand=sb.set)
        self._cart_canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Cart footer
        footer = tk.Frame(panel, bg=C["cart_bg"])
        footer.pack(fill="x", padx=16, pady=8)

        sep2 = tk.Frame(footer, bg=C["border"], height=1)
        sep2.pack(fill="x", pady=(0, 8))

        self._total_lbl = tk.Label(footer, text=f"Total:  {CURRENCY} 0.00",
                                   bg=C["cart_bg"], fg=C["text"],
                                   font=("Segoe UI", 12, "bold"))
        self._total_lbl.pack(anchor="e", pady=(0, 8))

        self._checkout_btn = tk.Button(footer, text="✓  Checkout",
                                       command=self._checkout,
                                       bg=C["checkout"], fg=C["white"],
                                       font=("Segoe UI", 11, "bold"),
                                       relief="flat", cursor="hand2",
                                       pady=10, state="disabled")
        self._checkout_btn.pack(fill="x")

        clr_btn = tk.Button(footer, text="Clear Cart",
                            command=self._clear_cart,
                            bg=C["border"], fg=C["muted"],
                            font=("Segoe UI", 9), relief="flat",
                            cursor="hand2", pady=4)
        clr_btn.pack(fill="x", pady=(4, 0))

    # ── CATEGORY & MENU ───────────────────────────────────────────────────────
    def _select_category(self, category):
        self.current.set(category)
        color = C[category]

        for cat, btn in self._tab_btns.items():
            if cat == category:
                btn.config(bg=color, fg=C["white"], font=("Segoe UI", 11, "bold"))
            else:
                btn.config(bg=C["sidebar"], fg="#AAB7C4", font=("Segoe UI", 11))

        self._load_menu(category)

    def _load_menu(self, category):
        for w in self._menu_outer.winfo_children():
            w.destroy()

        color = C[category]

        # Category banner
        banner = tk.Frame(self._menu_outer, bg=color, height=40)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        emoji = {"Breakfast": "🌅", "Lunch": "☀️", "Dinner": "🌙"}[category]
        tk.Label(banner, text=f"  {emoji}  {category} Menu",
                 bg=color, fg=C["white"],
                 font=("Segoe UI", 12, "bold")).pack(side="left", padx=20, pady=6)

        dishes = self.db.get_dishes(category)
        tk.Label(banner, text=f"{len(dishes)} dishes",
                 bg=color, fg=C["white"],
                 font=("Segoe UI", 9)).pack(side="right", padx=16)

        # Scrollable dish list
        container = tk.Frame(self._menu_outer, bg=C["bg"])
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=C["bg"], highlightthickness=0)
        sb = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=C["bg"])

        inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Mouse wheel scroll
        def _scroll(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _scroll)

        for dish in dishes:
            self._dish_card(inner, dish, color)

        if not dishes:
            tk.Label(inner, text="No dishes in this category.",
                     bg=C["bg"], fg=C["muted"],
                     font=("Segoe UI", 11)).pack(pady=40)

    def _dish_card(self, parent, dish, color):
        did, name, cat, price, ingredients = dish

        card = tk.Frame(parent, bg=C["card"],
                        highlightthickness=1,
                        highlightbackground=C["border"])
        card.pack(fill="x", padx=16, pady=6, ipady=6)

        # Color accent left strip
        strip = tk.Frame(card, bg=color, width=5)
        strip.pack(side="left", fill="y")

        content = tk.Frame(card, bg=C["card"])
        content.pack(side="left", fill="both", expand=True, padx=12, pady=8)

        # Top row: name + price
        top = tk.Frame(content, bg=C["card"])
        top.pack(fill="x")

        tk.Label(top, text=name, bg=C["card"], fg=C["text"],
                 font=("Segoe UI", 11, "bold"),
                 anchor="w", wraplength=480,
                 justify="left").pack(side="left", fill="x", expand=True)

        tk.Label(top, text=f"{CURRENCY} {price:,}",
                 bg=C["card"], fg=C["price"],
                 font=("Segoe UI", 12, "bold")).pack(side="right", padx=(8, 0))

        # Ingredients preview
        preview = (ingredients[:80] + "...") if len(ingredients) > 80 else ingredients
        tk.Label(content, text=f"🌿  {preview}",
                 bg=C["card"], fg=C["muted"],
                 font=("Segoe UI", 9), anchor="w",
                 wraplength=480, justify="left").pack(fill="x", pady=(2, 6))

        # Buttons row
        btn_row = tk.Frame(content, bg=C["card"])
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="View Ingredients",
                  command=lambda i=ingredients, n=name: self._show_ingredients(n, i),
                  bg=C["border"], fg=C["text"],
                  font=("Segoe UI", 9), relief="flat",
                  cursor="hand2", padx=10, pady=3).pack(side="left")

        tk.Button(btn_row, text="＋  Add to Cart",
                  command=lambda d=did, n=name, p=price: self._add_to_cart(d, n, p),
                  bg=color, fg=C["white"],
                  font=("Segoe UI", 9, "bold"), relief="flat",
                  cursor="hand2", padx=14, pady=3).pack(side="right")

    # ── INGREDIENTS POPUP ─────────────────────────────────────────────────────
    def _show_ingredients(self, name, ingredients):
        popup = tk.Toplevel(self)
        popup.title(f"Ingredients — {name}")
        popup.geometry("420x260")
        popup.resizable(False, False)
        popup.configure(bg=C["card"])
        popup.grab_set()

        tk.Label(popup, text=f"🌿  Ingredients", bg=C["card"],
                 fg=C["text"], font=("Segoe UI", 13, "bold")).pack(pady=(20, 4), padx=24, anchor="w")
        tk.Label(popup, text=name, bg=C["card"],
                 fg=C["muted"], font=("Segoe UI", 10, "italic")).pack(padx=24, anchor="w")

        tk.Frame(popup, bg=C["border"], height=1).pack(fill="x", padx=24, pady=10)

        items = [i.strip() for i in ingredients.split(",")]
        text_frame = tk.Frame(popup, bg=C["card"])
        text_frame.pack(fill="both", expand=True, padx=24)

        for i, item in enumerate(items):
            row = tk.Frame(text_frame, bg=C["card"])
            row.pack(fill="x", pady=1)
            tk.Label(row, text="•", bg=C["card"], fg=C["success"],
                     font=("Segoe UI", 10, "bold"), width=2).pack(side="left")
            tk.Label(row, text=item, bg=C["card"], fg=C["text"],
                     font=("Segoe UI", 10), anchor="w").pack(side="left")

        tk.Button(popup, text="Close", command=popup.destroy,
                  bg=C["primary"], fg=C["white"], relief="flat",
                  font=("Segoe UI", 10), cursor="hand2",
                  padx=20, pady=6).pack(pady=16)

    # ── CART ──────────────────────────────────────────────────────────────────
    def _add_to_cart(self, dish_id, name, price):
        qty = simpledialog.askinteger(
            "Quantity", f"How many portions of\n'{name}'?",
            parent=self, minvalue=1, maxvalue=20, initialvalue=1
        )
        if not qty:
            return

        # Check if already in cart → increase qty
        for item in self.cart:
            if item["id"] == dish_id:
                item["qty"] += qty
                self._refresh_cart()
                return

        self.cart.append({"id": dish_id, "name": name, "price": price, "qty": qty})
        self._refresh_cart()

    def _refresh_cart(self):
        for w in self._cart_inner.winfo_children():
            w.destroy()

        if not self.cart:
            tk.Label(self._cart_inner, text="Your cart is empty.",
                     bg=C["cart_bg"], fg=C["muted"],
                     font=("Segoe UI", 10)).pack(pady=20)
            self._total_lbl.config(text=f"Total:  {CURRENCY} 0.00")
            self._checkout_btn.config(state="disabled")
            return

        total = 0
        for idx, item in enumerate(self.cart):
            subtotal = item["price"] * item["qty"]
            total += subtotal

            row = tk.Frame(self._cart_inner, bg=C["cart_bg"])
            row.pack(fill="x", padx=4, pady=3)

            # Name (truncated if long)
            display_name = item["name"][:24] + "…" if len(item["name"]) > 24 else item["name"]
            tk.Label(row, text=display_name, bg=C["cart_bg"], fg=C["text"],
                     font=("Segoe UI", 9), anchor="w",
                     width=18, wraplength=140,
                     justify="left").pack(side="left")

            tk.Label(row, text=f"×{item['qty']}",
                     bg=C["cart_bg"], fg=C["muted"],
                     font=("Segoe UI", 9)).pack(side="left", padx=4)

            tk.Label(row, text=f"{CURRENCY}{subtotal:,}",
                     bg=C["cart_bg"], fg=C["price"],
                     font=("Segoe UI", 9, "bold")).pack(side="left", padx=4)

            tk.Button(row, text="✕",
                      command=lambda i=idx: self._remove_from_cart(i),
                      bg=C["cart_bg"], fg=C["danger"],
                      font=("Segoe UI", 8), relief="flat",
                      cursor="hand2").pack(side="right")

        self._total_lbl.config(text=f"Total:  {CURRENCY} {total:,}.00")
        self._checkout_btn.config(state="normal")

    def _remove_from_cart(self, idx):
        if 0 <= idx < len(self.cart):
            self.cart.pop(idx)
            self._refresh_cart()

    def _clear_cart(self):
        if self.cart and messagebox.askyesno("Clear Cart", "Remove all items from cart?"):
            self.cart.clear()
            self._refresh_cart()

    # ── CHECKOUT ──────────────────────────────────────────────────────────────
    def _checkout(self):
        if not self.cart:
            return

        total = sum(i["price"] * i["qty"] for i in self.cart)

        # Save to database
        items_for_db = [{"name": i["name"], "qty": i["qty"], "price": i["price"]} for i in self.cart]
        self.db.save_order(items_for_db, total)

        # Show receipt
        self._show_receipt(self.cart, total)
        self.cart.clear()
        self._refresh_cart()

    def _show_receipt(self, items, total):
        win = tk.Toplevel(self)
        win.title("Order Receipt")
        win.geometry("400x500")
        win.resizable(False, False)
        win.configure(bg=C["receipt_bg"])
        win.grab_set()

        ts = datetime.datetime.now().strftime("%d %b %Y  ·  %H:%M:%S")

        tk.Label(win, text="🍽  FOOD ORDERING SYSTEM",
                 bg=C["receipt_bg"], fg=C["text"],
                 font=("Segoe UI", 13, "bold")).pack(pady=(24, 2))
        tk.Label(win, text="ORDER RECEIPT",
                 bg=C["receipt_bg"], fg=C["muted"],
                 font=("Segoe UI", 9, "bold")).pack()
        tk.Label(win, text=ts, bg=C["receipt_bg"], fg=C["muted"],
                 font=("Segoe UI", 9)).pack(pady=(2, 10))

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=24)

        # Items
        item_frame = tk.Frame(win, bg=C["receipt_bg"])
        item_frame.pack(fill="x", padx=24, pady=10)

        for item in items:
            sub = item["price"] * item["qty"]
            row = tk.Frame(item_frame, bg=C["receipt_bg"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{item['name']} × {item['qty']}",
                     bg=C["receipt_bg"], fg=C["text"],
                     font=("Segoe UI", 10), anchor="w").pack(side="left")
            tk.Label(row, text=f"{CURRENCY} {sub:,}",
                     bg=C["receipt_bg"], fg=C["text"],
                     font=("Segoe UI", 10), anchor="e").pack(side="right")

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=24)

        total_row = tk.Frame(win, bg=C["receipt_bg"])
        total_row.pack(fill="x", padx=24, pady=10)
        tk.Label(total_row, text="TOTAL",
                 bg=C["receipt_bg"], fg=C["text"],
                 font=("Segoe UI", 12, "bold")).pack(side="left")
        tk.Label(total_row, text=f"{CURRENCY} {total:,}.00",
                 bg=C["receipt_bg"], fg=C["price"],
                 font=("Segoe UI", 14, "bold")).pack(side="right")

        tk.Label(win, text="Payment Method:  Cash",
                 bg=C["receipt_bg"], fg=C["muted"],
                 font=("Segoe UI", 9)).pack()

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=24, pady=10)

        tk.Label(win, text="✓  Order placed successfully!",
                 bg=C["receipt_bg"], fg=C["success"],
                 font=("Segoe UI", 11, "bold")).pack()
        tk.Label(win, text="Thank you for your order.",
                 bg=C["receipt_bg"], fg=C["muted"],
                 font=("Segoe UI", 10)).pack(pady=2)

        tk.Button(win, text="Close", command=win.destroy,
                  bg=C["success"], fg=C["white"],
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2",
                  padx=30, pady=8).pack(pady=20)

    # ── ORDER HISTORY ─────────────────────────────────────────────────────────
    def _show_history(self):
        win = tk.Toplevel(self)
        win.title("Order History")
        win.geometry("680x480")
        win.configure(bg=C["bg"])
        win.grab_set()

        tk.Label(win, text="📋  Order History",
                 bg=C["bg"], fg=C["text"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(20, 4), padx=20, anchor="w")

        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=20, pady=4)

        orders = self.db.get_orders()

        if not orders:
            tk.Label(win, text="No orders placed yet.",
                     bg=C["bg"], fg=C["muted"],
                     font=("Segoe UI", 11)).pack(pady=40)
            return

        # Treeview
        cols = ("ID", "Date & Time", "Items", "Total")
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        frame = tk.Frame(win, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        tree = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
        for col, w in zip(cols, [50, 180, 320, 100]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="w")

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        for order in orders:
            oid, ts, items, total = order
            items_str = ", ".join(f"{i['name']} ×{i['qty']}" for i in items)
            if len(items_str) > 55:
                items_str = items_str[:55] + "…"
            tree.insert("", "end", values=(
                f"#{oid}", ts, items_str, f"{CURRENCY} {total:,}"
            ))

        tk.Label(win, text=f"{len(orders)} order(s) on record.",
                 bg=C["bg"], fg=C["muted"],
                 font=("Segoe UI", 9)).pack(pady=8)

    # ── ADMIN PANEL ───────────────────────────────────────────────────────────
    def _show_admin(self):
        pin = simpledialog.askstring("Admin Access",
                                     "Enter Admin PIN:",
                                     parent=self, show="*")
        if pin is None:
            return
        if pin != ADMIN_PIN:
            messagebox.showerror("Access Denied", "Incorrect PIN.", parent=self)
            return
        self._open_admin_panel()

    def _open_admin_panel(self):
        win = tk.Toplevel(self)
        win.title("Admin Panel")
        win.geometry("760x540")
        win.configure(bg=C["bg"])
        win.grab_set()

        tk.Label(win, text="🔐  Admin Panel — Menu Management",
                 bg=C["bg"], fg=C["text"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(20, 4), padx=20, anchor="w")
        tk.Frame(win, bg=C["border"], height=1).pack(fill="x", padx=20, pady=4)

        # ── Dish table ──
        cols = ("ID", "Name", "Category", "Price (GH₵)", "Ingredients")
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        table_frame = tk.Frame(win, bg=C["bg"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(6, 0))

        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col, w in zip(cols, [40, 220, 90, 90, 260]):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="w")

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def refresh_table():
            tree.delete(*tree.get_children())
            for d in self.db.get_dishes():
                ingr_short = d[4][:40] + "…" if len(d[4]) > 40 else d[4]
                tree.insert("", "end", iid=str(d[0]),
                            values=(d[0], d[1], d[2], d[3], ingr_short))

        refresh_table()

        # ── Action buttons ──
        btn_bar = tk.Frame(win, bg=C["bg"])
        btn_bar.pack(fill="x", padx=20, pady=10)

        def get_selected_id():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Select Dish", "Please select a dish first.", parent=win)
                return None
            return int(sel[0])

        def add_dish():
            d = _DishDialog(win, title="Add New Dish")
            if d.result:
                n, cat, p, ing = d.result
                self.db.add_dish(n, cat, p, ing)
                refresh_table()
                self._load_menu(self.current.get())

        def edit_price():
            did = get_selected_id()
            if did is None:
                return
            new_price = simpledialog.askinteger("Edit Price",
                "Enter new price (GH₵):",
                parent=win, minvalue=1, maxvalue=99999)
            if new_price:
                self.db.update_price(did, new_price)
                refresh_table()
                self._load_menu(self.current.get())

        def delete_dish():
            did = get_selected_id()
            if did is None:
                return
            if messagebox.askyesno("Confirm Delete",
                    "Delete this dish? This cannot be undone.", parent=win):
                self.db.delete_dish(did)
                refresh_table()
                self._load_menu(self.current.get())

        for txt, cmd, bg in [
            ("＋  Add Dish",    add_dish,    C["success"]),
            ("✏  Edit Price",  edit_price,  C["primary"]),
            ("✕  Delete Dish", delete_dish, C["danger"]),
        ]:
            tk.Button(btn_bar, text=txt, command=cmd,
                      bg=bg, fg=C["white"],
                      font=("Segoe UI", 10), relief="flat",
                      cursor="hand2", padx=16, pady=6).pack(side="left", padx=4)

        tk.Button(btn_bar, text="Close", command=win.destroy,
                  bg=C["border"], fg=C["text"],
                  font=("Segoe UI", 10), relief="flat",
                  cursor="hand2", padx=16, pady=6).pack(side="right", padx=4)

    # ── CLOCK ─────────────────────────────────────────────────────────────────
    def _clock(self):
        now = datetime.datetime.now().strftime("%A,  %d %B %Y    %H:%M:%S")
        self._clock_lbl.config(text=now)
        self.after(1000, self._clock)


# ══════════════════════════════════════════════════════════════════════════════
# ADD DISH DIALOG
# ══════════════════════════════════════════════════════════════════════════════
class _DishDialog(tk.Toplevel):
    def __init__(self, parent, title="Add Dish"):
        super().__init__(parent)
        self.title(title)
        self.geometry("440x360")
        self.resizable(False, False)
        self.configure(bg=C["card"])
        self.grab_set()
        self.result = None
        self._build()
        self.wait_window()

    def _build(self):
        tk.Label(self, text="Add New Dish", bg=C["card"],
                 fg=C["text"], font=("Segoe UI", 13, "bold")).pack(pady=(20, 4), padx=24, anchor="w")
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=24, pady=6)

        fields = tk.Frame(self, bg=C["card"])
        fields.pack(fill="x", padx=24, pady=4)

        def lbl(text):
            tk.Label(fields, text=text, bg=C["card"], fg=C["muted"],
                     font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 1))

        lbl("Dish Name *")
        self._name = tk.Entry(fields, font=("Segoe UI", 10), relief="solid", bd=1)
        self._name.pack(fill="x")

        lbl("Category *")
        self._cat = ttk.Combobox(fields, values=["Breakfast", "Lunch", "Dinner"],
                                 state="readonly", font=("Segoe UI", 10))
        self._cat.set("Breakfast")
        self._cat.pack(fill="x")

        lbl("Price (GH₵) *")
        self._price = tk.Entry(fields, font=("Segoe UI", 10), relief="solid", bd=1)
        self._price.pack(fill="x")

        lbl("Ingredients (comma-separated) *")
        self._ingr = tk.Entry(fields, font=("Segoe UI", 10), relief="solid", bd=1)
        self._ingr.pack(fill="x")

        btn_row = tk.Frame(self, bg=C["card"])
        btn_row.pack(fill="x", padx=24, pady=16)

        tk.Button(btn_row, text="Save", command=self._save,
                  bg=C["success"], fg=C["white"],
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  cursor="hand2", padx=20, pady=6).pack(side="right")
        tk.Button(btn_row, text="Cancel", command=self.destroy,
                  bg=C["border"], fg=C["text"],
                  font=("Segoe UI", 10), relief="flat",
                  cursor="hand2", padx=20, pady=6).pack(side="right", padx=8)

    def _save(self):
        name  = self._name.get().strip()
        cat   = self._cat.get()
        ingr  = self._ingr.get().strip()
        price_str = self._price.get().strip()

        if not name or not ingr or not price_str:
            messagebox.showerror("Missing Fields", "Please fill in all fields.", parent=self)
            return
        try:
            price = int(price_str)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Price",
                "Price must be a positive whole number.", parent=self)
            return

        self.result = (name, cat, price, ingr)
        self.destroy()


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = FoodOrderingApp()
    app.mainloop()
