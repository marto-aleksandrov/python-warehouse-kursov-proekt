"""
models.py
---------
Дефинира класовете за системата за складова наличност.
"""


class Product:
    """Единична стока, съхранявана в склада."""

    def __init__(self, name, quantity, price, category="General"):
        # Конструктор (методът 'self', изискван от заданието).
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category

    def total_value(self):
        """Метод 1: обща стойност на стоката (количество * цена)."""
        return self.quantity * self.price

    def is_low_stock(self, threshold=5):
        """Метод 2: True, ако наличността е под или равна на прага."""
        return self.quantity <= threshold

    def restock(self, amount):
        """Метод 3: добавя бройки към текущото количество."""
        if amount <= 0:
            raise ValueError("Количеството за зареждане трябва да е положително.")
        self.quantity += amount
        return self.quantity

    def __repr__(self):
        return f"Product({self.name!r}, qty={self.quantity}, price={self.price:.2f} lv.)"


class Warehouse:
    """Склад, който съдържа множество обекти от тип Product."""

    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        """Добавя обект Product към склада."""
        self.products.append(product)

    def total_inventory_value(self):
        """Сумира стойността на всяка стока чрез цикъл."""
        total = 0
        for product in self.products:
            total += product.total_value()
        return total

    def find_low_stock(self, threshold=5):
        """Връща всички стоки, които трябва да се поръчат (цикъл + условие)."""
        low = []
        for product in self.products:
            if product.is_low_stock(threshold):
                low.append(product)
        return low

    def sort_by_quantity(self, descending=False):
        """Връща стоките, сортирани по количество."""
        return sorted(self.products, key=lambda p: p.quantity, reverse=descending)

    def sort_by_value(self, descending=True):
        """Връща стоките, сортирани по обща стойност."""
        return sorted(self.products, key=lambda p: p.total_value(), reverse=descending)
