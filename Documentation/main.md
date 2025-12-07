# 📑 Orchestration Flow Reference (src/main.py)

---

## 1. Module Objective

The **Orchestration Module** serves as the primary entry point and traffic controller for the entire ETL pipeline. Its objective is to define the rigorous execution sequence (E -> T -> L), manage environment configuration loading, and implement high-level error handling and logging for the scheduled job.

## 2. Key Dependencies

This module imports necessary configuration utilities and the core business logic from its sibling packages:

* 📚 **Configuration:** `dotenv` (for loading `.env` variables).
* 📝 **Logging:** Python's built-in `logging` module.
* 📦 **Core Modules:** Imports functions from `src.extract`, `src.transform`, and `src.load`.

## 3. Core Logic Flow and Execution Sequence

The entire ETL process is managed by the single `run_etl()` function, which enforces a strict, linear flow:

1.  **Configuration Initialization:** Loads the database credentials and API key from the `.env` file.
2.  **Extraction Call:** Executes the extraction methods (`extract_prices()`, `extract_fundamentals()`) to fetch raw data.
3.  **Transformation Call:** Passes the extracted data to the transformation methods to clean, validate, and prepare the Polars LazyFrames.
4.  **Loading Call:** Passes the cleaned data to the load methods for persistence into the MySQL database using the UPSERT mechanism.

## 4. Critical Design Decisions (Why the Code is Built This Way)

### A. Global Error Catching (Top-Level Try/Except)
* **Problem:** An unhandled error in a sub-module (e.g., a connection loss, a schema mismatch) could crash the process, potentially resulting in an execution failure that goes unnoticed by the scheduler (GitHub Actions).
* **Solution:** The entire `run_etl()` sequence is wrapped in a top-level `try...except Exception as e:` block.
* **Impact:** This ensures that *all* unhandled errors are caught, logged (with a timestamp and full traceback), and gracefully terminated, providing immediate visibility into job failure rather than silent stagnation.

### B. Environment Isolation
* **Problem:** Database and API credentials must be secured and isolated from the codebase.
* **Solution:** The `load_dotenv()` function is called exclusively within the `main.py` entry point.
* **Impact:** This ensures that configuration variables are loaded only once and are available throughout the execution session, preventing potential security risks associated with hardcoding or passing credentials unnecessarily between modules.

### C. Logging Standardization
* **Problem:** Ensuring consistent and chronological reporting across all ETL steps.
* **Solution:** Standard Python `logging` configuration is initialized here, setting the format to include timestamps and severity levels.
* **Impact:** This centralizes all pipeline status updates, making the debugging of the entire weekly batch execution traceable.
