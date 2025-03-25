import { useState } from "react";
import FileUpload from "../components/FileUpload";
import ResultCard from "../components/ResultCard";

function Detect() {
  const [video, setVideo] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!video) return;

    const formData = new FormData();
    formData.append("file", video);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/detect", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      // Extract confidence scores
      const realConfidence = (data.scores.real * 100).toFixed(2);
      const deepfakeConfidence = (data.scores.deepfake * 100).toFixed(2);
      const prediction = data.deepfake ? "Deepfake" : "Real";

      setResult(`Prediction: ${prediction} | Real: ${realConfidence}% | Deepfake: ${deepfakeConfidence}%`);
    } catch (error) {
      setResult("Error analyzing video. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br text-white pt-20">
      <h2 className="text-4xl font-bold text-cyan-400 mb-6">
        IS YOUR VIDEO <span className="text-cyan-300">FAKE?</span> CHECK IT!
      </h2>
      <FileUpload onUpload={setVideo} />
      <button 
        onClick={handleSubmit} 
        disabled={!video || loading} 
        className="px-6 py-2 mt-4 text-black font-bold border-2 border-black rounded-md bg-white hover:bg-black hover:text-white disabled:bg-gray-500 disabled:cursor-not-allowed transition"
      >
        {loading ? "Processing..." : "Submit"}
      </button>
      {result && <ResultCard result={result} />}
    </div>
  );
}

export default Detect;
