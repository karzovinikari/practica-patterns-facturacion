# Item (Un producto en la factura)
class Item:
    def __init__(self, id, product_category, price):
        self.id = id
        self.product_category = product_category
        self.price = price

# Factura (La entrada del sistema)
class Invoice:
    def __init__(self, items, discount_key):
        self.items = items
        self.discount_key = discount_key

# Salida (El resultado del cálculo)
class InvoiceResult:
    def __init__(self):
        self.subtotal = 0.0
        self.applied_discount = 0.0
        self.item_taxes = []
        self.total_taxes = 0.0
        self.final_total = 0.0