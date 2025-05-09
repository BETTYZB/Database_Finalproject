import csv
import os
from neo4j import GraphDatabase
from random import choice
from dotenv import load_dotenv


load_dotenv()

# Neo4j connection (no auth)
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)


def seed_neo4j_graph():
    with driver.session() as session:
        # Clear the graph
        session.run("MATCH (n) DETACH DELETE n")

        # Load data from CSVs
        investors = []
        entrepreneurs = []
        investor_path = os.path.join("data", "investors.csv")
        entrepreneur_path = os.path.join("data", "entrepreneurs.csv")

        with open(investor_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                investors.append(row)
                session.run("""
                    CREATE (:Investor {
                        id: $id,
                        industry: $industry_focus,
                        stage: $investment_stage
                    })
                """, id=row["id"], industry_focus=row["industry_focus"], investment_stage=row["investment_stage"])

        with open(entrepreneur_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                entrepreneurs.append(row)
                session.run("""
                    CREATE (:Entrepreneur {
                        id: $id,
                        industry: $industry,
                        stage: $startup_stage
                    })
                """, id=row["id"], industry=row["industry"], startup_stage=row["startup_stage"])

        # Add sample relationships
        for _ in range(50):
            inv = choice(investors)
            ent = choice(entrepreneurs)
            session.run("""
                MATCH (i:Investor {id: $inv_id}), (e:Entrepreneur {id: $ent_id})
                MERGE (i)-[:INVESTED_IN]->(e)
            """, inv_id=inv["id"], ent_id=ent["id"])

        for _ in range(50):
            ent = choice(entrepreneurs)
            inv = choice(investors)
            session.run("""
                MATCH (e:Entrepreneur {id: $ent_id}), (i:Investor {id: $inv_id})
                MERGE (e)-[:RECOMMENDED_TO]->(i)
            """, ent_id=ent["id"], inv_id=inv["id"])

        for _ in range(50):
            inv = choice(investors)
            ent = choice(entrepreneurs)
            session.run("""
                MATCH (i:Investor {id: $inv_id}), (e:Entrepreneur {id: $ent_id})
                MERGE (i)-[:MET]->(e)
            """, inv_id=inv["id"], ent_id=ent["id"])

    print(" Neo4j graph seeded with investors, entrepreneurs, and all 3 relationship types.")

def find_investors_by_industry(industry):
    with driver.session() as session:
        query = """
        MATCH (i:Investor)-[:INVESTED_IN]->(e:Entrepreneur)
        WHERE e.industry = $industry
        RETURN DISTINCT i.id AS investor_id
        """
        results = session.run(query, industry=industry)
        return [record["investor_id"] for record in results]
