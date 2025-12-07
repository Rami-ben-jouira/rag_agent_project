"""
rag_etl_new.py - ETL for new medical database structure
Populates Neo4j with enhanced medical data including age groups, severity, lifestyle, and environmental factors
"""
import json
import os
import re
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv

load_dotenv()

def sanitize(name: str) -> str:
    """Transform a name into a valid Neo4j identifier."""
    if not name:
        return "unknown"
    name = name.lower()
    # Remove special characters
    name = re.sub(r"[^a-z0-9_]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

def get_graph_db():
    """Initialize and return Neo4jGraph connection."""
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI", "neo4j://localhost:7687"),
        username=os.getenv("NEO4J_USERNAME", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD", "")
    )
    return graph

def populate_graph_from_json(graph: Neo4jGraph, json_path: str = "src/RAG Graph/new_medical_data.json"):
    """
    Reads JSON and populates Neo4j graph with:
    - Disease nodes (with metadata: age_groups, severity_levels, duration_patterns)
    - Symptom nodes
    - Treatment nodes
    - Cause nodes
    - LifestyleFactor nodes
    - EnvironmentalFactor nodes
    - Relationships: HAS_SYMPTOM, TREATED_WITH, CAUSED_BY, AFFECTED_BY_LIFESTYLE, TRIGGERED_BY_ENVIRONMENT
    """
    
    # Read JSON
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            medical_data = json.load(f)
        print(f"✅ File {json_path} read successfully")
    except FileNotFoundError:
        print(f"❌ ERROR: File {json_path} not found")
        return False
    except json.JSONDecodeError:
        print(f"❌ ERROR: Invalid JSON in {json_path}")
        return False
    
    print("🧱 Creating Neo4j graph with enhanced medical data...")
    
    disease_count = 0
    symptom_count = 0
    treatment_count = 0
    cause_count = 0
    lifestyle_count = 0
    environment_count = 0
    relation_count = 0
    
    try:
        for disease_entry in medical_data:
            disease_name = disease_entry.get("disease", "Unknown Disease")
            
            # Create Disease node with metadata
            age_groups = disease_entry.get("age_groups", [])
            severity_levels = disease_entry.get("severity_levels", [])
            duration_patterns = disease_entry.get("duration_patterns", [])
            
            graph.query(f"""
                MERGE (d:Disease {{name: "{disease_name}"}})
                SET d.age_groups = {json.dumps(age_groups)},
                    d.severity_levels = {json.dumps(severity_levels)},
                    d.duration_patterns = {json.dumps(duration_patterns)}
            """)
            disease_count += 1
            
            # Create HAS_SYMPTOM relationships
            for symptom_name in disease_entry.get("symptoms", []):
                symptom_name = symptom_name.strip()
                
                graph.query(f"""
                    MERGE (s:Symptom {{name: "{symptom_name}"}})
                    WITH s
                    MATCH (d:Disease {{name: "{disease_name}"}})
                    MERGE (d)-[:HAS_SYMPTOM]->(s)
                """)
                symptom_count += 1
                relation_count += 1
            
            # Create TREATED_WITH relationships
            for treatment_name in disease_entry.get("treatments", []):
                treatment_name = treatment_name.strip()
                
                graph.query(f"""
                    MERGE (t:Treatment {{name: "{treatment_name}"}})
                    WITH t
                    MATCH (d:Disease {{name: "{disease_name}"}})
                    MERGE (d)-[:TREATED_WITH]->(t)
                """)
                treatment_count += 1
                relation_count += 1
            
            # Create CAUSED_BY relationships
            for cause_name in disease_entry.get("causes", []):
                cause_name = cause_name.strip()
                
                graph.query(f"""
                    MERGE (c:Cause {{name: "{cause_name}"}})
                    WITH c
                    MATCH (d:Disease {{name: "{disease_name}"}})
                    MERGE (d)-[:CAUSED_BY]->(c)
                """)
                cause_count += 1
                relation_count += 1
            
            # Create AFFECTED_BY_LIFESTYLE relationships
            for lifestyle_factor in disease_entry.get("lifestyle_factors", []):
                lifestyle_factor = lifestyle_factor.strip()
                
                graph.query(f"""
                    MERGE (l:LifestyleFactor {{name: "{lifestyle_factor}"}})
                    WITH l
                    MATCH (d:Disease {{name: "{disease_name}"}})
                    MERGE (d)-[:AFFECTED_BY_LIFESTYLE]->(l)
                """)
                lifestyle_count += 1
                relation_count += 1
            
            # Create TRIGGERED_BY_ENVIRONMENT relationships
            for env_factor in disease_entry.get("environmental_factors", []):
                env_factor = env_factor.strip()
                
                graph.query(f"""
                    MERGE (e:EnvironmentalFactor {{name: "{env_factor}"}})
                    WITH e
                    MATCH (d:Disease {{name: "{disease_name}"}})
                    MERGE (d)-[:TRIGGERED_BY_ENVIRONMENT]->(e)
                """)
                environment_count += 1
                relation_count += 1
        
        print("✅ Graph created successfully!")
        print(f"""
📊 Statistics:
  - Diseases: {disease_count}
  - Symptoms: {symptom_count}
  - Treatments: {treatment_count}
  - Causes: {cause_count}
  - Lifestyle Factors: {lifestyle_count}
  - Environmental Factors: {environment_count}
  - Total Relationships: {relation_count}
        """)
        return True
    
    except Exception as e:
        print(f"❌ ERROR during graph population: {e}")
        import traceback
        traceback.print_exc()
        return False

def clear_graph(graph: Neo4jGraph):
    """Clear the Neo4j graph."""
    try:
        graph.query("MATCH (n) DETACH DELETE n")
        print("🗑️  Graph cleared successfully")
        return True
    except Exception as e:
        print(f"❌ ERROR clearing graph: {e}")
        return False

def main():
    """Main script: clear and populate graph."""
    
    print("=" * 60)
    print("🏥 Neo4j ETL - Enhanced Medical Data Population")
    print("=" * 60)
    
    # Initialize connection
    try:
        graph = get_graph_db()
        print(f"✅ Connected to Neo4j: {os.getenv('NEO4J_URI')}")
    except Exception as e:
        print(f"❌ Cannot connect to Neo4j: {e}")
        return False
    
    # Clear graph
    if not clear_graph(graph):
        return False
    
    # Populate graph
    if not populate_graph_from_json(graph):
        return False
    
    # Display final statistics
    try:
        stats = graph.query("MATCH (n) RETURN labels(n)[0] as type, COUNT(*) as count ORDER BY type")
        print("\n📈 Node Distribution:")
        for row in stats:
            print(f"  - {row.get('type', 'Unknown')}: {row.get('count', 0)}")
    except Exception as e:
        print(f"⚠️  Cannot display statistics: {e}")
    
    print("\n✅ ETL completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

