import unittest
# Importar las clases y funciones necesarias
from models import Item, Invoice, InvoiceResult
from invoice_processor import InvoiceProcessor
from strategies.discount_strategy import StudentDiscount, BlackFridayDiscount, NoDiscount
from strategies.tax_strategy import IVA_Tax, ImportTax

class TestDiscountStrategies(unittest.TestCase):
    """Pruebas unitarias para las estrategias de descuento."""
    
    # Un subtotal fijo para probar los descuentos
    SUBTOTAL_BASE = 1000.0
    
    def test_no_discount(self):
        # Escenario: Descuento nulo
        discount = NoDiscount().calculate_discount(self.SUBTOTAL_BASE)
        self.assertEqual(discount, 0.0)

    def test_student_discount(self):
        # Escenario: Descuento del 10%
        expected_discount = self.SUBTOTAL_BASE * 0.10  # 100.0
        discount = StudentDiscount().calculate_discount(self.SUBTOTAL_BASE)
        self.assertEqual(discount, expected_discount)
        
    def test_black_friday_discount(self):
        # Escenario: Descuento del 30%
        expected_discount = self.SUBTOTAL_BASE * 0.30  # 300.0
        discount = BlackFridayDiscount().calculate_discount(self.SUBTOTAL_BASE)
        self.assertEqual(discount, expected_discount)

class TestTaxStrategies(unittest.TestCase):
    """Pruebas unitarias para las estrategias de impuestos."""
    
    def test_iva_tax(self):
        # 1. Aplica IVA a un 'computer' (100.0 * 0.20 = 20.0)
        item_c = Item(id=1, product_category="computer", price=100.0)
        self.assertEqual(IVA_Tax().calculate_tax(item_c), 20.0)
        
        # 2. No aplica IVA a 'food_item'
        item_f = Item(id=2, product_category="food_item", price=100.0)
        self.assertEqual(IVA_Tax().calculate_tax(item_f), 0.0)

    def test_import_tax(self):
        # 1. Aplica Impuesto de Importación a un 'imported_car' (500.0 * 0.30 = 150.0)
        item_ic = Item(id=3, product_category="imported_car", price=500.0)
        self.assertEqual(ImportTax().calculate_tax(item_ic), 150.0)
        
        # 2. No aplica a 'car' normal
        item_car = Item(id=4, product_category="car", price=500.0)
        self.assertEqual(ImportTax().calculate_tax(item_car), 0.0)

class TestInvoiceProcessor(unittest.TestCase):
    """Prueba de integración para la lógica central de la factura."""
    
    def setUp(self):
        # Configuración de datos de prueba (igual a tu invoice_1.json, pero con otro descuento)
        items_data = [
            # 1. Computer: 1000.0 -> Paga IVA (200) + Importación (300) = 500.0
            {"id": 1, "product_category": "computer", "price": 1000.0}, 
            # 2. Food_item: 50.0 -> Paga 0 impuestos
            {"id": 2, "product_category": "food_item", "price": 50.0},    
            # 3. Car: 5000.0 -> Paga solo IVA (1000)
            {"id": 3, "product_category": "car", "price": 5000.0}        
        ]
        
        self.items = [Item(**i) for i in items_data]
        self.processor = InvoiceProcessor()

    def test_full_invoice_student_discount(self):
        """Prueba un escenario completo con Descuento de Estudiante (10%)."""
        
        invoice = Invoice(items=self.items, discount_key="student")
        result = self.processor.process(invoice)

        # Cálculos esperados
        expected_subtotal = 6050.0
        expected_discount = expected_subtotal * 0.10  # 605.0
        
        # Impuestos totales: 
        # Item 1 (computer): 200.0 (IVA) + 300.0 (Imp.) = 500.0
        # Item 2 (food_item): 0.0
        # Item 3 (car): 1000.0 (IVA) + 0.0 (Imp.) = 1000.0
        expected_total_taxes = 500.0 + 0.0 + 1000.0  # 1500.0
        
        # Total Final = (Subtotal - Descuento) + Impuestos
        expected_final_total = (6050.0 - 605.0) + 1500.0 # 5445.0 + 1500.0 = 6945.0

        # Verificaciones
        self.assertEqual(result.subtotal, expected_subtotal)
        self.assertAlmostEqual(result.applied_discount, expected_discount, places=2)
        self.assertAlmostEqual(result.total_taxes, expected_total_taxes, places=2)
        self.assertAlmostEqual(result.final_total, expected_final_total, places=2)

    def test_full_invoice_black_friday_discount(self):
        """Prueba un escenario completo con Descuento Black Friday (30%).
           Items: [computer, food_item, imported_car]
        """
        # Datos del caso simulado anteriormente
        items_data = [
            {"id": 1, "product_category": "computer", "price": 1000.0},
            {"id": 2, "product_category": "food_item", "price": 50.0},
            {"id": 3, "product_category": "imported_car", "price": 20000.0}
        ]
        items = [Item(**i) for i in items_data]
        
        invoice = Invoice(items=items, discount_key="black_friday")
        result = self.processor.process(invoice)

        # Cálculos esperados (revisados en la simulación anterior)
        expected_subtotal = 21050.0
        expected_discount = 21050.0 * 0.30  # 6315.0
        
        # Impuestos (computer: 500.0, food_item: 0.0, imported_car: 10000.0)
        expected_total_taxes = 10500.0 
        
        # Total Final = (21050.0 - 6315.0) + 10500.0
        expected_final_total = 25235.0

        self.assertEqual(result.subtotal, expected_subtotal)
        self.assertAlmostEqual(result.applied_discount, expected_discount, places=2)
        self.assertAlmostEqual(result.total_taxes, expected_total_taxes, places=2)
        self.assertAlmostEqual(result.final_total, expected_final_total, places=2)

    def test_edge_cases_and_tax_matrix(self):
        """Prueba casos con subtotal cero y matriz completa de impuestos."""

        # Matriz de Impuestos (Precio base = 100.0)
        items_matrix_data = [
            # 1. Paga IVA y Importación (computer)
            {"id": 10, "product_category": "computer", "price": 100.0},     # Tax: 20 + 30 = 50.0
            # 2. Paga solo IVA (car)
            {"id": 11, "product_category": "car", "price": 100.0},          # Tax: 20 + 0 = 20.0
            # 3. Paga solo Importación (Ninguno existe con estas reglas, pero si existiera)
            # Aquí usamos 'cellphone' que está categorizado como importado y no es food_item
            {"id": 12, "product_category": "cellphone", "price": 100.0},    # Tax: 20 + 30 = 50.0. No podemos aislar Importación/IVA con estas reglas.
            # 4. No paga impuestos (food_item)
            {"id": 13, "product_category": "food_item", "price": 100.0},    # Tax: 0 + 0 = 0.0
            # 5. Caso Límite: Subtotal CERO
            {"id": 14, "product_category": "car", "price": 0.0}              # Tax: 0.0
        ]
        
        items_matrix = [Item(**i) for i in items_matrix_data]
        
        # Usar la estrategia de descuento por defecto (NoDiscount)
        invoice = Invoice(items=items_matrix, discount_key="") 
        result = self.processor.process(invoice)

        # Cálculos esperados para la matriz
        expected_subtotal = 400.0
        expected_discount = 0.0
        
        # Total Impuestos: 50.0 (computer) + 20.0 (car) + 50.0 (cellphone) + 0.0 (food) + 0.0 (cero)
        expected_total_taxes = 120.0
        
        # Total Final = 400.0 - 0.0 + 120.0
        expected_final_total = 520.0

        self.assertEqual(result.subtotal, expected_subtotal)
        self.assertEqual(result.applied_discount, expected_discount)
        self.assertEqual(result.total_taxes, expected_total_taxes)
        self.assertEqual(result.final_total, expected_final_total)

if __name__ == '__main__':
    unittest.main()