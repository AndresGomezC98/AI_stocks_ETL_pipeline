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
