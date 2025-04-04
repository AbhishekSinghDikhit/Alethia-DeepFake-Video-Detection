const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br text-white px-4 sm:px-6 md:px-12">
      {/* Title */}
      <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-cyan-400 mb-4 text-center">
        Alethia Lab - Unmasking Deepfakes
      </h1>
      {/* Subtitle */}
      <p className="text-base sm:text-lg text-gray-300 text-center max-w-md sm:max-w-xl md:max-w-2xl">
        In an era of AI-generated content, deepfake videos can be dangerously misleading. 
        Our advanced detection system analyzes video content to determine its authenticity.
      </p>

      {/* Call to Action */}
      <div className="mt-6 sm:mt-8">
        <a
          href="/detect"
          className="px-5 sm:px-6 py-2 sm:py-3 text-base sm:text-lg font-bold text-black bg-cyan-400 rounded-md hover:bg-cyan-300 transition shadow-lg"
        >
          Detect Deepfake Now
        </a>
      </div>

      {/* Information Section */}
      <div className="mt-10 sm:mt-12 max-w-md sm:max-w-lg md:max-w-3xl text-center px-4">
        <h2 className="text-2xl sm:text-3xl font-bold text-cyan-300 mb-3 sm:mb-4">
          What are Deepfake Videos?
        </h2>
        <p className="text-gray-300 text-sm sm:text-lg leading-relaxed">
          Deepfake videos use <strong>AI-powered face-swapping</strong> to create 
          <strong> hyper-realistic but fake</strong> content. 
          While this technology has creative applications, it also poses serious threats 
          such as <strong>misinformation, fraud, and identity theft</strong>.
        </p>
      </div>
    </div>
  );
};

export default Home;
