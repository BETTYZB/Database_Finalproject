from db.postgres import get_entrepreneur_by_id
from db.mongo import db
from db.neo4j import driver

def log_meeting(investor_id, entrepreneur_id, notes, next_steps, rating):
    # Step 1: Validate users exist in PostgreSQL
    ent = get_entrepreneur_by_id(entrepreneur_id)
    if not ent:
        print("Entrepreneur not found in PostgreSQL.")
        return False

    # You can also create a `get_investor_by_id()` if you want stricter validation

    # Step 2: Insert meeting into MongoDB
    meeting = {
        "investor_id": investor_id,
        "entrepreneur_id": entrepreneur_id,
        "notes": notes,
        "next_steps": next_steps,
        "rating": rating,
        "status": "pending"
    }

    db.meetings.insert_one(meeting)
    print("Meeting logged in MongoDB.")

    # Step 3: Create or update MET relationship in Neo4j
    with driver.session() as session:
        session.run("""
            MATCH (i:Investor {id: $inv_id}), (e:Entrepreneur {id: $ent_id})
            MERGE (i)-[m:MET]->(e)
            SET m.timestamp = timestamp(), m.rating = $rating
        """, inv_id=investor_id, ent_id=entrepreneur_id, rating=rating)

    print("Relationship updated in Neo4j.")
    return True
