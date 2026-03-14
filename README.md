# 📝 AI Auto-Grader System

An automated, multi-agent AI grading pipeline that evaluates student answers against dynamically generated rubrics and outputs a clean PDF report card. Built using the [CAMEL-AI](https://camel-ai.org/) framework and powered by lightning-fast Groq inference.

---

## ✨ Features

* **📂 Dynamic File Ingestion:** Simply provide your text files. The system automatically ingests all `.txt` documents provided to build its knowledge base—no strict file naming conventions required.
* **🤖 Multi-Agent Architecture:** Utilizes two distinct AI agents—a **Rubric Agent** (to generate strict answer keys from your provided curriculum) and an **Evaluator Agent** (to grade the student).
* **⚡ Lightning Fast:** Leverages Groq's Llama 3 models for near-instant reasoning and text generation.
* **📄 PDF Generation:** Automatically compiles the final evaluation into a neatly formatted `.pdf` report card.

---

## 📂 Project Structure

```text
your-project-folder/
│
├── camel/                  # Your Python virtual environment (ignored in Git)
├── .gitignore              # Specifies intentionally untracked files
├── grade_system.py         # The main execution script
│
├── *.txt                   # Your input files (e.g., questions, curriculum, student answers)
└── Student_Result.pdf      # Output: Generated automatically after evaluation