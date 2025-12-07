# 🚀 How to Run the Medical Knowledge Graph RAG System

## Prerequisites

Before running the project, you need:

1. **Python 3.9+** installed
2. **Groq API Key** (free at https://console.groq.com)
3. **Neo4j AuraDB instance** (free tier at https://neo4j.com/cloud/aura/)

---

## Step-by-Step Setup

### Step 1: Clone/Navigate to Project

```bash
cd c:\rag_agent_project
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. **Copy the example file:**
   ```bash
   copy .env-example .env
   ```
   (Linux/Mac: `cp .env-example .env`)

2. **Edit `.env` file** with your credentials:

   ```env
   # Neo4j Database Configuration
   NEO4J_URI=neo4j+s://your-neo4j-instance.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_neo4j_password_here

   # Groq LLM Configuration
   GROQ_MODEL_NAME=llama-3.3-70b-versatile
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

   **Where to get credentials:**
   - **Groq API Key**: https://console.groq.com/keys (free, no credit card)
   - **Neo4j AuraDB**: https://neo4j.com/cloud/aura/ (free tier: 200K nodes)

### Step 5: Populate Database (First Time Only)

The database will auto-seed on first run, but you can also manually populate it:

```bash
python src/rag_etl.py
```

This will:
- Clear existing data
- Load 14 diseases from `medical_data.json`
- Create 109 symptoms, 92 treatments, 92 causes
- Establish 293 relationships

**Expected output:**
```
✅ Connecté à Neo4j: neo4j+s://...
🗑️  Graphe vidé avec succès
🧱 Création du graphe Neo4j avec données enrichies...
✅ Graphe créé avec succès !
📊 Statistiques:
  - Maladies (Disease): 14
  - Symptômes (Symptom): 109
  - Traitements (Treatment): 92
  - Causes (Cause): 92
  - Relations totales: 293
```

### Step 6: Run the Application

**Windows:**
```bash
python -m streamlit run app.py
```

**Alternative (if streamlit is in PATH):**
```bash
streamlit run app.py
```

The application will:
- Start on `http://localhost:8501`
- Auto-check database and seed if empty
- Open in your default browser

---

## Using the Application

### 1. **Open Browser**
Navigate to: `http://localhost:8501`

### 2. **Configure API Keys (if needed)**
- Use the sidebar to enter your Groq API key
- Or ensure it's in your `.env` file

### 3. **Ask Medical Questions**

**Examples in English:**
- "I have fever and cough"
- "What disease is treated with Metformin?"
- "What causes Diabetes?"
- "Tell me about Asthma"
- "How to prevent Hypertension?"

**Examples in French:**
- "Je souffre de fatigue et de vertiges"
- "Quels sont les symptômes du diabète?"
- "Comment traiter l'hypertension?"
- "Qu'est-ce qui cause l'asthme?"

### 4. **View Results**
- The system will analyze your question (10-15 seconds)
- Two agents will process it:
  - **Diagnostician**: Queries the knowledge graph
  - **Explainer**: Structures the response
- Results appear in the main area

---

## Troubleshooting

### ❌ "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### ❌ "Neo4j Connection Error"

**Check:**
1. Verify `.env` file has correct `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`
2. Ensure Neo4j AuraDB instance is running
3. Check URI format: `neo4j+s://xxxxx.databases.neo4j.io` (note the `+s` for secure)

**Test connection:**
```python
python -c "from src.graph import get_graph_db; graph = get_graph_db(); print('✅ Connected!')"
```

### ❌ "Groq API Key Invalid"

**Solution:**
1. Get free key at: https://console.groq.com/keys
2. Add to `.env`: `GROQ_API_KEY=gsk_your_key_here`
3. Restart Streamlit

### ❌ "Streamlit command not found"

**Solution:**
```bash
python -m streamlit run app.py
```

### ❌ "Database is empty"

**Solution:**
```bash
python src/rag_etl.py
```

Or click "Seed Database" button in Streamlit sidebar.

### ❌ "Rate limit exceeded" (Groq)

**Solution:**
- Groq free tier: 30 requests/minute
- Wait 1-2 minutes between requests
- Or upgrade to paid tier

---

## Quick Start (TL;DR)

```bash
# 1. Setup
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt

# 2. Configure
copy .env-example .env
# Edit .env with your credentials

# 3. Populate database
python src/rag_etl.py

# 4. Run
python -m streamlit run app.py
```

Open: `http://localhost:8501`

---

## Development Mode

### Run with Debug Output

```bash
python -m streamlit run app.py --logger.level=debug
```

### Test Individual Components

**Test RAG Tool:**
```python
python -c "from src.rag_tool import MedicalRAGTool; tool = MedicalRAGTool(); print(tool._run('I have fever and cough'))"
```

**Test Crew:**
```python
python -c "from src.crew import MedicalCrew; crew = MedicalCrew(); print(crew.run('I have fever'))"
```

**Test Database:**
```python
python -c "from src.graph import get_graph_db; graph = get_graph_db(); result = graph.query('MATCH (n) RETURN count(n)'); print(result)"
```

---

## Production Deployment

For production, consider:

1. **Environment Variables**: Use secure secret management
2. **Database**: Use Neo4j AuraDB (already cloud-hosted)
3. **Streamlit Cloud**: Deploy to https://streamlit.io/cloud
4. **API Keys**: Rotate regularly
5. **Rate Limiting**: Implement proper rate limiting
6. **Error Handling**: Add comprehensive error handling
7. **Logging**: Add structured logging

---

## Next Steps

- ✅ System is running
- 📚 Read `README.md` for detailed architecture
- 📖 Check `ARCHITECTURE_TECHNIQUE.md` for technical details
- 🔍 Explore `QUI_APPELLE_QUI.md` for communication flow

---

**Need Help?** Check the troubleshooting section above or review the error messages in the terminal.

