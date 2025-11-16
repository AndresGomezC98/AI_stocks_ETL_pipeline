import requests
from config.settings import AV_API_KEY
from src.database.querys import get_last_price_ticket
from datetime import date,timedelta,datetime
frecuency="TIME_SERIES_WEEKLY_ADJUSTED"

def extract_prices_weekly(ticket:str):
        data=dict()
        last_price=get_last_price_ticket(ticket)
        URL= "https://www.alphavantage.co/query"
        URL_final= f"{URL}?function={frecuency}&symbol={ticket}&apikey={AV_API_KEY}"
        try:
                response = requests.get(URL_final)
        except:
                raise Exception(" la conexion fallo con la API")
        response.raise_for_status()
        initial_data=response.json()
        if last_price[0] is None:
                start_date=date(2020,1,1)
                
                
        else:
                start_date_i=last_price[0]
                start_date= start_date_i+timedelta(weeks=1)
                
        raw_data=initial_data["Weekly Adjusted Time Series"]
        for x,y in raw_data.items():
                        date_x =datetime.strptime(x,'%Y-%m-%d').date()
                        if date_x<start_date:
                                pass
                        else:
                                data[x]= y

        
        
        return data
        




 
'''print("--- INICIANDO PRUEBA DE EXTRACCIÓN AB#202 ---")
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
'''
  

