# TerraEngine
### Mapping Mars for Tomorrow’s Harvest

## 🧠 Overview
TerraEngine is a NASA Space Apps Challenge 2025 project designed to help identify the most suitable and cost-efficient locations for growing crops on the Martian surface.

The platform integrates AI-driven analysis, interactive mapping, and logistical optimization to evaluate potential agricultural sites on Mars. By analyzing environmental, mechanical, and chemical factors, TerraEngine determines where specific crops (like potatoes, tomatoes, etc.) can grow most effectively — and what resources are needed to make that growth sustainable.

Our mission is simple: to make Mars a little greener, one data point at a time.

## 🌱 Inspiration

As we move toward human colonization of Mars, one of the biggest challenges will be establishing reliable and sustainable food systems. Growing crops in space isn’t just about biology — it’s about logistics, resource availability, and environmental adaptation.

TerraEngine was born from the idea that intelligent systems can help us plan ahead — predicting, visualizing, and optimizing where life can thrive beyond Earth.

## 👩‍🚀 Team TerraEngine

### Team Members:

**Gargi Pathak — AI Systems & Logistics Optimization**

**Shanthan Sudhini — Software Development & Backend Integration**

**Laksh Kumar — Data Analytics & Modeling**

**Kaushik Saravanan — Interactive Mapping & Frontend Systems**

**Mohnish Maheshwari — Research & Environmental Data Analysis**


## 🔍 Key Features

✅ Interactive Mars Map: Explore potential agricultural zones and click to reveal full site analytics.

✅ Suitability Scoring System: AI evaluates the viability of different crops based on Martian conditions.

✅ Resource Availability Insights: Understand what’s missing (nutrients, temperature, moisture, etc.) for each site.

✅ Logistical Cost Analysis: Calculates the transportation and supply costs required for each viable site.

✅ Metadata Dashboard: Summarizes environmental, chemical, and mechanical properties per location.

✅ Knowledge-Based Explanations: AI-generated insights explaining why certain areas are better suited than others.


## 🧩 System Architecture

``` System Architecture Overview
┌────────────────────────────────────────────────────────────┐
│                        Frontend                            │
│     React + Mapbox GL | Interactive Mars Visualization      │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│                        Backend                             │
│     FastAPI / Node.js | Crop Suitability & Logistics APIs   │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│                     Database Layer                         │
│     PostgreSQL + PostGIS | Spatial & Environmental Data     │
└────────────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────────────┐
│                     AI & Modeling                          │
│     ML Models | Crop Suitability, Cost Estimation           │
└────────────────────────────────────────────────────────────┘

```

## 🧮 Data & Methodology

TerraEngine combines open-source planetary datasets with simulation-based models:

1. NASA MOLA (Mars Orbiter Laser Altimeter) topographic data

2. THEMIS infrared surface temperature maps

3. Soil composition and regolith simulation datasets

4. Hypothetical greenhouse and transport cost parameters

**Each site on the map is scored based on**:

**A. Environmental Viability (temperature, radiation, water proximity)**

**B. Soil & Chemical Balance (nutrients, pH, density)**

**C. Resource Accessibility (energy, water, and materials)**

**D. Cost Efficiency (transportation and logistics)**

## 🖥️ Tech Stack

Frontend: React.js, Mapbox GL, Tailwind CSS

Backend: SerpAPI, Node.js

Database: PostgreSQL + PostGIS

AI/ML: Scikit-learn, Pandas, XGBoost

Visualization: Plotly, D3.js


## ⚙️ Installation & Setup

**Clone the repository**

```git clone (https://github.com/lakshkumar06/TerraEngine.git)```

**Navigate into the directory**

```cd TerraEngine```

**Install dependencies (for backend)**

```pip install -r requirements.txt``` 

**Install dependencies (for frontend)**

```npm install```

**Run the backend**

```uvicorn main:app --reload```

**Run the frontend**

```npm run dev```

## 🌐 Usage

**Launch the app**

1. Choose a crop (e.g., Potato 🥔).

2. Explore Mars interactively using the map interface.

3. Click on different hotspots to view full-site analytics.

4. Compare sites by suitability score, cost, and sustainability metrics.

## 🧭 Future Scope

Integration with real NASA satellite and rover datasets

Addition of AI-driven crop adaptation simulations

Expansion to multi-planetary optimization models

Real-time mission planning dashboard

Collaborative research mode for scientists and students

## 🛠️ Contributing

This project was built for the NASA Space Apps Challenge 2025.

We’re open to feedback, discussions, and collaboration with researchers and engineers passionate about space agriculture and sustainability!

## 💫 Acknowledgements

**NASA Open Data Portal**

**Mars Orbital Imagery Teams**

**Space Apps Organizers & Mentors**

The entire TerraEngine family for making this vision real 🌍💖
