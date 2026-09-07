# 🏙️ Mumbai Smart Urban Operations Platform

An AI-powered smart city platform designed to help Mumbai manage **monsoon flooding**, **traffic congestion**, and **emergency hospital routing**.

---

## 💡 What Does This Project Do?

1. **🚦 Predicts Traffic & Travel Times**
   - Estimates how many minutes a trip will take on Mumbai's major roads.
   - Tells you whether traffic congestion is **Low**, **Medium**, or **High**.

2. **🌧️ Predicts Waterlogging & Flood Risk**
   - Monitors chronic flood spots (like Hindmata, Milan Subway, Kurla, etc.).
   - Predicts water depth (in cm) and warns city authorities before streets flood.

3. **🏥 Tracks Emergency Hospital Beds**
   - Tracks available general and ICU beds in major trauma hospitals (KEM, Sion, Nair, etc.).
   - Alerts authorities if nearby road flooding blocks ambulance access.

4. **🔮 "What-If" Crisis Simulation**
   - Allows city officials to test emergency scenarios before they happen:
     - *"What if Mumbai gets 50% heavier rainfall today?"*
     - *"What if the Western Express Highway closes due to an incident?"*

5. **🗺️ Interactive Map Layers (GIS)**
   - Provides ready-to-use map overlays (roads, flood hotspots, hospitals) for live dashboards.

---

## 📊 How Well Does the AI Perform?

Trained on real Mumbai traffic telemetry and historical monsoon weather data:

- **Traffic Prediction**: **~80% to 84% accuracy** (estimates trip times within 2–3 minutes of real-world conditions).
- **Flood Prediction**: **~81% to 83% accuracy** (reliably flags safe vs dangerous waterlogging levels).

---

## 🚀 How to Run (Quickstart)

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python main.py serve
```

### 3. Test in Your Browser
Open this link in your browser:  
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

You can click on any endpoint, enter sample numbers, and get instant predictions!

---

### 🧪 Run Tests (Optional)
To verify all 17 system tests pass:
```bash
python -m pytest
```

### 🐳 Run with Docker (Optional)
```bash
docker compose up --build
```
