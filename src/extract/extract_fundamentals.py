import requests
from config.settings import AV_API_KEY
from datetime import date,timedelta,datetime
from database.db_services import get_last_quarter_fundamentals


def extract_fundamentals(ticket:str):
    data_final=dict()
    date= get_last_quarter_fundamentals(ticket)
    functionF="OVERVIEW"
    URL="https://www.alphavantage.co/query"
    URL_API=f"{URL}?function={functionF}&symbol={ticket}&apikey={AV_API_KEY}"
    try:
        response=requests.get(URL_API)
    except:
        raise Exception("connection fail, check and try again")

    response.raise_for_status()
    data_fundamentals=response.json()

    if date[0] is None:
        start_date_quearter=date(2020,1,1)
    else:
        start_date_quearter=date[0]

    data_raw=data_fundamentals["LatestQuarter"]
    date_data_raw= datetime.strptime(data_raw,'%Y-%m-%d').date()
    if date_data_raw <= start_date_quearter:
        return data_final
    else:
        data_final=data_fundamentals
        return data_fundamentals
    







 
        














'''
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
        '''