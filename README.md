# <a href="https://kalyanm45.github.io/BlogBoard-AI-Blog-Generator/">BlogBoard â€” Autonomous AI Article Generator</a>

<p align="center"> <img src="https://img.shields.io/github/license/KalyanM45/BlogBoard-AI-Blog-Generator?style=ROUND" alt="License" /> <img src="https://img.shields.io/github/stars/KalyanM45/BlogBoard-AI-Blog-Generator?style=ROUND" alt="Stars" /> <img src="https://img.shields.io/github/forks/KalyanM45/BlogBoard-AI-Blog-Generator?style=ROUND" alt="Forks" /> <img src="https://img.shields.io/github/issues/KalyanM45/BlogBoard-AI-Blog-Generator?style=ROUND"alt="Issues" />
</p>

## About The Project

BlogBoard is an end-to-end, fully automated blogging platform. It autonomously schedules, writes, formats, and publishes deep-dive technical articles on Machine Learning and Artificial Intelligence directly to a fast, static frontend website.

Powered by **LangGraph** for stateful workflow execution and **Groq** for blazing-fast LLM inference, it ensures that high-quality, zero-fluff, production-grade articles are generated and deployed automatically via **GitHub Actions**.

## Library Requirements

 - Python 3.12+
 - langgraph>=0.2.20
 - groq>=0.11.0
 - python-dotenv>=1.0.1
 - uv (for dependency management)

## Getting Started

This will help you understand how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

## Run Locally on Windows

Open PowerShell in the repository root:

```powershell
cd "C:\Users\manis\Desktop\New folder (5)\Multi-Agentic-Blog-Generation"
```

Install the Python dependencies:

```powershell
python -m pip install -e .
```

Make sure `.env` contains the Groq, Supabase Storage, Tavily, and Guardian credentials. Then start the local website:

```powershell
.\scripts\start.ps1
```

Open the dashboard in your browser:

```text
http://localhost:8000
```

To generate and publish a tutorial article through Groq and Supabase Storage:

```powershell
.\scripts\start.ps1 -Generate
```

To generate and publish an AI News article using the news research APIs:

```powershell
.\scripts\start.ps1 -Generate -News
```

To generate an article for a specific date:

```powershell
.\scripts\start.ps1 -Generate -Date 2026-10-16
```

The frontend reads public `articles.json` and Markdown files from Supabase Storage. The Supabase secret credentials remain server-side in `.env` and must never be added to frontend JavaScript.

## Installation Steps

### Installation from GitHub

Follow these steps to install and set up the project directly from the GitHub repository:

1. **Clone the Repository**
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to install the project.
   - Run the following command to clone the GitHub repository:
     ```bash
     git clone https://github.com/KalyanM45/BlogBoard-AI-Blog-Generator.git
     ```

2. **Create a Virtual Environment** (Recommended)
   - It's a good practice to create a virtual environment to manage project dependencies. Run the following command:
     ```bash
     uv venv
     ```

3. **Activate the Virtual Environment**
   - Activate the virtual environment based on your operating system:
       ```bash
       # On Linux/Mac:
       source .venv/bin/activate
       # On Windows:
       .venv\Scripts\activate
       ```

4. **Install Dependencies**
   - Navigate to the project directory:
     ```bash
     cd BlogBoard-AI-Blog-Generator
     ```
   - Run the following command to install project dependencies:
     ```bash
     uv pip install -r backend/requirements.txt
     ```

5. **Run the Project**
   - Start the backend pipeline by running the appropriate command:
     ```bash
     python backend/run.py
     ```

6. **Access the Project**
   - Serve the frontend locally using Python's built-in HTTP server:
     ```bash
     python -m http.server 8000 --directory frontend
     ```
   - Open a web browser and navigate to `http://localhost:8000`.

### Start frontend and generator together

On Windows, run the single startup script:

```powershell
.\scripts\start.ps1
```

This starts the static frontend at `http://localhost:8000`. To also generate and publish one tutorial article:

```powershell
.\scripts\start.ps1 -Generate
```

To generate AI News instead:

```powershell
.\scripts\start.ps1 -Generate -News
```

For a specific date:

```powershell
.\scripts\start.ps1 -Generate -Date 2026-10-16
```

Supabase Storage exposes public files at:

```text
https://<project-ref>.supabase.co/storage/v1/object/public/blogboard/<object-key>
```

The application uses the S3-compatible Supabase Storage API through `boto3` for server-side reads and writes. Only the public read URL is used by the browser.
