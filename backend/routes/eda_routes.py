from flask import Blueprint, request, jsonify, Response, stream_with_context
from backend.agents.eda_agents import setup_groupchat_with_agents
import os
import pandas as pd
import time
import json
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager, config_list_from_json
eda_bp = Blueprint("eda_bp", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@eda_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filename": file.filename})

@eda_bp.route("/analyze", methods=["GET"])
def analyze_file():
    def event_stream(filename):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            yield f"data: {json.dumps({'error': f'File {filename} not found'})}\n\n"
            return

        df = pd.read_csv(filepath)
        preview_str = df.head().to_string()
        yield f"data: {json.dumps({'preview': preview_str})}\n\n"

        user_proxy, manager, message = setup_groupchat_with_agents(preview_str)
        user_proxy.initiate_chat(manager, message=message)

        for msg in manager.groupchat.messages:
            if isinstance(msg, dict):
                sender = msg.get("name", "Unknown")
                content = msg.get("content", "NO CONTENT")
            else:
                sender = getattr(msg, "sender", "Unknown")
                content = getattr(msg, "content", "NO CONTENT")

            combined = f"{sender}: {content}"
            yield f"data: {json.dumps({'message': combined})}\n\n"
            time.sleep(0.3)

    try:
        filename = request.args.get("filename")
        if not filename:
            return jsonify({"error": "Missing 'filename' in request"}), 400
        return Response(stream_with_context(event_stream(filename)), content_type="text/event-stream")
    except Exception as e:
        return jsonify({"error": f"Streaming failed: {str(e)}"}), 500