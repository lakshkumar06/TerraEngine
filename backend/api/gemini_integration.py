"""
Gemini AI and serpAPI Integration for TerraEngine
This module provides AI-powered insights for Mars crop recommendations
"""

import os
import json
from typing import Dict, List, Any

from decouple import config
GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
SERP_API_KEY = config('SERP_API_KEY', default=None)
if not GEMINI_API_KEY:
    raise RuntimeError('GEMINI_API_KEY is required and was not found in environment')
if not SERP_API_KEY:
    raise RuntimeError('SERP_API_KEY is required and was not found in environment')

# SERP API Integration - For web search and real-time data
import requests


class GeminiRecommendationEngine:
    """
    AI-powered recommendation engine using Google Gemini and SERP API
    """
    
    def __init__(self, api_key: str = None, serp_api_key: str = None):
        """
        Initialize AI clients (Gemini and SERP API)
        
        Args:
            api_key: Google Gemini API key (if not provided, uses environment variable)
            serp_api_key: SERP API key for web search (if not provided, uses environment variable)
        """
        self.api_key = api_key or GEMINI_API_KEY
        self.serp_api_key = serp_api_key or SERP_API_KEY
        self.enabled = True
        self.serp_enabled = True
        
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Gemini AI initialized successfully with gemini-2.0-flash!")
    
    def search_serp_api(self, query: str) -> Dict[str, Any]:
        """
        SERP API Integration - Search for real-time Mars agriculture data
        
        Args:
            query: Search query for SERP API
            
        Returns:
            Dict with search results (currently placeholder for hackathon demo)
        """
        serp_url = "https://serpapi.com/search.json"
        params = {
            'api_key': self.serp_api_key,
            'q': query,
            'engine': 'google'
        }
        response = requests.get(serp_url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        return {'enabled': True, 'results': data}
    
    def generate_crop_insights(self, crop_data: Dict, regions: List[Dict]) -> Dict[str, Any]:
        """
        Generate AI-powered insights for crop recommendations
        
        Args:
            crop_data: Dictionary containing crop information and requirements
            regions: List of top matching regions with scores
            
        Returns:
            Dictionary containing AI-generated insights and recommendations
        """
        # require AI to be enabled
        
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
            raise
    
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
        """Deprecated: Fallback removed. This method should not be called."""
        
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
        
        raise RuntimeError('AI fallback is disabled')
    
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
        # require AI to be enabled
        
        try:
            # Create detailed prompt for region-specific analysis with emphasis on variety
            prompt = f"""You are an expert Mars agriculture scientist analyzing {region_data.get('name', 'Unknown')} for growing {crop_name}.

CRITICAL: Make this analysis UNIQUE and SPECIFIC to this exact crop-region combination. Consider the specific characteristics of {crop_name} and how they interact with this particular Martian location.

REGION: {region_data.get('name', 'Unknown')}
COMPATIBILITY SCORE: {score}/10

{crop_name.upper()} SPECIFIC REQUIREMENTS:
- pH Range: {crop_details.get('ph_range', 'Unknown')}
- Soil Needs: {crop_details.get('soil_texture', 'Unknown')}
- Temperature: {crop_details.get('temperature_range', 'Unknown')}°C
- Water/Moisture: {crop_details.get('moisture_regime', 'Unknown')}

THIS REGION'S UNIQUE CONDITIONS:
- Coordinates: {region_data.get('latitude', 'Unknown')}, {region_data.get('longitude', 'Unknown')}
- Elevation: {region_data.get('elevation', 'Unknown')} meters
- Current pH: {region_data.get('ph', 'Unknown')}
- Perchlorate: {region_data.get('perchlorate_wt_pct', 'Unknown')}% (toxicity concern)
- Water Available: {region_data.get('water_release_wt_pct', 'Unknown')}%
- Terrain Type: {region_data.get('terrain_type', 'Unknown')}
- Mineral Composition: {region_data.get('major_minerals', 'Unknown')}
- Special Notes: {region_data.get('notes', 'None')}

Generate a UNIQUE analysis (250-350 words) with:

**1. Why This Score?** 
Explain specifically how {crop_name}'s requirements match or mismatch this location's conditions. Use actual numbers and be detailed about the gap between ideal and actual conditions.

**2. Key Advantages (2-4 specific points)**
What UNIQUE aspects of {region_data.get('name', 'Unknown')} make it suitable for {crop_name}? Consider:
- Specific minerals that benefit this crop
- Terrain features helpful for this plant
- Climate advantages at this latitude
- Any historical geological features

**3. Main Challenges (2-4 critical issues)**
What SPECIFIC problems will {crop_name} face HERE? Be detailed about:
- Exact soil amendments needed
- Specific perchlorate mitigation for this crop
- Temperature control requirements
- Water management challenges unique to this crop

**4. Success Factors**
Give 3-5 CONCRETE, actionable steps for growing {crop_name} successfully at {region_data.get('name', 'Unknown')}. Include:
- Specific technologies or techniques needed
- Timeline estimates (days/weeks)
- Resource requirements (energy, water, materials)
- Monitoring parameters

**5. Bottom Line**
Provide a SPECIFIC recommendation:
- Highly Recommended (score 7-10): Ready with minimal prep
- Recommended with Preparation (score 4-6): Feasible with moderate investment
- Challenging but Possible (score 2-3): Requires significant resources
- Not Recommended (score 0-1): Better alternatives exist

IMPORTANT: Make each analysis distinctly different. Vary your language, focus on different aspects, and provide crop-specific and location-specific insights. DO NOT use generic phrases - be specific to {crop_name} and {region_data.get('name', 'Unknown')}."""

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
            raise
    
    def _generate_fallback_region_analysis(self, crop_name: str, region_data: Dict, score: int) -> str:
        """Deprecated: Fallback removed. This method should not be called."""
        import hashlib
        
        region_name = region_data.get('name', 'Unknown')
        
        # Create a deterministic "seed" based on crop and region for consistent but varied output
        seed = int(hashlib.md5(f"{crop_name}{region_name}".encode()).hexdigest()[:8], 16)
        
        if score >= 5:
            recommendation = "Highly Recommended"
            outlook = "excellent"
            prep_time = f"{20 + (seed % 20)} days"
            success_rate = f"{75 + (seed % 20)}%"
        elif score >= 3:
            recommendation = "Recommended with Moderate Preparation"
            outlook = "good"
            prep_time = f"{30 + (seed % 30)} days"
            success_rate = f"{55 + (seed % 25)}%"
        elif score >= 0:
            recommendation = "Challenging - Significant Preparation Required"
            outlook = "challenging"
            prep_time = f"{60 + (seed % 40)} days"
            success_rate = f"{30 + (seed % 20)}%"
        else:
            recommendation = "Not Recommended"
            outlook = "poor"
            prep_time = f"{90 + (seed % 60)} days"
            success_rate = f"{10 + (seed % 15)}%"
        
        # Vary the analysis based on seed
        challenges = [
            "pH adjustment and soil acidification",
            "perchlorate decontamination systems",
            "temperature control infrastructure",
            "water recycling and irrigation setup"
        ]
        
        advantages = [
            f"Favorable elevation at {region_data.get('elevation', 'N/A')} meters",
            f"Water content of {region_data.get('water_release_wt_pct', 'N/A')}% available",
            f"Strategic location at {region_data.get('latitude', 'N/A')}",
            f"Suitable terrain: {region_data.get('terrain_type', 'N/A')}"
        ]
        
        # Select 2-3 items based on seed
        selected_challenges = [challenges[i] for i in range((seed % 2) + 2)]
        selected_advantages = [advantages[i] for i in range((seed % 2) + 2)]
        
        raise RuntimeError('AI fallback is disabled')
    
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
    
    def answer_question(self, question: str, context: Dict) -> Dict:
        """
        Answer a user's question about a specific crop-region combination
        
        Args:
            question: User's question
            context: Dictionary with crop_name, region_name, score, and optionally conversation_history
            
        Returns:
            Dictionary with answer and metadata
        """
        # require AI to be enabled
        
        try:
            crop_name = context.get('crop_name', 'Unknown')
            region_name = context.get('region_name', 'Unknown')
            score = context.get('score', 0)
            conversation_history = context.get('conversation_history', [])
            
            # Build context-aware prompt
            prompt = f"""You are a Mars agriculture expert. A user is exploring growing {crop_name} at {region_name} (compatibility score: {score}/10).

CONTEXT:
- Crop: {crop_name}
- Location: {region_name} on Mars
- Compatibility Score: {score}/10

USER'S QUESTION: "{question}"

Provide a focused, concise answer (2-4 sentences, 50-100 words). Be specific to {crop_name} and {region_name}. 

"""
            
            # Add conversation history if exists
            if conversation_history:
                prompt += "\nPREVIOUS CONVERSATION:\n"
                for i, qa in enumerate(conversation_history[-3:]):  # Last 3 exchanges
                    prompt += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
            
            prompt += f"""
Now answer the user's current question: "{question}"

Guidelines:
- Keep it brief (2-4 sentences)
- Be specific to {crop_name} at {region_name}
- If explaining why something won't work, give a short alternative suggestion
- Use practical, actionable language
- Don't repeat information from previous answers
"""
            
            # Generate answer
            response = self.model.generate_content(prompt)
            answer_text = response.text.strip()
            
            return {
                'enabled': True,
                'answer': answer_text,
                'question': question,
                'timestamp': 'now'
            }
            
        except Exception as e:
            print(f"Error answering question: {e}")
            return {
                'enabled': False,
                'error': str(e),
                'answer': f"I encountered an error processing your question. Please try rephrasing or ask something else about {context.get('crop_name', 'this crop')} cultivation at {context.get('region_name', 'this location')}."
            }
    
    def analyze_cultivation_costs(self, crop_name: str, crop_details: Dict, region_data: Dict, score: int) -> Dict:
        """
        Generate cost analysis for growing a crop in a specific Mars region
        
        Args:
            crop_name: Name of the crop
            crop_details: Dictionary with crop requirements
            region_data: Dictionary containing region information
            score: Compatibility score from algorithm
            
        Returns:
            Dictionary with cost breakdown (one-time, sustained, detailed)
        """
        # require AI to be enabled
        
        try:
            # Create detailed prompt for cost analysis
            prompt = f"""You are a Mars colonization economist specializing in agricultural cost estimation.

Analyze the costs for setting up and maintaining {crop_name} cultivation at {region_data.get('name', 'Unknown')} on Mars.

REGION: {region_data.get('name', 'Unknown')}
CROP: {crop_name}
COMPATIBILITY SCORE: {score}/10
LOCATION: {region_data.get('latitude', 'Unknown')}, {region_data.get('longitude', 'Unknown')}
TERRAIN: {region_data.get('terrain_type', 'Unknown')}
ELEVATION: {region_data.get('elevation', 'Unknown')} meters

Provide REALISTIC cost estimates in USD. Generate:

1. **ONE-TIME SETUP COST** (total initial investment):
   - Give a single total figure for initial setup
   - Consider: transportation, habitat construction, equipment, initial supplies
   
2. **ANNUAL SUSTAINED COST** (per year operational cost):
   - Give a single annual figure for ongoing operations
   - Consider: energy, water recycling, nutrients, maintenance, labor

3. **DETAILED BREAKDOWN** (itemized list):
   Format as JSON with these exact keys:
   {{
     "transportation": {{"cost": number, "description": "brief note"}},
     "habitat_construction": {{"cost": number, "description": "brief note"}},
     "equipment": {{"cost": number, "description": "brief note"}},
     "initial_supplies": {{"cost": number, "description": "brief note"}},
     "energy_systems": {{"cost": number, "description": "brief note"}},
     "water_recycling": {{"cost": number, "description": "brief note"}},
     "soil_preparation": {{"cost": number, "description": "brief note"}},
     "climate_control": {{"cost": number, "description": "brief note"}},
     "annual_energy": {{"cost": number, "description": "per year"}},
     "annual_water": {{"cost": number, "description": "per year"}},
     "annual_nutrients": {{"cost": number, "description": "per year"}},
     "annual_maintenance": {{"cost": number, "description": "per year"}},
     "annual_labor": {{"cost": number, "description": "per year"}}
   }}

IMPORTANT:
- Make costs vary based on the compatibility score ({score}/10)
- Lower scores = higher costs (more preparation needed)
- Higher scores = lower costs (better natural conditions)
- Be SPECIFIC to {crop_name} needs at {region_data.get('name', 'Unknown')}
- Consider actual Mars mission economics
- Use round numbers (no cents)
- Return ONLY the JSON data, no additional text

Return format:
{{
  "one_time_cost": total_number,
  "annual_sustained_cost": total_number,
  "breakdown": {{detailed breakdown as above}}
}}"""

            # Generate cost analysis
            response = self.model.generate_content(prompt)
            ai_text = response.text.strip()
            
            # Try to parse JSON from response
            try:
                # Remove markdown code blocks if present
                if '```json' in ai_text:
                    ai_text = ai_text.split('```json')[1].split('```')[0].strip()
                elif '```' in ai_text:
                    ai_text = ai_text.split('```')[1].split('```')[0].strip()
                
                cost_data = json.loads(ai_text)
                cost_data['enabled'] = True
                return cost_data
                
            except json.JSONDecodeError:
                raise
            
        except Exception as e:
            raise
    
    def recommend_regions_for_crop(self, crop_name: str, crop_details: Dict, all_regions: list) -> list:
        """
        Use Gemini to intelligently recommend best regions for a crop
        
        Args:
            crop_name: Name of the crop
            crop_details: Crop requirements dict
            all_regions: List of all available regions
            
        Returns:
            List of recommended region names with scores
        """
        # require AI to be enabled
        
        try:
            # Prepare regions summary for Gemini
            regions_summary = []
            for r in all_regions[:31]:  # Limit to prevent token overflow
                name = r.get('name', r.get('region', 'Unknown'))
                regions_summary.append(f"- {name}: pH {r.get('ph', 'N/A')}, Elevation {r.get('elevation', r.get('elevation_m', 'N/A'))}m, Water {r.get('water_release_wt_pct', 'N/A')}%, Terrain: {r.get('terrain_type', 'N/A')}")
            
            prompt = f"""You are a Mars agriculture expert. Select the BEST 5-7 regions for growing {crop_name}.

CROP REQUIREMENTS:
- pH: {crop_details.get('ph_range', 'Unknown')}
- Soil: {crop_details.get('soil_texture', 'Unknown')}
- Temperature: {crop_details.get('temperature_range', 'Unknown')}°C
- Moisture: {crop_details.get('moisture_regime', 'Unknown')}

AVAILABLE MARS REGIONS:
{chr(10).join(regions_summary[:31])}

IMPORTANT:
- Select 5-7 regions that BEST match {crop_name}'s needs
- Different crops should get DIFFERENT top regions (some overlap OK)
- Consider: soil chemistry, water, terrain, location advantages
- Provide variety in your selections

Return ONLY valid JSON (no markdown):
{{
  "recommendations": [
    {{"region": "Region Name", "score": 8.5, "reason": "Brief why"}},
    ...
  ]
}}"""

            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean JSON from markdown
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            data = json.loads(text)
            return data.get('recommendations', [])[:7]
            
        except Exception as e:
            raise
    
    def _generate_fallback_cost_analysis(self, crop_name: str, region_data: Dict, score: int) -> Dict:
        """Deprecated: Fallback removed. This method should not be called."""
        import hashlib
        
        region_name = region_data.get('name', 'Unknown')
        
        # Create a deterministic seed for consistent but varied costs
        seed = int(hashlib.md5(f"{crop_name}{region_name}".encode()).hexdigest()[:8], 16)
        
        # Base costs that scale inversely with compatibility score
        # Lower score = higher costs
        score_multiplier = 2.0 - (score / 10.0)  # Range: 1.0 to 2.0
        variance = (seed % 20000) / 100  # Add some variance
        
        # One-time costs (in thousands USD)
        base_one_time = 5000000  # $5M base
        one_time_cost = int((base_one_time * score_multiplier) + variance)
        
        # Annual costs (in thousands USD)
        base_annual = 500000  # $500K base
        annual_cost = int((base_annual * score_multiplier) + (variance / 10))
        
        # Detailed breakdown
        breakdown = {
            "transportation": {
                "cost": int(one_time_cost * 0.35),
                "description": f"SpaceX Starship cargo delivery to {region_name}"
            },
            "habitat_construction": {
                "cost": int(one_time_cost * 0.25),
                "description": "Pressurized greenhouse with radiation shielding"
            },
            "equipment": {
                "cost": int(one_time_cost * 0.15),
                "description": f"Specialized equipment for {crop_name} cultivation"
            },
            "initial_supplies": {
                "cost": int(one_time_cost * 0.10),
                "description": "Seeds, nutrients, soil amendments, tools"
            },
            "energy_systems": {
                "cost": int(one_time_cost * 0.08),
                "description": "Solar panels and battery storage systems"
            },
            "water_recycling": {
                "cost": int(one_time_cost * 0.04),
                "description": "Closed-loop water purification and recycling"
            },
            "soil_preparation": {
                "cost": int(one_time_cost * 0.02),
                "description": f"Perchlorate removal and pH adjustment for {crop_name}"
            },
            "climate_control": {
                "cost": int(one_time_cost * 0.01),
                "description": "HVAC systems for temperature/humidity control"
            },
            "annual_energy": {
                "cost": int(annual_cost * 0.40),
                "description": "Power for lighting, heating, and life support"
            },
            "annual_water": {
                "cost": int(annual_cost * 0.15),
                "description": "Water extraction and recycling operations"
            },
            "annual_nutrients": {
                "cost": int(annual_cost * 0.20),
                "description": f"Fertilizers and supplements for {crop_name}"
            },
            "annual_maintenance": {
                "cost": int(annual_cost * 0.15),
                "description": "Equipment repairs and system upkeep"
            },
            "annual_labor": {
                "cost": int(annual_cost * 0.10),
                "description": "Agricultural technician time allocation"
            }
        }
        
        raise RuntimeError('AI fallback is disabled')


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
