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
      const response = await fetch("https://alethia-backend.azurewebsites.net/detect", {
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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br text-white px-4 sm:px-6 md:px-12 pt-16 sm:pt-20">
      <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-cyan-400 mb-4 sm:mb-6 text-center">
        IS YOUR VIDEO <span className="text-cyan-300">FAKE?</span> CHECK IT!
      </h2>

      {/* Upload Component */}
      <div className="w-full max-w-xs sm:max-w-sm md:max-w-md">
        <FileUpload onUpload={setVideo} />
      </div>

      {/* Submit Button */}
      <button 
        onClick={handleSubmit} 
        disabled={!video || loading} 
        className="px-4 sm:px-6 py-2 sm:py-3 mt-4 sm:mt-6 text-sm sm:text-base text-black font-bold border-2 border-black rounded-md bg-white hover:bg-black hover:text-white disabled:bg-gray-500 disabled:cursor-not-allowed transition"
      >
        {loading ? "Processing..." : "Submit"}
      </button>

      {/* Result Card */}
      {result && (
        <div className="w-full max-w-xs sm:max-w-sm md:max-w-lg mt-4 sm:mt-6">
          <ResultCard result={result} />
        </div>
      )}
    </div>
  );
}

export default Detect;
