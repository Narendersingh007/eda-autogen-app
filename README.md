![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)

# 📊 EDA Autogen App

**EDA Autogen App** is a powerful, interactive tool for automatic Exploratory Data Analysis (EDA) powered by multi-agent AI. Upload any CSV file and watch AI agents collaborate to provide comprehensive analysis with visualizations, insights, and improvement suggestions.

Built with **Streamlit** and powered by local LLMs via Ollama, this app runs entirely offline and provides a beautiful, responsive interface for data analysis.

---

## 🚀 Features

- ✅ **Beautiful Web Interface** - Modern, responsive Streamlit UI
- 📁 **Easy File Upload** - Drag & drop CSV files for instant analysis
- 🤖 **Multi-Agent AI Collaboration**:
  - **User Agent**: initiates and guides the EDA process
  - **Coder Agent**: writes Python code for data analysis and visualization
  - **Critic Agent**: reviews, scores, and suggests improvements
  - **Analyst Agent**: provides business insights and recommendations
- 📊 **Interactive Visualizations** - Charts and plots using matplotlib and seaborn
- 🧠 **Auto-generated Insights** - Comprehensive analysis with actionable recommendations
- ⚙️ **Configurable Parameters** - Adjust model, creativity, and conversation depth
- 🔒 **100% Offline** - Runs completely locally using [Ollama](https://ollama.com/)
- 💾 **Export Results** - Download complete analysis reports

---

## 🛠️ Tech Stack

| Component           | Technology                                |
| ------------------- | ----------------------------------------- |
| **Frontend**        | Streamlit (Python-based web framework)    |
| **AI Engine**       | AutoGen GroupChat with local LLMs         |
| **LLM Provider**    | Ollama (mistral, llama3, codellama, qwen) |
| **Data Processing** | pandas, numpy                             |
| **Visualization**   | matplotlib, seaborn                       |
| **Language**        | Python 3.8+                               |

---

## 🧩 Project Structure

```text
eda-autogen-app/
├── app.py                 # Main Streamlit application
├── run.py                 # Launcher script with dependency checks
├── requirements.txt       # Python dependencies
├── backend/
│   └── agents/           # AI agent definitions and GroupChat setup
│       ├── eda_agents.py # Main agent configuration
│       ├── coder.py      # Coder agent implementation
│       ├── critic.py     # Critic agent implementation
│       └── user_proxy.py # User proxy agent
├── .gitignore
├── README.md
└── LICENSE
```

---

## ⚙️ Quick Setup

### 🐍 **Prerequisites**

- Python 3.8 or higher
- [Ollama](https://ollama.com/) installed and running

### 🚀 **Installation & Launch**

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd eda-autogen-app
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama**

   ```bash
   ollama serve
   ollama run mistral
   ```

4. **Launch the app**

   ```bash
   python run.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Or manually navigate to the URL

---

## 🎯 **Usage Workflow**

1. **Upload Dataset** - Drag & drop any CSV file
2. **Configure Analysis** - Select model, adjust parameters in sidebar
3. **Start Analysis** - Click "Start AI Analysis" button
4. **Watch Collaboration** - Observe AI agents working together
5. **Review Results** - Examine code, visualizations, and insights
6. **Download Report** - Save complete analysis for later use

---

## ⚙️ **Configuration Options**

### **Model Selection**

- **mistral** - Fast, balanced performance (recommended)
- **llama3** - High quality, slower processing
- **codellama** - Specialized for code generation
- **qwen** - Good balance of speed and quality

### **Analysis Parameters**

- **Creativity Level** - Control randomness in AI responses
- **Max Rounds** - Limit conversation depth for faster results
- **Custom Prompts** - Modify agent behavior through system messages

---

## 🔧 **Advanced Setup**

### **Custom Model Configuration**

Edit `backend/agents/eda_agents.py` to:

- Add new Ollama models
- Modify agent system messages
- Adjust conversation parameters
- Customize analysis workflows

### **Environment Variables**

```bash
export OLLAMA_BASE_URL="http://localhost:11434/v1"
export DEFAULT_MODEL="mistral"
export MAX_TOKENS=2048
```

---

## 🧪 **Example Output**

The app generates:

- **Data Overview** - Statistics, data types, missing values
- **Visualizations** - Histograms, scatter plots, correlation matrices
- **Code Quality Scores** - Detailed evaluation of analysis
- **Business Insights** - Actionable recommendations
- **Exportable Reports** - Complete analysis documentation

---

## 🐛 **Troubleshooting**

### **Common Issues**

1. **Ollama Connection Failed**

   - Ensure Ollama is running: `ollama serve`
   - Check if model is downloaded: `ollama list`

2. **Dependencies Missing**

   - Run: `pip install -r requirements.txt`
   - Check Python version: `python --version`

3. **Port Already in Use**

   - Change port in `run.py` or kill existing process
   - Use: `lsof -ti:8501 | xargs kill -9`

4. **Memory Issues**
   - Reduce `max_rounds` in configuration
   - Use smaller datasets for testing

---

## 🚀 **Development**

### **Running in Development Mode**

```bash
streamlit run app.py --server.port 8501 --server.address localhost
```

### **Adding New Features**

- **New Agents**: Add to `backend/agents/`
- **UI Components**: Modify `app.py`
- **Data Processing**: Extend pandas functionality
- **Visualizations**: Add new chart types

---

## 📸 **Screenshots**

_[Screenshots will be added here showing the new Streamlit interface]_

---

## 🧑‍💻 **Author**

**Narender Singh**

- ✉️ narendersingh123987@gmail.com
- 🔗 [GitHub Profile]

---

## 📜 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

## 💬 **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

### **Development Guidelines**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 🌟 **Why Streamlit?**

- **Faster Development** - Focus on AI logic, not UI code
- **Better Data Display** - Native pandas and matplotlib support
- **Responsive Design** - Works perfectly on all devices
- **Real-time Updates** - Seamless integration with AI agents
- **Professional Look** - Beautiful interface out of the box
- **Python Native** - Single language for entire application

---

**🎉 Ready to transform your data analysis workflow? Launch the app and experience the power of AI-driven EDA!**
