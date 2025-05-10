from db.postgres import connect_postgres
from db.mongo import db
from db.neo4j import driver

# This function retrieves a summary of the dashboard for a user based on their role
# It fetches data from PostgreSQL, MongoDB, and Neo4j databases
def get_dashboard_summary(user_id, role="investor"):
    summary = {"user_id": user_id, "role": role}

    # PostgreSQL → Get profile + investment data
    conn = connect_postgres()
    cur = conn.cursor()

    if role == "investor":
        cur.execute("SELECT * FROM investors WHERE id = %s", (user_id,))
        profile = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM investments WHERE investor_id = %s", (user_id,))
        inv_count = cur.fetchone()[0]
    else:
        cur.execute("SELECT * FROM entrepreneurs WHERE id = %s", (user_id,))
        profile = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM investments WHERE entrepreneur_id = %s", (user_id,))
        inv_count = cur.fetchone()[0]

    summary["profile"] = profile
    summary["investment_count"] = inv_count

    cur.close()
    conn.close()

    # MongoDB → Meeting logs (last 3)
    logs = db.meetings.find({"investor_id" if role == "investor" else "entrepreneur_id": user_id}).sort("_id", -1).limit(3)
    summary["recent_meetings"] = list(logs)

    # Neo4j → Connection count
    with driver.session() as session:
        if role == "investor":
            q = "MATCH (i:Investor {id: $id})--(e:Entrepreneur) RETURN count(e) AS connections"
        else:
            q = "MATCH (e:Entrepreneur {id: $id})--(i:Investor) RETURN count(i) AS connections"

        result = session.run(q, id=user_id)
        summary["connections"] = result.single()["connections"]

    return summary
