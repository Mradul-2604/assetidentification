import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, X } from 'lucide-react';

const ImageUpload = ({ onUpload, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const processFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const handleClear = () => {
    setPreview(null);
    setSelectedFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const handleSubmit = () => {
    if (selectedFile) {
      onUpload(selectedFile);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto backdrop-blur-md bg-surface/80 p-8 rounded-3xl shadow-xl border border-slate-700/50">
      <h2 className="text-2xl font-extrabold mb-6 text-center text-white">Upload Asset Image</h2>
      
      {!preview ? (
        <div 
          className={`relative flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-2xl transition-all duration-300 ease-in-out cursor-pointer ${
            dragActive ? 'border-primary bg-primary/10 scale-[1.02]' : 'border-slate-600 hover:border-primary hover:bg-slate-800/50'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            onChange={handleChange}
            className="hidden"
          />
          <UploadCloud className={`w-16 h-16 mb-4 transition-colors ${dragActive ? 'text-primary' : 'text-slate-400'}`} />
          <p className="text-lg font-bold text-slate-300">Drag & drop your image here</p>
          <p className="text-sm text-slate-500 mt-2 font-medium">or click to browse from device</p>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          <div className="relative w-full rounded-2xl overflow-hidden shadow-md group border border-slate-700">
            <img src={preview} alt="Preview" className="w-full h-auto max-h-80 object-contain bg-black/40" />
            <button 
              onClick={handleClear}
              className="absolute top-3 right-3 bg-red-500/90 hover:bg-red-600 text-white p-2 rounded-full transition-all opacity-0 group-hover:opacity-100 shadow-sm"
              title="Remove image"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className={`mt-6 w-full py-4 rounded-2xl font-extrabold text-lg transition-all duration-300 flex items-center justify-center gap-3 text-white ${
              isLoading 
                ? 'bg-primary/50 cursor-not-allowed shadow-none' 
                : 'bg-gradient-to-r from-primary via-secondary to-accent hover:shadow-[0_10px_25px_rgba(236,72,153,0.4)] transform hover:-translate-y-1'
            }`}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing Image...
              </>
            ) : (
              <>
                <ImageIcon className="w-6 h-6" />
                Identify Asset
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
