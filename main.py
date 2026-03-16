import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from dotenv import load_dotenv
from fpdf import FPDF

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.configs import GroqConfig

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Setup Groq Model
model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    model_type="llama-3.1-8b-instant", 
    model_config_dict=GroqConfig(temperature=0.1).as_dict(),
)

# Initialize Agents
rubric_agent = ChatAgent(
    system_message="You are an expert curriculum designer. Generate a strict, clear grading rubric and answer key from the provided text. State exactly what points must be present to award full marks.",
    model=model
)

evaluator_agent = ChatAgent(
    system_message="You are a strict but fair teacher. Evaluate the student answers against the rubric. Output ONLY a clean summary of marks obtained per question, feedback, and a Total Score.",
    model=model
)

def generate_report_card_pdf(evaluation_text, output_filename="Student_Result.pdf"):
    """Generates a PDF report from the evaluator's text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Student Evaluation Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    # FPDF natively handles multi-line strings
    pdf.multi_cell(0, 10, txt=evaluation_text)
    pdf.output(output_filename)
    return output_filename

@app.get("/")
async def read_index():
    """Serves the frontend HTML page."""
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/grade")
async def grade_papers(
    question_paper: UploadFile = File(...),
    textbook: UploadFile = File(...),
    student_answers: UploadFile = File(...)
):
    # Read the uploaded files directly from memory
    qp_text = (await question_paper.read()).decode('utf-8')
    tb_text = (await textbook.read()).decode('utf-8')
    sa_text = (await student_answers.read()).decode('utf-8')

    # Step 1: Agent 1 creates the rubric
    rubric_prompt = f"Question Paper:\n{qp_text}\n\nTextbook Context:\n{tb_text}"
    rubric_response = rubric_agent.step(rubric_prompt)
    answer_key = rubric_response.msgs[0].content

    # Step 2: Agent 2 grades the student
    eval_prompt = f"Grading Rubric:\n{answer_key}\n\nStudent Answer Sheet:\n{sa_text}"
    evaluation_response = evaluator_agent.step(eval_prompt)
    final_grade_report = evaluation_response.msgs[0].content

    # Step 3: Generate the PDF and send it back to the user
    pdf_filename = generate_report_card_pdf(final_grade_report)
    
    # Return the PDF file so the user's browser downloads it automatically
    return FileResponse(
        path=pdf_filename, 
        media_type='application/pdf', 
        filename="Graded_Report.pdf"
    )