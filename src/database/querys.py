# query para obtener la ultima fecha del ticket
query_date_max = '''
            SELECT MAX(date_key) 
            FROM fact_historical_prices
            WHERE ticker_id= %s;
            '''

# query to get last date of fundamentals LatestQuarter

query_date_max_fundamentals = '''
                                SELECT MAX(reporting_date)
                                FROM fact_fundamentals
                                WHERE ticker_id=%s;
                                '''

#QUERY TO LOAD PRICES HISTORY

query_to_load=('''
        INSERT INTO fact_historical_prices(ticker_id,date_key,open_price,high_price,low_price,close_price,volume) 
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        ''')
        
# QUERY TO LOAD FUNDAMENTALS

query_to_load_fundamentals=('''
                            INSERT INTO fact_fundamentals(ticker_id,reporting_date,market_capitalization,pe_ratio,peg_ratio,EPS,forwardPE)
                            VALUES(%s,%s,%s,%s,%s,%s,%s)
                            ''')
      

# QUERY TO GETTHE TICKER_ID REGARDING TICKER_SYMBOL OF DIM_TICKER
query_to_get_ticker_id ='''
                        SELECT ticker_id 
                        FROM dim_ticker
                        WHERE ticker_symbol = %s; 

                        '''



# QUERY TO INSERT INITIAL VALUES IN DIM_TICKER TABLE

query_to_insert =('''
                  INSERT INTO dim_ticker(ticker_symbol)
                  VALUES(%s);
                  ''')

