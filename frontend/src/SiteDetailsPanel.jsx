import React, { useState } from 'react'

const SiteDetailsPanel = ({ site, onClose, cropMatches, regions, onRegionSelect }) => {
  const [isClosing, setIsClosing] = useState(false)

  const handleClose = () => {
    setIsClosing(true)
    setTimeout(() => {
      onClose()
    }, 300) // Match animation duration
  }

  const getScoreColor = (score) => {
    if (score >= 5) return 'text-green-400'
    if (score >= 2) return 'text-yellow-400'
    if (score >= 0) return 'text-orange-400'
    return 'text-red-400'
  }

  // If no site is selected, show ranked results
  if (!site && cropMatches?.top_matches) {
    return (
      <div className={`absolute top-5 right-5 w-106 overflow-y-scroll  bottom-5  z-50 rounded-[20px] bg-gray-900`}>
        <div className="h-full  text-white p-5 ">
          <h2 className="text-xl font-semibold mb-4 text-red-400">
            {cropMatches.crop} - Best Growing Regions
          </h2>
          
          <div className="space-y-3">
            {cropMatches.top_matches.map((match, index) => (
              <div 
                key={index} 
                className="bg-gray-800 rounded-lg p-4 cursor-pointer hover:bg-gray-700 transition-colors"
                onClick={() => {
                  const region = regions.find(r => r.name === match.region);
                  if (region) onRegionSelect(region);
                }}
              >
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-white">
                    #{index + 1} {match.region}
                  </h3>
                  <div className={`text-lg font-bold ${getScoreColor(match.score)}`}>
                    {match.score}
                  </div>
                </div>

                <div className="text-xs">
                  <strong>Key factors:</strong>
                  <ul className="mt-1 pl-2">
                    {match.reasons.slice(0, 3).map((reason, reasonIndex) => (
                      <li key={reasonIndex} className="text-gray-300">
                        {reason}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // If no site and no crop matches, don't show panel
  if (!site) return null

  // Find the crop match for this region
  const regionMatch = cropMatches?.top_matches?.find(match => match.region === site.name)

  return (
    <div className={`absolute top-5 right-5 w-106 overflow-y-scroll  bottom-5  z-50 rounded-[20px] bg-gray-900 ${isClosing ? 'animate-slide-out-right' : 'animate-slide-in-right'}`}>
      <div className="h-full bg-gray-900 text-white p-5 rounded-[20px]">
      <button 
        onClick={handleClose}
        className="bg-red-500 text-white border-none px-4 py-2 rounded cursor-pointer mb-5 transition-colors duration-300 hover:bg-red-600"
      >
        Close
      </button>
      
      <h2 className="text-red-500 mb-5 text-xl font-bold">
        {site.name}
      </h2>
      
      <div className="mb-4">
        <strong>Coordinates:</strong><br />
        Latitude: {site.latitude}<br />
        Longitude: {site.longitude}
      </div>
      
      {site.elevation && (
        <div className="mb-4">
          <strong>Elevation:</strong> {site.elevation} m
        </div>
      )}
      
      {site.ph && (
        <div className="mb-4">
          <strong>pH Level:</strong> {site.ph}
        </div>
      )}
      
      {site.perchlorate_wt_pct && (
        <div className="mb-4">
          <strong>Perchlorate:</strong> {site.perchlorate_wt_pct}%
        </div>
      )}
      
      {site.water_release_wt_pct && (
        <div className="mb-4">
          <strong>Water Release:</strong> {site.water_release_wt_pct}%
        </div>
      )}
      
      {site.terrain_type && (
        <div className="mb-4">
          <strong>Terrain Type:</strong> {site.terrain_type}
        </div>
      )}
      
      {site.major_minerals && (
        <div className="mb-4">
          <strong>Major Minerals:</strong> {site.major_minerals}
        </div>
      )}
      
      {site.notes && (
        <div className="mb-6">
          <strong>Notes:</strong> {site.notes}
        </div>
      )}
      
      {/* Crop Compatibility Section */}
      {regionMatch && cropMatches && (
        <div className="mt-6 border-t border-gray-700 pt-6">
          <h3 className="text-red-500 mb-4 text-lg font-semibold">
            {cropMatches.crop} Compatibility
          </h3>
          
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <div className="flex justify-between items-center mb-3">
              <h4 className="font-semibold text-white">Compatibility Score</h4>
              <div className={`text-2xl font-bold ${
                regionMatch.score >= 5 ? 'text-green-400' :
                regionMatch.score >= 2 ? 'text-yellow-400' :
                regionMatch.score >= 0 ? 'text-orange-400' : 'text-red-400'
              }`}>
                {regionMatch.score}
              </div>
            </div>
            
            <div className="text-sm">
              <strong>Compatibility Factors:</strong>
              <ul className="mt-2 pl-4">
                {regionMatch.reasons.map((reason, index) => (
                  <li key={index} className="text-gray-300 mb-1">
                    • {reason}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
      
    </div>
    </div>
  )
}

export default SiteDetailsPanel
