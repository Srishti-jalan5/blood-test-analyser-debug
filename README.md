# Blood Test Analyzer – Debugged and Enhanced

This repository documents a FastAPI application enhanced with CrewAI agents to analyze blood test reports. The system has been upgraded with asynchronous processing and persistent database storage.

## Getting Started

To install all required libraries, activate your virtual environment and run:
`pip install -r requirements.txt`

## Debugging Summary

This project initially had multiple bugs across several files. Fixes included:

* Addressing undefined variables and missing imports
* Correcting async usage and method bindings
* Cleaning up version conflicts in dependencies

I attempted debugging and testing more than five times due to repeated compatibility issues, especially on my Intel i3 system with limited resources.

## System Constraints

* Intel i3 processor, 8GB RAM, Windows 10
* Frequent issues: slow dependency resolution, version incompatibility, environment delays

## Key Features

* Analyze blood test PDFs using AI agents
* Uses Celery and Redis for concurrent request processing
* Results are saved in SQLite for later reference
* API available with Swagger at `/docs`

## Queue & Database Support

Submitted blood test reports are processed asynchronously through Celery workers using Redis as the broker. Each result is stored in a SQLite database with the original query and filename.

## Folder Overview

* `agents.py` – defines the agents (Doctor, Verifier, etc.)
* `tools.py` – PDF reader tool
* `task.py` – task configuration for agents
* `main.py` – FastAPI app
* `celery_worker.py` – Celery background worker
* `database.py` & `models.py` – SQLite setup

## How to Run

1. Clone the repository and open the folder
2. Create a virtual environment and activate it
3. Install the required packages
4. Start the Redis server
5. Run the Celery worker
6. Launch the FastAPI app using Uvicorn

## Endpoints

* `POST /analyze` → Submits a PDF for analysis
* `GET /result/{task_id}` → Fetches result from database

## Bug Fix Summary

### agents.py

* Fixed undefined `llm` assignment.
* Corrected use of `tool=` to `tools=[...]` for agents.
* Added missing `memory`, `verbose`, and `allow_delegation` arguments.

### tools.py

* Converted `read_data_tool` to a static method for compatibility with CrewAI.
* Imported `PDFLoader` correctly from `langchain.document_loaders`.
* Cleaned unnecessary async logic and added string cleanup in report parsing.

### task.py

* Task `tools` reference was misaligned; corrected to use `tools=[...]`.
* Fixed agent references and task `expected_output` formatting.

### main.py

* Refactored analysis logic into a Celery background task to prevent API blocking.
* Improved exception handling and ensured temp files are cleaned up.
* Added `/result/{task_id}` endpoint to retrieve results from DB.

### celery\_worker.py

* Added a background task that receives query and file path, reads the report, executes CrewAI workflow, and stores the result in the database.

### database.py / models.py

* Defined `AnalysisResult` table with `task_id`, `query`, `result`, and `filename` fields.
* Connected SQLite using SQLAlchemy ORM and created necessary schema.

### requirements.txt

* Removed conflicting versions (e.g., `onnxruntime==1.18.0`).
* Locked `crewai==0.130.0` and set compatible versions of `openai`, `pydantic`, and `langchain-core`.
* Cleaned unused or broken packages after multiple install failures.

## Core Dependencies

* FastAPI, Uvicorn, Celery, Redis
* crewai==0.130.0, openai>=1.13.3
* pydantic>=2.4.2, numpy, pandas, sqlalchemy

## Author

Srishti Jalan
Email: [srishtijalan622@gmail.com](mailto:srishtijalan622@gmail.com)
Phone: 7003824749
[LinkedIn](https://www.linkedin.com/in/srishti-jalan)

Built with: CrewAI · FastAPI · Celery · Redis · SQLAlchemy
