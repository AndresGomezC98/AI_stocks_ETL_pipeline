# 📑 Database Schema Reference (database/schema.sql)

---

## 1. Schema Architecture: Optimized Star Schema

The project utilizes an **Optimized Star Schema** designed for time-series financial analytics and efficient querying by downstream AI models. This structure separates static, descriptive entities (Dimensions) from high-volume, transactional data (Facts).

## 2. Table Definitions and Integrity

### 2.1. Dimension Table: dim_ticker
This table serves as the primary lookup for all financial assets tracked by the pipeline.

| Column | Data Type | Constraint | Purpose |
| :--- | :--- | :--- | :--- |
| **ticker_id** | INT | PRIMARY KEY, AUTO_INCREMENT | Surrogate key for efficient joins. |
| **ticker_symbol** | VARCHAR(10) | UNIQUE, NOT NULL | The stock or ETF symbol (e.g., 'NVDA', 'QQQ'). |
| **is_benchmark** | BOOLEAN | NOT NULL | Flags if the ticker is an index or benchmark (e.g., QQQ). |

### 2.2. Fact Table: fact_historical_prices
This table stores daily adjusted price and volume information.

| Column | Data Type | Constraint | Purpose |
| :--- | :--- | :--- | :--- |
| **ticker_id** | INT | FOREIGN KEY (dim_ticker) | Links to the specific asset. |
| **date_key** | DATE | NOT NULL | The trading date. |
| **open_price** | DECIMAL(10, 2) | NOT NULL | Daily open price. |
| **close_price** | DECIMAL(10, 2) | NOT NULL | Daily adjusted close price (used for analysis). |
| **volume** | **BIGINT** | NOT NULL | Volume of shares traded. |
| **PRIMARY KEY** | | (ticker_id, date_key) | **Composite Key** for unique record identification. |

### 2.3. Fact Table: fact_fundamental_indicators
This table stores quarterly fundamental financial data.

| Column | Data Type | Constraint | Purpose |
| :--- | :--- | :--- | :--- |
| **ticker_id** | INT | FOREIGN KEY (dim_ticker) | Links to the specific asset. |
| **reporting_date** | DATE | NOT NULL | The date the quarter was reported. |
| **latest_quarter** | DATE | NOT NULL | Date of the most recent quarter (from API). |
| **pe_ratio** | DECIMAL(15, 6) | NOT NULL | Price-to-Earnings ratio. |
| **eps** | DECIMAL(15, 6) | NOT NULL | Earnings Per Share. |
| **PRIMARY KEY** | | (ticker_id, reporting_date) | **Composite Key** for unique record identification. |

## 3. Critical Design Decisions (Data Integrity)

### A. High Volume Support (BIGINT)
* **Problem:** Standard `INT` data types cannot hold the transaction volume of high-liquidity stocks (exceeding 2.1 billion). This led to `Out of range` errors during the ETL process.
* **Solution:** The `volume` column in `fact_historical_prices` is explicitly set to **`BIGINT`** (up to 9 quintillion), ensuring the database can successfully store large market movements without overflow.

### B. Idempotency and Uniqueness (Composite Keys)
* **Problem:** Running the pipeline multiple times results in duplicate attempts for the same ticker on the same day/quarter.
* **Solution:** Both fact tables use a **Composite Primary Key** combining `ticker_id` and the respective date field (`date_key` or `reporting_date`).
* **Impact:** This enforces the uniqueness of each record and is the enabling factor for the **UPSERT** logic used in the Load module.

### C. NOT NULL Constraints
* **Problem:** The Load module is configured to use the `ON DUPLICATE KEY UPDATE` statement, which requires all columns to be present. The API sometimes provides `NULL` values.
* **Solution:** All non-key fields are set to **`NOT NULL`**. The Transformation module handles the filling of `NULL` values with `0.0` or default values to satisfy this constraint prior to loading.
