import React, { useState, useEffect } from 'react';
import { fetchHistory } from '../services/api';

const History = () => {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [brandFilter, setBrandFilter] = useState('');

  const loadHistory = async (brand) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchHistory(brand);
      setHistory(data);
    } catch (err) {
      setError(err.message || 'Failed to load history.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Initial load
    loadHistory('');
  }, []);

  const handleFilterSubmit = (e) => {
    e.preventDefault();
    loadHistory(brandFilter);
  };

  return (
    <div className="w-full h-[calc(100vh-200px)] flex flex-col bg-slate-800/50 backdrop-blur-md rounded-2xl border border-white/10 shadow-2xl overflow-hidden mt-4">
      <div className="p-6 border-b border-white/10 flex flex-col md:flex-row justify-between items-center gap-4 shrink-0">
        <h2 className="text-2xl font-bold text-white">Prediction History</h2>
        <form onSubmit={handleFilterSubmit} className="flex w-full md:w-auto gap-2">
          <input
            type="text"
            placeholder="Filter by Brand (e.g., Samsung)"
            value={brandFilter}
            onChange={(e) => setBrandFilter(e.target.value)}
            className="flex-1 bg-slate-900/50 border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
          <button type="submit" className="bg-primary hover:bg-primary/80 text-white px-4 py-2 rounded-lg font-medium transition-colors">
            Search
          </button>
        </form>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {isLoading && <div className="text-center text-slate-400">Loading history...</div>}
        
        {error && <div className="text-red-400 text-center">{error}</div>}
        
        {!isLoading && !error && history.length === 0 && (
          <div className="text-center text-slate-400 mt-10 text-lg">
            No prediction history available.
          </div>
        )}

        {!isLoading && !error && history.map((item) => (
          <div key={item.id} className="bg-slate-900/50 border border-white/5 rounded-xl p-4 flex flex-col sm:flex-row gap-6 items-center hover:bg-slate-900/80 transition-colors">
            <div className="w-32 h-32 shrink-0 rounded-lg overflow-hidden bg-slate-800/80 border border-white/10 flex items-center justify-center p-2">
              <img 
                src={`http://localhost:8000${item.image_path}`} 
                alt={`${item.brand} ${item.model_name}`} 
                className="max-w-full max-h-full object-contain"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="%234a5568" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>';
                }}
              />
            </div>
            <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-4 gap-y-4 w-full">
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Brand</p>
                <p className="text-lg font-semibold text-white">{item.brand}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Model</p>
                <p className="text-lg font-semibold text-white">{item.model_name}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Confidence</p>
                <p className="text-lg font-semibold text-accent">{item.confidence.toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">Date</p>
                <p className="text-sm text-slate-300">
                  {new Date(item.timestamp).toLocaleString('en-GB', {
                    day: '2-digit', month: 'short', year: 'numeric'
                  })}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default History;
