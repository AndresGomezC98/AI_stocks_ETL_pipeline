\# 📑 Extraction Module Reference (src/extract/)



\## 1. Module ObjectiveThe objective of this module is the secure and rate-controlled extraction of raw financial data from the Alpha Vantage API. It serves as the data gateway for the pipeline, handling two main types of data:

💰 Historical Price Data: Time-series data for the fact\_historical\_prices table.

📊 Corporate Fundamental Data: Quarterly metrics for the fact\_fundamental\_indicators table.



\## 2. Dependencies and Constraints🔌 External Dependency: Alpha Vantage API, utilizing the OVERVIEW and TIME\_SERIES\_DAILY\_ADJUSTED endpoints.

⚠️ Rate Limit Constraint (Critical): The free tier imposes a strict limit of 5 requests per minute. This constraint fundamentally governs the execution speed and control flow of the entire ETL process.

🔐 Authentication: Requires the AV\_API\_KEY loaded via the .env configuration file for secure communication.



\## 3. Core Logic Flow and Error HandlingThe extraction functions are designed with a Fail-Safe strategy:



❌ Connection Errors: All API calls are wrapped in try/except blocks to catch network or connection failures, preventing abrupt termination.

🛑 HTTP Errors: response.raise\_for\_status() is used to explicitly verify non-200 HTTP responses (e.g., 404, 500), immediately raising an error to avoid processing corrupt data.

🤝 Graceful Degradation: If a single ticker fails (due to a temporary API error), the script logs the issue and continues with the next ticker.



\## 4. Critical Design Decisions (Why the Code is Built This Way)Two key architectural decisions were made to ensure pipeline stability and data integrity:



\### A. Rate Limit Mitigation (Throttling)Problem: Rapid sequential calls to the API resulted in the 5 calls per minute quota being exceeded, leading to API errors and script failures.Solution: A mandatory, fixed-duration pause (time.sleep(20)) is executed after every single API request. 



This ensures the total number of requests is limited to a maximum of 3 per minute, guaranteeing compliance and preventing service interruption.



\### B. Handling Non-Applicable Tickers (ETFs)Problem: Tickers representing ETFs (e.g., QQQ) do not have corporate fundamental data. 

The API returns an incomplete JSON structure missing the expected key "LatestQuarter", which would cause a KeyError in the transformation step.Solution: The core logic is protected by a dedicated try...except KeyError block. 



If the required key is absent, the function returns None instead of raising an exception. This "soft failure" allows the downstream Transformation and Loading stages to skip the record cleanly without halting the entire batch.



\## 5. Data Outputs and Hand-offThis module is responsible for obtaining the raw or lightly processed data and passing it to the Transformation Module.FunciónTipo de SalidaValor de Entrega

extract\_prices() pd.DataFrameA Pandas DataFrame containing raw time-series 

data.extract\_fundamentals()  dict o NoneA Python dictionary containing the raw JSON fundamentals, or None if data was skipped due to API errors or missing keys (e.g., ETFs).

