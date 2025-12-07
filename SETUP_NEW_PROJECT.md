# 🚀 Complete Setup Guide - New Medical Diagnosis System

## Overview

This is a **completely refactored version** of the medical diagnosis system with:
- ✅ **Flask-based professional UI** (replaces Streamlit)
- ✅ **New medical database** (15 different diseases)
- ✅ **Structured input form** (symptoms, duration, severity, age, lifestyle, environment)
- ✅ **Enhanced Neo4j graph** with lifestyle and environmental factors

---

## Step 1: Install Dependencies

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate      # Linux/Mac

# Install new dependencies
pip install flask>=3.0.0 flask-cors>=4.0.0
```

---

## Step 2: Set Up Your Own Neo4j Database

### Option A: Use Existing Neo4j (Already Configured)
If you already have Neo4j credentials in `.env`, skip to Step 3.

### Option B: Create New Neo4j AuraDB Account

**Follow the detailed guide**: See `NEO4J_SETUP_GUIDE.md`

**Quick Steps:**
1. Go to https://neo4j.com/cloud/aura/
2. Sign up for free account
3. Create new database instance
4. Copy connection details:
   - URI: `neo4j+s://xxxxx.databases.neo4j.io`
   - Username: `neo4j`
   - Password: (your password)

5. Update `.env` file:
```env
NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here
GROQ_MODEL_NAME=llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_key_here
```

---

## Step 3: Populate New Database

**Important**: This uses the NEW medical database with 15 different diseases.

```bash
# Populate with new medical data
python src/rag_etl_new.py
```

**Expected Output:**
```
🏥 Neo4j ETL - Enhanced Medical Data Population
✅ Connected to Neo4j: neo4j+s://...
🗑️  Graph cleared successfully
✅ File src/RAG Graph/new_medical_data.json read successfully
🧱 Creating Neo4j graph with enhanced medical data...
✅ Graph created successfully!

📊 Statistics:
  - Diseases: 15
  - Symptoms: ~150+
  - Treatments: ~100+
  - Causes: ~100+
  - Lifestyle Factors: ~50+
  - Environmental Factors: ~50+
  - Total Relationships: ~500+
```

**New Diseases Include:**
- Seasonal Allergies
- Chronic Fatigue Syndrome
- Irritable Bowel Syndrome
- Sleep Apnea
- Fibromyalgia
- Rheumatoid Arthritis
- Chronic Migraine
- COPD
- Chronic Kidney Disease
- Osteoarthritis
- Depression
- Anxiety Disorders
- Chronic Back Pain
- Psoriasis
- Hypothyroidism
- Chronic Sinusitis

---

## Step 4: Run Flask Application

```bash
# Start Flask server
python app_flask.py
```

**The application will:**
- Start on `http://localhost:5000`
- Auto-seed database if empty
- Show professional web interface

**Open in browser**: http://localhost:5000

---

## Step 5: Using the New Interface

### Structured Input Form

The new interface collects:

1. **Symptom Description** (Required)
   - Detailed description of symptoms

2. **Duration**
   - Less than 1 week
   - 1-2 weeks
   - 2-4 weeks
   - 1-3 months
   - 3-6 months
   - 6-12 months
   - More than 1 year
   - Chronic (ongoing)

3. **Severity**
   - Mild
   - Moderate
   - Severe
   - Very Severe

4. **Age Group**
   - Child (0-12 years)
   - Teen (13-19 years)
   - Adult (20-64 years)
   - Elderly (65+ years)

5. **Lifestyle Factors** (Multiple selection)
   - Sedentary lifestyle
   - Smoking
   - Regular alcohol consumption
   - Poor diet
   - High stress
   - Poor sleep quality
   - Obesity
   - Regular exercise

6. **Environmental Context** (Multiple selection)
   - High pollen season
   - Air pollution
   - Work-related stress
   - Weather changes
   - Exposure to allergens
   - Occupational hazards
   - Recent travel
   - Social isolation

### Example Usage

**Input:**
- Symptoms: "Persistent fatigue, joint pain in hands and knees, morning stiffness"
- Duration: "3-6 months"
- Severity: "Moderate"
- Age Group: "Adult (20-64 years)"
- Lifestyle: "Sedentary lifestyle", "High stress"
- Environment: "Work-related stress"

**Output:**
- AI analyzes all factors
- Matches against graph database
- Returns structured diagnosis with:
  - Matching diseases
  - Symptom correlation
  - Recommended treatments
  - Possible causes
  - Confidence levels

---

## API Endpoints

### POST `/api/analyze`
Analyze medical symptoms with structured input.

**Request:**
```json
{
  "symptoms": "Persistent fatigue and joint pain",
  "duration": "3-6 months",
  "severity": "Moderate",
  "age_group": "Adult (20-64 years)",
  "lifestyle_factors": ["Sedentary lifestyle", "High stress"],
  "environmental_context": ["Work-related stress"]
}
```

**Response:**
```json
{
  "success": true,
  "result": "Full AI analysis text...",
  "input_data": {...}
}
```

### POST `/api/seed`
Manually seed the database.

### GET `/api/health`
Health check endpoint.

---

## Differences from Original Project

| Feature | Original | New Version |
|---------|----------|------------|
| **UI Framework** | Streamlit | Flask + HTML/CSS/JS |
| **Input Method** | Simple text | Structured form |
| **Database** | 14 diseases (French) | 15 diseases (English) |
| **Graph Structure** | Basic (Disease-Symptom-Treatment-Cause) | Enhanced (+ Lifestyle + Environment) |
| **Input Fields** | 1 (symptoms text) | 6 (symptoms, duration, severity, age, lifestyle, environment) |
| **UI Style** | Streamlit default | Professional custom design |

---

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask flask-cors
```

### ❌ "Database connection failed"
- Check `.env` file has correct Neo4j credentials
- Verify database is running in AuraDB console
- Test connection: `python -c "from src.graph import get_graph_db; get_graph_db()"`

### ❌ "No diseases found"
- Run: `python src/rag_etl_new.py` to populate database
- Check `src/RAG Graph/new_medical_data.json` exists

### ❌ "Port 5000 already in use"
```bash
# Change port in app_flask.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

---

## File Structure

```
rag_agent_project/
├── app_flask.py              # NEW: Flask application
├── app.py                    # OLD: Streamlit (can be removed)
├── templates/
│   └── index.html            # NEW: Professional web interface
├── src/
│   ├── rag_etl_new.py       # NEW: ETL for new database
│   ├── rag_etl.py            # OLD: Original ETL
│   ├── crew.py               # Updated for structured inputs
│   ├── rag_tool.py           # Updated for structured inputs
│   └── RAG Graph/
│       ├── new_medical_data.json  # NEW: 15 diseases
│       └── medical_data.json      # OLD: 14 diseases (French)
├── .env                      # Your credentials
├── NEO4J_SETUP_GUIDE.md      # Neo4j setup instructions
└── SETUP_NEW_PROJECT.md      # This file
```

---

## Next Steps

1. ✅ **Test the interface**: Fill out form and analyze symptoms
2. ✅ **Customize UI**: Edit `templates/index.html` for branding
3. ✅ **Add more diseases**: Edit `src/RAG Graph/new_medical_data.json`
4. ✅ **Deploy**: Use Flask deployment options (Heroku, AWS, etc.)

---

## Production Deployment

For production:
1. Set `debug=False` in `app_flask.py`
2. Use production WSGI server (Gunicorn, uWSGI)
3. Configure environment variables securely
4. Use HTTPS
5. Set up proper logging
6. Add authentication if needed

---

**Your new professional medical diagnosis system is ready! 🎉**

