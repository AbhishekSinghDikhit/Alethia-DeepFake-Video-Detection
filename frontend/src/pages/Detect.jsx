import { useState } from "react";
import "/src/App.css";

function Detect() {
  const [video, setVideo] = useState(null);
  const [result, setResult] = useState("");

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setVideo(file);
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/detect", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setResult(`Result: ${data.result} | Confidence: ${data.confidence}`);
  };

  return (
    <div className="detect-container">
      <h2 className="detect-title">IS YOUR VIDEO FAKE? CHECK IT!</h2>
      <input type="file" accept="video/*" onChange={handleUpload} className="upload-btn" />
      <p className="result">{result}</p>
    </div>
  );
}

export default Detect;
