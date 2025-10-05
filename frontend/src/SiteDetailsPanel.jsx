import React, { useState, useEffect } from 'react'

const SiteDetailsPanel = ({ site, onClose, cropMatches, regions, onRegionSelect }) => {
  const [isClosing, setIsClosing] = useState(false)
  const [aiInsights, setAiInsights] = useState(null)
  const [loadingAI, setLoadingAI] = useState(false)
  const [aiError, setAiError] = useState(null)
  
  // Q&A State
  const [conversation, setConversation] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState('')
  const [askingQuestion, setAskingQuestion] = useState(false)
  
  // Cost Analysis State
  const [costData, setCostData] = useState(null)
  const [loadingCost, setLoadingCost] = useState(false)
  const [costError, setCostError] = useState(null)
  const [showDetailedCosts, setShowDetailedCosts] = useState(false)

  const handleClose = () => {
    setIsClosing(true)
    // Reset AI insights state
    setAiInsights(null)
    setLoadingAI(false)
    setAiError(null)
    // Reset Q&A state
    setConversation([])
    setCurrentQuestion('')
    // Reset cost state
    setCostData(null)
    setLoadingCost(false)
    setCostError(null)
    setShowDetailedCosts(false)
    
    setTimeout(() => {
      setIsClosing(false) // Reset closing state
      onClose()
    }, 300) // Match animation duration
  }

  // Handle asking a question
  const handleAskQuestion = async () => {
    if (!currentQuestion.trim() || !cropMatches?.crop || !site?.name) return
    
    setAskingQuestion(true)
    
    // Find the match data for scoring
    const regionMatch = cropMatches?.top_matches?.find(match => 
      (match.region_name || match.region) === site.name
    )
    
    try {
      const response = await fetch('http://localhost:8000/api/regions/ask_question/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: currentQuestion,
          crop_name: cropMatches.crop,
          region_name: site.name,
          score: regionMatch?.score || 0,
          conversation_history: conversation
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        
        // Add to conversation history
        setConversation(prev => [...prev, {
          question: currentQuestion,
          answer: data.answer
        }])
        
        // Clear input
        setCurrentQuestion('')
      } else {
        console.error('Failed to get answer')
      }
    } catch (error) {
      console.error('Error asking question:', error)
    } finally {
      setAskingQuestion(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleAskQuestion()
    }
  }

  const getScoreColor = (score) => {
    return 'text-gray-300'
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
  
  // Fetch cost analysis when a region is selected
  useEffect(() => {
    const fetchCostAnalysis = async () => {
      // Only fetch if we have a site selected AND crop matches
      if (!site || !cropMatches?.crop) {
        setCostData(null)
        return
      }

      // Find the match data for this region
      const regionMatch = cropMatches?.top_matches?.find(match => 
        (match.region_name || match.region) === site.name
      )

      if (!regionMatch) {
        setCostData(null)
        return
      }

      setLoadingCost(true)
      setCostError(null)

      try {
        const response = await fetch('http://localhost:8000/api/regions/analyze_costs/', {
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
          setCostData(data.cost_analysis)
        } else {
          setCostError('Failed to load cost analysis')
        }
      } catch (error) {
        console.error('Error fetching cost analysis:', error)
        setCostError('Error connecting to cost analysis service')
      } finally {
        setLoadingCost(false)
      }
    }

    fetchCostAnalysis()
  }, [site, cropMatches])

  // If no site is selected, show ranked results
  if (!site && cropMatches?.top_matches) {
    return (
      <div className="absolute top-5 right-5 w-116 max-h-[calc(100vh-40px)] overflow-y-auto z-50 rounded-[20px] bg-gray-900 shadow-2xl hide-scrollbar">
        <div className="text-white p-5">
          <h2 className="text-xl font-semibold mb-4 text-gray-200 sticky top-0 bg-gray-900 pb-2 z-10">
            {cropMatches.crop} - Top {cropMatches.top_matches.length} Growing Regions
          </h2>
          
          <div className="space-y-3 pb-4">
            {cropMatches.top_matches.map((match, index) => {
              const regionName = match.region_name || match.region;
              return (
                <div 
                  key={`${regionName}-${index}`}
                  className="bg-gray-800 rounded-lg p-4 cursor-pointer hover:bg-gray-700 transition-colors border border-gray-700 hover:border-gray-500"
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
    <div className={`absolute top-5 right-5 w-106 max-h-[calc(100vh-40px)] overflow-y-auto z-50 rounded-[20px] bg-gray-900 shadow-2xl hide-scrollbar ${isClosing ? 'animate-slide-out-right' : 'animate-slide-in-right'}`}>
      <div className="text-white p-5">
        <button 
          onClick={handleClose}
          className="bg-gray-700 text-white border-none px-4 py-2 rounded cursor-pointer mb-5 transition-colors duration-300 hover:bg-gray-600 sticky top-0 z-20"
        >
          ←
        </button>
        
        <h2 className="text-gray-200 mb-5 text-xl font-bold">
          {site.name}
        </h2>
        
        {/* Compatibility Overview */}
        {regionMatch && cropMatches && (
          <div className={`mb-6 rounded-lg p-4 border bg-gray-800/50 border-gray-700`}>
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-lg font-semibold text-white">Growing Compatibility</h3>
              <div className={`text-3xl font-bold text-orange-700`}>
                {regionMatch.score}/10
              </div>
            </div>
            <div className={`text-sm font-medium text-gray-300`}>
              {getCompatibilityLevel(regionMatch.score).level} match for {cropMatches.crop}
            </div>
          </div>
        )}
        
        {/* COST ANALYSIS SECTION */}
        {cropMatches && costData && !loadingCost && !costError && (
          <div className="mb-6 space-y-4">
            {/* One-Time Cost */}
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-gray-300 text-sm font-semibold mb-1">One-Time Setup Cost</h3>
                  <p className="text-gray-400 text-xs">Initial investment for infrastructure</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-gray-200">
                    ${(costData.one_time_cost / 1000000).toFixed(2)}M
                  </div>
                  <p className="text-xs text-gray-400">USD</p>
                </div>
              </div>
            </div>
            
            {/* Sustained Cost */}
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-gray-300 text-sm font-semibold mb-1">Annual Sustained Cost</h3>
                  <p className="text-gray-400 text-xs">Yearly operational expenses</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-gray-200">
                    ${(costData.annual_sustained_cost / 1000).toFixed(0)}K
                  </div>
                  <p className="text-xs text-gray-400">USD per year</p>
                </div>
              </div>
            </div>
            
            {/* Detailed Cost Breakdown - Dropdown */}
            <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
              <button
                onClick={() => setShowDetailedCosts(!showDetailedCosts)}
                className="w-full px-4 py-3 flex justify-between items-center hover:bg-gray-750 transition-colors"
              >
                <div className="flex items-center gap-2">
                  <span className="text-white font-semibold text-sm">Detailed Cost Breakdown</span>
                </div>
                <span className={`text-gray-400 transform transition-transform ${showDetailedCosts ? 'rotate-180' : ''}`}>
                  ▼
                </span>
              </button>
              
              {showDetailedCosts && costData.breakdown && (
                <div className="p-4 border-t border-gray-700 bg-gray-900/50">
                  <div className="space-y-3">
                    {/* One-Time Costs */}
                    <div>
                      <h4 className="text-gray-300 font-semibold text-sm mb-2 flex items-center">
                        Initial Setup Costs
                      </h4>
                      <div className="space-y-2 pl-2">
                        {['transportation', 'habitat_construction', 'equipment', 'initial_supplies', 'energy_systems', 'water_recycling', 'soil_preparation', 'climate_control'].map((key) => {
                          const item = costData.breakdown[key];
                          if (!item) return null;
                          return (
                            <div key={key} className="flex justify-between items-start text-xs bg-gray-800/50 p-2 rounded">
                              <div className="flex-1">
                                <div className="text-white font-medium capitalize">
                                  {key.replace(/_/g, ' ')}
                                </div>
                                <div className="text-gray-400 text-xs mt-0.5">{item.description}</div>
                              </div>
                              <div className="text-gray-200 font-bold ml-2 whitespace-nowrap">
                                ${(item.cost / 1000000).toFixed(2)}M
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                    
                    {/* Annual Costs */}
                    <div className="pt-3 border-t border-gray-700">
                      <h4 className="text-gray-300 font-semibold text-sm mb-2 flex items-center">
                        Annual Operating Costs
                      </h4>
                      <div className="space-y-2 pl-2">
                        {['annual_energy', 'annual_water', 'annual_nutrients', 'annual_maintenance', 'annual_labor'].map((key) => {
                          const item = costData.breakdown[key];
                          if (!item) return null;
                          return (
                            <div key={key} className="flex justify-between items-start text-xs bg-gray-800/50 p-2 rounded">
                              <div className="flex-1">
                                <div className="text-white font-medium capitalize">
                                  {key.replace(/annual_/g, '').replace(/_/g, ' ')}
                                </div>
                                <div className="text-gray-400 text-xs mt-0.5">{item.description}</div>
                              </div>
                              <div className="text-gray-200 font-bold ml-2 whitespace-nowrap">
                                ${(item.cost / 1000).toFixed(0)}K
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                    
                    {/* AI Note if fallback */}
                    {costData.note && (
                      <div className="mt-3 p-2 bg-gray-800 border border-gray-700 rounded text-xs text-gray-300">
                        {costData.note}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Loading State for Costs */}
        {cropMatches && loadingCost && (
          <div className="mb-6 bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-300 mr-3"></div>
              <span className="text-gray-300 text-sm">Calculating costs...</span>
            </div>
          </div>
        )}
        
        {/* Error State for Costs */}
        {cropMatches && costError && (
          <div className="mb-6 bg-gray-800 rounded-lg p-4 border border-gray-700">
            <p className="text-gray-300 text-sm">{costError}</p>
          </div>
        )}
        
        {/* AI INSIGHTS SECTION - MIDDLE OF DASHBOARD */}
        {cropMatches && (
          <div className="mb-6">
            <div className="flex items-center mb-3">
              <h3 className="text-gray-200 text-lg font-semibold flex items-center">
                AI Insights
              </h3>
              {aiInsights?.enabled && (
                <span className="ml-2 px-2 py-1 text-xs bg-gray-800 text-gray-300 rounded">
                  Powered by Gemini
                </span>
              )}
            </div>
            
            {loadingAI && (
              <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-300 mr-3"></div>
                  <span className="text-gray-300">Analyzing region with AI...</span>
                </div>
              </div>
            )}
            
            {aiError && (
              <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <p className="text-gray-300 text-sm">{aiError}</p>
              </div>
            )}
            
            {!loadingAI && !aiError && aiInsights && (
              <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg p-5 border border-gray-700 shadow-lg">
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
                    <span className={`px-3 py-1 rounded font-medium text-sm bg-gray-800 text-gray-200`}>
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
        
        {/* INTERACTIVE Q&A SECTION */}
        {cropMatches && aiInsights && !loadingAI && (
          <div className="mb-6">
            <h3 className="text-gray-200 text-lg font-semibold mb-3 flex items-center">
              Ask Questions
            </h3>
            
            {/* Conversation History */}
            {conversation.length > 0 && (
              <div className="space-y-3 mb-4">
                {conversation.map((qa, index) => (
                  <div key={index} className="space-y-2">
                    {/* User Question */}
                    <div className="bg-gray-800 border-l-4 border-gray-600 rounded-r-lg p-3">
                      <div className="text-gray-300 text-xs mb-1 font-semibold">You asked:</div>
                      <div className="text-gray-200 text-sm">{qa.question}</div>
                    </div>
                    
                    {/* AI Answer */}
                    <div className="bg-gray-800 border-l-4 border-gray-600 rounded-r-lg p-3">
                      <div className="text-gray-300 text-xs mb-1 font-semibold">AI Answer:</div>
                      <div className="text-gray-200 text-sm leading-relaxed">{qa.answer}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {/* Question Input */}
            <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <textarea
                value={currentQuestion}
                onChange={(e) => setCurrentQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={`Ask anything about growing ${cropMatches.crop} at ${site.name}...
Examples:
• "What if we use hydroponics instead?"
• "How much water would we need daily?"
• "Can we grow this year-round?"`}
                className="w-full bg-gray-900 text-white p-3 rounded border border-gray-600 focus:border-gray-500 outline-none resize-none text-sm"
                rows="3"
                disabled={askingQuestion}
              />
              
              <div className="flex justify-between items-center mt-3">
                <span className="text-gray-400 text-xs">
                  {conversation.length > 0 && `${conversation.length} question(s) asked`}
                </span>
                <button
                  onClick={handleAskQuestion}
                  disabled={!currentQuestion.trim() || askingQuestion}
                  className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium flex items-center gap-2"
                >
                  {askingQuestion ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-300"></div>
                      Thinking...
                    </>
                  ) : (
                    <>
                      <span>Ask AI</span>
                    </>
                  )}
                </button>
              </div>
              
              {conversation.length === 0 && (
                <div className="mt-3 text-gray-500 text-xs italic">
                  Tip: Ask specific questions about cultivation challenges, timelines, or alternatives
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Key Compatibility Factors */}
        {regionMatch && (
          <div className="mb-6">
            <h3 className="text-gray-200 mb-3 text-lg font-semibold">Key Compatibility Factors</h3>
            <div className="space-y-2">
              {regionMatch.reasons.map((reason, index) => (
                <div key={index} className="bg-gray-800 rounded p-3 text-sm">
                  <div className="flex items-start">
                    <span className={`w-2 h-2 rounded-full mt-2 mr-3 bg-gray-500`}></span>
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
            <h3 className="text-gray-200 mb-3 text-lg font-semibold">Growing Recommendations</h3>
            <div className="space-y-3">
              {getRecommendations(site, regionMatch).map((rec, index) => (
                <div key={index} className={`rounded-lg p-3 border-l-4 bg-gray-800 border-gray-600`}>
                  <div className="font-medium text-white text-sm mb-1">{rec.title}</div>
                  <div className="text-gray-300 text-xs">{rec.message}</div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Site Details (Minimized) */}
        <div className="mb-6">
          <h3 className="text-gray-200 mb-3 text-lg font-semibold">Site Conditions</h3>
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
            <h3 className="text-gray-200 mb-3 text-lg font-semibold">Next Steps</h3>
            <div className="bg-gray-800 rounded-lg p-4">
              <div className="text-sm text-gray-300 space-y-2">
                <div className="flex items-start">
                  <span className="text-gray-400 mr-2">1.</span>
                  <span>Assess soil preparation requirements based on compatibility score</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 mr-2">2.</span>
                  <span>Plan irrigation and environmental control systems</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 mr-2">3.</span>
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
