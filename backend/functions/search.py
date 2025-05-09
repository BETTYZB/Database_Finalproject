from db.postgres import connect_postgres
from db.mongo import db
from db.neo4j import driver

def search_startups_by_industry(industry):
    results = []

    # Step 1: Get entrepreneurs from PostgreSQL by industry
    conn = connect_postgres()
    cur = conn.cursor()
    cur.execute("SELECT * FROM entrepreneurs WHERE industry = %s", (industry,))
    rows = cur.fetchall()
    conn.close()

    # Step 2: Filter by those with high ratings in MongoDB
    qualified = []
    for row in rows:
        ent_id = row[0]
        logs = db.meetings.find({"entrepreneur_id": ent_id})
        ratings = [log.get("rating", 0) for log in logs if "rating" in log]
        if ratings:
            avg = sum(ratings) / len(ratings)
            if avg >= 4:
                qualified.append(ent_id)

    # Step 3: Rank by number of investor connections in Neo4j
    for ent_id in qualified:
        with driver.session() as session:
            q = """
            MATCH (e:Entrepreneur {id: $id})<--(i:Investor)
            RETURN count(i) AS investor_count
            """
            result = session.run(q, id=ent_id)
            count = result.single()["investor_count"]
            results.append({"entrepreneur_id": ent_id, "investor_connections": count})

    # Sort by most connections
    results.sort(key=lambda x: x["investor_connections"], reverse=True)
    return results
