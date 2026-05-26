import React from 'react';
import { ExternalLink, CheckCircle2, AlertCircle } from 'lucide-react';

const ResultsDisplay = ({ result }) => {
  if (!result) return null;

  const { asset_name, brand, possible_models, note } = result;

  return (
    <div className="w-full h-full flex flex-col space-y-6 animate-fade-in-up">
      {/* Overview Card */}
      <div className="bg-surface/80 backdrop-blur-xl border border-slate-700/50 p-8 rounded-3xl shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h2 className="text-sm font-bold tracking-widest text-primary uppercase mb-2">Analysis Complete</h2>
            <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
              {asset_name}
            </h1>
            <p className="text-xl text-slate-300 mt-3 flex items-center gap-2">
              Brand Detected: <span className="font-bold text-white bg-slate-700 px-3 py-1 rounded-md">{brand}</span>
            </p>
          </div>
          <div className="bg-blue-500/10 border border-blue-500/20 p-5 rounded-2xl max-w-xs shadow-sm">
            <p className="text-sm text-blue-200 flex items-start gap-2 leading-relaxed">
              <CheckCircle2 className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
              {note}
            </p>
          </div>
        </div>
      </div>

      {/* Models Grid */}
      <div className="flex-1 overflow-y-auto pr-2 pb-6 space-y-4">
        <h3 className="text-2xl font-bold px-2 text-white shrink-0">Top Matched Models</h3>
        {possible_models && possible_models.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {possible_models.map((model, idx) => {
              const score = Number(model.confidence || 0);
              const scorePercentage = Math.round(score * 100);
              
              return (
              <div 
                key={idx} 
                className={`relative overflow-hidden rounded-2xl bg-surface border transition-all duration-300 hover:shadow-[0_0_15px_rgba(59,130,246,0.2)] hover:-translate-y-2 ${
                  idx === 0 ? 'border-primary shadow-lg' : 'border-slate-700 hover:border-slate-500'
                }`}
              >
                {idx === 0 && (
                  <div className="absolute top-0 left-0 w-full bg-gradient-to-r from-primary via-secondary to-accent text-center py-1.5 text-xs font-bold uppercase tracking-widest text-white shadow-sm z-10">
                    Best Match
                  </div>
                )}
                
                {model.image_url ? (
                  <div className="h-48 w-full bg-white p-6 flex items-center justify-center mt-6">
                    <img src={model.image_url} alt={model.model_name} className="max-h-full max-w-full object-contain mix-blend-multiply drop-shadow-sm" />
                  </div>
                ) : (
                  <div className="h-48 w-full bg-slate-800 flex items-center justify-center text-slate-500 mt-6">
                    <ImageIcon className="w-12 h-12 opacity-50" />
                  </div>
                )}
                
                <div className="p-6">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Model No.</span>
                    <span className={`text-xs font-extrabold px-2.5 py-1 rounded-full shadow-sm ${
                      score > 0.7 ? 'bg-green-500/20 text-green-400' : 
                      score > 0.4 ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'
                    }`}>
                      {scorePercentage}% Match
                    </span>
                  </div>
                  <h4 className="text-xl font-black text-white mb-1 truncate" title={model.model_number}>{model.model_number}</h4>
                  <p className="text-sm text-slate-400 line-clamp-2 mb-4 h-10 font-medium">{model.model_name}</p>
                  
                  <a 
                    href={model.source} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 text-sm font-bold text-primary hover:text-secondary transition-colors"
                  >
                    View Source <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>
            )})}
          </div>
        ) : (
          <div className="p-10 text-center bg-surface border border-slate-700 rounded-2xl shadow-sm">
            <AlertCircle className="w-12 h-12 text-slate-400 mx-auto mb-4" />
            <p className="text-lg text-slate-300 font-medium">No matching models found.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Simple ImageIcon component for fallback
const ImageIcon = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
    <circle cx="8.5" cy="8.5" r="1.5"></circle>
    <polyline points="21 15 16 10 5 21"></polyline>
  </svg>
);

export default ResultsDisplay;
