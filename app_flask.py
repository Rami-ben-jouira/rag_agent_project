"""
Flask-based Professional Medical Diagnosis Interface
Replaces Streamlit with a modern web application
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from src.crew import MedicalCrew
from src.graph import seed_db, get_graph_db
from dotenv import load_dotenv
import json

load_dotenv(override=True)

# Force all OpenAI calls to go through Groq
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"

app = Flask(__name__)
CORS(app)

# Initialize database on startup
def initialize_database():
    """Initialize database on application startup"""
    try:
        graph = get_graph_db()
        result = graph.query("MATCH (n) RETURN count(n) as count")
        node_count = result[0]['count'] if result else 0
        print(f"\n{'='*60}")
        print(f"[STARTUP] Database has {node_count} nodes")
        if node_count == 0:
            print("[STARTUP] Database is empty, seeding with sample data...")
            seed_db()
            result = graph.query("MATCH (n) RETURN count(n) as count")
            print(f"[STARTUP] After seeding: {result[0]['count']} nodes")
        else:
            print("[STARTUP] Database already has data, skipping seed")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\n[STARTUP ERROR] Could not check/seed database: {e}")
        import traceback
        traceback.print_exc()

# Initialize database
with app.app_context():
    initialize_database()

@app.route('/')
def index():
    """Main page with structured input form"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for medical analysis"""
    try:
        data = request.json
        
        # Extract structured input
        symptoms = data.get('symptoms', '')
        duration = data.get('duration', '')
        severity = data.get('severity', '')
        age_group = data.get('age_group', '')
        lifestyle_factors = data.get('lifestyle_factors', [])
        environmental_context = data.get('environmental_context', [])
        
        # Build comprehensive query
        query_parts = []
        query_parts.append(f"Patient symptoms: {symptoms}")
        
        if duration:
            query_parts.append(f"Duration: {duration}")
        if severity:
            query_parts.append(f"Severity: {severity}")
        if age_group:
            query_parts.append(f"Age group: {age_group}")
        if lifestyle_factors:
            query_parts.append(f"Lifestyle factors: {', '.join(lifestyle_factors)}")
        if environmental_context:
            query_parts.append(f"Environmental context: {', '.join(environmental_context)}")
        
        full_query = ". ".join(query_parts)
        
        # Check API keys
        if not (os.getenv("GROQ_API_KEY") or os.getenv("GOOGLE_API_KEY")):
            return jsonify({
                'error': 'Please configure API keys in .env file'
            }), 400
        
        # Run CrewAI analysis
        crew = MedicalCrew()
        crew_output = crew.run(full_query)
        
        # Convert CrewOutput to string for JSON serialization
        # CrewOutput is a Pydantic model - convert to string
        # The __str__ method should return the actual output text
        result_text = str(crew_output)
        
        return jsonify({
            'success': True,
            'result': result_text,
            'input_data': {
                'symptoms': symptoms,
                'duration': duration,
                'severity': severity,
                'age_group': age_group,
                'lifestyle_factors': lifestyle_factors,
                'environmental_context': environmental_context
            }
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/seed', methods=['POST'])
def seed_database():
    """API endpoint to seed database"""
    try:
        seed_db()
        return jsonify({
            'success': True,
            'message': 'Database seeded successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        graph = get_graph_db()
        result = graph.query("MATCH (n) RETURN count(n) as count")
        node_count = result[0]['count'] if result else 0
        
        return jsonify({
            'status': 'healthy',
            'database_connected': True,
            'node_count': node_count,
            'groq_configured': bool(os.getenv("GROQ_API_KEY"))
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

