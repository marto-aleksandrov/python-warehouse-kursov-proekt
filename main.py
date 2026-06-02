"""
main.py
-------
Използва класовете Product и Warehouse, за да реши конкретна задача:
изграждане на склад, сортиране на стоките и откриване на ниски наличности.

Uses the Product and Warehouse classes to solve a concrete task:
build a warehouse, sort the stock, and detect low inventory.
"""

from tabulate import tabulate

from models import Product, Warehouse


def build_warehouse():
    """Create a warehouse and fill it with sample products using a loop."""
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


def print_table(products, title):
    """Print a list of products as a formatted table."""
    print(f"\n{title}")
    rows = []
    for p in products:
        status = "НИСКА" if p.is_low_stock() else "OK"
        rows.append([
            p.name, p.category, p.quantity,
            f"{p.price:.2f}", f"{p.total_value():.2f}", status,
        ])
    headers = ["Продукт", "Категория", "К-во", "Цена", "Стойност", "Наличност"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def main():
    warehouse = build_warehouse()

    # 1) All products sorted by quantity (ascending).
    print_table(warehouse.sort_by_quantity(),
                "Стоки, сортирани по количество (възходящо):")

    # 2) All products sorted by total value (descending).
    print_table(warehouse.sort_by_value(),
                "Стоки, сортирани по обща стойност (низходящо):")

    # 3) Find and report low-stock products (loop + conditional).
    low_stock = warehouse.find_low_stock(threshold=5)
    print("\nСтоки с ниска наличност (<= 5 бройки):")
    if low_stock:
        for product in low_stock:
            print(f"  - {product.name}: само {product.quantity} бр. -> трябва да се поръча")
    else:
        print("  Няма стоки с ниска наличност.")

    # 4) Restock the low-stock products and show the updated inventory.
    for product in low_stock:
        product.restock(20)
    print_table(warehouse.sort_by_quantity(),
                "\nОбновена наличност (след зареждане с по 20 бройки):")

    # 5) Total value of the whole warehouse.
    print(f"\nОбща стойност на склада: {warehouse.total_inventory_value():.2f} лв.")


if __name__ == "__main__":
    main()
