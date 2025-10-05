import React, { useState, useEffect } from 'react'

const SiteDetailsPanel = ({ site, onClose }) => {
  const [isClosing, setIsClosing] = useState(false)

  const handleClose = () => {
    setIsClosing(true)
    setTimeout(() => {
      onClose()
    }, 300) // Match animation duration
  }

  if (!site) return null

  return (
    <div className={`absolute top-0 right-0 w-106 py-5 pr-5 h-screen overflow-y-auto z-50 ${isClosing ? 'animate-slide-out-right' : 'animate-slide-in-right'}`}>
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
        <strong>ID:</strong> {site.id}
      </div>
      
      <div className="mb-4">
        <strong>Location:</strong> {site.location}
      </div>
      
      <div className="mb-4">
        <strong>Coordinates:</strong><br />
        Latitude: {site.lat}°<br />
        Longitude: {site.lon}°
      </div>
      
      <h3 className="text-red-500 mt-6 mb-4 text-lg font-semibold">
        Simulator Parameters
      </h3>
      
      <div className="mb-3">
        <strong>Regolith Type:</strong> {site.simulator_parameters.regolith_type}
      </div>
      
      <div className="mb-3">
        <strong>Water Availability:</strong> {site.simulator_parameters.water_availability}
      </div>
      
      <div className="mb-3">
        <strong>Perchlorate Level:</strong> {site.simulator_parameters.perchlorate_level}
      </div>
      
      <div className="mb-3">
        <strong>Required Pretreatment:</strong> {site.simulator_parameters.required_pretreatment}
      </div>
      
      <div className="mb-4">
        <strong>Required Nutrient Additions:</strong>
        <ul className="mt-1 pl-5">
          {site.simulator_parameters.required_nutrient_additions.map((nutrient, index) => (
            <li key={index}>
              {nutrient.nutrient} - <span className={nutrient.priority === 'Critical' ? 'text-red-500' : 'text-orange-400'}>{nutrient.priority}</span>
            </li>
          ))}
        </ul>
      </div>
      
      <div>
        <strong>Hazards:</strong>
        <ul className="mt-1 pl-5">
          {site.simulator_parameters.hazards.map((hazard, index) => (
            <li key={index} className="text-red-400">{hazard}</li>
          ))}
        </ul>
      </div>
    </div>
    </div>
  )
}

export default SiteDetailsPanel
