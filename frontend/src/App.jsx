import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/ResultsDisplay';
import { uploadAndPredict } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await uploadAndPredict(file);
      setResult(data);
    } catch (err) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen bg-background text-text overflow-hidden flex flex-col">
      {/* Dynamic Background Elements */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-secondary/20 blur-[120px]"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 flex flex-col h-full overflow-hidden">
        <header className="text-center mb-8 shrink-0 animate-fade-in-down">
          <h1 className="text-4xl md:text-5xl font-black mb-3 tracking-tight text-white">
            Asset <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-secondary to-accent">Intelligence</span>
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto font-medium leading-relaxed">
            Upload an image of any device to instantly identify its make and model.
          </p>
        </header>

        <main className={`w-full flex-1 flex ${result ? 'flex-col lg:flex-row gap-8 items-start' : 'flex-col items-center justify-center'} min-h-0 overflow-hidden`}>
          <div className={`${result ? 'w-full lg:w-1/3 shrink-0' : 'w-full'} flex flex-col transition-all duration-500 max-h-full`}>
            <ImageUpload onUpload={handleUpload} isLoading={isLoading} />
            
            {error && (
              <div className="mt-4 p-4 bg-red-500/10 border border-red-500/50 rounded-xl text-red-400 w-full max-w-xl mx-auto text-center shadow-sm">
                <p className="font-semibold">{error}</p>
              </div>
            )}
          </div>
          
          {result && !isLoading && (
            <div className="w-full lg:w-2/3 h-full overflow-hidden flex flex-col animate-fade-in-up">
              <ResultsDisplay result={result} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
