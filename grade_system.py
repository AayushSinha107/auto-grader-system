import os
from dotenv import load_dotenv
from fpdf import FPDF
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.configs import GroqConfig

# Load environment variables (Make sure GROQ_API_KEY is in your .env)
load_dotenv()

# ==========================================
# 1. SETUP THE GROQ MODEL
# ==========================================
model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    # Updated to the new, currently supported Llama 3.1 model:
    model_type="llama-3.1-8b-instant", 
    model_config_dict=GroqConfig(temperature=0.1).as_dict(), 
)

# ==========================================
# 2. DEFINE THE AGENTS
# ==========================================
rubric_agent = ChatAgent(
    system_message=(
        "You are an expert curriculum designer. Your job is to read a question paper "
        "and a textbook excerpt, and generate a strict, clear grading rubric and answer key. "
        "State exactly what points must be present to award full marks."
    ),
    model=model
)

evaluator_agent = ChatAgent(
    system_message=(
        "You are a strict but fair teacher. You will be given a grading rubric and a "
        "student's answer sheet. Evaluate the answers against the rubric. "
        "Output ONLY a clean summary of marks obtained per question, feedback, and a Total Score. "
        "Do not include conversational filler."
    ),
    model=model
)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def read_text_file(filepath):
    """Utility to read input text files."""
    # In a real scenario, you'd handle file-not-found errors here
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_report_card_pdf(evaluation_text, output_filename="ReportCard.pdf"):
    """Generates a PDF report from the evaluator's text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Student Evaluation Report", ln=True, align='C')
    pdf.ln(10) # Add a line break
    
    # Body
    pdf.set_font("Arial", size=12)
    # Handle multi-line text natively in FPDF
    pdf.multi_cell(0, 10, txt=evaluation_text)
    
    pdf.output(output_filename)
    print(f"✅ Success! Report card saved as {output_filename}")

# ==========================================
# 4. MAIN PIPELINE EXECUTION
# ==========================================
def main():
    print("Starting the grading pipeline...")

    # For this script to work, create these 3 simple text files in your directory
    # and put some dummy text in them.
    try:
        question_paper = read_text_file("question_paper.txt")
        textbook_context = read_text_file("textbook.txt")
        student_answers = read_text_file("student_answers.txt")
    except FileNotFoundError:
        print("Please create 'question_paper.txt', 'textbook.txt', and 'student_answers.txt' in this folder with some sample text to run this.")
        return

    # Step 1: Generate the Rubric
    print("Agent 1 is creating the answer key...")
    rubric_prompt = f"Question Paper:\n{question_paper}\n\nTextbook Context:\n{textbook_context}"
    rubric_response = rubric_agent.step(rubric_prompt)
    answer_key = rubric_response.msgs[0].content

    # Step 2: Evaluate the Student
    print("Agent 2 is grading the student's paper...")
    eval_prompt = f"Grading Rubric:\n{answer_key}\n\nStudent Answer Sheet:\n{student_answers}"
    evaluation_response = evaluator_agent.step(eval_prompt)
    final_grade_report = evaluation_response.msgs[0].content

    # Step 3: Generate PDF
    print("Generating PDF report...")
    generate_report_card_pdf(final_grade_report, "Student_Result.pdf")

if __name__ == "__main__":
    main()