"""
models.py
---------
Дефинира класовете за системата за складова наличност.
Defines the data model for a simple warehouse / inventory system.
"""


class Product:
    """A single product stored in the warehouse."""

    def __init__(self, name, quantity, price, category="General"):
        # Constructor (the 'self' method required by the assignment).
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category

    def total_value(self):
        """Method 1: total stock value of this product (quantity * price)."""
        return self.quantity * self.price

    def is_low_stock(self, threshold=5):
        """Method 2: True if the stock is at or below the threshold."""
        return self.quantity <= threshold

    def restock(self, amount):
        """Method 3: add units to the current quantity."""
        if amount <= 0:
            raise ValueError("Restock amount must be positive.")
        self.quantity += amount
        return self.quantity

    def __repr__(self):
        return f"Product({self.name!r}, qty={self.quantity}, price={self.price:.2f} lv.)"


class Warehouse:
    """A warehouse that holds many Product objects."""

    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        """Add a Product object to the warehouse."""
        self.products.append(product)

    def total_inventory_value(self):
        """Sum the value of every product using a loop."""
        total = 0
        for product in self.products:
            total += product.total_value()
        return total

    def find_low_stock(self, threshold=5):
        """Return all products that need reordering (loop + conditional)."""
        low = []
        for product in self.products:
            if product.is_low_stock(threshold):
                low.append(product)
        return low

    def sort_by_quantity(self, descending=False):
        """Return products sorted by quantity."""
        return sorted(self.products, key=lambda p: p.quantity, reverse=descending)

    def sort_by_value(self, descending=True):
        """Return products sorted by total stock value."""
        return sorted(self.products, key=lambda p: p.total_value(), reverse=descending)
