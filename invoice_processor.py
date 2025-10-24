from models import Item, Invoice, InvoiceResult
from strategies.discount_strategy import get_discount_strategy, DiscountStrategy
from strategies.tax_strategy import IVA_Tax, ImportTax, TaxStrategy

class InvoiceProcessor:
    
    def process(self, invoice: Invoice) -> InvoiceResult:
        result = InvoiceResult()
        
        # 1. Calcular Subtotal
        # Subtotal es la suma de los precios de todos los items
        subtotal = sum(item.price for item in invoice.items)
        result.subtotal = subtotal
        
        # 2. Aplicar Estrategia de Descuento
        # La clase solo pide la estrategia, no sabe cómo calcula
        discount_strategy = get_discount_strategy(invoice.discount_key)
        applied_discount = discount_strategy.calculate_discount(subtotal)
        result.applied_discount = applied_discount

        # Base para Impuestos (Subtotal - Descuento? No, según enunciado, impuestos se aplican item por item)
        # Vamos a seguir la lógica de que los impuestos se aplican sobre el precio del ítem.

        total_taxes = 0.0
        
        # 3. Aplicar Estrategia de Impuestos (Múltiples)
        # Una lista de todas las estrategias de impuestos a considerar
        tax_strategies = [IVA_Tax(), ImportTax()]
        
        for item in invoice.items:
            item_total_tax = 0.0
            
            # Recorrer TODAS las estrategias de impuestos para CADA ítem
            for tax_strategy in tax_strategies:
                # Cada estrategia decide si aplica y cuánto
                item_total_tax += tax_strategy.calculate_tax(item)
            
            # Acumular resultados
            result.item_taxes.append({"id": item.id, "tax": item_total_tax})
            total_taxes += item_total_tax
            
        result.total_taxes = total_taxes
        
        # 4. Calcular Total Final
        # Total Final = (Subtotal - Descuento) + Total Impuestos
        result.final_total = (subtotal - applied_discount) + total_taxes
        
        return result