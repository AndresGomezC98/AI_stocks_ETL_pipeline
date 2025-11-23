#DRIVER OF ETL PROCESS
from config.AI_tickers import list_AI_tickers
from database.connection import get_db_connection
from src.extract.extract_prices import extract_prices_weekly,get_last_price_ticket
from src.transform.transform_prices import transform_plain_dict_price
from src.load.load_prices import load_historical_prices

def main():
    tickets =list_AI_tickers
    try:
        connection_prices = get_db_connection()

        for x in tickets:
        

            extract=extract_prices_weekly(x)
            transform = transform_plain_dict_price(x,extract)
            loading=load_historical_prices(connection_prices,transform)
    finally:
        if connection_prices:
            connection_prices.close()
            

    pass

if __name__=="__main__":
    main()