from src.database.connection import get_db_connection


def get_last_price_ticket(ticket:str):
    connection=None
    cur= None
    try:
        ticket_to_find=(ticket,)
        connection= get_db_connection()
        cur= connection.cursor()
        query = '''
            SELECT MAX(date_key) 
            FROM fact_historical_prices
            WHERE ticker_id= %s;
            '''
        cur.execute(query,ticket_to_find)
        data=cur.fetchone()
        return data
    finally:
        # 2. Gestión de Recursos: Cerrar SIEMPRE
        if cur:
            cur.close()
        if connection:
            connection.close()




