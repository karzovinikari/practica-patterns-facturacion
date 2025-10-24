# Estrategia de Impuestos

class TaxStrategy:
    """Interfaz para las estrategias de impuesto."""
    def calculate_tax(self, item):
        raise NotImplementedError("Debe ser implementado por la estrategia concreta.")
    
class IVA_Tax(TaxStrategy):
    """Impuesto: IVA (20%). Aplica a casi todo."""
    def calculate_tax(self, item):
        # No aplica a food_item
        if item.product_category == "food_item":
            return 0.0
        return item.price * 0.20

class ImportTax(TaxStrategy):
    """Impuesto: Derechos de importación (30%). Aplica a productos importados."""
    IMPORTED_CATEGORIES = ["imported_car", "cellphone", "computer"]
    
    def calculate_tax(self, item):
        # Aplica solo a categorías específicas
        if item.product_category in self.IMPORTED_CATEGORIES:
            return item.price * 0.30
        return 0.0