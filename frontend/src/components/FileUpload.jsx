import { useState } from "react";

function FileUpload({ onUpload }) {
  const [video, setVideo] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    setVideo(file);
    onUpload(file);
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      {video && (
        <video src={URL.createObjectURL(video)} controls className="w-80 h-48 rounded-lg shadow-md" />
      )}
      <input type="file" accept="video/*" onChange={handleFileChange} className="hidden" id="upload" />
      <label htmlFor="upload" className="px-4 py-2 bg-cyan-400 text-black font-bold rounded-md cursor-pointer hover:bg-cyan-300 transition">
        Upload Video
      </label>
    </div>
  );
}

export default FileUpload;
