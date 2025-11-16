import requests
from config.settings import AV_API_KEY
functionF="OVERVIEW"
def extract_fundamentals(ticket):
    URL="https://www.alphavantage.co/query"
    URL_API=f"{URL}?function={functionF}&symbol={ticket}&apikey={AV_API_KEY}"
    try:
        response=requests.get(URL_API)
    except:
        raise Exception("connection fail, check and try again")

    response.raise_for_status()
    data_fundamentals=response.json()
    return data_fundamentals


print("--- INICIANDO PRUEBA DE EXTRACCIÓN FUNDAMENTALES AB#203 ---")
TICKET_DE_PRUEBA = "MSFT" # Usamos Microsoft como prueba
    
try:
        datos_extraidos = extract_fundamentals(TICKET_DE_PRUEBA)
        print(f"✅ Extracción Exitosa para {TICKET_DE_PRUEBA}.")
        print("Estructura de la respuesta (keys principales):")
        
        # Esto nos mostrará las secciones principales del JSON de Alpha Vantage
        print(datos_extraidos.keys())
        
except Exception as e:
        print(f"❌ ¡FALLO EN LA EXTRACCIÓN! Revisa tu clave API o la conexión.")
        print(f"Detalles del error: {e}")