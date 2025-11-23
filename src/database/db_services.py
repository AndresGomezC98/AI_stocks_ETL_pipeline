from database.connection import get_db_connection
from database.querys import query_date_max,query_date_max_fundamentals,query_to_get_ticker_id,query_to_insert
from config.AI_tickers import list_AI_tickers



# FUNCTION TO GET LAST PRICE TO USE IN EXTRACT_PRICES.PY
def get_last_price_ticket(ticket:str):
    connection=None
    cur= None
    try:
        ticket_to_find=(ticket,)
        connection= get_db_connection()
        cur= connection.cursor()
        query = query_date_max
        cur.execute(query,ticket_to_find)
        data=cur.fetchone() # fetchone return a tuple with two values the last date and empty value : (last_date," ")
        return data
    finally:
        # 2. Gestión de Recursos: Cerrar SIEMPRE
        if cur:
            cur.close()
        if connection:
            connection.close()


# FUNCTION TO GET LAST PRICE TO USE IN EXTRACT_FUNDAMENTALS.PY
def get_last_quarter_fundamentals(ticket:str):
    connection =None
    cur =None
    parameters =(ticket,)
    try:
        connection=get_db_connection()
        cur= connection.cursor()
        cur.execute(query_date_max_fundamentals,parameters)
        last_quarter=cur.fetchone()
        
        return last_quarter
    
    finally:
        if connection:
            connection.close()
        if cur:
            cur.close()


# FUNTCION TO GER DE TICKER_ID BASED ON TICKER_SYMBOL
def get_ticker_id (ticket:str):
    connection =None
    cur= None
    parameter=(ticket,)
    try:
        connection= get_db_connection()
        cur =connection.cursor()
        cur.execute(query_to_get_ticker_id,parameter)
        ticket_id_t=cur.fetchone()
        ticket_id =ticket_id_t[0]

        return  ticket_id
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()



# FUNCTION TO GET TICKER_ID OR INSERT_ TICKET LIKE STRING 

def get_or_create_ticker_id (ticker_symbol:str):
    connection=None
    cur= None
    try:
        connection=get_db_connection()
        cur=connection.cursor()
        parameter =(ticker_symbol,)
        cur.execute(query_to_get_ticker_id,parameter)
        ticket_id=cur.fetchone()
        if ticket_id is None:
            parameter_i=(ticker_symbol,)
            cur.execute(query_to_insert,parameter_i)
            connection.commit()
            cur.execute(query_to_get_ticker_id,parameter_i)
            ticket_insert=cur.fetchone()
            ticket_id_f=ticket_insert[0]
            
            return ticket_id_f
        else:
            return ticket_id[0]
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()



