# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# import os
# import uuid
# import asyncio

# from crewai import Crew, Process
# from agents import doctor
# from task import help_patients

# app = FastAPI(title="Blood Test Report Analyser")

# def run_crew(query: str, file_path: str="data/sample.pdf"):
#     """To run the whole crew"""
#     medical_crew = Crew(
#         agents=[doctor],
#         tasks=[help_patients],
#         process=Process.sequential,
#     )
    
#     result = medical_crew.kickoff({'query': query})
#     return result

# @app.get("/")
# async def root():
#     """Health check endpoint"""
#     return {"message": "Blood Test Report Analyser API is running"}

# @app.post("/analyze")
# async def analyze_blood_report(
#     file: UploadFile = File(...),
#     query: str = Form(default="Summarise my Blood Test Report")
# ):
#     """Analyze blood test report and provide comprehensive health recommendations"""
    
#     # Generate unique filename to avoid conflicts
#     file_id = str(uuid.uuid4())
#     file_path = f"data/blood_test_report_{file_id}.pdf"
    
#     try:
#         # Ensure data directory exists
#         os.makedirs("data", exist_ok=True)
        
#         # Save uploaded file
#         with open(file_path, "wb") as f:
#             content = await file.read()
#             f.write(content)
        
#         # Validate query
#         if query=="" or query is None:
#             query = "Summarise my Blood Test Report"
            
#         # Process the blood report with all specialists
#         response = run_crew(query=query.strip(), file_path=file_path)
        
#         return {
#             "status": "success",
#             "query": query,
#             "analysis": str(response),
#             "file_processed": file.filename
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
#     finally:
#         # Clean up uploaded file
#         if os.path.exists(file_path):
#             try:
#                 os.remove(file_path)
#             except:
#                 pass  # Ignore cleanup errors

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from celery_worker import analyze_blood_report_task
from models import AnalysisResult
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

def save_to_db(filename, query, result):
    db = SessionLocal()
    record = AnalysisResult(filename=filename, query=query, result=result)
    db.add(record)
    db.commit()
    db.close()

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        task = analyze_blood_report_task.delay(query.strip(), file_path)

        return {
            "status": "processing",
            "task_id": task.id,
            "message": "Your report is being analyzed. Use /result/{task_id} to fetch result."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")

    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass


@app.get("/result/{task_id}")
def get_result(task_id: str):
    result = analyze_blood_report_task.AsyncResult(task_id)
    if result.state == "SUCCESS":
        output = result.result
        # Save to DB when task completes
        save_to_db(filename="uploaded_file.pdf", query="Summarise my Blood Test Report", result=output)
        return {"status": "completed", "result": output}
    return {"status": result.state}