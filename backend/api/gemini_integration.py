"""
Gemini AI Integration for TerraEngine
This module provides AI-powered insights for Mars crop recommendations
"""

import os
import json
from typing import Dict, List, Any

try:
    from decouple import config
    GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
except:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', None)


class GeminiRecommendationEngine:
    """
    AI-powered recommendation engine using Google Gemini
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini AI client
        
        Args:
            api_key: Google Gemini API key (if not provided, uses environment variable)
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.enabled = bool(self.api_key)
        
        if self.enabled:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                print("✅ Gemini AI initialized successfully with gemini-2.0-flash!")
            except Exception as e:
                print(f"Warning: Could not initialize Gemini AI: {e}")
                self.enabled = False
    
    def generate_crop_insights(self, crop_data: Dict, regions: List[Dict]) -> Dict[str, Any]:
        """
        Generate AI-powered insights for crop recommendations
        
        Args:
            crop_data: Dictionary containing crop information and requirements
            regions: List of top matching regions with scores
            
        Returns:
            Dictionary containing AI-generated insights and recommendations
        """
        if not self.enabled:
            return {
                'enabled': False,
                'message': 'Gemini AI not configured. Using algorithmic recommendations.',
                'recommendation': self._generate_fallback_insights(crop_data, regions)
            }
        
        try:
            # Prepare prompt for Gemini
            prompt = self._create_analysis_prompt(crop_data, regions)
            
            # Generate content using Gemini AI
            response = self.model.generate_content(prompt)
            ai_text = response.text
            
            return {
                'enabled': True,
                'insights': ai_text,
                'analysis': self._parse_ai_response(ai_text),
                'confidence': 'high'
            }
            
        except Exception as e:
            print(f"Error generating AI insights: {e}")
            return {
                'enabled': False,
                'error': str(e),
                'recommendation': self._generate_fallback_insights(crop_data, regions)
            }
    
    def _create_analysis_prompt(self, crop_data: Dict, regions: List[Dict]) -> str:
        """Create a detailed prompt for Gemini AI analysis"""
        
        crop_name = crop_data.get('crop', 'Unknown')
        crop_reqs = crop_data.get('crop_requirements', {})
        
        prompt = f"""
You are an expert in Mars agriculture and terraforming. Analyze the following data and provide insights.

CROP: {crop_name}
REQUIREMENTS:
- pH Range: {crop_reqs.get('ph_range', 'Unknown')}
- Soil Texture: {crop_reqs.get('soil_texture', 'Unknown')}
- Temperature Range: {crop_reqs.get('temperature_range', 'Unknown')}
- Moisture Regime: {crop_reqs.get('moisture_regime', 'Unknown')}

TOP RECOMMENDED REGIONS:
"""
        
        for idx, region in enumerate(regions[:5], 1):
            prompt += f"\n{idx}. {region.get('region', 'Unknown')} (Score: {region.get('score', 0)})"
            prompt += f"\n   Reasons: {', '.join(region.get('reasons', [])[:3])}\n"
        
        prompt += """

Please provide:
1. A brief summary of why these regions are suitable for this crop
2. Key challenges to address for successful cultivation
3. Specific recommendations for soil preparation and environmental control
4. Estimated success probability for each of the top 3 regions

Keep the response concise and actionable for Mars colonization planners.
"""
        
        return prompt
    
    def _generate_fallback_insights(self, crop_data: Dict, regions: List[Dict]) -> str:
        """Generate basic insights without AI (fallback mode)"""
        
        crop_name = crop_data.get('crop', 'this crop')
        
        if not regions:
            return f"No suitable regions found for {crop_name}. Consider environmental modifications or alternative crops."
        
        top_region = regions[0]
        score = top_region.get('score', 0)
        
        if score >= 5:
            quality = "excellent"
            outlook = "highly recommended"
        elif score >= 3:
            quality = "good"
            outlook = "recommended with moderate preparation"
        elif score >= 0:
            quality = "moderate"
            outlook = "possible with significant soil treatment"
        else:
            quality = "poor"
            outlook = "not recommended without extensive terraforming"
        
        insights = f"""
Based on analysis of 31 Martian regions, {crop_name} shows {quality} compatibility with the identified locations.

TOP RECOMMENDATION: {top_region.get('region', 'Unknown')}
- Compatibility Score: {score}/10
- Key advantages: {', '.join(top_region.get('reasons', [])[:2])}

CULTIVATION OUTLOOK: {outlook.capitalize()}

NEXT STEPS:
1. Conduct detailed soil analysis for perchlorate and heavy metal content
2. Plan irrigation systems based on local water availability
3. Design environmental control systems for temperature and humidity regulation
4. Establish nutrient supplementation protocols

For best results, consider implementing controlled environment agriculture (CEA) with Martian regolith enrichment.
"""
        
        return insights.strip()
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response into structured data"""
        
        return {
            'summary': response_text[:200] + '...' if len(response_text) > 200 else response_text,
            'full_text': response_text,
            'recommendations_count': response_text.count('•') + response_text.count('1.')
        }
    
    def analyze_region_compatibility(self, crop_name: str, crop_details: Dict, region_data: Dict, score: int) -> Dict:
        """
        Analyze a specific region's compatibility with a crop
        
        Args:
            crop_name: Name of the crop
            crop_details: Dictionary with crop requirements
            region_data: Dictionary containing region information
            score: Compatibility score from algorithm
            
        Returns:
            Dictionary with detailed compatibility analysis
        """
        if not self.enabled:
            return {
                'enabled': False,
                'message': 'AI analysis not available',
                'analysis': self._generate_fallback_region_analysis(crop_name, region_data, score)
            }
        
        try:
            # Create detailed prompt for region-specific analysis
            prompt = f"""You are an expert in Mars agriculture and terraforming. Analyze this specific Martian region for growing {crop_name}.

REGION: {region_data.get('name', 'Unknown')}
COMPATIBILITY SCORE: {score}/10

CROP REQUIREMENTS:
- pH Range: {crop_details.get('ph_range', 'Unknown')}
- Soil Texture: {crop_details.get('soil_texture', 'Unknown')}
- Temperature: {crop_details.get('temperature_range', 'Unknown')}
- Moisture: {crop_details.get('moisture_regime', 'Unknown')}

REGION CONDITIONS:
- Location: {region_data.get('latitude', 'Unknown')}, {region_data.get('longitude', 'Unknown')}
- Elevation: {region_data.get('elevation', 'Unknown')} m
- pH: {region_data.get('ph', 'Unknown')}
- Perchlorate Level: {region_data.get('perchlorate_wt_pct', 'Unknown')}%
- Water Content: {region_data.get('water_release_wt_pct', 'Unknown')}%
- Terrain: {region_data.get('terrain_type', 'Unknown')}
- Minerals: {region_data.get('major_minerals', 'Unknown')}
- Notes: {region_data.get('notes', 'None')}

Provide a focused analysis (200-300 words) covering:
1. **Why This Score?** - Explain the compatibility score in context
2. **Key Advantages** - What makes this region suitable (2-3 points)
3. **Main Challenges** - Critical issues to address (2-3 points)
4. **Success Factors** - What would make cultivation succeed here
5. **Bottom Line** - Clear recommendation (Highly Recommended / Recommended with Preparation / Challenging / Not Recommended)

Be specific, actionable, and focus on Mars colonization practicality."""

            # Generate AI analysis
            response = self.model.generate_content(prompt)
            ai_text = response.text
            
            return {
                'enabled': True,
                'analysis': ai_text,
                'score': score,
                'region': region_data.get('name', 'Unknown'),
                'recommendation_level': self._get_recommendation_level(score)
            }
            
        except Exception as e:
            print(f"Error generating region AI insights: {e}")
            return {
                'enabled': False,
                'error': str(e),
                'analysis': self._generate_fallback_region_analysis(crop_name, region_data, score)
            }
    
    def _generate_fallback_region_analysis(self, crop_name: str, region_data: Dict, score: int) -> str:
        """Generate basic region analysis without AI"""
        region_name = region_data.get('name', 'Unknown')
        
        if score >= 5:
            recommendation = "Highly Recommended"
            outlook = "excellent"
        elif score >= 3:
            recommendation = "Recommended with Moderate Preparation"
            outlook = "good"
        elif score >= 0:
            recommendation = "Challenging - Significant Preparation Required"
            outlook = "challenging"
        else:
            recommendation = "Not Recommended"
            outlook = "poor"
        
        return f"""**{region_name} - Compatibility Score: {score}/10**

**Overall Assessment:** This region shows {outlook} potential for {crop_name} cultivation based on our analysis.

**Key Factors:**
- Location: {region_data.get('latitude', 'Unknown')}
- Terrain: {region_data.get('terrain_type', 'Unknown')}
- pH Level: {region_data.get('ph', 'Unknown')}
- Water Availability: {region_data.get('water_release_wt_pct', 'Unknown')}%

**Recommendation:** {recommendation}

**Note:** For detailed AI-powered insights, ensure Gemini API is configured.
"""
    
    def _get_recommendation_level(self, score: int) -> str:
        """Get recommendation level based on score"""
        if score >= 5:
            return "highly_recommended"
        elif score >= 3:
            return "recommended"
        elif score >= 0:
            return "challenging"
        else:
            return "not_recommended"


# Initialize global instance
gemini_engine = GeminiRecommendationEngine()


def get_ai_recommendations(crop_data: Dict, regions: List[Dict]) -> Dict:
    """
    Convenience function to get AI recommendations
    
    Usage:
        from api.gemini_integration import get_ai_recommendations
        
        insights = get_ai_recommendations(crop_data, top_regions)
    """
    return gemini_engine.generate_crop_insights(crop_data, regions)
