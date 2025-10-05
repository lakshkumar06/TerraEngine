import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import RocketAnimation from './RocketAnimation'

const Search = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleSearch = () => {
    if (!searchQuery.trim()) return
    
    setIsLoading(true)
    console.log('Searching for:', searchQuery)
    
    // Extract crop name from search query (simple extraction)
    const cropName = extractCropName(searchQuery)
    
    // Navigate to map with crop parameter
    setTimeout(() => {
      navigate(`/map?crop=${encodeURIComponent(cropName)}`)
    }, 3000)
  }

  const extractCropName = (query) => {
    // Simple crop name extraction - look for common crop keywords
    const cropKeywords = ['tomato', 'carrot', 'cress', 'mustard', 'rye', 'vetch', 'moringa', 'potato', 'wheat', 'corn', 'lettuce', 'spinach']
    
    const lowerQuery = query.toLowerCase()
    for (const keyword of cropKeywords) {
      if (lowerQuery.includes(keyword)) {
        return keyword.charAt(0).toUpperCase() + keyword.slice(1)
      }
    }
    
    // If no specific crop found, try to extract from "like X" patterns
    const likeMatch = query.match(/like\s+([^?]+)/i)
    if (likeMatch) {
      return likeMatch[1].trim()
    }
    
    // Default fallback
    return searchQuery
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="flex flex-col items-center justify-start min-h-screen bg-[#0d0d0d] text-white">
      <RocketAnimation isVisible={isLoading} />

      {/* Hero (full page) */}
      <section
        className="w-full min-h-screen bg-cover bg-center flex flex-col items-center justify-center px-5 relative"
        style={{ backgroundImage: "url('/image.png')" }}
      >
        {/* Gradient overlay over hero background */}
        <div className="absolute inset-0" style={{ background: 'linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #0d0d0d 95%)' }}></div>

        {/* Floating logo top-left */}
        <div className="absolute top-8 left-8 pointer-events-none z-10">
          <img src="/logo.png" alt="TerraEngine logo" className="w-20 h-20 rounded-full" />
        </div>
        {/* Logo/Title */}
        <h1 className="text-8xl heroheading font-medium text-white mb-12 text-center drop-shadow-md z-10">
          TerraEngine
        </h1>

        {/* Search Container */}
        <div className="flex flex-col items-center w-full max-w-3xl z-10">
          {/* Search Bar - pill with outline and right circular button */}
          <div className="relative w-full">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Where can I plant starchy vegetables like Potatoes?"
              className="w-full h-16 text-lg pl-6 pr-20 bg-white/5 text-white placeholder-[#b0b0b0] rounded-full border-2 border-black outline-none"
            />
            <button
              onClick={handleSearch}
              disabled={isLoading || !searchQuery.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-black text-white flex items-center justify-center disabled:opacity-50"
              aria-label="Search"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6">
                <circle cx="11" cy="11" r="7"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </button>
          </div>

          {/* Example queries */}
          <div className="mt-6 text-center text-gray-200">
            <div className="flex flex-wrap justify-center gap-2">
              {['Tomato', 'Carrot', 'Rye', 'Field Mustard'].map((crop) => (
                <button
                  key={crop}
                  onClick={() => setSearchQuery(`Where can I plant ${crop}?`)}
                  className="px-3 py-1 text-sm bg-white/80 text-black rounded-full border border-black hover:bg-white"
                >
                  {crop}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features - text only, minimal */}
      <div className="w-full max-w-6xl px-5 mt-16 mb-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="rounded-2xl border border-gray-700/70 bg-white/5 p-6">
            <h3 className="text-2xl font-semibold mb-3">Interactive Maps</h3>
            <p className="text-gray-300 leading-relaxed">Explore Mars with detailed satellite imagery and site markers.</p>
          
          </div>
          <div className="rounded-2xl border border-gray-700/70 bg-white/5 p-6">
            <h3 className="text-2xl font-semibold mb-3">Site Analysis</h3>
            <p className="text-gray-300 leading-relaxed">Detailed parameters for agricultural simulation and planning.</p>

          </div>
          <div className="rounded-2xl border border-gray-700/70 bg-white/5 p-6">
            <h3 className="text-2xl font-semibold mb-3">Real-time Data</h3>
            <p className="text-gray-300 leading-relaxed">Access current Mars exploration data and research findings.</p>

          </div>
        </div>
      </div>
    </div>
  )
}

export default Search
