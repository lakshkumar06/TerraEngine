import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const Search = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const handleSearch = () => {
    if (searchQuery.trim()) {
      console.log('Searching for:', searchQuery)
      // Redirect to map page regardless of search query
      navigate('/map')
    } else {
      // Even if empty, redirect to map
      navigate('/map')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
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

        {/* Search Buttons */}
        <div className="flex gap-4">
          <button
            onClick={handleSearch}
            className="px-6 py-3 text-base bg-gray-600 text-white border-none rounded-md cursor-pointer transition-colors duration-300 hover:bg-gray-500"
          >
            Search
          </button>
          
          <button
            onClick={() => setSearchQuery('')}
            className="px-12 py-3 text-base bg-red-500 text-white border-none rounded-md cursor-pointer transition-colors duration-300 hover:bg-red-600"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="absolute bottom-5 text-sm text-gray-400">
        Search Mars exploration sites and simulator data
      </div>
    </div>
  )
}

export default Search
