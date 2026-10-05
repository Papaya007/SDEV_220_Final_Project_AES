class Employee:
    def __init__(self, employee_id, name):
        self.employee_id = employee_id
        self.name = name


class ClothingItem:
    def __init__(self, item_name, size, price):
        self.item_name = item_name
        self.size = size
        self.price = price


class Order:
    def __init__(self, employee):
        self.employee = employee
        self.items = []

    def add_item(self, clothing_item, quantity):
        self.items.append({
            "item": clothing_item,
            "quantity": quantity
        })

    def display_summary(self):
        print("\nAES Indiana FR Clothing Order")
        print("--------------------------------")
        print("Employee:", self.employee.name)
        print("Employee ID:", self.employee.employee_id)
        print("\nItems Ordered:")

        for order_item in self.items:
            item = order_item["item"]
            quantity = order_item["quantity"]

            print(
                item.item_name,
                "- Size:", item.size,
                "- Quantity:", quantity
            )


# Test data
employee = Employee("12345", "Julian Paiz")

shirt = ClothingItem("FR Long Sleeve Shirt", "M", 65.00)
pants = ClothingItem("FR Work Pants", "30x30", 85.00)

order = Order(employee)

order.add_item(shirt, 2)
order.add_item(pants, 1)

order.display_summary()
