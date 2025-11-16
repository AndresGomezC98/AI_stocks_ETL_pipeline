import requests
from config.settings import AV_API_KEY 
frecuency="TIME_SERIES_WEEKLY_ADJUSTED"

def extract_prices_weekly(ticket:str):
   URL= "https://www.alphavantage.co/query"
   URL_final= f"{URL}?function={frecuency}&symbol={ticket}&apikey={AV_API_KEY}"
   try:
    response = requests.get(URL_final)
   except:
     raise Exception(" la conexion fallo con la API")
   
   response.raise_for_status()

   data=response.json()
   return data 
 
print("--- INICIANDO PRUEBA DE EXTRACCIÓN AB#202 ---")
TICKET_DE_PRUEBA = "MSFT" # Usamos Microsoft como prueba
    
try:
        datos_extraidos = extract_prices_weekly(TICKET_DE_PRUEBA)
        print(f"✅ Extracción Exitosa para {TICKET_DE_PRUEBA}.")
        print("Estructura de la respuesta (keys principales):")
        
        # Esto nos mostrará las secciones principales del JSON de Alpha Vantage
        print(datos_extraidos.keys())
        
except Exception as e:
        print(f"❌ ¡FALLO EN LA EXTRACCIÓN! Revisa tu clave API o la conexión.")
        print(f"Detalles del error: {e}")

  

