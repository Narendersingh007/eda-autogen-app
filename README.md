![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)

# 📊 EDA Autogen App

**EDA Autogen App** is an advanced, interactive tool for automatic Exploratory Data Analysis (EDA), powered by multi-agent AI and flexible LLM support. Users can upload CSV datasets and watch AI agents collaborate to analyze data, generate Python code, review outputs, and provide actionable insights—all via a Streamlit web interface.

---

## 🚀 Features

- ✅ **Modern Web Interface** — Responsive Streamlit UI with drag & drop CSV upload.
- 🤖 **Multi-Agent Collaboration**:
  - **User Agent**: Orchestrates the EDA process.
  - **Coder Agent**: Generates Python code for analysis and visualization.
  - **Critic Agent**: Reviews code quality and suggests improvements.
  - **Analyst Agent**: Provides business insights and recommendations.
- 📊 **Live Code Execution** — Python code from agents is executed in real time, including plots and DataFrame modifications.
- ⚙️ **Configurable Parameters** — Select LLM provider, model, creativity, and conversation depth.
- 🔒 **Flexible LLM Support** — Works with Ollama (local), OpenAI, or Gemini (cloud).
- 💾 **Exportable Reports** — Download full analysis including all agent messages and visualizations.
- 🧠 **Auto-Generated Insights** — Comprehensive analysis with actionable recommendations.
- 🛠️ **Performance Tracking** — Progress bars, execution time estimates, and error warnings.

---

## 🧩 Workflow

1. **Upload Dataset**
   - Drag & drop CSV file in Streamlit UI.
   - Preview basic statistics: rows, columns, data types, memory usage.

2. **Configuration**
   - Select LLM provider: Ollama (local), OpenAI, or Gemini (cloud).
   - Choose model and adjust temperature & max conversation rounds.
   - Provider-specific status and requirements displayed.

3. **Start Analysis**
   - Initializes multi-agent group chat (User, Coder, Critic, Analyst).
   - Passes dataset and configuration to agents.

4. **Agent Collaboration**
   - Agents exchange messages to perform EDA.
   - Coder generates Python code, Critic reviews it, Analyst provides business insights.
   - All interactions displayed live in the UI.

5. **Live Execution**
   - Code executed on the fly, plots rendered via matplotlib/seaborn.
   - Data modifications and errors shown in real time.

6. **Results & Export**
   - Display of summary stats, plots, agent conversation.
   - Downloadable full analysis report.

---

## 🛠️ Architecture & Tech Stack

| Layer         | Technology/Module                         | Purpose                                      |
|---------------|------------------------------------------|----------------------------------------------|
| **Frontend**  | Streamlit                                | Interactive web UI, file upload, visualization|
| **Agents**    | `eda_agents.py`                           | Multi-agent orchestration (User, Coder, Critic, Analyst) |
| **LLM Client**| `llm_client.py`                           | Unified interface for Ollama, OpenAI, Gemini  |
| **Config**    | `config.py`                               | Provider/model selection, API keys, defaults |
| **Data**      | pandas, numpy                             | Data loading and processing                  |
| **Visualization** | matplotlib, seaborn                    | Plotting and charts                           |
| **Other**     | requests, time, os, sys                   | API calls, performance tracking               |

---

## 🤖 LLM Provider Support

- **Ollama**: Local and offline, supports models like mistral, llama3, codellama, qwen. Privacy-focused.  
- **OpenAI**: Cloud-based GPT models, requires API key (GPT-3.5, GPT-4).  
- **Gemini**: Google cloud LLM, requires API key, supports Gemini-1.5 models.  

The unified client (`llm_client.py`) abstracts differences between providers for seamless switching and robust error handling.

---

## 🐛 Troubleshooting & Extensibility

- **Provider not configured**: UI provides instructions to start Ollama or set API keys.  
- **Add new agents/models**: Extend `eda_agents.py` and update `config.py`.  
- **Custom workflows**: Modify agent prompts and system messages.  

---

## 📦 Project Structure

```text
eda-autogen-app/
├── app.py                 # Main Streamlit app
├── run.py                 # Launcher script
├── requirements.txt       # Dependencies
├── backend/
│   ├── agents/            # Agent definitions
│   │   ├── eda_agents.py
│   │   ├── coder.py
│   │   ├── critic.py
│   │   └── user_proxy.py
│   └── llm_client.py      # Unified LLM client
├── config.py              # Provider/model config
├── .gitignore
├── README.md
└── LICENSE
```


## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher  
- [Ollama](https://ollama.com/) (for local LLM)  
- API keys for OpenAI or Gemini (if using cloud LLMs)  

### Installation

```bash
# Clone the repository
git clone (https://github.com/Narendersingh007/eda-autogen-app)
cd eda-autogen-app

# Install dependencies
pip install -r requirements.txt

### Launch App

```bash
# For local LLM
ollama serve
ollama pull mistral

# Set API keys (if using cloud LLMs)
export OPENAI_API_KEY='your-openai-key'
export GEMINI_API_KEY='your-gemini-key'

# Start Streamlit app
streamlit run app.py

```
---

## 🌟 Why This Project Stands Out

- Combines multi-agent AI with real-time code execution and visualization.  
- Supports both local and cloud LLMs for flexibility, privacy, and performance.  
- Professional UI/UX with live feedback, error handling, and progress tracking.  
- Extensible architecture allows adding new agents, models, and workflows.  
- Ideal portfolio project demonstrating Python, Streamlit, AI/ML, and full-stack integration skills.

---

## 👤 Author

**Narender Singh**  
✉️ narendersingh123987@gmail.com  
🔗 [GitHub Profile](https://github.com/Narendersingh007)

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 💬 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/your-feature`)  
3. Make your changes  
4. Add tests if applicable  
5. Submit a Pull Request

---
