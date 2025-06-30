# 📊 EDA Autogen App

**EDA Autogen App** is an interactive web application that allows users to upload a CSV file and receive automatic exploratory data analysis (EDA) using multi-agent AI. Built with a React frontend, Flask backend, and powered by Ollama for local LLMs, the app provides live-streamed analysis and visualizations.

---

## 🚀 Features

- ✅ Upload your own `.csv` dataset
- 🤖 Automated EDA with intelligent agents (Coder & Critic)
- 🧠 Live-streamed chat between agents with insightful feedback
- 🔍 Data preview and summary statistics
- 📈 Suggestions for improving EDA, transformations, visualizations, etc.
- 🔒 Works fully offline with local LLMs via Ollama

---

## 🛠️ Tech Stack

- **Frontend**: React, JavaScript, CSS
- **Backend**: Flask, Python
- **LLM Engine**: [Ollama](https://ollama.com/) with `llama3` or other local models
- **Agents Framework**: [AutoGen](https://github.com/microsoft/autogen) with Group Chat
- **Visualization**: matplotlib, seaborn
- **File Upload**: Flask + FormData API

---

## 📂 Project Structure

eda-autogen-app/
├── backend/
│ ├── agents/ # LLM & agent logic
│ ├── routes/ # Flask API endpoints
│ ├── uploads/ # Temporary file storage
│ └── main.py # Flask app entrypoint
├── frontend/
│ ├── public/
│ ├── src/
│ │ └── App.jsx # React UI
│ └── package.json
├── .gitignore
├── README.md
└── requirements.txt

---

## ⚙️ Setup Instructions

### 1. Backend Setup (Python + Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m backend.main
```
2. Frontend Setup (React)
```bash
cd frontend
npm install
npm run dev  # or npm start
```
3. Ollama Setup (local LLM)
```bash
ollama serve  # Start Ollama server
ollama run llama3  # Make sure model is downloaded and working
```
Sample Dataset
You can test the app using your own .csv file or a synthetic one.
Make sure your file is under 100 MB (GitHub limit is enforced)

.gitignore Highlights

The repo ignores:
	•	All .csv files
	•	Upload folders
	•	node_modules/
	•	Python caches and .env

This prevents large or sensitive files from being committed.

Future Enhancements
	•	Support for multiple model types (e.g., GPT-4, Mixtral)
	•	More intelligent suggestions & visual summaries
	•	Exportable PDF/Markdown reports
	•	Integration with SQL and other data sources
```
