'use client';

import { useState, useEffect } from 'react';
import { Search, ArrowLeft, Zap, Activity } from 'lucide-react';
import Image from 'next/image';

interface Manhwa {
  id: number;
  title: string;
  image: string;
  genres?: string;
  tropes?: string;
  description?: string;
  popularity?: number;
}

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedManhwa, setSelectedManhwa] = useState<Manhwa | null>(null);
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [selectedTropes, setSelectedTropes] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<Manhwa[]>([]);
  const [trending, setTrending] = useState<Manhwa[]>([]);
  const [searchResults, setSearchResults] = useState<Manhwa[]>([]);
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/trending')
      .then(res => res.json())
      .then(data => {
        const formattedData = data.map((item: any) => ({
          id: item.id,
          title: item.title,
          image: item.image || 'https://via.placeholder.com/400x560',
        }));
        setTrending(formattedData);
        setIsLoading(false);
      })
      .catch(err => {
        console.error('Error:', err);
        setIsLoading(false);
      });
  }, []);

  const handleSearch = () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }
    const mockResults: Manhwa[] = Array.from({ length: 5 }, (_, i) => ({
      id: 100 + i,
      title: `${searchQuery} Result ${i + 1}`,
      image: `https://via.placeholder.com/400x560`,
    }));
    setSearchResults(mockResults);
  };

  const handleNeuralScan = () => {
    setIsScanning(true);
    setTimeout(() => {
      const mockRecs: Manhwa[] = Array.from({ length: 4 }, (_, i) => ({
        id: 200 + i,
        title: `Recommended ${selectedGenres.join(', ')} ${i + 1}`,
        image: `https://via.placeholder.com/400x200`,
      }));
      setRecommendations(mockRecs);
      setShowRecommendations(true);
      setIsScanning(false);
    }, 2000);
  };

  const toggleGenre = (genre: string) => {
    setSelectedGenres(prev =>
      prev.includes(genre) ? prev.filter(g => g !== genre) : [...prev, genre]
    );
  };

  const toggleTrope = (trope: string) => {
    setSelectedTropes(prev =>
      prev.includes(trope) ? prev.filter(t => t !== trope) : [...prev, trope]
    );
  };

  if (selectedManhwa) {
    return (
      <div className="min-h-screen bg-[#0a0a1a] text-[#e0e0ff] p-4 md:p-8">
        {/* Back Button with Bloom Effect */}
        <button
          onClick={() => setSelectedManhwa(null)}
          className="group mb-6 flex items-center gap-2 px-6 py-3 bg-black/40 border border-white/10 rounded-lg hover:border-cyan-400/50 transition-all duration-300 relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-500/10 to-cyan-500/0 group-hover:animate-pulse"></div>
          <ArrowLeft className="w-5 h-5 text-cyan-400 relative z-10" />
          <span className="font-bold text-cyan-400 relative z-10">RETURN TO HUB</span>
        </button>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Image Column */}
          <div className="space-y-4">
            <div className="relative group overflow-hidden rounded-lg border border-white/10">
              {/* Scanline Overlay */}
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-cyan-500/5 to-transparent animate-pulse pointer-events-none z-10"></div>
              <Image
                src={selectedManhwa.image}
                alt={selectedManhwa.title}
                width={400}
                height={560}
                className="w-full group-hover:scale-105 transition-transform duration-500"
              />
            </div>
            
            
              <a
              href={`https://www.google.com/search?q=${encodeURIComponent(selectedManhwa.title + ' manhwa')}`}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center justify-center gap-2 w-full px-6 py-3 bg-black/40 border border-cyan-400/30 rounded-lg hover:border-cyan-400 hover:shadow-[0_0_20px_rgba(0,255,255,0.3)] transition-all duration-300 relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-500/10 to-cyan-500/0 group-hover:animate-pulse"></div>
              <Search className="w-5 h-5 text-cyan-400 relative z-10" />
              <span className="font-bold text-cyan-400 relative z-10">SEARCH GOOGLE</span>
            </a>
          </div>
          
          {/* Info Column */}
          <div className="lg:col-span-2 space-y-6">
            <h1 className="text-4xl md:text-5xl font-black bg-gradient-to-r from-cyan-400 via-white to-cyan-400 bg-clip-text text-transparent">
              {selectedManhwa.title}
            </h1>
            
            {/* Metadata with Monospace */}
            <div className="space-y-3 font-mono text-sm">
              <div className="flex items-center gap-3 p-3 bg-black/40 border border-white/10 rounded">
                <span className="text-cyan-400 font-bold">STATUS:</span>
                <span className="text-purple-400">⭐ {selectedManhwa.popularity?.toLocaleString()} READS</span>
              </div>
              
              <div className="p-4 bg-black/40 border border-white/10 rounded">
                <div className="text-cyan-400 font-bold mb-2">GENRES:</div>
                <div className="text-gray-300">{selectedManhwa.genres || 'Unknown'}</div>
              </div>
              
              <div className="p-4 bg-black/40 border border-white/10 rounded">
                <div className="text-cyan-400 font-bold mb-2">TROPES:</div>
                <div className="text-gray-300">{selectedManhwa.tropes || 'Unknown'}</div>
              </div>
              
              <div className="p-4 bg-black/40 border border-white/10 rounded">
                <div className="text-cyan-400 font-bold mb-2">DESCRIPTION:</div>
                <div className="text-gray-300 leading-relaxed font-sans">{selectedManhwa.description || 'No description available.'}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a1a] text-[#e0e0ff]">
      {/* Header with Data Stream Loading */}
      <div className="sticky top-0 z-50 bg-[#0a0a1a]/95 backdrop-blur-sm border-b border-cyan-500/20">
        <div className="flex flex-col md:flex-row items-center justify-between p-4 md:p-6 gap-4">
          <h1 className="text-3xl md:text-5xl font-black bg-gradient-to-r from-cyan-400 via-white to-cyan-400 bg-clip-text text-transparent">
            MANHWA INTEL
          </h1>
          <div className="relative w-full md:w-64">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="SEARCH DATABASE..."
              className="w-full px-4 py-3 bg-black/40 border border-cyan-400/30 rounded-lg focus:border-cyan-400 focus:shadow-[0_0_20px_rgba(0,255,255,0.2)] outline-none text-cyan-400 font-mono text-sm placeholder-cyan-400/30 transition-all"
            />
          </div>
        </div>
        {/* Data Stream Progress Bar */}
        {isLoading && (
          <div className="h-0.5 w-full bg-black/40 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-transparent via-cyan-400 to-transparent animate-pulse"></div>
          </div>
        )}
      </div>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="p-4 md:p-6">
          <h3 className="text-xl text-cyan-400 font-mono mb-6">SEARCH RESULTS: {searchQuery}</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 md:gap-4">
            {searchResults.map((item) => (
              <div
                key={item.id}
                className="group relative bg-black/40 border border-white/10 rounded-lg p-2 md:p-3 hover:border-cyan-400/50 hover:shadow-[0_0_20px_rgba(0,255,255,0.2)] transition-all duration-300 cursor-pointer overflow-hidden"
                onClick={() => setSelectedManhwa(item)}
              >
                {/* Scanline Effect */}
                <div className="absolute inset-0 bg-[repeating-linear-gradient(0deg,transparent,transparent_2px,rgba(0,255,255,0.03)_2px,rgba(0,255,255,0.03)_4px)] pointer-events-none"></div>
                <div className="relative overflow-hidden rounded">
                  <Image 
                    src={item.image} 
                    alt={item.title} 
                    width={400} 
                    height={560} 
                    className="w-full h-48 md:h-56 object-cover group-hover:scale-110 transition-transform duration-500" 
                  />
                </div>
                <p className="text-xs mt-2 line-clamp-2 text-gray-300">{item.title}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex flex-col lg:flex-row gap-6 p-4 md:p-6">
        {/* Left - Trending District */}
        <div className="flex-1">
          <h2 className="text-2xl md:text-3xl font-bold text-cyan-400 border-l-4 border-cyan-400 pl-4 mb-6 font-mono">
            TRENDING DISTRICT
          </h2>
          
          {/* Bento Grid - Mobile First (2 cols mobile, 5 cols desktop) */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 md:gap-4 mb-4">
            {trending.slice(0, 5).map((manhwa, i) => (
              <div
                key={manhwa.id}
                className="group relative bg-black/40 border border-white/10 rounded-lg p-2 md:p-3 h-72 md:h-96 hover:border-cyan-400/50 hover:shadow-[0_0_20px_rgba(0,255,255,0.2)] hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden"
                onClick={async () => { 
                  const res = await fetch(`https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/manhwa/${manhwa.id}`); 
                  const data = await res.json(); 
                  setSelectedManhwa(data); 
                }}
              >
                {/* Rank Badge with Glow */}
                <div className="absolute top-2 left-2 w-6 h-6 md:w-7 md:h-7 rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center text-[#0a0a1a] font-black text-xs md:text-sm z-20 shadow-[0_0_10px_rgba(0,255,255,0.5)]">
                  {i + 1}
                </div>
                
                {/* Scanline Overlay */}
                <div className="absolute inset-0 bg-[repeating-linear-gradient(0deg,transparent,transparent_2px,rgba(0,255,255,0.03)_2px,rgba(0,255,255,0.03)_4px)] pointer-events-none z-10"></div>
                
                {/* Image with Zoom Effect */}
                <div className="relative overflow-hidden rounded mb-2">
                  <Image 
                    src={manhwa.image} 
                    alt={manhwa.title} 
                    width={400} 
                    height={560} 
                    className="w-full h-48 md:h-64 object-cover group-hover:scale-110 transition-transform duration-500" 
                  />
                </div>
                
                <p className="text-[10px] md:text-xs line-clamp-2 leading-tight text-gray-300 relative z-10">{manhwa.title}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 md:gap-4">
            {trending.slice(5, 10).map((manhwa, i) => (
              <div
                key={manhwa.id}
                className="group relative bg-black/40 border border-white/10 rounded-lg p-2 md:p-3 h-72 md:h-96 hover:border-cyan-400/50 hover:shadow-[0_0_20px_rgba(0,255,255,0.2)] hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden"
                onClick={async () => { 
                  const res = await fetch(`https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/manhwa/${manhwa.id}`); 
                  const data = await res.json(); 
                  setSelectedManhwa(data); 
                }}
              >
                <div className="absolute top-2 left-2 w-6 h-6 md:w-7 md:h-7 rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center text-[#0a0a1a] font-black text-xs md:text-sm z-20 shadow-[0_0_10px_rgba(0,255,255,0.5)]">
                  {i + 6}
                </div>
                
                <div className="absolute inset-0 bg-[repeating-linear-gradient(0deg,transparent,transparent_2px,rgba(0,255,255,0.03)_2px,rgba(0,255,255,0.03)_4px)] pointer-events-none z-10"></div>
                
                <div className="relative overflow-hidden rounded mb-2">
                  <Image 
                    src={manhwa.image} 
                    alt={manhwa.title} 
                    width={400} 
                    height={560} 
                    className="w-full h-48 md:h-64 object-cover group-hover:scale-110 transition-transform duration-500" 
                  />
                </div>
                
                <p className="text-[10px] md:text-xs line-clamp-2 leading-tight text-gray-300 relative z-10">{manhwa.title}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right - System Menu */}
        <div className="w-full lg:w-80 space-y-6">
          <h2 className="text-2xl md:text-3xl font-bold text-cyan-400 border-l-4 border-cyan-400 pl-4 font-mono">
            SYSTEM MENU
          </h2>

          {/* Genres Selector */}
          <div className="bg-black/40 border border-white/10 rounded-lg p-4 md:p-5">
            <h3 className="text-cyan-400 text-lg font-mono font-bold mb-3 flex items-center gap-2">
              <Activity className="w-4 h-4" />
              GENRES
            </h3>
            <div className="flex flex-wrap gap-2">
              {['ACTION', 'FANTASY', 'ROMANCE', 'THRILLER', 'CYBERPUNK', 'MYSTERY'].map(genre => (
                <button
                  key={genre}
                  onClick={() => toggleGenre(genre)}
                  className={`relative px-3 py-1.5 rounded text-xs font-mono font-bold transition-all duration-300 ${
                    selectedGenres.includes(genre)
                      ? 'bg-cyan-400 text-[#0a0a1a] shadow-[0_0_15px_rgba(0,255,255,0.6)]'
                      : 'bg-black/60 text-cyan-400/60 border border-cyan-400/20 hover:border-cyan-400/50 hover:text-cyan-400'
                  }`}
                >
                  {selectedGenres.includes(genre) && (
                    <span className="absolute -top-1 -right-1 w-2 h-2 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_8px_rgba(0,255,255,0.8)]"></span>
                  )}
                  {genre}
                </button>
              ))}
            </div>
          </div>

          {/* Tropes Selector */}
          <div className="bg-black/40 border border-white/10 rounded-lg p-4 md:p-5">
            <h3 className="text-purple-400 text-lg font-mono font-bold mb-3 flex items-center gap-2">
              <Zap className="w-4 h-4" />
              TROPES
            </h3>
            <div className="flex flex-wrap gap-2">
              {['SYSTEM', 'REINCARNATION', 'CYBER-ENHANCEMENT', 'TIME TRAVEL', 'DUNGEON CRAWL', 'APOCALYPSE'].map(trope => (
                <button
                  key={trope}
                  onClick={() => toggleTrope(trope)}
                  className={`relative px-3 py-1.5 rounded text-xs font-mono font-bold transition-all duration-300 ${
                    selectedTropes.includes(trope)
                      ? 'bg-purple-500 text-[#0a0a1a] shadow-[0_0_15px_rgba(255,0,255,0.6)]'
                      : 'bg-black/60 text-purple-400/60 border border-purple-400/20 hover:border-purple-400/50 hover:text-purple-400'
                  }`}
                >
                  {selectedTropes.includes(trope) && (
                    <span className="absolute -top-1 -right-1 w-2 h-2 bg-purple-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(255,0,255,0.8)]"></span>
                  )}
                  {trope}
                </button>
              ))}
            </div>
          </div>

          {/* Neural Scan Button with Bloom Effect & Scanning Animation */}
          <button
            onClick={handleNeuralScan}
            disabled={isScanning}
            className="group relative w-full px-6 py-4 bg-black/60 border-2 border-cyan-400 rounded-lg overflow-hidden transition-all duration-300 hover:shadow-[0_0_30px_rgba(0,255,255,0.4)] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {/* Bloom Effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-500/20 to-cyan-500/0 group-hover:animate-pulse"></div>
            
            {/* Scanning Animation */}
            {isScanning && (
              <div className="absolute inset-0 overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-cyan-400/30 to-transparent animate-[scan_2s_linear_infinite]"></div>
              </div>
            )}
            
            <span className="relative z-10 font-bold text-cyan-400 text-lg font-mono flex items-center justify-center gap-2">
              {isScanning ? (
                <>
                  <Activity className="w-5 h-5 animate-pulse" />
                  SCANNING...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  INITIATE NEURAL SCAN
                </>
              )}
            </span>
          </button>

          {/* Recommendations */}
          {showRecommendations && (
            <div className="bg-black/40 border border-white/10 rounded-lg p-4 md:p-5 space-y-4">
              <h3 className="text-cyan-400 font-mono font-bold mb-3">RECOMMENDATIONS</h3>
              {recommendations.map(rec => (
                <div
                  key={rec.id}
                  className="group relative cursor-pointer overflow-hidden rounded-lg border border-white/10 hover:border-cyan-400/50 transition-all"
                  onClick={() => setSelectedManhwa(rec)}
                >
                  <div className="absolute inset-0 bg-[repeating-linear-gradient(0deg,transparent,transparent_2px,rgba(0,255,255,0.03)_2px,rgba(0,255,255,0.03)_4px)] pointer-events-none"></div>
                  <Image 
                    src={rec.image} 
                    alt={rec.title} 
                    width={400} 
                    height={560} 
                    className="w-full h-32 md:h-40 object-cover group-hover:scale-105 transition-transform duration-500" 
                  />
                  <p className="text-xs text-center py-2 text-gray-300 bg-black/60">{rec.title}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Add Scanning Animation Keyframes */}
      <style jsx>{`
        @keyframes scan {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
      `}</style>
    </div>
  );
}
