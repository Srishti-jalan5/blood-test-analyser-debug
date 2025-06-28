# Project Setup and Execution Guide

## Getting Started

### Install Required Libraries

```sh
pip install -r requirements.txt
```

## You're All Not Set!

🐛 **Debug Mode Activated!** The project had several bugs that were identified and fixed manually. Below is a guide to what was done.

---

## Debugging Instructions (What I Did)

1. **Identified the Bug**: I carefully read each file and understood what wasn’t working.
2. **Fixed the Bugs**: I resolved all runtime issues, async bugs, tool misuses, and missing modules.
3. **Tested the Fixes**: Verified the fixes by running the full pipeline locally (API + Celery + Redis + DB).
4. **Re-tested (Many Times)**: I had to attempt the full debug cycle more than **5 times** due to compatibility and environment limitations.

---

## System Notes

* My system: Intel i3, 8GB RAM, Windows 10
* Due to limited resources, dependency resolution was **very slow**
* Errors like `resolution-too-deep`, `ModuleNotFoundError`, and `dependency conflicts` occurred frequently
* Manually adjusted many versions in `requirements.txt` to make it work reliably

---

## Features Implemented

* Upload and analyze blood test PDFs
* CrewAI agents (Doctor, Verifier, Nutritionist, Fitness Coach)
* Queue system using Celery + Redis for background processing
* Stores analysis results using SQLite + SQLAlchemy
* REST API with Swagger `/docs`

---

## Queue Worker Model & Database Integration

To support concurrent processing, this project uses **Celery** with a **Redis queue**. When a report is submitted, it's processed in the background asynchronously.

Each result is stored in an **SQLite database** (`analysis.db`) along with the uploaded file name and query string, making the analysis persistent and accessible.

---

## Project Structure


blood-test-analyser-debug/
├── agents.py
├── tools.py
├── task.py
├── main.py               # FastAPI app with Celery task routing
├── celery_worker.py      # Background worker
├── models.py             # SQLite DB schema
├── database.py           # SQLAlchemy connection setup
├── requirements.txt      # All required dependencies
├── data/                 # Uploaded PDFs
├── output/               # (Optional) Results or logs
└── analysis.db           # SQLite DB file


---

## Setup Instructions

### 1. Clone the repo and enter the folder:

```bash
git clone <your-repo-url>
cd blood-test-analyser-debug
```

### 2. Create and activate virtualenv

```bash
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1   # On Windows PowerShell
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### 4. Start Redis

Make sure Redis is running locally:

```bash
redis-server
```

(Use WSL or Memurai if on Windows)

### 5. Run Celery worker:

```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

### 6. Start FastAPI server:

```bash
uvicorn main:app --reload
```

Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### `POST /analyze`

* Upload PDF and Query
* Returns `task_id` for background processing

### `GET /result/{task_id}`

* Fetch result of previously submitted task
* Auto-saves result to SQLite DB

---

## Bugs Fixed (File-wise Debug Summary)

### agents.py

* Bug: `llm = llm` → undefined LLM instance
* Fix: Load and pass LLM correctly to all agents

### tools.py

* Bug: `read_data_tool` was async without `@staticmethod`
* Bug: PDFLoader class wasn't imported correctly
* Fix: Made `read_data_tool` a static method and ensured PDFLoader is imported

### main.py

* Bug: Synchronous blood report analysis blocked UI
* Fix: Offloaded processing to Celery queue using `analyze_blood_report_task`
* Added `/result/{task_id}` endpoint for async polling

### task.py

* Bug: Tasks didn’t support modular tooling
* Fix: Corrected tools list, structured around CrewAI agent pattern

### requirements.txt

* Bug: Conflicting dependencies (onnxruntime, pydantic, openai, langchain)
* Fix: Resolved versions to match CrewAI compatibility (`onnxruntime==1.22.0`, `pydantic>=2.4.2`)

---

## Requirements (key)

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

---

## Contact

Srishti Jalan
Email: [srishtijalan622@gmail.com](mailto:srishtijalan622@gmail.com)
Phone: 7003824749
LinkedIn: [Srishti Jalan](https://www.linkedin.com/in/srishti-jalan)

---

Built using CrewAI, FastAPI, Celery, and SQLAlchemy

