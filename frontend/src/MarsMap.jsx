import { useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import { Style, Circle, Fill, Stroke, Text } from 'ol/style';
import SiteDetailsPanel from './SiteDetailsPanel';
import 'ol/ol.css';

const MarsMap = () => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const previousViewRef = useRef(null);
  const [searchParams] = useSearchParams();
  const [selectedSite, setSelectedSite] = useState(null);
  const [regions, setRegions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cropMatches, setCropMatches] = useState(null);
  const [cropName, setCropName] = useState(null);

  // Get crop parameter from URL
  useEffect(() => {
    const crop = searchParams.get('crop');
    if (crop) {
      setCropName(crop);
      fetchCropMatches(crop);
    }
  }, [searchParams]);

  // Fetch crop matches when crop is selected - THIS RETURNS TOP 5 REGIONS
  const fetchCropMatches = async (crop) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/api/crops/match_crop/?crop=${encodeURIComponent(crop)}&top_n=5`);
      if (response.ok) {
        const data = await response.json();
        setCropMatches(data);
        
        // IMPORTANT: Set regions to ONLY the top 5 matches, not all regions
        if (data.top_matches && data.top_matches.length > 0) {
          const top5Regions = data.top_matches.map(match => ({
            id: match.region_id,
            name: match.region_name,
            latitude: match.latitude,
            longitude: match.longitude,
            elevation: match.elevation,
            ph: match.ph,
            perchlorate_wt_pct: match.perchlorate_wt_pct,
            water_release_wt_pct: match.water_release_wt_pct,
            major_minerals: match.major_minerals,
            terrain_type: match.terrain_type,
            notes: match.notes,
            score: match.score,
            reasons: match.reasons
          }));
          setRegions(top5Regions);
        }
      }
    } catch (error) {
      console.error('Error fetching crop matches:', error);
    } finally {
      setLoading(false);
    }
  };

  // Only fetch regions if no crop is specified (show all for exploration)
  useEffect(() => {
    const crop = searchParams.get('crop');
    
    // If there's no crop query, fetch all regions for exploration
    if (!crop) {
      const fetchAllRegions = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/regions/list_regions/');
          if (response.ok) {
            const data = await response.json();
            setRegions(data);
          }
        } catch (error) {
          console.error('Error fetching regions:', error);
        } finally {
          setLoading(false);
        }
      };
      fetchAllRegions();
    } else {
      setLoading(false);
    }
  }, [searchParams]);

  useEffect(() => {
    if (!mapRef.current || loading) return;

    // Create Mars basemap layer
    const marsLayer = new TileLayer({
      source: new XYZ({
        url: 'https://cartocdn-gusc.global.ssl.fastly.net/opmbuilder/api/v1/map/named/opm-mars-basemap-v0-2/all/{z}/{x}/{y}.png',
        maxZoom: 8,
        zoom: 0,

      })
    });

    // Create vector source for markers
    const vectorSource = new VectorSource();

    // Helper function to parse coordinates
    const parseCoordinates = (coordStr) => {
      if (!coordStr) return null;
      
      // Handle format like "4.5895°S" or "137.4417°E" or "-4.5895"
      const match = coordStr.match(/(-?\d+\.?\d*)°?\s*([NSEW]?)/);
      if (match) {
        let value = parseFloat(match[1]);
        const direction = match[2];
        if (direction === 'S' || direction === 'W') value = -value;
        return value;
      }
      return parseFloat(coordStr);
    };

    // Add markers from regions data
    regions.forEach(region => {
      const lat = parseCoordinates(region.latitude);
      const lon = parseCoordinates(region.longitude);
      
      console.log(`Region: ${region.Region}, Lat: ${region.latitude} -> ${lat}, Lon: ${region.longitude} -> ${lon}`);
      
      if (lat !== null && lon !== null) {
        const marker = new Feature({
          geometry: new Point([lon, lat]),
          regionData: region
        });

        vectorSource.addFeature(marker);
        console.log(`Added marker for ${region.Region} at [${lon}, ${lat}]`);
      } else {
        console.log(`Skipped marker for ${region.Region} - invalid coordinates`);
      }
    });

    // Create vector layer for markers
    const vectorLayer = new VectorLayer({
      source: vectorSource,
      style: new Style({
        image: new Circle({
          radius: 10,
          fill: new Fill({ color: '#ff4444' }),
          stroke: new Stroke({ color: '#ffffff', width: 3 })
        }),
        
      })
    });

    // Create map
    const map = new Map({
      target: mapRef.current,
      layers: [marsLayer, vectorLayer],
      view: new View({
        center: [0, 0], // Center on Mars equator
        zoom: 2,
        projection: 'EPSG:4326'
      })
    });

    // Store map instance for later access
    mapInstanceRef.current = map;

    // Add click handler for markers
    map.on('click', (event) => {
      const feature = map.forEachFeatureAtPixel(event.pixel, (feature) => feature);
      if (feature) {
        const properties = feature.getProperties();
        setSelectedSite(properties.regionData);
      }
    });

    return () => {
      map.setTarget(null);
      mapInstanceRef.current = null;
    };
  }, [regions, loading]);

  // Zoom to region when site is selected
  useEffect(() => {
    if (selectedSite && mapInstanceRef.current) {
      const view = mapInstanceRef.current.getView();
      
      // Save current view state before zooming
      if (!previousViewRef.current) {
        previousViewRef.current = {
          center: view.getCenter(),
          zoom: view.getZoom()
        };
      }
      
      // Parse coordinates
      const parseCoord = (coordStr) => {
        if (!coordStr) return null;
        const match = coordStr.match(/(-?\d+\.?\d*)°?\s*([NSEW]?)/);
        if (match) {
          let value = parseFloat(match[1]);
          const direction = match[2];
          if (direction === 'S' || direction === 'W') value = -value;
          return value;
        }
        return parseFloat(coordStr);
      };
      
      const lat = parseCoord(selectedSite.latitude);
      const lon = parseCoord(selectedSite.longitude);
      
      if (lat !== null && lon !== null) {
        // Animate zoom to region
        view.animate({
          center: [lon, lat],
          zoom: 5,
          duration: 1000
        });
      }
    }
  }, [selectedSite]);

  // Function to zoom back out and return to list view
  const handleClosePanel = () => {
    console.log('Closing panel, returning to list view');
    
    if (mapInstanceRef.current && previousViewRef.current) {
      const view = mapInstanceRef.current.getView();
      
      // Animate back to previous view
      view.animate({
        center: previousViewRef.current.center,
        zoom: previousViewRef.current.zoom,
        duration: 1000
      });
      
      // Clear saved view after animation
      setTimeout(() => {
        previousViewRef.current = null;
      }, 1000);
    }
    
    // Clear selected site to return to list view
    setSelectedSite(null);
  };

  if (loading) {
    return (
      <div className="w-screen h-screen flex items-center justify-center bg-gray-900 text-white">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-500 mx-auto mb-4"></div>
          <p>Loading Mars regions...</p>
        </div>
      </div>
    );
  }

  const getScoreColor = (score) => {
    if (score >= 5) return 'text-green-400'
    if (score >= 2) return 'text-yellow-400'
    if (score >= 0) return 'text-orange-400'
    return 'text-red-400'
  }

  return (
    <div className="w-screen h-screen m-0 p-0 relative">
      {/* Map */}
      <div ref={mapRef} className="w-full h-full" />
      
      {/* Right Panel */}
      <SiteDetailsPanel 
        site={selectedSite} 
        onClose={handleClosePanel}
        cropMatches={cropMatches}
        regions={regions}
        onRegionSelect={setSelectedSite}
      />
    </div>
  );
};

export default MarsMap;

