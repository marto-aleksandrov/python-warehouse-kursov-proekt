"""
main.py
-------
Графичен интерфейс (tkinter) за системата за складова наличност.
Използва класовете Product и Warehouse от models.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from models import Product, Warehouse


def build_warehouse():
    """Създава склад и го запълва с примерни стоки чрез цикъл."""
    warehouse = Warehouse("Главен склад")
    sample_products = [
        ("Лаптоп", 12, 1450.00, "Електроника"),
        ("Мишка", 3, 25.50, "Аксесоари"),
        ("Клавиатура", 8, 60.00, "Аксесоари"),
        ("Монитор", 2, 320.00, "Електроника"),
        ("USB кабел", 40, 7.90, "Аксесоари"),
        ("Принтер", 5, 210.00, "Електроника"),
    ]
    for name, qty, price, category in sample_products:
        warehouse.add_product(Product(name, qty, price, category))
    return warehouse


class WarehouseApp(tk.Tk):
    """Главен прозорец на приложението."""

    LOW_STOCK_THRESHOLD = 5

    def __init__(self, warehouse):
        super().__init__()
        self.warehouse = warehouse

        self.title("Система за складова наличност")
        self.geometry("840x620")
        self.minsize(720, 560)
        self.configure(bg="#f3f4f6")

        self._build_styles()
        self._build_header()
        self._build_toolbar()
        self._build_table()
        self._build_form()
        self._build_statusbar()

        self.refresh_table(self.warehouse.products)

    # ---------- Изграждане на интерфейса ----------

    def _build_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10),
                        fieldbackground="white", background="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)

    def _build_header(self):
        header = tk.Frame(self, bg="#1f2937")
        header.pack(fill="x")
        tk.Label(header, text="Система за складова наличност",
                 bg="#1f2937", fg="white", font=("Segoe UI", 16, "bold"),
                 pady=14, padx=16).pack(side="left")

    def _build_toolbar(self):
        # Първи ред бутони - действия върху таблицата.
        row1 = tk.Frame(self, bg="#f3f4f6")
        row1.pack(fill="x", padx=12, pady=(12, 3))
        ttk.Button(row1, text="Сортирай по количество",
                   command=self.sort_by_quantity).pack(side="left", padx=(0, 6))
        ttk.Button(row1, text="Сортирай по стойност",
                   command=self.sort_by_value).pack(side="left", padx=6)
        ttk.Button(row1, text="Зареди ниските (+20)",
                   command=self.restock_low).pack(side="left", padx=6)

        # Втори ред бутони - триене и работа с файлове.
        row2 = tk.Frame(self, bg="#f3f4f6")
        row2.pack(fill="x", padx=12, pady=(0, 6))
        ttk.Button(row2, text="Изтрий избраната",
                   command=self.delete_selected).pack(side="left", padx=(0, 6))
        ttk.Button(row2, text="Запази във файл",
                   command=self.save_to_file).pack(side="left", padx=6)
        ttk.Button(row2, text="Зареди от файл",
                   command=self.load_from_file).pack(side="left", padx=6)

    def _build_table(self):
        container = tk.Frame(self, bg="#f3f4f6")
        container.pack(fill="both", expand=True, padx=12)

        columns = ("name", "category", "quantity", "price", "value", "status")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=10)
        headings = {
            "name": "Продукт", "category": "Категория", "quantity": "К-во",
            "price": "Цена (лв.)", "value": "Стойност (лв.)", "status": "Наличност",
        }
        widths = {"name": 160, "category": 130, "quantity": 70,
                  "price": 110, "value": 130, "status": 110}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            anchor = "w" if col in ("name", "category") else "center"
            self.tree.column(col, width=widths[col], anchor=anchor)

        self.tree.tag_configure("low", background="#fde2e1", foreground="#b91c1c")
        self.tree.tag_configure("ok", background="white")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_form(self):
        form = tk.LabelFrame(self, text="Добави нова стока", bg="#f3f4f6",
                             font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        form.pack(fill="x", padx=12, pady=10)

        self.entries = {}
        fields = [("name", "Име"), ("quantity", "Количество"),
                  ("price", "Цена"), ("category", "Категория")]
        for i, (key, label) in enumerate(fields):
            tk.Label(form, text=label, bg="#f3f4f6").grid(
                row=0, column=i * 2, padx=(0, 4), sticky="w")
            entry = ttk.Entry(form, width=14)
            entry.grid(row=0, column=i * 2 + 1, padx=(0, 12))
            self.entries[key] = entry

        ttk.Button(form, text="Добави", command=self.add_product).grid(
            row=1, column=0, columnspan=2, pady=(10, 0), sticky="w")

    def _build_statusbar(self):
        self.status_var = tk.StringVar()
        tk.Label(self, textvariable=self.status_var, bg="#e5e7eb", anchor="w",
                 padx=12, pady=6, font=("Segoe UI", 10)).pack(fill="x", side="bottom")

    # ---------- Логика ----------

    def refresh_table(self, products):
        """Изчиства таблицата и я попълва наново със списъка стоки."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in products:
            low = p.is_low_stock(self.LOW_STOCK_THRESHOLD)
            status = "НИСКА" if low else "OK"
            tag = "low" if low else "ok"
            self.tree.insert("", "end", tags=(tag,), values=(
                p.name, p.category, p.quantity,
                f"{p.price:.2f}", f"{p.total_value():.2f}", status,
            ))
        self.update_status()

    def update_status(self):
        """Обновява лентата със статус (брой стоки, ниски, обща стойност)."""
        total = self.warehouse.total_inventory_value()
        count = len(self.warehouse.products)
        low = len(self.warehouse.find_low_stock(self.LOW_STOCK_THRESHOLD))
        self.status_var.set(
            f"Брой стоки: {count}     |     Ниска наличност: {low}     |     "
            f"Обща стойност: {total:.2f} лв."
        )

    def sort_by_quantity(self):
        self.refresh_table(self.warehouse.sort_by_quantity())

    def sort_by_value(self):
        self.refresh_table(self.warehouse.sort_by_value())

    def restock_low(self):
        """Зарежда всички стоки с ниска наличност с по 20 бройки."""
        low_stock = self.warehouse.find_low_stock(self.LOW_STOCK_THRESHOLD)
        if not low_stock:
            messagebox.showinfo("Зареждане", "Няма стоки с ниска наличност.")
            return
        for product in low_stock:
            product.restock(20)
        self.refresh_table(self.warehouse.sort_by_quantity())
        names = ", ".join(p.name for p in low_stock)
        messagebox.showinfo("Зареждане", f"Заредени с по 20 бройки: {names}")

    def delete_selected(self):
        """Изтрива избраната в таблицата стока след потвърждение."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Изтриване", "Първо изберете стока от таблицата.")
            return
        name = self.tree.item(selection[0], "values")[0]
        if messagebox.askyesno("Изтриване",
                                f"Сигурни ли сте, че искате да изтриете '{name}'?"):
            self.warehouse.remove_product(name)
            self.refresh_table(self.warehouse.products)

    def save_to_file(self):
        """Запазва текущия склад в избран от потребителя JSON файл."""
        path = filedialog.asksaveasfilename(
            defaultextension=".json", initialfile="sklad.json",
            filetypes=[("JSON файлове", "*.json"), ("Всички файлове", "*.*")])
        if not path:
            return
        try:
            self.warehouse.save_to_file(path)
            messagebox.showinfo("Запазване", "Складът е запазен успешно.")
        except Exception as error:
            messagebox.showerror("Грешка", f"Неуспешно запазване: {error}")

    def load_from_file(self):
        """Зарежда склад от избран JSON файл и обновява таблицата."""
        path = filedialog.askopenfilename(
            filetypes=[("JSON файлове", "*.json"), ("Всички файлове", "*.*")])
        if not path:
            return
        try:
            self.warehouse.load_from_file(path)
            self.refresh_table(self.warehouse.products)
            messagebox.showinfo("Зареждане", "Складът е зареден успешно.")
        except Exception as error:
            messagebox.showerror("Грешка", f"Неуспешно зареждане: {error}")

    def add_product(self):
        """Чете полетата от формата, проверява ги и добавя нова стока."""
        name = self.entries["name"].get().strip()
        category = self.entries["category"].get().strip() or "General"
        qty_text = self.entries["quantity"].get().strip()
        price_text = self.entries["price"].get().strip()

        if not name:
            messagebox.showerror("Грешка", "Въведете име на стоката.")
            return
        try:
            quantity = int(qty_text)
            price = float(price_text)
        except ValueError:
            messagebox.showerror(
                "Грешка", "Количеството трябва да е цяло число, а цената - число.")
            return
        if quantity < 0 or price < 0:
            messagebox.showerror("Грешка", "Стойностите трябва да са положителни.")
            return

        self.warehouse.add_product(Product(name, quantity, price, category))
        self.refresh_table(self.warehouse.products)
        for entry in self.entries.values():
            entry.delete(0, "end")


def main():
    warehouse = build_warehouse()
    app = WarehouseApp(warehouse)
    app.mainloop()


if __name__ == "__main__":
    main()
