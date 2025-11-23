# query para obtener la ultima fecha del ticket
query_date_max = '''
            SELECT MAX(date_key) 
            FROM fact_historical_prices
            WHERE ticker_id= %s;
            '''


#QUERY PARA CARGAR LOS DATOS Y EXPORTARLA:

query_to_load=('''
        INSERT INTO fact_historical_prices(ticker_id,date_key,open_price,high_price,low_price,close_price,volume) 
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        ''')
        
      
       



