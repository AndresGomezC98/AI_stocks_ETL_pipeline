## JOURNAL OF PROJECT, LEARNINGS AND KEY CONCEPTS FOR BETTER ORGANIZATION

**09/11/25**Today I advanced with some issues, firts I finished file README.md with a structure more professional and clear for future collaboratos or hiring professional teams, next I sign in to Azure in order to configure Azure boards this is because, I want to implement methodologies agiles like scrum to future projects in company or indidivual projects so I defined main PBI('User history') and the tasks for each one of sprints but I only configurate the first sprint, in addition using git for VCS I connect my local repository with repository of Azure to follow updates in both locations.

### DEVELOP BRANCH 11/09/25
Porject starts with developing of file settings and in this file I can learn some new tips regarding best practices and useful libraries like OS and some modules of itself, these are the main key concepts and learnings today:
1. OS library allow me to do some commands in python similar that in bash like talk with system operative
2. library python-dotenv: this is a great tool for best secure practices because I learn that i need to have first a file with my secure information regarding passwords for API, database among others like my secure box, this is when I pull my project in cloud with git or other tool i don't want this information will be share with others so i learn this useful tips of code:
>> 2.1: from dotenv import load_dotenv import os to have the library to work
        load_dotenv(): this automatically read my .env file and save the key-value in a file document call os.environ 
        next I used the method os.getenv this allow me to get the information of os.environ and manage as well exceptions
        and errors. I learned this OS.getenv(' value for search', None) None is a value for default just in case 
        if we don't find a key value it isn't a string.

3. I created a list with main tickers for my project this tickers are main for AI field and at last of list we are use a one stock that doesn't belong to AI field but is a great and solid company in market this is to compare the bubble of AI. 

### CONTINUE DEVELOP PROJECT 11/15/2025

📝 AB#202: Price Extraction Logic & Project ArchitectureThis task focused on creating a robust, modular function (extract_prices_weekly) to fetch historical data from Alpha Vantage, integrating essential professional Python architecture and testing practices.

🐍 Core Function Logic & Error HandlingComponentAction TakenKey LearningModularityDefined extract_prices_weekly(ticket: str).

The function handles only one task (fetch one ticker) to be easily reusable and testable.

API RequestBuilt URL using f-strings and performed the call with requests.get().F-strings are the standard way to inject variables cleanly into URLs.

Connection SafetyUsed a try...except block around the API call.This captures low-level network failures (e.g., timeout or no internet connection).API Error CheckImplemented response.raise_for_status().This is the professional standard for handling HTTP errors (like 403 or 404) returned by the server, ensuring we only proceed if the status is successful (2xx).

Return ValueConverted the response with data = response.json() and used return data.Confirmed that requests.json() converts the API string directly into a usable Python dictionary (dict).

🏛️ Architectural Learnings & TestingConceptExplanationPractical FixPackage RecognitionPython needs __init__.py files (the "package passport" 🛂) inside folders (config/, src/) to recognize them as importable modules. Without them, imports fail.Must be maintained in all source directories (config/, src/, src/extract/).

Import ErrorThe ModuleNotFoundError occurs when Python runs a deep file (extract.py) and cannot look "up" to find sibling packages (like config).The file structure was correct, but the execution was wrong.Professional ExecutionThe command python -m package.module (e.g., python -m src.extract.extract) forces Python to start searching for packages from the project root, solving the import issue.Use python -m for all package executions from the root.

Unit TestingThe if __name__ == "__main__": block is used to create temporary, isolated tests.It allows us to confirm the function works before integrating it into main.py.




📝 Project Journal Entry: Tasks AB#202 & AB#101 ReviewI. Task AB#202:
 Price Extraction (Refactoring and Testing)Objective: 

Create a modular and robust function to extract weekly adjusted stock prices from the Alpha Vantage API.

Concept ImplementationKey LearningAPI CallFunction extract_prices_weekly(ticker: str) was finalized, correctly integrating the AV_API_KEY from config.settings.Modularity is essential. 

The function takes only the ticker as input, making it easily reusable.URL SyntaxUsed f-strings to construct the API URL with the correct parameters (function, symbol, apikey).f-strings (f"...") provide the cleanest and most readable way to inject variables into strings.

HTTP Error HandlingUsed response.raise_for_status().This is the professional standard for immediate error detection. It automatically raises an exception if the API returns a non-200 status code (e.g., 404, 500), stopping the process and preventing bad data.

Success ConfirmationThe function was successfully tested and returned dict_keys(['Meta Data', 'Weekly Adjusted Time Series']), confirming connection and data format.

II. Core Python Architecture & Execution
This section addresses the crucial ModuleNotFoundError encountered during testing.

Concept Explanation Why It’s Important The __init__.py File This file (which can be empty) acts as a "package passport" 🛂. Python only recognizes a directory (config/, src/database/) as an importable package if this file is present.Without it, Python cannot navigate your project structure to find modules like settings.py or connection.py when executing from a nested folder.

The python -m Command Standard execution (python src/file.py) only knows its current location. python -m src.module.file (using dots instead of slashes) forces Python to treat the project's root folder as the starting point.This correctly resolves all absolute imports (e.g., from config.settings import...), allowing the program to find sibling packages from anywhere.
III. Advanced Patterns: Security and Resource Management
In Task AB#101 (Idempotency), we implemented patterns crucial for secure and reliable database interaction.
1. The try...finally Block (Resource Safety) 🔒Problem: If an error occurs (e.g., a network crash) after opening a database connection, the connection remains open, leading to resource leaks on the database server.Solution: The finally block contains code that executes guaranteed, regardless of whether the try block succeeded or failed.Implementation: We placed the essential cleanup (cursor.close() and connection.close()) inside finally to ensure resources are released after every use.

2. Scope and Safe Closing (connection = None)We initialized connection = None and cursor = None before the try block.Why? If the try block fails before creating the connection object, the finally block still needs to reference those variables. By initializing them to None, we safely use the conditional check: if connection: connection.close(). This prevents a crash if the resource was never successfully opened.

3. SQL Parameterization (Security) 🛡️Problem: Directly injecting a variable (like ticker) into a SQL string (WHERE ticker_id = '{ticker}') creates a security vulnerability called SQL Injection.Solution: We used the standard SQL parameter marker %s in the query string and passed the variable separately as a tuple ((ticket,)) in the cursor.execute() method.Key Learning: This separates the code from the data, ensuring the variable is treated purely as a value, making the query safe and functional.

### 🗓️ Date: [23/11/2025]
### 🎯 Topic: Finalizing ETL Pipeline & Implementing Robust Load (L) Layer

Today's focus was on connecting all ETL pieces (E, T, L) into a unified and transactional pipeline, solving the critical dependency on the `dim_ticker` dimension table.

#### 1. Dimension Management: The UPSERT Pattern 🔑

The core learning was how to **infer and manage dimension keys** within the ETL process, specifically for the `dim_ticker` table.

* **Problem:** The Transformation (T) layer requires an integer `ticker_id`, but the Extraction (E) layer only has the string symbol (`ticker`).
* **Solution (UPSERT Logic):** We implemented `get_or_create_ticker_id` in `db_services.py` using a simple application-level pattern:
    1.  `SELECT`: Attempt to retrieve the `ticker_id` using the symbol.
    2.  `IF None`: If the result is `None` (new ticker), execute `INSERT INTO dim_ticker(ticker_symbol) VALUES (%s);`.
    3.  `COMMIT` & `SELECT Again`: We execute `connection.commit()` to confirm the new row and immediately perform the `SELECT` again to retrieve the newly generated `AUTO_INCREMENT` ID.

#### 2. Transactional Robustness and Connection Handling 🔗

We refactored the Load (L) layer for maximum robustness and modularity.

* **Internal vs. External Connection:**
    * **External (Initial Design):** Passing the `connection` object to the load function (e.g., `load_data(conn, data)`). This is efficient for massive bulk operations but makes the orchestrator (`main.py`) responsible for opening and safely closing a single connection.
    * **Internal (Final Design):** The load function calls `get_db_connection()` internally. This simplifies the orchestrator (no need to pass the connection) and ensures **each load operation safely opens and closes its own resources** (cursor and connection).
* **Transactional Integrity (`try/except/finally`):** This structure is essential for database operations:
    * `try`: Execute `cur.execute(...)` and **`connection.commit()`** (success).
    * `except Exception as e`: If any error occurs, execute **`connection.rollback()`** to ensure no partial transaction remains in the DB, and then **`raise e`** to halt the pipeline and notify the orchestrator.
    * `finally`: **Always** ensures the `cur.close()` and `connection.close()` methods are called, regardless of success or failure.

#### 3. Handling Cursor Output 🧠

A crucial distinction when interacting with the cursor (`cur`):

* `cur.execute(SELECT ...)`: Returns the **number of rows** affected or selected (usually 0 or 1).
* `cur.fetchone()`: Must be called *after* `cur.execute` for a `SELECT` query to retrieve the actual data (a tuple) or `None` if no row was found.

#### 4. Polars LazyFrame and Type Coercion

* Confirmed that Polars `LazyFrame` successfully handles the explicit schema definition (e.g., `pl.Int64`, `pl.Date`) and strict data quality validation (e.g., `pl.col("pe_ratio") < 0`) before the data is materialized and loaded, ensuring strong **Data Quality**.
