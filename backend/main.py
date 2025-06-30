from flask import Flask
from flask_cors import CORS
from backend.routes.eda_routes import eda_bp
from backend.config.llm_config import llm_config  # Assuming config/llm_config.py contains llm_config

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend (e.g., React) can access API

# Register Blueprints
app.register_blueprint(eda_bp)

@app.route("/")
def home():
    return {"message": "EDA AutoGen backend is running 🚀"}

if __name__ == "__main__":
    app.run(debug=True)