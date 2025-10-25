from fastapi import FastAPI
from models import Invoice, InvoiceResult
from invoice_processor import InvoiceProcessor

# El Contexto y el corazón de tu lógica de negocio
processor = InvoiceProcessor()

# 1. Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Facturación Strategy API",
    description="API que calcula descuentos e impuestos usando el patrón Strategy."
)

# 2. Definición del Endpoint POST /calculate
# Recibe un objeto Invoice (validado por Pydantic) y devuelve un InvoiceResult.
@app.post("/calculate", response_model=InvoiceResult, status_code=200)
def calculate_invoice(invoice: Invoice):
    """
    Procesa una factura aplicando la estrategia de descuento y los impuestos por ítem.
    """
    
    # El modelo de entrada (Invoice) ya contiene los objetos Item validados.
    
    # 3. Delegación a la lógica de negocio (InvoiceProcessor)
    # Aquí se utiliza todo el patrón Strategy
    result_object = processor.process(invoice)
    
    # 4. Devolver el resultado
    # FastAPI/Pydantic automáticamente convierte el objeto 'result_object' a JSON 
    # en el formato de InvoiceResult (que definiste en models.py)
    return result_object

# Ejemplo de endpoint GET simple para verificar que la API está viva
@app.get("/")
async def root():
    return {"message": "API de Facturación en funcionamiento. Use /calculate (POST) para procesar una factura."}