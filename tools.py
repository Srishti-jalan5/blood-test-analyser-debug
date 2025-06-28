import os
from crewai_tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader


# Tool to read blood test report PDFs
class BloodTestReportTool(BaseTool):
    name = "Read Blood Test PDF"
    description = "Reads and returns the text content of a blood test report from a PDF file."

    def _run(self, file_path: str) -> str:
        """Reads and extracts text from the PDF at the given path."""
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        
        try:
            docs = PyPDFLoader(file_path).load()
            content = "\n".join([doc.page_content.strip() for doc in docs])
            return content
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

# Optional placeholder tool (not used currently, can be wired to Nutritionist Agent if needed)
class NutritionTool(BaseTool):
    name = "Analyze Nutrition Data"
    description = "Analyzes nutrition implications from blood test data."

    def _run(self, blood_data: str) -> str:
        return "Nutrition analysis functionality is a placeholder."

# Optional placeholder tool (not used currently, can be wired to Exercise Specialist if needed)
class ExerciseTool(BaseTool):
    name = "Generate Exercise Plan"
    description = "Creates a custom exercise plan based on blood test data."

    def _run(self, blood_data: str) -> str:
        return "Exercise planning functionality is a placeholder."
