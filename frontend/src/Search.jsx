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
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <RocketAnimation isVisible={isLoading} />
      
      {/* Logo/Title */}
      <h1 className="text-6xl font-bold text-red-500 mb-12 text-center">
        TerraEngine
      </h1>

      {/* Search Container */}
      <div className="flex flex-col items-center w-full max-w-2xl px-5">
        {/* Search Bar */}
        <div className="relative w-full mb-8">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Where can I plant starchy vegetables like Potatoes?"
            className="w-full h-15 text-lg px-5 border-2 border-gray-600 rounded-full bg-gray-800 text-white outline-none transition-colors duration-300 focus:border-red-500"
          />
        </div>

        {/* Search Button */}
        <button
          onClick={handleSearch}
          disabled={isLoading || !searchQuery.trim()}
          className="px-8 py-4 text-lg bg-red-500 text-white border-none rounded-md cursor-pointer transition-colors duration-300 hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Searching...' : 'Find Growing Regions'}
        </button>
      </div>

      {/* Example queries */}
      <div className="mt-8 text-center text-gray-400">
        <p className="mb-2">Try searching for:</p>
        <div className="flex flex-wrap justify-center gap-2">
          {['Tomato', 'Carrot', 'Rye', 'Field Mustard'].map((crop) => (
            <button
              key={crop}
              onClick={() => setSearchQuery(`Where can I plant ${crop}?`)}
              className="px-3 py-1 text-sm bg-gray-800 text-gray-300 rounded-full hover:bg-gray-700 transition-colors"
            >
              {crop}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Search
