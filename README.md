![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen)
# 📊 EDA Autogen App

**EDA Autogen App** is a full-stack, interactive tool for automatic Exploratory Data Analysis (EDA) powered by multi-agent AI. Upload any CSV file and receive a live, collaborative analysis from AI agents — complete with visualizations, summaries, and improvement suggestions.

Built with a React frontend, Flask backend, and local LLMs via Ollama, this app runs entirely offline.

---

## 🚀 Features

- ✅ Upload `.csv` datasets for instant analysis
- 🤖 Multi-agent collaboration:
  - **User Agent**: initiates EDA
  - **Coder Agent**: writes EDA code
  - **Critic Agent**: reviews, scores, and suggests improvements
  - **Analyst Agent**: summarizes final findings
- 📊 Visualizations using `matplotlib` and `seaborn`
- 🧠 Auto-generated insights & transformation logic
- 🔄 Live chat interface with agent personalities
- 💡 Suggestions to improve EDA quality
- 🔒 Runs completely **offline** using [Ollama](https://ollama.com/)

---

## 🛠️ Tech Stack

| Layer      | Tech Used                             |
|------------|----------------------------------------|
| Frontend   | React, TailwindCSS, Vite               |
| Backend    | Flask, Python                          |
| LLM Engine | Ollama (`mistral`, `llama3`, etc.)     |
| Agents     | [AutoGen GroupChat](https://github.com/microsoft/autogen) |
| Plotting   | `matplotlib`, `seaborn`                |

---

## 🧩 Project Structure
```text
eda-autogen-app/
├── backend/
│   ├── agents/            # LLM agents and GroupChat setup
│   ├── llm/               # Ollama LLM wrapper
│   ├── routes/            # Flask API endpoints
│   ├── uploads/           # Uploaded CSV files
│   └── main.py            # Flask app entry point
├── frontend/
│   ├── src/               # React components and styling
│   └── public/            # Static assets
├── .gitignore
├── README.md
└── requirements.txt       # Python dependencies
```
---

## ⚙️ Setup Guide

### 🐍 Backend (Python + Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m backend.main
```

### ⚛️ Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

### 🤖 Ollama LLM Setup

Install Ollama from https://ollama.com

Start the local LLM server:
```bash
ollama serve
```
Pull and run a model ( mistral):
```bash
ollama run mistral
```
Backend connects to http://localhost:11434/v1 by default.

🧪 Example Workflow
	1.	Upload a .csv file via the UI.
	2.	See a preview of your data.
	3.	Watch the agents (User, Coder, Critic, Analyst) chat and collaborate.
	4.	View generated code, visualizations, and critique.
	5.	Receive a final summary of insights + suggested improvements.

 📸 Screenshots
 <img width="1470" height="956" alt="Screenshot 2025-07-11 at 11 38 04 PM" src="https://github.com/user-attachments/assets/b60278b1-e53e-4b61-904d-cd4e3124f44d" />
<img width="1470" height="956" alt="Screenshot 2025-07-11 at 11 38 46 PM" src="https://github.com/user-attachments/assets/71b00630-dca1-4782-a469-d61d433be635" />
<img width="1470" height="956" alt="Screenshot 2025-07-11 at 11 39 04 PM" src="https://github.com/user-attachments/assets/b44666cf-b291-4133-915d-5537826cece8" />

🧑‍💻 Author

Narender Singh
✉️ narendersingh123987@gmail.com

📜 License

MIT License. Feel free to fork and build on top of this.

💬 Contributing

Pull requests are welcome!
For major changes, open an issue first to discuss what you would like to change.
 

 
  is this fine 
