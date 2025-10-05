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
            print(f"Error generating region AI insights: {e}")
            return {
                'enabled': False,
                'error': str(e),
                'analysis': self._generate_fallback_region_analysis(crop_name, region_data, score)
            }
    
    def _generate_fallback_region_analysis(self, crop_name: str, region_data: Dict, score: int) -> str:
        """Generate varied region analysis without AI (with some randomization for uniqueness)"""
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
        
        return f"""**{region_name} Analysis for {crop_name}**

**Compatibility Score: {score}/10** - {outlook.capitalize()} growing potential

**Why This Score?**
This location presents {outlook} conditions for {crop_name} cultivation. The compatibility assessment considers soil pH ({region_data.get('ph', 'Unknown')}), terrain characteristics, and available water resources ({region_data.get('water_release_wt_pct', 'Unknown')}%).

**Key Advantages:**
{chr(10).join(f'• {adv}' for adv in selected_advantages)}

**Main Challenges:**
{chr(10).join(f'• {challenge}' for challenge in selected_challenges)}

**Success Metrics:**
- Estimated preparation time: {prep_time}
- Projected success rate: {success_rate}
- Resource intensity: {'Low' if score >= 5 else 'Moderate' if score >= 3 else 'High'}

**Bottom Line:** {recommendation}

*Note: For detailed AI-powered insights specific to {crop_name} at {region_name}, Gemini API provides comprehensive analysis including exact soil amendments, timeline projections, and technology requirements.*
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
    
    def answer_question(self, question: str, context: Dict) -> Dict:
        """
        Answer a user's question about a specific crop-region combination
        
        Args:
            question: User's question
            context: Dictionary with crop_name, region_name, score, and optionally conversation_history
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.enabled:
            return {
                'enabled': False,
                'message': 'AI Q&A not available',
                'answer': 'Please configure Gemini API to enable interactive Q&A.'
            }
        
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
