# Estrategia de Descuento

class DiscountStrategy:
    """Interfaz para las estrategias de descuento."""
    def calculate_discount(self, subtotal):
        raise NotImplementedError("Debe ser implementado por la estrategia concreta.")
    
class NoDiscount(DiscountStrategy):
    """Estrategia: Sin descuento."""
    def calculate_discount(self, subtotal):
        return 0.0

class StudentDiscount(DiscountStrategy):
    """Estrategia: Descuento de estudiante (10%)."""
    def calculate_discount(self, subtotal):
        return subtotal * 0.10

class BlackFridayDiscount(DiscountStrategy):
    """Estrategia: Descuento de Black Friday (30%)."""
    def calculate_discount(self, subtotal):
        return subtotal * 0.30

DISCOUNT_STRATEGIES = {
    "": NoDiscount(), # Para el campo vacío
    "student": StudentDiscount(),
    "black_friday": BlackFridayDiscount()
}

def get_discount_strategy(discount_key):
    """Selecciona la estrategia de descuento según la clave."""
    return DISCOUNT_STRATEGIES.get(discount_key, NoDiscount())