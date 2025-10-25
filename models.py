# models.py (Ajustado para FastAPI/Pydantic)
from pydantic import BaseModel, Field
from typing import List

# Item (Un producto en la factura)
class Item(BaseModel): # <-- Herencia de BaseModel para validación
    id: int
    product_category: str
    price: float

# Factura (La entrada del sistema)
class Invoice(BaseModel): # <-- Herencia de BaseModel
    items: List[Item]
    discount_key: str = Field(alias="discount")

# Salida (El resultado del cálculo, adaptado para ser un diccionario en la API)
class InvoiceResult(BaseModel):
    subtotal: float = 0.0
    applied_discount: float = 0.0
    item_taxes: List[dict] = Field(default_factory=list) # Usar default_factory para listas
    total_taxes: float = 0.0
    final_total: float = 0.0

# Si solo usas las clases puras en la lógica del procesador, asegúrate de
# mantener la versión de __init__ en models.py, o manejar la conversión si heredas de BaseModel.
# Por simplicidad, asumiremos que heredar de BaseModel no rompe el resto de tu código.