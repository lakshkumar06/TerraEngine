from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from .models import MarsCrop, MarsRegion
from .utils import match_crop_to_regions
import json
import os


class MarsSiteViewSet(viewsets.ViewSet):
    """
    ViewSet for Mars exploration sites data.
    """
    queryset = None  # Using custom actions, not standard CRUD
    
    @action(detail=False, methods=['get'])
    def list_sites(self, request):
        """Return all Mars exploration sites."""
        try:
            # Load data from JSON file (you can replace this with database queries later)
            data = [
                {
                    "id": "SIM-001",
                    "name": "Gale Crater Base (Curiosity Site)",
                    "location": "Near Equatorial/Ancient Lake Bed",
                    "lat": -4.5895,
                    "lon": 137.4417,
                    "simulator_parameters": {
                        "regolith_type": "Fine-Grained Sedimentary",
                        "water_availability": "Moderate (Requires Drilling/Extraction)",
                        "perchlorate_level": "High",
                        "required_pretreatment": "Intensive Regolith Washing/Heating",
                        "required_nutrient_additions": [
                            {"nutrient": "Reactive Nitrogen", "priority": "Critical"},
                            {"nutrient": "Potassium", "priority": "Low"}
                        ],
                        "hazards": ["Perchlorate Toxicity", "Nanophase Iron Oxide"]
                    }
                },
                {
                    "id": "SIM-002",
                    "name": "Utopia Planitia Base (Subsurface Ice)",
                    "location": "Northern Mid-Latitudes/Vast Plain",
                    "lat": 46.7,
                    "lon": 117.6,
                    "simulator_parameters": {
                        "regolith_type": "Volcanic/Basaltic",
                        "water_availability": "High (Subsurface Ice Deposit)",
                        "perchlorate_level": "Variable (Moderate)",
                        "required_pretreatment": "Moderate Washing",
                        "required_nutrient_additions": [
                            {"nutrient": "Reactive Nitrogen", "priority": "Critical"},
                            {"nutrient": "Organic Carbon", "priority": "High"}
                        ],
                        "hazards": ["Seasonal Dust Storms", "Potential Hexavalent Chromium ($Cr^{6+}$)"]
                    }
                }
            ]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def get_site(self, request, pk=None):
        """Return specific Mars exploration site by ID."""
        try:
            # This would typically query a database
            sites = [
                {
                    "id": "SIM-001",
                    "name": "Gale Crater Base (Curiosity Site)",
                    "location": "Near Equatorial/Ancient Lake Bed",
                    "lat": -4.5895,
                    "lon": 137.4417,
                    "simulator_parameters": {
                        "regolith_type": "Fine-Grained Sedimentary",
                        "water_availability": "Moderate (Requires Drilling/Extraction)",
                        "perchlorate_level": "High",
                        "required_pretreatment": "Intensive Regolith Washing/Heating",
                        "required_nutrient_additions": [
                            {"nutrient": "Reactive Nitrogen", "priority": "Critical"},
                            {"nutrient": "Potassium", "priority": "Low"}
                        ],
                        "hazards": ["Perchlorate Toxicity", "Nanophase Iron Oxide"]
                    }
                },
                {
                    "id": "SIM-002",
                    "name": "Utopia Planitia Base (Subsurface Ice)",
                    "location": "Northern Mid-Latitudes/Vast Plain",
                    "lat": 46.7,
                    "lon": 117.6,
                    "simulator_parameters": {
                        "regolith_type": "Volcanic/Basaltic",
                        "water_availability": "High (Subsurface Ice Deposit)",
                        "perchlorate_level": "Variable (Moderate)",
                        "required_pretreatment": "Moderate Washing",
                        "required_nutrient_additions": [
                            {"nutrient": "Reactive Nitrogen", "priority": "Critical"},
                            {"nutrient": "Organic Carbon", "priority": "High"}
                        ],
                        "hazards": ["Seasonal Dust Storms", "Potential Hexavalent Chromium ($Cr^{6+}$)"]
                    }
                }
            ]
            
            site = next((s for s in sites if s['id'] == pk), None)
            if site:
                return Response(site, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Site not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarsCropViewSet(viewsets.ViewSet):
    """
    ViewSet for Mars crops data.
    """
    queryset = MarsCrop.objects.all()
    
    @action(detail=False, methods=['get'])
    def list_crops(self, request):
        """Return all Mars crops."""
        try:
            crops = MarsCrop.objects.all()
            crop_data = []
            for crop in crops:
                crop_data.append({
                    'id': crop.id,
                    'name': crop.crop,
                    'germination': crop.germination_on_mars_simulant,
                    'biomass': crop.biomass,
                    'flowered_seed': crop.flowered_seed,
                    'notes': crop.notes,
                    'preferred_ph_range': crop.preferred_ph_range,
                    'soil_texture': crop.terrain_soil_texture,
                    'temperature_range': crop.temperature_range_c,
                    'humidity_range': crop.humidity_rh_range,
                    'moisture_regime': crop.moisture_regime
                })
            return Response(crop_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def match_crop(self, request):
        """Match a crop to best regions."""
        crop_name = request.GET.get('crop')
        top_n = int(request.GET.get('top_n', 3))
        
        if not crop_name:
            return Response({'error': 'Crop name required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Find the crop
            crop = MarsCrop.objects.filter(crop__icontains=crop_name).first()
            if not crop:
                return Response({'error': f'Crop "{crop_name}" not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Get all regions
            regions = list(MarsRegion.objects.all())
            
            # Run matching algorithm
            matches = match_crop_to_regions(crop, regions, top_n)
            
            return Response({
                'crop': crop.crop,
                'crop_details': {
                    'preferred_ph_range': crop.preferred_ph_range,
                    'soil_texture': crop.terrain_soil_texture,
                    'temperature_range': crop.temperature_range_c,
                    'moisture_regime': crop.moisture_regime
                },
                'top_matches': matches
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarsRegionViewSet(viewsets.ViewSet):
    """
    ViewSet for Mars regions data.
    """
    queryset = MarsRegion.objects.all()
    
    @action(detail=False, methods=['get'])
    def list_regions(self, request):
        """Return all Mars regions."""
        try:
            regions = MarsRegion.objects.all()
            region_data = []
            for region in regions:
                region_data.append({
                    'id': region.id,
                    'name': region.region,
                    'latitude': region.latitude_deg,
                    'longitude': region.longitude_deg,
                    'elevation': region.elevation_m,
                    'perchlorate_wt_pct': region.perchlorate_wt_pct,
                    'water_release_wt_pct': region.water_release_wt_pct,
                    'ph': region.ph,
                    'major_minerals': region.major_minerals,
                    'terrain_type': region.terrain_type,
                    'notes': region.notes
                })
            return Response(region_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
