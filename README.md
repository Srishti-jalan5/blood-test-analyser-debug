# Blood Test Analyzer – Debugged and Enhanced

This repository contains a FastAPI-based application powered by CrewAI agents to analyze blood test reports. The application has been debugged and extended with features like asynchronous task processing via Celery and result persistence via SQLite.

---

## Getting Started

### 1. Install Required Libraries

Ensure you're in your virtual environment:

```bash
pip install -r requirements.txt
```

---

## Debugging Summary

This project initially had multiple bugs across core files and required several iterations of debugging, dependency fixing, and local testing.

### What I Did:

1. **Bug Identification** – Reviewed each Python file to trace the error sources.
2. **Bug Fixing** – Applied corrections to function signatures, async handling, LLM instantiation, and module imports.
3. **Testing** – Re-ran the full FastAPI server + Celery queue after every fix.
4. **Retry Count** – Attempted and debugged the setup more than **5 times** due to dependency issues and resource constraints on an Intel i3 system.

---

## System Constraints

* **Machine**: Intel i3, 8GB RAM, Windows 10
* **Issues Faced**:

  * Dependency resolution errors (`resolution-too-deep`, version conflicts)
  * Virtual environment performance delays
  * Compatibility fixes due to limited hardware

---

## Key Features

* Upload and analyze blood test reports (PDF)
* CrewAI multi-agent collaboration (Doctor, Verifier, Nutritionist, Fitness Coach)
* Celery + Redis queue for background task execution
* SQLite database integration to persist query results
* Interactive API documentation at `/docs`

---

## Queue Worker Model & Database Integration

The system uses a **Celery worker** and **Redis broker** to process analysis tasks asynchronously. Results are saved into a **SQLite database**, allowing the user to retrieve previous analysis using task IDs.

---

## Project Structure

```
blood-test-analyser-debug/
├── agents.py
├── tools.py
├── task.py
├── main.py
├── celery_worker.py
├── models.py
├── database.py
├── requirements.txt
├── data/
├── output/
└── analysis.db
```

---

## Setup Instructions

### Clone and Setup

```bash
git clone <your-repo-url>
cd blood-test-analyser-debug
```

### Create Virtual Environment

```bash
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### Install Requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Start Redis Server

```bash
redis-server
```

### Run Celery Worker

```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

### Run FastAPI Server

```bash
uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### `POST /analyze`

* Upload blood report
* Queue analysis task

### `GET /result/{task_id}`

* Retrieve analysis result from database

---

## Bugs Fixed – File-wise Summary

### `agents.py`

* Fixed undefined `llm` reference
* Corrected tool assignments and agent instantiation

### `tools.py`

* Made `read_data_tool` a static method
* Fixed missing import: `PDFLoader`

### `main.py`

* Moved analysis logic to Celery background job
* Added async-safe result retrieval endpoint

### `task.py`

* Repaired CrewAI tool/task linking

### `requirements.txt`

* Removed strict/conflicting versions
* Resolved: `pydantic`, `onnxruntime`, `openai`, `langchain` issues

---

## Core Dependencies

```txt
fastapi
uvicorn
crewai==0.130.0
openai>=1.13.3
python-dotenv
pydantic>=2.4.2
celery
redis
sqlalchemy
numpy
pandas
```

---

## Author

**Srishti Jalan**
📧 [srishtijalan622@gmail.com](mailto:srishtijalan622@gmail.com)
📞 7003824749
🔗 [LinkedIn](https://www.linkedin.com/in/srishti-jalan)

---

Built using: CrewAI · FastAPI · Celery · Redis · SQLAlchemy
