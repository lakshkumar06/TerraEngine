import { useEffect, useRef, useState } from 'react';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import { Style, Circle, Fill, Stroke } from 'ol/style';
import marsData from './data.json';
import SiteDetailsPanel from './SiteDetailsPanel';
import 'ol/ol.css';

const MarsMap = () => {
  const mapRef = useRef(null);
  const [selectedSite, setSelectedSite] = useState(null);

  useEffect(() => {
    if (!mapRef.current) return;

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

    // Add markers from data.json
    marsData.forEach(site => {
      const marker = new Feature({
        geometry: new Point([site.lon, site.lat]),
        name: site.name,
        location: site.location,
        id: site.id
      });

      vectorSource.addFeature(marker);
    });

    // Create vector layer for markers
    const vectorLayer = new VectorLayer({
      source: vectorSource,
      style: new Style({
        image: new Circle({
          radius: 8,
          fill: new Fill({ color: '#ff4444' }),
          stroke: new Stroke({ color: '#ffffff', width: 3 })
        })
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

    // Add click handler for markers
    map.on('click', (event) => {
      const feature = map.forEachFeatureAtPixel(event.pixel, (feature) => feature);
      if (feature) {
        const properties = feature.getProperties();
        const siteData = marsData.find(site => site.id === properties.id);
        setSelectedSite(siteData);
      }
    });

    return () => {
      map.setTarget(null);
    };
  }, []);

  return (
    <div className="w-screen h-screen m-0 p-0 relative">
      {/* Map */}
      <div ref={mapRef} className="w-full h-full" />
      
      {/* Right Panel */}
      <SiteDetailsPanel 
        site={selectedSite} 
        onClose={() => setSelectedSite(null)} 
      />
    </div>
  );
};

export default MarsMap;

