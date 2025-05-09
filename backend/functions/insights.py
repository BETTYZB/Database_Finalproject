from db.postgres import connect_postgres
from db.mongo import db
from db.neo4j import driver

def aggregate_platform_insights():
    insights = {}

    # 🔹 PostgreSQL Stats
    conn = connect_postgres()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM investors")
    insights["total_investors"] = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM entrepreneurs")
    insights["total_entrepreneurs"] = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(amount), 0) FROM investments")
    insights["total_funding"] = float(cur.fetchone()[0])

    cur.execute("SELECT industry, COUNT(*) FROM entrepreneurs GROUP BY industry ORDER BY COUNT(*) DESC LIMIT 3")
    insights["top_industries"] = cur.fetchall()

    cur.close()
    conn.close()

    # 🔹 MongoDB Stats
    all_logs = db.meetings.find()
    total = 0
    rating_sum = 0
    issues = 0
    for log in all_logs:
        total += 1
        rating_sum += log.get("rating", 0)
        note = log.get("notes", "").lower()
        if "problem" in note or "late" in note or "conflict" in note:
            issues += 1

    insights["avg_meeting_rating"] = round(rating_sum / total, 2) if total else None
    insights["issue_flagged_logs"] = issues

    # 🔹 Neo4j Graph Insights
    with driver.session() as session:
        # Most connected user (by degree)
        q1 = """
        MATCH (p)-[r]-()
        WITH p, COUNT(r) AS connections
        RETURN p.id AS id, connections
        ORDER BY connections DESC
        LIMIT 1
        """
        r1 = session.run(q1).single()
        insights["most_connected_user"] = dict(r1) if r1 else {}

        # Isolated users (no connections)
        q2 = """
        MATCH (p)
        WHERE NOT (p)--()
        RETURN COUNT(p) AS isolated
        """
        r2 = session.run(q2).single()
        insights["isolated_users"] = r2["isolated"]

    return insights
