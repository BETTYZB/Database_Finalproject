import csv, json, uuid, random, os
from faker import Faker
from neo4j import GraphDatabase

fake = Faker()

DATA_DIR = os.path.join(os.getcwd(), "data")


# Generate PostgreSQL CSVs

def generate_postgres_data(inv_ids, ent_ids):
    with open(f"{DATA_DIR}/investors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "country", "available_funds", "industry_focus", "investment_stage", "status"])
        for id in inv_ids:
            writer.writerow([
                id,
                fake.name(),
                fake.country(),
                round(random.uniform(100000, 5000000), 2),
                random.choice(["tech", "health", "finance", "education"]),
                random.choice(["seed", "series_a", "series_b"]),
                random.choice(["active", "inactive"])
            ])

    with open(f"{DATA_DIR}/entrepreneurs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "startup_name", "industry", "funding_needed", "founded_year", "location", "startup_stage"])
        for id in ent_ids:
            writer.writerow([
                id,
                fake.name(),
                fake.company(),
                random.choice(["tech", "health", "finance", "education"]),
                round(random.uniform(50000, 1000000), 2),
                random.randint(2010, 2024),
                fake.country(),
                random.choice(["idea", "seed", "growth"])
            ])

    with open(f"{DATA_DIR}/investments.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "investor_id", "entrepreneur_id", "amount", "date", "stage"])
        for _ in range(50):
            writer.writerow([
                str(uuid.uuid4()),
                random.choice(inv_ids),
                random.choice(ent_ids),
                round(random.uniform(20000, 500000), 2),
                fake.date_this_decade(),
                random.choice(["seed", "series_a"])
            ])

# ─────────────────────────────────────────
# Generate MongoDB JSON
# ─────────────────────────────────────────

def generate_meeting_logs_json(inv_ids, ent_ids):
    logs = []
    for _ in range(250):
        logs.append({
            "investor_id": random.choice(inv_ids),
            "entrepreneur_id": random.choice(ent_ids),
            "status": random.choice(["declined", "accepted"]),
            "notes": fake.sentence(),
            "rating": random.randint(1, 5)
        })
    with open(f"{DATA_DIR}/meeting_logs_250.json", "w") as f:
        json.dump(logs, f, indent=2)

# ─────────────────────────────────────────
# Generate Neo4j Graph Data
# ─────────────────────────────────────────

def seed_neo4j_graph(inv_ids, ent_ids):
    driver = GraphDatabase.driver("bolt://127.0.0.1:7687", auth=None)

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        for id in inv_ids:
            session.run("CREATE (:Investor {id: $id})", id=id)

        for id in ent_ids:
            session.run("CREATE (:Entrepreneur {id: $id})", id=id)

        for _ in range(50):
            session.run("""
                MATCH (i:Investor {id: $i}), (e:Entrepreneur {id: $e})
                MERGE (i)-[:INVESTED_IN]->(e)
            """, i=random.choice(inv_ids), e=random.choice(ent_ids))

        for _ in range(50):
            session.run("""
                MATCH (e:Entrepreneur {id: $e}), (i:Investor {id: $i})
                MERGE (e)-[:RECOMMENDED_TO]->(i)
            """, i=random.choice(inv_ids), e=random.choice(ent_ids))

        for _ in range(50):
            session.run("""
                MATCH (i:Investor {id: $i}), (e:Entrepreneur {id: $e})
                MERGE (i)-[:MET]->(e)
            """, i=random.choice(inv_ids), e=random.choice(ent_ids))

    driver.close()
    print(" Neo4j graph seeded with nodes and relationships.")

# ─────────────────────────────────────────
# Run Everything
# ─────────────────────────────────────────

def generate_all():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    investor_ids = [str(uuid.uuid4()) for _ in range(50)]
    entrepreneur_ids = [str(uuid.uuid4()) for _ in range(50)]

    print(" Generating PostgreSQL CSVs...")
    generate_postgres_data(investor_ids, entrepreneur_ids)

    print(" Generating MongoDB JSON...")
    generate_meeting_logs_json(investor_ids, entrepreneur_ids)

    print(" Seeding Neo4j Graph...")
    seed_neo4j_graph(investor_ids, entrepreneur_ids)

    print("All data generated and saved in /data folder!")

if __name__ == "__main__":
    generate_all()
