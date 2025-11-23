#DRIVER OF ETL PROCESS
from config.AI_tickers import list_AI_tickers
from database.connection import get_db_connection
from src.extract.extract_prices import extract_prices_weekly
from src.extract.extract_fundamentals import extract_fundamentals
from src.transform.transform_prices import transform_plain_dict_price
from src.transform.transform_fundamentals import transform_fundamentals_plain
from src.load.load_prices import load_historical_prices
from src.load.load_fundamentals import load_fundamental_indicators
from database.querys import query_to_get_ticker_id
from database.db_services import get_or_create_ticker_id

def main():
    tickets =list_AI_tickers
    
    
        
    for x in tickets:
        
        
        # main for ETL to prices
        ticker_id=get_or_create_ticker_id(x)
        extract=extract_prices_weekly(x)
        transform = transform_plain_dict_price(ticker_id,extract)
        loading=load_historical_prices(transform)

        # main for ETL to fundamentals

        extract_f=extract_fundamentals(x)
        transform_f=transform_fundamentals_plain(ticker_id,extract_f)
        loading_f=load_fundamental_indicators(transform_f)

        
            

 

if __name__=="__main__":
    main()