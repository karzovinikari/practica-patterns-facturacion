import json
import os
from models import Item, Invoice, InvoiceResult 
from invoice_processor import InvoiceProcessor 

INPUT_DIR = "input_files"
OUTPUT_DIR = "output_files"

def load_invoice_data(file_path):
    """Lee el contenido JSON del archivo y lo convierte al objeto Invoice."""
    
    # Manejo de archivos (Lectura)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mapeo a objetos de Modelos
    items = [Item(**i) for i in data["items"]]
    invoice = Invoice(items=items, discount_key=data.get("discount", ""))
    
    return invoice

def save_invoice_result(result: InvoiceResult, original_filename: str):
    """Convierte el resultado del objeto InvoiceResult a JSON y lo guarda en el disco."""
    
    # 1. Asegurar que la carpeta de salida exista
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 2. Determinar la ruta y el nombre del archivo de salida
    base_name = os.path.splitext(original_filename)[0] 
    output_filename = f"{base_name}_output.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # 3. Preparar el resultado para JSON (Conversión de objeto a diccionario)
    # Nota: Se asume que InvoiceResult tiene los atributos 'subtotal', etc.
    output_dict = {
        "subtotal": result.subtotal,
        "applied_discount": result.applied_discount,
        "item_taxes": result.item_taxes,
        "total_taxes": result.total_taxes,
        "final_total": result.final_total
    }
    
    # 4. Manejo de archivos (Escritura)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_dict, f, indent=4)
    
    print(f"✅ Factura procesada y guardada en: {output_path}")


def main():
    # El Contexto del patrón Strategy
    processor = InvoiceProcessor()
    
    # Lógica de orquestación (Flujo principal)
    
    # 1. Recorrer todos los archivos en la carpeta de entrada
    if not os.path.exists(INPUT_DIR):
        print(f"Error: La carpeta '{INPUT_DIR}' no existe. Por favor, créala y añade archivos JSON.")
        return

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(INPUT_DIR, filename)
            
            try:
                print(f"\n⚙️ Iniciando procesamiento de: {filename}")
                
                # 2. Cargar datos usando la función local
                invoice = load_invoice_data(file_path)
                
                # 3. Procesar la factura (Aquí se utiliza el patrón Strategy)
                result = processor.process(invoice)
                
                # 4. Guardar el resultado usando la función local
                save_invoice_result(result, filename)
                
            except Exception as e:
                print(f"❌ Error crítico al procesar {filename}. Detalle: {e}")


if __name__ == "__main__":
    main()