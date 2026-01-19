'use client';

import { useState, useEffect } from 'react';
import { Search, ArrowLeft } from 'lucide-react';
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

  // Mock data
  useEffect(() => {
    fetch('https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/trending')
      .then(res => res.json())
      .then(data => {
        const formattedData = data.map((item: any, i: number) => ({
          id: item.id,
          title: item.title,
          image: item.image || 'https://via.placeholder.com/400x560',
        }));
        setTrending(formattedData);
      })
      .catch(err => console.error('Error:', err));
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
    const mockRecs: Manhwa[] = Array.from({ length: 4 }, (_, i) => ({
      id: 200 + i,
      title: `Recommended ${selectedGenres.join(', ')} ${i + 1}`,
      image: `https://via.placeholder.com/400x200`,
    }));
    setRecommendations(mockRecs);
    setShowRecommendations(true);
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
      <div className="min-h-screen bg-gradient-to-br from-[#0a0a1a] via-[#1a1a2e] to-[#16213e] text-[#e0e0ff] p-8">
        <button
          onClick={() => setSelectedManhwa(null)}
          className="mb-6 flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border-2 border-cyan-400 rounded-lg shadow-[0_0_15px_rgba(0,255,255,0.5)] hover:shadow-[0_0_25px_rgba(0,255,255,0.8)] hover:-translate-y-0.5 transition-all font-bold text-cyan-400"
        >
          <ArrowLeft className="w-5 h-5" />
          BACK TO NEURAL HUB
        </button>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-4">
            <Image
              src={selectedManhwa.image}
              alt={selectedManhwa.title}
              width={400}
              height={560}
              className="w-full rounded-lg shadow-lg hover:scale-105 transition-transform"
            />
            
            <a
              href={`https://www.google.com/search?q=${encodeURIComponent(selectedManhwa.title + ' manhwa')}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full px-6 py-3 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border-2 border-cyan-400 rounded-lg shadow-[0_0_15px_rgba(0,255,255,0.5)] hover:shadow-[0_0_25px_rgba(0,255,255,0.8)] transition-all font-bold text-cyan-400"
            >
              <Search className="w-5 h-5" />
              Search on Google
            </a>
        </div>
          
          <div className="md:col-span-2 space-y-4">
            <h1 className="text-5xl font-black bg-gradient-to-r from-cyan-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent animate-pulse">
              {selectedManhwa.title}
            </h1>
            <p className="text-purple-400 text-xl">⭐ Popularity: {selectedManhwa.popularity}</p>
            <p><strong className="text-cyan-400">Genres:</strong> {selectedManhwa.genres}</p>
            <p><strong className="text-cyan-400">Tropes:</strong> {selectedManhwa.tropes}</p>
            <p className="text-gray-300 leading-relaxed"><strong className="text-cyan-400">Description:</strong> {selectedManhwa.description}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a1a] via-[#1a1a2e] to-[#16213e] text-[#e0e0ff]">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-cyan-500/30">
        <h1 className="text-5xl font-black bg-gradient-to-r from-cyan-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent animate-pulse drop-shadow-[0_0_20px_rgba(0,255,255,0.7)]">
          MANHWA INTEL
        </h1>
        <div className="relative w-64">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="🔍 Search..."
            className="w-full px-4 py-3 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border-2 border-cyan-400 rounded-lg shadow-[0_0_15px_rgba(0,255,255,0.5)] focus:shadow-[0_0_25px_rgba(0,255,255,0.8)] outline-none text-cyan-400 font-bold placeholder-cyan-400/50"
          />
        </div>
      </div>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="p-6">
          <h3 className="text-2xl text-cyan-400 text-center mb-6">Search: {searchQuery}</h3>
          <div className="grid grid-cols-5 gap-4">
            {searchResults.map((item) => (
              <div
                key={item.id}
                className="bg-[#0a0a1a]/80 border-2 border-transparent bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-lg p-3 h-80 hover:-translate-y-1.5 hover:shadow-[0_0_25px_rgba(0,255,255,0.5)] transition-all cursor-pointer"
                onClick={() => setSelectedManhwa(item)}
              >
                <Image src={item.image} alt={item.title} width={400} height={560} className="w-full h-56 object-cover rounded" />
                <p className="text-xs mt-2 line-clamp-2">{item.title}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex gap-6 p-6">
        {/* Left - Trending */}
        <div className="flex-1">
          <h2 className="text-3xl font-bold text-cyan-400 border-l-4 border-purple-500 pl-4 mb-6">
            𓊝 TRENDING DISTRICT
          </h2>
          
          <div className="grid grid-cols-5 gap-4 mb-4">
            {trending.slice(0, 5).map((manhwa, i) => (
              <div
                key={manhwa.id}
                className="relative bg-[#0a0a1a]/80 border-2 border-transparent bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-lg p-3 h-96 hover:-translate-y-1.5 hover:shadow-[0_0_25px_rgba(0,255,255,0.5)] transition-all cursor-pointer"
                onClick={async () => { const res = await fetch(`https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/manhwa/${manhwa.id}`); const data = await res.json(); setSelectedManhwa(data); }}
              >
                <div className="absolute top-3 left-3 w-7 h-7 rounded-full bg-gradient-to-r from-purple-500 to-cyan-400 flex items-center justify-center text-[#0a0a1a] font-black text-sm">
                  {i + 1}
                </div>
                <Image src={manhwa.image} alt={manhwa.title} width={400} height={560} className="w-full h-64 object-cover rounded" /> 
                <p className="text-xs mt-2 line-clamp-2 leading-tight">{manhwa.title}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-5 gap-4">
            {trending.slice(5, 10).map((manhwa, i) => (
              <div
                key={manhwa.id}
                className="relative bg-[#0a0a1a]/80 border-2 border-transparent bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-lg p-3 h-96 hover:-translate-y-1.5 hover:shadow-[0_0_25px_rgba(0,255,255,0.5)] transition-all cursor-pointer"
                onClick={async () => { const res = await fetch(`https://fuzzy-space-system-7v6gv6qwq79xfw5w6-8000.app.github.dev/manhwa/${manhwa.id}`); const data = await res.json(); setSelectedManhwa(data); }}
              >
                <div className="absolute top-3 left-3 w-7 h-7 rounded-full bg-gradient-to-r from-purple-500 to-cyan-400 flex items-center justify-center text-[#0a0a1a] font-black text-sm">
                  {i + 6}
                </div>
                <Image src={manhwa.image} alt={manhwa.title} width={400} height={560} className="w-full h-64 object-cover rounded" />
            
                <p className="text-xs mt-2 line-clamp-2 leading-tight">{manhwa.title}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right - Neural Interface */}
        <div className="w-80 space-y-6">
          <h2 className="text-3xl font-bold text-cyan-400 border-l-4 border-purple-500 pl-4">
            𓊝 NEURAL INTERFACE
          </h2>

          {/* Genres */}
          <div className="bg-[#0a0a1a]/80 border-2 border-transparent bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-lg p-5">
            <h3 className="text-cyan-400 text-xl font-bold mb-3">GENRES</h3>
            <div className="flex flex-wrap gap-2">
              {['ACTION', 'FANTASY', 'ROMANCE', 'THRILLER', 'CYBERPUNK', 'MYSTERY'].map(genre => (
                <button
                  key={genre}
                  onClick={() => toggleGenre(genre)}
                  className={`px-3 py-1.5 rounded text-xs font-bold transition-all ${
                    selectedGenres.includes(genre)
                      ? 'bg-cyan-400 text-[#0a0a1a] shadow-[0_0_15px_rgba(0,255,255,0.5)]'
                      : 'bg-gray-700/50 text-cyan-400 border border-cyan-400/30'
                  }`}
                >
                  {genre}
                </button>
              ))}
            </div>
          </div>

          {/* Tropes */}
          <div className="bg-[#0a0a1a]/80 border-2 border-transparent bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-lg p-5">
            <h3 className="text-cyan-400 text-xl font-bold mb-3">TROPES</h3>
            <div className="flex flex-wrap gap-2">
              {['SYSTEM', 'REINCARNATION', 'CYBER-ENHANCEMENT', 'TIME TRAVEL', 'DUNGEON CRAWL', 'APOCALYPSE'].map(trope => (
                <button
                  key={trope}
                  onClick={() => toggleTrope(trope)}
                  className={`px-3 py-1.5 rounded text-xs font-bold transition-all ${
                    selectedTropes.includes(trope)
                      ? 'bg-purple-500 text-[#0a0a1a] shadow-[0_0_15px_rgba(255,0,255,0.5)]'
                      : 'bg-gray-700/50 text-purple-400 border border-purple-400/30'
                  }`}
                >
                  {trope}
                </button>
              ))}
            </div>
          </div>

          {/* Scan Button */}
          <button
            onClick={handleNeuralScan}
            className="w-full px-6 py-4 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border-2 border-cyan-400 rounded-lg shadow-[0_0_15px_rgba(0,255,255,0.5)] hover:shadow-[0_0_25px_rgba(0,255,255,0.8)] hover:-translate-y-0.5 transition-all font-bold text-cyan-400 text-lg"
          >
            𓊝 INITIATE NEURAL SCAN
          </button>

          {/* Recommendations */}
          {showRecommendations && (
            <div className="bg-[#0a0a1a]/80 border-2 border-transparent bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-lg p-5 space-y-4">
              {recommendations.map(rec => (
                <div
                  key={rec.id}
                  className="cursor-pointer hover:opacity-80 transition-opacity"
                  onClick={() => setSelectedManhwa(rec)}
                >
                  <Image src={rec.image} alt={rec.title} width={400} height={560} className="w-full h-40 object-cover rounded-lg" />
                  <p className="text-xs text-center mt-2">{rec.title}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}