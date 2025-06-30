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

### 2. Frontend Setup (React)

```bash
cd frontend
npm install
npm run dev  # or npm start
```

### 3. Ollama Setup (local LLM)

To run the app locally with LLM support, you'll need [Ollama](https://ollama.com/), a tool for running large language models locally.

#### Installation

Follow installation instructions for your platform from https://ollama.com/download

#### Start Ollama Server

```bash
ollama serve  # Starts the Ollama server in background
```

#### Pull and Run Model

You can use `llama3` or any other supported model:

```bash
ollama run llama3
```

This will download the model if not already present and verify it's working.

Make sure Ollama is running at `http://localhost:11434` which is the default expected by the backend.
