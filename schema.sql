# -----------------------------------------------------
# DISEÑO FINAL DEL ESQUEMA DE ESTRELLA (STAR SCHEMA)
# Tarea AB#102: dim_ticker, fact_historical_prices, fact_fundamentals
# -----------------------------------------------------

-- 1. TABLA DE DIMENSIÓN: dim_ticker (Clave Simple: Subrogada)
CREATE TABLE IF NOT EXISTS dim_ticker (
  ticker_id INT NOT NULL AUTO_INCREMENT,
  ticker_symbol VARCHAR(10) NOT NULL UNIQUE,
  is_benchmark BOOLEAN NOT NULL DEFAULT FALSE,
  
  PRIMARY KEY (ticker_id)
) ENGINE = InnoDB;

-- 2. TABLA DE HECHOS: fact_historical_prices (Clave Compuesta: ticker_id + date_key)
CREATE TABLE IF NOT EXISTS fact_historical_prices (
  ticker_id INT NOT NULL,
  date_key DATE NOT NULL,
  open_price FLOAT NOT NULL,
  high_price FLOAT NOT NULL,
  low_price FLOAT NOT NULL,
  close_price FLOAT NOT NULL,
  volume INT NOT NULL,
  volatility FLOAT,
  
  -- CLAVE COMPUESTA: Combina el "qué" y el "cuándo" para la unicidad
  PRIMARY KEY (ticker_id, date_key),
  
  -- CLAVE FORÁNEA: Define la relación con la dimensión
  FOREIGN KEY (ticker_id) REFERENCES dim_ticker (ticker_id)
) ENGINE = InnoDB;

-- 3. TABLA DE HECHOS: fact_fundamentals (Clave Compuesta: ticker_id + reporting_date)
CREATE TABLE IF NOT EXISTS fact_fundamentals (
  ticker_id INT NOT NULL,
  reporting_date DATE NOT NULL,
  market_capitalization BIGINT NOT NULL,
  pe_ratio FLOAT NOT NULL,
  peg_ratio FLOAT NOT NULL,
  EPS FLOAT NOT NULL,
  forwardPE FLOAT NOT NULL,
  
  -- CLAVE COMPUESTA: La firma única del reporte trimestral
  PRIMARY KEY (ticker_id, reporting_date),
  
  -- CLAVE FORÁNEA: Define la relación con la dimensión
  FOREIGN KEY (ticker_id) REFERENCES dim_ticker (ticker_id)
) ENGINE = InnoDB;


	
