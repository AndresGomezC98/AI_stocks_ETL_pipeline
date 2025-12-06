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
