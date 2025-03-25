const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br text-white px-6">
      {/* Title */}
      <h1 className="text-5xl font-extrabold text-cyan-400 mb-4 text-center">
        Alethia Lab - Unmasking Deepfakes
      </h1>
      {/* Subtitle */}
      <p className="text-lg text-gray-300 text-center max-w-2xl">
        In an era of AI-generated content, deepfake videos can be dangerously misleading. 
        Our advanced detection system analyzes video content to determine its authenticity.
      </p>

      {/* Call to Action */}
      <div className="mt-8">
        <a
          href="/detect"
          className="px-6 py-3 text-lg font-bold text-black bg-cyan-400 rounded-md hover:bg-cyan-300 transition shadow-lg"
        >
          Detect Deepfake Now
        </a>
      </div>

      {/* Information Section */}
      <div className="mt-12 max-w-3xl text-center">
        <h2 className="text-3xl font-bold text-cyan-300 mb-4">
          What are Deepfake Videos?
        </h2>
        <p className="text-gray-300 text-lg leading-relaxed">
          Deepfake videos use **AI-powered face-swapping** to create **hyper-realistic but fake** content. 
          While this technology has creative applications, it also poses serious threats such as **misinformation, fraud, and identity theft**.
        </p>
      </div>
    </div>
  );
};

export default Home;
