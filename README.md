# Real Estate Assistant (Backend-Focused Capstone Project)

A backend-driven Real Estate Assistant that supports natural language property search, follow-up queries using session memory, and LLM-powered responses.

This project focuses on backend architecture, correctness, and testing rather than UI polish.

---

## Features

- Natural language property search
- Follow-up queries with session-based context memory
- Intent extraction (city, BHK, budget, filters)
- LLM-powered answer generation
- Modular backend architecture
- Automated testing with pytest
- HTML test and coverage reports

---

## Tech Stack

- Python 3.12
- FastAPI
- Ollama (Local LLM)
- ChromaDB (Vector database)
- Streamlit (minimal UI)
- Pytest, pytest-cov, pytest-html

---

## Project Structure (Logical View)

app folder  
- main.py (FastAPI entry point)  
- config (application settings)  
- models (Pydantic models)  
- routes (API endpoints)  
- services (business logic, LLM, search, intent extraction)  
- vectordb (ChromaDB integration)  
- ui (Streamlit app)  

tests folder  
- test_chat_api.py  
- test_intent_extractor.py  
- test_search_service.py  
- reports (pytest and coverage HTML reports)  

Other files  
- requirements.txt  
- .gitignore  
- .coveragerc  
- README.md  

---

## How to Run the Project

### 1. Prerequisites

Make sure you have the following installed:

- Python 3.12+
- Git
- Ollama (running locally)
- A supported Ollama model pulled (example: llama3.1:8b)

Start Ollama before running the project:

ollama serve

---

### 2. Clone the Repository

git clone <your-repository-url>
cd real_estate_assistant

---

### 3. Create and Activate Virtual Environment

Create the virtual environment:

python -m venv venv

Activate on Windows (PowerShell):

venv\Scripts\activate

Activate on macOS / Linux:

source venv/bin/activate

---

### 4. Install Dependencies

pip install -r requirements.txt

---

### 5. Run the Backend (FastAPI)

Start the FastAPI server:

uvicorn app.main:app --reload

Backend will be available at:

http://127.0.0.1:8000

---

### 6. Run the Streamlit UI (Optional)

In a new terminal (with the virtual environment activated):

streamlit run app/ui/streamlit_app.py

The Streamlit UI will open automatically in your browser.

---

### 7. Run Tests

Run all tests:

pytest

Generate HTML test and coverage reports:

pytest --html=tests/reports/pytest_report.html --self-contained-html --cov=app --cov-report=html:tests/reports/coverage

Reports will be generated in:

tests/reports/

---

### 8. Deactivate Virtual Environment (Optional)

After you’re done:

deactivate

---

## Running Tests

Run all tests:

pytest

Generate HTML test report and coverage report:

pytest --html=tests/reports/pytest_report.html --self-contained-html --cov=app --cov-report=html:tests/reports/coverage

Reports will be generated inside the tests/reports folder.

---

## Test Coverage

- Overall coverage: approximately 56%
- Core backend logic is covered
- UI and vector database layers are intentionally excluded
- Coverage configuration handled via .coveragerc

---

## Design Decisions

- Backend-first architecture
- Clean separation of routes, services, and models
- Session-based memory for follow-up queries
- Non-breaking enhancements approach
- UI kept intentionally minimal

---

## Notes for Reviewers

- Emphasis is on backend design and testing
- LLM usage is abstracted behind services
- Suitable for real-world backend applications
- Includes proper test reporting and coverage setup

---

## Author

Yash Visave 