import { useState } from "react";
import "./App.css";

function App() {
	const [file, setFile] = useState(null);
	const [loading, setLoading] = useState(false);
	const [preview, setPreview] = useState("");
	const [chatHistory, setChatHistory] = useState([]);
	const [error, setError] = useState(null);

	const handleFileChange = (e) => {
		setFile(e.target.files[0]);
	};

	const handleUpload = async () => {
		if (!file) return alert("Please select a CSV file");

		setLoading(true);
		setError(null);
		setPreview("");
		setChatHistory([]);

		const formData = new FormData();
		formData.append("file", file);

		try {
			const uploadResponse = await fetch("http://localhost:5000/upload", {
				method: "POST",
				body: formData,
			});
			const uploadData = await uploadResponse.json();
			if (!uploadResponse.ok)
				throw new Error(uploadData.error || "Upload failed");
			const filename = uploadData.filename;
			const eventSource = new EventSource(
				`http://localhost:5000/analyze?filename=${filename}`
			);
			
			eventSource.onmessage = (event) => {
				const data = JSON.parse(event.data);
				if (data.preview) setPreview(data.preview);
				if (data.message) {
					setChatHistory((prev) => [...prev, data.message]);
				}
			};

			eventSource.onerror = (err) => {
				eventSource.close();
				setLoading(false);
			};
		} catch (error) {
			setError(error.message);
		
			setLoading(false);
		}
	};

	const getRoleClass = (sender) => {
		const lower = sender.toLowerCase();
		if (lower.includes("user")) return "chat-message user";
		if (lower.includes("coder")) return "chat-message coder";
		if (lower.includes("critic")) return "chat-message critic";
		return "chat-message";
	};

	return (
		<div className="app-container">
			<h1>📊 EDA Autogen App</h1>

			<input type="file" accept=".csv" onChange={handleFileChange} />
			<br />
			<button onClick={handleUpload} disabled={loading}>
				{loading ? "Analyzing..." : "Upload and Analyze"}
			</button>

			{error && (
				<div className="error-box">
					<strong>Error:</strong> {error}
				</div>
			)}

			{preview && (
				<div className="preview-section">
					<h3>🔍 Data Preview:</h3>
					<pre>{preview}</pre>
				</div>
			)}

			{chatHistory.length > 0 && (
				<div className="chat-section">
					<h3>🧠 Agent Chat History:</h3>
					{chatHistory.map((msg, idx) => {
						const [sender, ...rest] = msg.split(":");
						const content = rest.join(":").trim();
						if (!content) return null;

						return (
							<div key={idx} className={getRoleClass(sender)}>
								<strong>{sender.trim()}:</strong> {content}
							</div>
						);
					})}
				</div>
			)}
		</div>
	);
}

export default App;
