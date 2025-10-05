# Gemini-Powered Region Recommendations

## 🎯 Feature Requirements

### 1. Dynamic Region Selection
- Use Gemini AI to recommend top 5 regions for each crop
- Different crops should get different (but possibly overlapping) recommendations
- Not hardcoded - AI generates based on crop characteristics

### 2. User Researched Regions
- When user clicks custom location on map
- Add as "User Researched Region" badge
- Display at bottom of region list
- Shows custom analysis for that location

## 🔧 Implementation Plan

### Backend Changes

#### 1. New Gemini Method: `recommend_regions_for_crop()`
```python
def recommend_regions_for_crop(self, crop_name, crop_details, all_regions):
    """
    Use Gemini to intelligently select top 5-7 regions for a crop
    
    Args:
        crop_name: Name of the crop
        crop_details: Crop requirements (pH, moisture, temp, etc.)
        all_regions: List of all 31 Mars regions
    
    Returns:
        List of 5-7 recommended region names with reasoning
    """
```

**Prompt Structure:**
```
You are a Mars agriculture expert. Analyze which regions are best for {crop}.

CROP: {crop_name}
REQUIREMENTS:
- pH: {ph_range}
- Soil: {soil_texture}  
- Temperature: {temperature_range}
- Moisture: {moisture_regime}

AVAILABLE REGIONS (31 total):
{list of regions with key characteristics}

Select 5-7 BEST regions for this crop. Consider:
1. Soil chemistry match
2. Water availability
3. Terrain suitability
4. Location advantages
5. Variety in recommendations

Return JSON:
{
  "top_regions": [
    {
      "region_name": "...",
      "score": 0-10,
      "reasoning": "Why this region works for {crop}"
    }
  ]
}
```

#### 2. Update `match_crop` endpoint
- Call Gemini to get recommended regions
- Calculate compatibility scores for recommended regions
- Return top 5 with full details
- Cache results to avoid repeated API calls

### Frontend Changes

#### 1. Display Recommended Regions
```jsx
{/* AI-Recommended Regions (Top 5) */}
<div className="mb-4">
  <h3 className="text-cyan-300 font-semibold mb-2">
    🤖 AI-Recommended Regions
  </h3>
  {topMatches.map((region, index) => (
    <RegionCard key={index} region={region} rank={index + 1} />
  ))}
</div>
```

#### 2. User Researched Regions Section
```jsx
{/* User-Clicked Custom Locations */}
{userResearchedRegions.length > 0 && (
  <div className="mt-6 pt-4 border-t border-gray-700">
    <h3 className="text-purple-300 font-semibold mb-2 flex items-center">
      <span className="mr-2">🔬</span>
      User Researched Regions
    </h3>
    {userResearchedRegions.map((region, index) => (
      <div key={index} className="mb-2 bg-purple-900/20 rounded-lg p-3 border border-purple-500/30">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-purple-200 font-medium text-sm">
              {region.name}
            </div>
            <div className="text-purple-300/60 text-xs">
              Custom Analysis
            </div>
          </div>
          <div className="text-purple-400 font-bold">
            {region.score}/10
          </div>
        </div>
      </div>
    ))}
  </div>
)}
```

#### 3. State Management
```jsx
const [topRegions, setTopRegions] = useState([]) // Gemini recommended
const [userResearchedRegions, setUserResearchedRegions] = useState([]) // User clicked

// When user clicks map location
const handleLocationClick = (locationData) => {
  setUserResearchedRegions(prev => [...prev, locationData])
  setSelectedSite(locationData)
}
```

## 📊 Benefits

### AI-Powered Recommendations
- **Smart Selection**: Gemini analyzes crop needs vs region characteristics
- **Varied Results**: Different crops get different top regions
- **Reasoning**: Each recommendation includes explanation
- **Dynamic**: Not limited to predetermined list

### User Research Capability
- **Exploration**: Users can analyze any location
- **Comparison**: Compare AI recommendations vs custom locations
- **Learning**: See why certain areas work better
- **Flexibility**: Not constrained to top 5

## 🎨 UI Design

### Region Card Styling

**AI-Recommended (Top 5)**
```
┌─────────────────────────────────┐
│ 🤖 AI-Recommended Regions       │
├─────────────────────────────────┤
│ #1 Gale Crater           [8.5/10]│
│    • Excellent water access      │
│    • Favorable pH                │
│                          [View]   │
├─────────────────────────────────┤
│ #2 Jezero Crater        [8.2/10]│
│ #3 Utopia Planitia      [7.8/10]│
│ #4 Hellas Basin         [7.5/10]│
│ #5 Acidalia Planitia    [7.2/10]│
└─────────────────────────────────┘

────────────────────────────────────

┌─────────────────────────────────┐
│ 🔬 User Researched Regions      │
├─────────────────────────────────┤
│ Mars Location (45.3°, -120.5°)   │
│ Custom Analysis           [6.5/10]│
│                          [View]   │
└─────────────────────────────────┘
```

### Color Scheme
- **AI Recommended**: Cyan/Blue gradient
- **User Researched**: Purple/Violet gradient
- **Selected**: Green highlight
- **Badges**: Rounded pills with icons

## 🔄 Data Flow

```
1. User searches "tomato"
   ↓
2. Backend: Gemini analyzes all 31 regions
   ↓
3. Gemini returns top 5-7 recommendations
   ↓
4. Calculate detailed compatibility scores
   ↓
5. Frontend displays top 5 with reasons
   ↓
6. User clicks custom location (optional)
   ↓
7. Analyze custom location
   ↓
8. Add to "User Researched" section
   ↓
9. Both lists visible simultaneously
```

## 📝 Example Output

### Tomato Search
**AI Recommended:**
1. Gale Crater (8.5/10) - Excellent water, moderate pH
2. Jezero Crater (8.2/10) - Ancient lakebed, minerals
3. Utopia Planitia (7.8/10) - Subsurface ice
4. Hellas Basin (7.5/10) - Low elevation, warmer
5. Acidalia Planitia (7.2/10) - Smooth plains

**User Researched:**
- Custom (45°N, 120°W) - 6.5/10 - High altitude challenge

### Potato Search
**AI Recommended:**
1. Utopia Planitia (9.0/10) - Perfect for root crops
2. Arcadia Planitia (8.5/10) - Ice-rich soil
3. Gale Crater (8.0/10) - Good drainage
4. Amazonis Planitia (7.8/10) - Smooth terrain
5. Chryse Planitia (7.5/10) - Ancient floodplain

## 🚀 Implementation Steps

1. ✅ Add Gemini region recommendation method
2. ✅ Update match_crop endpoint to use Gemini
3. ✅ Add caching to avoid repeated calls
4. ✅ Update frontend to separate AI vs User regions
5. ✅ Style user researched section
6. ✅ Test with multiple crops
7. ✅ Verify recommendations vary by crop

---

**Status**: Ready for implementation
**Priority**: High
**Estimated Time**: 2-3 hours
