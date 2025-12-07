# 📑 Transformation Module Reference (src/transform/)

---

## 1. Module Objective

The **Transformation Module** is the core processing layer of the ETL pipeline. Its objective is to convert the raw, heterogeneous data structures received from the Extraction module (Python dictionaries, Pandas DataFrames, or `None` values) into a **clean, homogeneous, and schema-compliant Polars LazyFrame (`pl.LazyFrame`)**. This ensures high data quality and consistency before loading into the MySQL database.

## 2. Dependencies and Inputs

* 🛠️ **Dependencies:** The module relies heavily on the **Polars** library (`import polars as pl`) for high-performance columnar manipulation, and the built-in **`datetime`** module for date management.
* 📦 **Input Handling:** This module is designed to safely handle all potential inputs from the Extraction module:
    1. A standard **Python Dictionary** (for fundamentals).
    2. A **Pandas DataFrame** (for historical prices).
    3. The sentinel value **`None`** (indicating skipped or failed extraction).

## 3. Core Logic Flow and Data Quality Checks

### A. Data Type Casting and Formatting
The module ensures strict data type adherence:
* 🔢 Numerical fields are explicitly cast to `FLOAT64` or `INT64` to prevent silent data truncation.
* 📅 Date fields are converted from Python `date` objects to the standard **`YYYY-MM-DD` string format** before loading, satisfying the requirements of the MySQL database connector.

### B. Internal Data Quality Validation
The pipeline includes a **Fail-Fast** check to prevent loading obviously corrupt data:
* The transformation process includes a check (`is_violation`) for negative or zero values in key financial metrics (e.g., `pe_ratio`, `market_capitalization`, `EPS`).
* If a violation is detected, a `ValueError` is raised, halting the pipeline immediately to prevent the propagation of mathematically impossible data points.

## 4. Critical Design Decisions (Why the Code is Built This Way)

### A. Performance: Polars over Pandas
* **Decision:** Polars was chosen over Pandas as the transformation engine.
* **Justification:** Polars offers superior **memory efficiency** and **processing speed** when handling large, financial time-series data due to its columnar architecture and use of Rust for execution.

### B. Handling Missing Inputs (`None` Value)
* **Problem:** If the Extraction module encounters an ETF or an API error, it hands off the value **`None`**. Attempting to process this would crash the system.
* **Solution:** An explicit conditional check (`if data_fundamentals is None`) is performed. If true, the module immediately returns an **empty Polars LazyFrame** (`pl.DataFrame().lazy()`).
* **Impact:** This ensures the output type is always a `pl.LazyFrame`, which the subsequent **Load Module** can handle safely.

### C. SQL Constraint Satisfaction
* **Problem:** Numerical data fields often contain `None` or `NaN` from the API, violating MySQL's `NOT NULL` constraints during insertion.
* **Solution:** The transformation logic uses the Polars method **`.fill_null(0.0)`** for all relevant numeric columns.
* **Impact:** This guarantees that no `NULL` value enters the database, upholding the schema integrity defined in the `schema.sql`.

## 5. Data Outputs and Hand-off

The module guarantees a single output structure regardless of the input:

| Output Structure | Description | Hand-off Value |
| :--- | :--- | :--- |
| **`pl.LazyFrame`** | A high-performance, schema-compliant frame, ready for loading. | The fully cleaned and transformed data structure, ready for the final Load module. |
