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
    INSERT INTO fact_historical_prices(ticker_id,date_key,open_price,high_price,low_price,close_price,volume,Volatility) 
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        open_price = VALUES(open_price),
        high_price = VALUES(high_price),
        low_price = VALUES(low_price),
        close_price = VALUES(close_price),
        volume = VALUES(volume),
        Volatility = VALUES(Volatility)
        ''')
        
# QUERY TO LOAD FUNDAMENTALS

query_to_load_fundamentals=('''
                            INSERT INTO fact_fundamentals(ticker_id,reporting_date,market_capitalization,pe_ratio,peg_ratio,EPS,forwardPE)
                            VALUES(%s,%s,%s,%s,%s,%s,%s)
                            ON DUPLICATE KEY UPDATE
                                market_capitalization= VALUES(market_capitalization),
                                pe_ratio= VALUES(pe_ratio),
                                peg_ratio= VALUES(peg_ratio),
                                EPS= VALUES(EPS),
                                forwardPE= VALUES(forwardPE) 
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



query_ratio_pe_and_volatility = ('''
    SELECT 
        dim_ticker.ticker_symbol,
        fact_fundamental_indicators.pe_ratio,
        volatilidad_agregada.avg_volatility
    FROM dim_ticker
    
    -- 1. Unión con la tabla de Fundamentales (Datos Trimestrales)
    JOIN fact_fundamental_indicators 
        ON fact_fundamental_indicators.ticker_id = dim_ticker.ticker_id
        
    -- 2. Unión con la Volatilidad Agregada (Tabla Derivada)
    -- Esto convierte el dato semanal a un promedio por ticker para evitar la explosión de filas.
    JOIN (
        SELECT ticker_id, AVG(volatility) AS avg_volatility
        FROM fact_historical_prices
        GROUP BY ticker_id
    ) AS volatilidad_agregada 
        ON volatilidad_agregada.ticker_id = dim_ticker.ticker_id
        
    WHERE 
        -- Filtro 1: El P/E Ratio (Valor) debe ser inferior a 25
        fact_fundamental_indicators.pe_ratio < 25 
        
        -- Filtro 2: Excluimos el Benchmark de los resultados
        AND dim_ticker.ticker_symbol != 'QQQ'
        
        -- Filtro 3: Volatilidad (Riesgo) menor que el promedio del Benchmark (Subconsulta Escalar)
        AND volatilidad_agregada.avg_volatility < (
            -- Subconsulta para calcular el AVG(volatility) de QQQ
            SELECT AVG(fact_historical_prices.volatility)
            FROM fact_historical_prices
            JOIN dim_ticker 
                ON dim_ticker.ticker_id = fact_historical_prices.ticker_id
            WHERE dim_ticker.ticker_symbol = 'QQQ'
        );
''')





