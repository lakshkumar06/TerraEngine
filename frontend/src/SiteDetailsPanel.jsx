import React, { useState, useEffect } from 'react'

const SiteDetailsPanel = ({ site, onClose, cropMatches, regions, onRegionSelect }) => {
  const [isClosing, setIsClosing] = useState(false)
  const [aiInsights, setAiInsights] = useState(null)
  const [loadingAI, setLoadingAI] = useState(false)
  const [aiError, setAiError] = useState(null)

  const handleClose = () => {
    setIsClosing(true)
    // Reset AI insights state
    setAiInsights(null)
    setLoadingAI(false)
    setAiError(null)
    
    setTimeout(() => {
      setIsClosing(false) // Reset closing state
      onClose()
    }, 300) // Match animation duration
  }

  const getScoreColor = (score) => {
    if (score >= 5) return 'text-green-400'
    if (score >= 2) return 'text-yellow-400'
    if (score >= 0) return 'text-orange-400'
    return 'text-red-400'
  }

  // Fetch AI insights when a region is selected
  useEffect(() => {
    const fetchAIInsights = async () => {
      // Only fetch if we have a site selected AND crop matches (meaning there's a crop search active)
      if (!site || !cropMatches?.crop) {
        setAiInsights(null)
        return
      }

      // Find the match data for this region
      const regionMatch = cropMatches?.top_matches?.find(match => 
        (match.region_name || match.region) === site.name
      )

      if (!regionMatch) {
        setAiInsights(null)
        return
      }

      setLoadingAI(true)
      setAiError(null)

      try {
        const response = await fetch('http://localhost:8000/api/regions/analyze_region/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            region_name: site.name,
            crop_name: cropMatches.crop,
            score: regionMatch.score
          })
        })

        if (response.ok) {
          const data = await response.json()
          setAiInsights(data.ai_insights)
        } else {
          setAiError('Failed to load AI insights')
        }
      } catch (error) {
        console.error('Error fetching AI insights:', error)
        setAiError('Error connecting to AI service')
      } finally {
        setLoadingAI(false)
      }
    }

    fetchAIInsights()
  }, [site, cropMatches])

  // If no site is selected, show ranked results
  if (!site && cropMatches?.top_matches) {
    return (
      <div className="absolute top-5 right-5 w-106 max-h-[calc(100vh-40px)] overflow-y-auto z-50 rounded-[20px] bg-gray-900 shadow-2xl">
        <div className="text-white p-5">
          <h2 className="text-xl font-semibold mb-4 text-red-400 sticky top-0 bg-gray-900 pb-2 z-10">
            {cropMatches.crop} - Top {cropMatches.top_matches.length} Growing Regions
          </h2>
          
          <div className="space-y-3 pb-4">
            {cropMatches.top_matches.map((match, index) => {
              const regionName = match.region_name || match.region;
              return (
                <div 
                  key={`${regionName}-${index}`}
                  className="bg-gray-800 rounded-lg p-4 cursor-pointer hover:bg-gray-700 transition-colors border border-gray-700 hover:border-red-500"
                  onClick={() => {
                    const region = regions.find(r => r.name === regionName || r.name === match.region);
                    if (region) {
                      console.log('Selecting region:', region);
                      onRegionSelect(region);
                    }
                  }}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-white">
                      #{index + 1} {regionName}
                    </h3>
                    <div className={`text-lg font-bold ${getScoreColor(match.score)}`}>
                      Score: {match.score}
                    </div>
                  </div>

                  <div className="text-xs">
                    <strong>Why this region:</strong>
                    <ul className="mt-1 pl-2 space-y-1">
                      {match.reasons && match.reasons.slice(0, 3).map((reason, reasonIndex) => (
                        <li key={reasonIndex} className="text-gray-300 flex items-start">
                          <span className="text-green-400 mr-1">•</span>
                          <span>{reason}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    )
  }

  // If no site and no crop matches, don't show panel
  if (!site) return null

  // Find the crop match for this region
  const regionMatch = cropMatches?.top_matches?.find(match => 
    (match.region_name || match.region) === site.name
  )

  const getCompatibilityLevel = (score) => {
    if (score >= 5) return { level: 'Excellent', color: 'green', bg: 'bg-green-900/30', border: 'border-green-500' }
    if (score >= 3) return { level: 'Good', color: 'yellow', bg: 'bg-yellow-900/30', border: 'border-yellow-500' }
    if (score >= 1) return { level: 'Moderate', color: 'orange', bg: 'bg-orange-900/30', border: 'border-orange-500' }
    return { level: 'Poor', color: 'red', bg: 'bg-red-900/30', border: 'border-red-500' }
  }

  const getRecommendations = (site, regionMatch) => {
    const recommendations = []
    
    if (site.perchlorate_wt_pct > 0.5) {
      recommendations.push({
        type: 'warning',
        title: 'High Perchlorate Content',
        message: 'Soil treatment required to neutralize perchlorates before planting'
      })
    }
    
    if (site.ph && site.ph.includes('High')) {
      recommendations.push({
        type: 'info',
        title: 'Alkaline Soil',
        message: 'Consider acidifying treatments or select pH-tolerant crop varieties'
      })
    }
    
    if (site.terrain_type && site.terrain_type.includes('smooth')) {
      recommendations.push({
        type: 'success',
        title: 'Suitable Terrain',
        message: 'Flat terrain ideal for automated farming equipment and irrigation systems'
      })
    }
    
    if (regionMatch && regionMatch.score < 3) {
      recommendations.push({
        type: 'warning',
        title: 'Low Compatibility',
        message: 'Consider alternative crops or extensive soil preparation before planting'
      })
    }
    
    return recommendations
  }

  return (
    <div className={`absolute top-5 right-5 w-106 max-h-[calc(100vh-40px)] overflow-y-auto z-50 rounded-[20px] bg-gray-900 shadow-2xl ${isClosing ? 'animate-slide-out-right' : 'animate-slide-in-right'}`}>
      <div className="text-white p-5">
        <button 
          onClick={handleClose}
          className="bg-red-500 text-white border-none px-4 py-2 rounded cursor-pointer mb-5 transition-colors duration-300 hover:bg-red-600 sticky top-0 z-20"
        >
          ← Back to List
        </button>
        
        <h2 className="text-red-500 mb-5 text-xl font-bold">
          {site.name}
        </h2>
        
        {/* Compatibility Overview */}
        {regionMatch && cropMatches && (
          <div className={`mb-6 rounded-lg p-4 border ${getCompatibilityLevel(regionMatch.score).bg} ${getCompatibilityLevel(regionMatch.score).border}`}>
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-lg font-semibold text-white">Growing Compatibility</h3>
              <div className={`text-3xl font-bold text-${getCompatibilityLevel(regionMatch.score).color}-400`}>
                {regionMatch.score}/10
              </div>
            </div>
            <div className={`text-sm font-medium text-${getCompatibilityLevel(regionMatch.score).color}-300`}>
              {getCompatibilityLevel(regionMatch.score).level} match for {cropMatches.crop}
            </div>
          </div>
        )}
        
        {/* AI INSIGHTS SECTION - MIDDLE OF DASHBOARD */}
        {cropMatches && (
          <div className="mb-6">
            <div className="flex items-center mb-3">
              <h3 className="text-red-400 text-lg font-semibold flex items-center">
                <span className="mr-2">🤖</span> AI Insights
              </h3>
              {aiInsights?.enabled && (
                <span className="ml-2 px-2 py-1 text-xs bg-green-900/30 text-green-400 rounded">
                  Powered by Gemini
                </span>
              )}
            </div>
            
            {loadingAI && (
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-500 mr-3"></div>
                  <span className="text-gray-300">Analyzing region with AI...</span>
                </div>
              </div>
            )}
            
            {aiError && (
              <div className="bg-red-900/20 rounded-lg p-4 border border-red-500/30">
                <p className="text-red-300 text-sm">{aiError}</p>
              </div>
            )}
            
            {!loadingAI && !aiError && aiInsights && (
              <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg p-5 border-2 border-red-500/30 shadow-lg">
                <div className="prose prose-invert prose-sm max-w-none">
                  <div className="text-gray-200 whitespace-pre-wrap leading-relaxed" 
                       style={{ fontFamily: 'system-ui, -apple-system, sans-serif' }}>
                    {aiInsights.analysis?.split('\n').map((line, index) => {
                      // Handle markdown-style bold
                      if (line.includes('**')) {
                        const parts = line.split('**')
                        return (
                          <p key={index} className="mb-2">
                            {parts.map((part, i) => 
                              i % 2 === 1 ? <strong key={i} className="text-white font-semibold">{part}</strong> : part
                            )}
                          </p>
                        )
                      }
                      // Handle bullet points
                      if (line.trim().startsWith('*') || line.trim().startsWith('-')) {
                        return (
                          <li key={index} className="ml-4 mb-1 text-gray-300">
                            {line.replace(/^[\*\-]\s*/, '')}
                          </li>
                        )
                      }
                      // Regular paragraphs
                      if (line.trim()) {
                        return <p key={index} className="mb-2 text-gray-300">{line}</p>
                      }
                      return <br key={index} />
                    })}
                  </div>
                </div>
                
                {aiInsights.recommendation_level && (
                  <div className={`mt-4 pt-4 border-t border-gray-700 flex items-center justify-between`}>
                    <span className="text-gray-400 text-sm">AI Recommendation Level:</span>
                    <span className={`px-3 py-1 rounded font-medium text-sm ${
                      aiInsights.recommendation_level === 'highly_recommended' ? 'bg-green-900/30 text-green-400' :
                      aiInsights.recommendation_level === 'recommended' ? 'bg-yellow-900/30 text-yellow-400' :
                      aiInsights.recommendation_level === 'challenging' ? 'bg-orange-900/30 text-orange-400' :
                      'bg-red-900/30 text-red-400'
                    }`}>
                      {aiInsights.recommendation_level.replace('_', ' ').toUpperCase()}
                    </span>
                  </div>
                )}
              </div>
            )}
            
            {!loadingAI && !aiError && !aiInsights && (
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <p className="text-gray-400 text-sm text-center">
                  Select a region from a crop search to see AI-powered insights
                </p>
              </div>
            )}
          </div>
        )}
        
        {/* Key Compatibility Factors */}
        {regionMatch && (
          <div className="mb-6">
            <h3 className="text-red-400 mb-3 text-lg font-semibold">Key Compatibility Factors</h3>
            <div className="space-y-2">
              {regionMatch.reasons.map((reason, index) => (
                <div key={index} className="bg-gray-800 rounded p-3 text-sm">
                  <div className="flex items-start">
                    <span className={`w-2 h-2 rounded-full mt-2 mr-3 ${
                      reason.toLowerCase().includes('good') || reason.toLowerCase().includes('suitable') ? 'bg-green-400' :
                      reason.toLowerCase().includes('moderate') || reason.toLowerCase().includes('acceptable') ? 'bg-yellow-400' :
                      reason.toLowerCase().includes('poor') || reason.toLowerCase().includes('unsuitable') ? 'bg-red-400' : 'bg-gray-400'
                    }`}></span>
                    <span className="text-gray-300">{reason}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Recommendations */}
        {regionMatch && (
          <div className="mb-6">
            <h3 className="text-red-400 mb-3 text-lg font-semibold">Growing Recommendations</h3>
            <div className="space-y-3">
              {getRecommendations(site, regionMatch).map((rec, index) => (
                <div key={index} className={`rounded-lg p-3 border-l-4 ${
                  rec.type === 'success' ? 'bg-green-900/20 border-green-400' :
                  rec.type === 'warning' ? 'bg-yellow-900/20 border-yellow-400' :
                  rec.type === 'info' ? 'bg-blue-900/20 border-blue-400' : 'bg-gray-800'
                }`}>
                  <div className="font-medium text-white text-sm mb-1">{rec.title}</div>
                  <div className="text-gray-300 text-xs">{rec.message}</div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Site Details (Minimized) */}
        <div className="mb-6">
          <h3 className="text-red-400 mb-3 text-lg font-semibold">Site Conditions</h3>
          <div className="bg-gray-800 rounded-lg p-4 text-sm">
            <div className="grid grid-cols-2 gap-3">
              {site.elevation && (
                <div>
                  <div className="text-gray-400 text-xs">Elevation</div>
                  <div className="text-white">{site.elevation} m</div>
                </div>
              )}
              {site.ph && (
                <div>
                  <div className="text-gray-400 text-xs">pH Level</div>
                  <div className="text-white">{site.ph}</div>
                </div>
              )}
              {site.perchlorate_wt_pct && (
                <div>
                  <div className="text-gray-400 text-xs">Perchlorate</div>
                  <div className="text-white">{site.perchlorate_wt_pct}%</div>
                </div>
              )}
              {site.terrain_type && (
                <div>
                  <div className="text-gray-400 text-xs">Terrain</div>
                  <div className="text-white">{site.terrain_type}</div>
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Action Plan */}
        {regionMatch && (
          <div className="mb-6">
            <h3 className="text-red-400 mb-3 text-lg font-semibold">Next Steps</h3>
            <div className="bg-gray-800 rounded-lg p-4">
              <div className="text-sm text-gray-300 space-y-2">
                <div className="flex items-start">
                  <span className="text-red-400 mr-2">1.</span>
                  <span>Assess soil preparation requirements based on compatibility score</span>
                </div>
                <div className="flex items-start">
                  <span className="text-red-400 mr-2">2.</span>
                  <span>Plan irrigation and environmental control systems</span>
                </div>
                <div className="flex items-start">
                  <span className="text-red-400 mr-2">3.</span>
                  <span>Consider crop rotation and companion planting strategies</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default SiteDetailsPanel
