from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from .models import MarsCrop, MarsRegion
from .utils import match_crop_to_regions
from .gemini_integration import get_ai_recommendations
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
        """Match a crop to best regions using Gemini AI - returns top 5 by default."""
        crop_name = request.GET.get('crop')
        top_n = int(request.GET.get('top_n', 5))  # Default to 5 regions
        
        if not crop_name:
            return Response({'error': 'Crop name required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Find the crop
            crop = MarsCrop.objects.filter(crop__icontains=crop_name).first()
            if not crop:
                return Response({'error': f'Crop "{crop_name}" not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Get all regions
            regions_queryset = MarsRegion.objects.all()
            regions_list = []
            for r in regions_queryset:
                regions_list.append({
                    'name': r.region,
                    'region': r.region,
                    'latitude': r.latitude_deg,
                    'longitude': r.longitude_deg,
                    'elevation': r.elevation_m,
                    'elevation_m': r.elevation_m,
                    'ph': r.ph,
                    'perchlorate_wt_pct': r.perchlorate_wt_pct,
                    'water_release_wt_pct': r.water_release_wt_pct,
                    'major_minerals': r.major_minerals,
                    'terrain_type': r.terrain_type,
                    'notes': r.notes
                })
            
            # Prepare crop details for Gemini
            crop_details = {
                'ph_range': crop.preferred_ph_range,
                'soil_texture': crop.terrain_soil_texture,
                'temperature_range': crop.temperature_range_c,
                'moisture_regime': crop.moisture_regime
            }
            
            # Use Gemini AI to recommend regions
            from .gemini_integration import gemini_engine
            gemini_recommendations = gemini_engine.recommend_regions_for_crop(
                crop_name=crop.crop,
                crop_details=crop_details,
                all_regions=regions_list
            )
            
            # Get detailed region information for Gemini-recommended regions
            detailed_matches = []
            for rec in gemini_recommendations[:top_n]:
                region_name = rec.get('region', rec) if isinstance(rec, dict) else rec
                region = MarsRegion.objects.filter(region__icontains=region_name).first()
                if region:
                    detailed_matches.append({
                        'region_id': region.id,
                        'region_name': region.region,
                        'score': rec.get('score', 7.5) if isinstance(rec, dict) else 7.5,
                        'reasons': [rec.get('reason', 'AI-recommended based on crop requirements')] if isinstance(rec, dict) else ['AI-recommended'],
                        'latitude': region.latitude_deg,
                        'longitude': region.longitude_deg,
                        'elevation': region.elevation_m,
                        'ph': region.ph,
                        'perchlorate_wt_pct': region.perchlorate_wt_pct,
                        'water_release_wt_pct': region.water_release_wt_pct,
                        'major_minerals': region.major_minerals,
                        'terrain_type': region.terrain_type,
                        'notes': region.notes
                    })
            
            return Response({
                'crop': crop.crop,
                'crop_details': {
                    'preferred_ph_range': crop.preferred_ph_range,
                    'soil_texture': crop.terrain_soil_texture,
                    'temperature_range': crop.temperature_range_c,
                    'moisture_regime': crop.moisture_regime,
                    'germination': crop.germination_on_mars_simulant,
                    'biomass': crop.biomass,
                    'flowered_seed': crop.flowered_seed
                },
                'top_matches': detailed_matches,
                'total_regions_analyzed': len(regions_list)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def recommend_with_ai(self, request):
        """Use Gemini AI to enhance crop recommendations with insights."""
        crop_name = request.data.get('crop')
        top_n = int(request.data.get('top_n', 5))
        
        if not crop_name:
            return Response({'error': 'Crop name required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get basic recommendations first
            crop = MarsCrop.objects.filter(crop__icontains=crop_name).first()
            if not crop:
                return Response({'error': f'Crop "{crop_name}" not found'}, status=status.HTTP_404_NOT_FOUND)
            
            regions = list(MarsRegion.objects.all())
            matches = match_crop_to_regions(crop, regions, top_n)
            
            # Prepare data for AI analysis
            recommendation_data = {
                'crop': crop.crop,
                'crop_requirements': {
                    'ph_range': crop.preferred_ph_range,
                    'soil_texture': crop.terrain_soil_texture,
                    'temperature_range': crop.temperature_range_c,
                    'moisture_regime': crop.moisture_regime
                },
                'top_regions': matches
            }
            
            # Get AI-powered insights using Gemini
            ai_insights = get_ai_recommendations(recommendation_data, matches)
            
            return Response({
                'crop': crop.crop,
                'recommendations': matches,
                'ai_insights': ai_insights,
                'data': recommendation_data,
                'message': 'AI-enhanced recommendations' if ai_insights.get('enabled') else 'Algorithmic recommendations (Gemini not configured)'
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
    
    @action(detail=False, methods=['post'])
    def analyze_region(self, request):
        """Get AI-powered insights for a specific region and crop combination."""
        region_name = request.data.get('region_name')
        crop_name = request.data.get('crop_name')
        score = request.data.get('score', 0)
        
        if not region_name or not crop_name:
            return Response(
                {'error': 'Both region_name and crop_name are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get region data
            region = MarsRegion.objects.filter(region=region_name).first()
            if not region:
                return Response(
                    {'error': f'Region "{region_name}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get crop data
            crop = MarsCrop.objects.filter(crop__icontains=crop_name).first()
            if not crop:
                return Response(
                    {'error': f'Crop "{crop_name}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare region data for AI
            region_data = {
                'name': region.region,
                'latitude': region.latitude_deg,
                'longitude': region.longitude_deg,
                'elevation': region.elevation_m,
                'ph': region.ph,
                'perchlorate_wt_pct': region.perchlorate_wt_pct,
                'water_release_wt_pct': region.water_release_wt_pct,
                'terrain_type': region.terrain_type,
                'major_minerals': region.major_minerals,
                'notes': region.notes
            }
            
            # Prepare crop details
            crop_details = {
                'ph_range': crop.preferred_ph_range,
                'soil_texture': crop.terrain_soil_texture,
                'temperature_range': crop.temperature_range_c,
                'moisture_regime': crop.moisture_regime
            }
            
            # Get AI insights using Gemini
            from .gemini_integration import gemini_engine
            ai_insights = gemini_engine.analyze_region_compatibility(
                crop_name=crop.crop,
                crop_details=crop_details,
                region_data=region_data,
                score=int(score)
            )
            
            return Response({
                'region': region_name,
                'crop': crop.crop,
                'score': score,
                'ai_insights': ai_insights
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def ask_question(self, request):
        """Interactive Q&A - Ask follow-up questions about a region-crop combination."""
        question = request.data.get('question')
        crop_name = request.data.get('crop_name')
        region_name = request.data.get('region_name')
        score = request.data.get('score', 0)
        conversation_history = request.data.get('conversation_history', [])
        
        if not question or not crop_name or not region_name:
            return Response(
                {'error': 'question, crop_name, and region_name are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Prepare context for AI
            context = {
                'crop_name': crop_name,
                'region_name': region_name,
                'score': score,
                'conversation_history': conversation_history
            }
            
            # Get answer from Gemini
            from .gemini_integration import gemini_engine
            result = gemini_engine.answer_question(question, context)
            
            return Response({
                'question': question,
                'answer': result.get('answer', 'No answer available'),
                'enabled': result.get('enabled', False),
                'crop': crop_name,
                'region': region_name
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def analyze_costs(self, request):
        """Get AI-powered cost analysis for growing a crop in a specific region."""
        region_name = request.data.get('region_name')
        crop_name = request.data.get('crop_name')
        score = request.data.get('score', 0)
        
        if not region_name or not crop_name:
            return Response(
                {'error': 'Both region_name and crop_name are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get region data
            region = MarsRegion.objects.filter(region=region_name).first()
            if not region:
                return Response(
                    {'error': f'Region "{region_name}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get crop data
            crop = MarsCrop.objects.filter(crop__icontains=crop_name).first()
            if not crop:
                return Response(
                    {'error': f'Crop "{crop_name}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare region data
            region_data = {
                'name': region.region,
                'latitude': region.latitude_deg,
                'longitude': region.longitude_deg,
                'elevation': region.elevation_m,
                'ph': region.ph,
                'perchlorate_wt_pct': region.perchlorate_wt_pct,
                'water_release_wt_pct': region.water_release_wt_pct,
                'terrain_type': region.terrain_type,
                'major_minerals': region.major_minerals,
                'notes': region.notes
            }
            
            # Prepare crop details
            crop_details = {
                'ph_range': crop.preferred_ph_range,
                'soil_texture': crop.terrain_soil_texture,
                'temperature_range': crop.temperature_range_c,
                'moisture_regime': crop.moisture_regime
            }
            
            # Get cost analysis using Gemini
            from .gemini_integration import gemini_engine
            cost_analysis = gemini_engine.analyze_cultivation_costs(
                crop_name=crop.crop,
                crop_details=crop_details,
                region_data=region_data,
                score=int(score)
            )
            
            return Response({
                'region': region_name,
                'crop': crop.crop,
                'score': score,
                'cost_analysis': cost_analysis
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def analyze_location(self, request):
        """Analyze an arbitrary location on Mars for crop cultivation."""
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        crop_name = request.data.get('crop_name')
        
        if latitude is None or longitude is None or not crop_name:
            return Response(
                {'error': 'latitude, longitude, and crop_name are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            import hashlib
            import random
            
            # Get crop data
            crop = MarsCrop.objects.filter(crop__icontains=crop_name).first()
            if not crop:
                return Response(
                    {'error': f'Crop "{crop_name}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Generate deterministic data based on lat/long
            location_seed = int(hashlib.md5(f"{latitude}{longitude}".encode()).hexdigest()[:8], 16)
            random.seed(location_seed)
            
            # Generate location metadata
            location_name = f"Mars Location ({float(latitude):.2f}°, {float(longitude):.2f}°)"
            elevation = random.randint(-8000, 21000)  # Mars elevation range
            ph = round(random.uniform(7.5, 9.5), 1)  # Alkaline soil
            perchlorate = round(random.uniform(0.1, 2.0), 2)
            water_content = round(random.uniform(0.5, 5.0), 1)
            
            # Determine terrain type based on latitude
            abs_lat = abs(float(latitude))
            if abs_lat < 30:
                terrain_types = ['Smooth plains', 'Rugged terrain', 'Ancient lakebed']
            elif abs_lat < 60:
                terrain_types = ['Cratered highlands', 'Smooth plains', 'Valley networks']
            else:
                terrain_types = ['Polar layered deposits', 'Ice-rich terrain', 'Smooth plains']
            
            terrain = random.choice(terrain_types)
            
            # Determine major minerals based on region
            if abs_lat < 30:
                minerals = ['Olivine, Pyroxene, Plagioclase', 'Phyllosilicates, Sulfates', 'Hematite, Clay minerals']
            else:
                minerals = ['Pyroxene, Plagioclase', 'Ice, Sulfates', 'Phyllosilicates']
            
            major_minerals = random.choice(minerals)
            
            # Create a temporary region dict for scoring
            temp_region = {
                'region': location_name,
                'latitude_deg': float(latitude),
                'longitude_deg': float(longitude),
                'elevation_m': elevation,
                'ph': ph,
                'perchlorate_wt_pct': perchlorate,
                'water_release_wt_pct': water_content,
                'terrain_type': terrain,
                'major_minerals': major_minerals,
                'notes': f'Analyzed location at {latitude}°, {longitude}°'
            }
            
            # Generate a compatibility score based on various factors
            base_score = random.randint(3, 8)
            
            # Adjust score based on factors
            if perchlorate < 0.5:
                base_score += 1
            if water_content > 3.0:
                base_score += 1
            if 7.5 < ph < 8.5:
                base_score += 0.5
                
            compatibility_score = min(10, max(0, round(base_score, 1)))
            
            # Get crop details
            crop_details = {
                'ph_range': crop.preferred_ph_range,
                'soil_texture': crop.terrain_soil_texture,
                'temperature_range': crop.temperature_range_c,
                'moisture_regime': crop.moisture_regime
            }
            
            from .gemini_integration import gemini_engine
            
            # Get AI analysis
            ai_insights = gemini_engine.analyze_region_compatibility(
                crop_name=crop.crop,
                crop_details=crop_details,
                region_data=temp_region,
                score=int(compatibility_score)
            )
            
            # Get cost analysis
            cost_analysis = gemini_engine.analyze_cultivation_costs(
                crop_name=crop.crop,
                crop_details=crop_details,
                region_data=temp_region,
                score=int(compatibility_score)
            )
            
            return Response({
                'location': {
                    'name': location_name,
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'elevation': elevation,
                    'ph': ph,
                    'perchlorate_wt_pct': perchlorate,
                    'water_release_wt_pct': water_content,
                    'terrain_type': terrain,
                    'major_minerals': major_minerals,
                    'notes': f'AI-analyzed location on Mars'
                },
                'crop': crop.crop,
                'compatibility_score': compatibility_score,
                'ai_insights': ai_insights,
                'cost_analysis': cost_analysis,
                'metadata': {
                    'elevation_description': 'Below Mars mean' if elevation < 0 else 'Above Mars mean',
                    'water_availability': 'High' if water_content > 3 else 'Moderate' if water_content > 1.5 else 'Low',
                    'perchlorate_level': 'High' if perchlorate > 1.0 else 'Moderate' if perchlorate > 0.5 else 'Low',
                    'soil_alkalinity': 'High' if ph > 9 else 'Moderate'
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
