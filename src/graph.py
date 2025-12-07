import os
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv

load_dotenv()

def get_graph_db():
    """
    Initializes and returns the Neo4jGraph connection.
    """
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )
    return graph

def seed_db():
    """
    Seeds the database with enhanced medical data from new_medical_data.json.
    """
    from src.rag_etl_new import populate_graph_from_json, clear_graph
    
    graph = get_graph_db()
    
    # Clear existing data first
    print("Clearing existing data...")
    clear_graph(graph)
    
    print("Seeding database with enhanced medical data...")
    
    # Use the new ETL function
    success = populate_graph_from_json(graph, "src/RAG Graph/new_medical_data.json")
    
    if success:
        print("Database seeded successfully.")
    else:
        print("Warning: Database seeding may have encountered issues.")

if __name__ == "__main__":
    seed_db()
