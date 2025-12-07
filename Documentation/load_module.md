# 📑 Load Module Reference (src/load/)

---

## 1. Module Objective

The **Load Module** is the final step in the ETL pipeline, responsible for connecting to the MySQL data warehouse and reliably persisting the transformed financial data. The primary goal is to ensure data integrity and process high volumes efficiently.

## 2. Dependencies and Constraints

* 💾 **External Dependency:** MySQL Server.
* 🛠️ **Python Libraries:** `mysql.connector` (used for database connectivity).
* ⚙️ **Configuration:** Requires all database credentials (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) to be loaded from the `.env` file.
* 📦 **Input:** A **Polars LazyFrame** (`pl.LazyFrame`) from the Transformation module.

## 3. Core Logic Flow and Data Persistence

The loading process follows three distinct steps for both price data and fundamental data:

1.  **Data Preparation:** The input `pl.LazyFrame` is converted into a standard Python structure (**list of tuples**) using the `.collect().rows()` method, which is the required format for batch insertion.
2.  **SQL Execution:** A dedicated SQL query utilizing the **UPSERT** pattern is prepared.
3.  **Batch Insertion:** The `cursor.executemany()` function is used to send the entire list of records to the database in a single transaction.

## 4. Critical Design Decisions (Why the Code is Built This Way)

### A. Idempotency via UPSERT
* **Problem:** Re-running the ETL script would attempt to insert records that already exist (same `ticker_id` and `date_key`), resulting in a **Primary Key Violation** error and script failure.
* **Solution:** All insertion queries use the **UPSERT** pattern (`INSERT INTO ... ON DUPLICATE KEY UPDATE`).
* **Impact:** This ensures the pipeline is **idempotent**: any existing rows are updated with the newest data, and new rows are inserted, preventing failures upon re-execution.

### B. High-Performance Batch Insertion
* **Problem:** Using a simple Python `for` loop with `cursor.execute()` for each row creates significant network overhead, making the loading process slow.
* **Solution:** The **`cursor.executemany()`** method is utilized.
* **Impact:** This drastically reduces the number of round trips between the application and the database, making the data persistence process much faster and more efficient, particularly for large batches of historical data.

### C. Graceful Handling of Empty Data
* **Problem:** The Transformation module returns an empty `pl.LazyFrame` when an ETF (like QQQ) is encountered.
* **Solution:** The loading function is designed to handle this empty list.
* **Impact:** When `executemany()` receives an empty list of records, it performs a no-operation (no-op) and continues successfully, ensuring the script does not crash when skipping non-applicable tickers.

## 5. Data Outputs and Hand-off

The Load Module is the final output layer and does not hand off data to other Python modules.

| Action | Result | Database Impact |
| :--- | :--- | :--- |
| **Success** | Successful `cursor.executemany()` transaction. | Data is persisted or updated in `fact_historical_prices` and `fact_fundamental_indicators`. |
| **Failure** | Database connection error or SQL syntax error. | Transaction is rolled back to maintain integrity. |
