# 🎓 AI Auto-Grader Web App

A full-stack, multi-agent AI grading platform that evaluates student submissions against dynamically generated rubrics and outputs a clean PDF report card. 

Built with the [CAMEL-AI](https://camel-ai.org/) framework, powered by lightning-fast Groq inference, and served via a modern **FastAPI** backend with a **Tailwind CSS** frontend.

---

## ✨ Features

* **🖥️ Modern Web Interface:** A clean, user-friendly browser interface to upload files and generate reports seamlessly.
* **📂 Dynamic File Ingestion:** Drop your `.txt` files directly into the web UI. No hardcoded file names or terminal commands required.
* **🤖 Multi-Agent Architecture:** Utilizes two distinct AI agents:
  * **Rubric Agent:** Generates strict, fair answer keys from your provided curriculum.
  * **Evaluator Agent:** Grades the student's submission against the generated rubric.
* **⚡ Lightning Fast:** Leverages Groq's Llama 3.1 models for near-instant reasoning and evaluation.
* **📄 Automatic PDF Generation:** Compiles the final evaluation into a neatly formatted `.pdf` report card delivered straight to your browser.

---

## 📂 Project Structure

```text
your-project-folder/
│
├── camel/                  # Python virtual environment (ignored in Git)
├── .gitignore              # Specifies intentionally untracked files
├── main.py                 # The FastAPI server and AI agent logic
├── index.html              # The Tailwind CSS frontend UI
│
└── Graded_Report.pdf       # Output: Downloaded automatically after evaluation