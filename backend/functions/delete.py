from db.postgres import connect_postgres
from db.mongo import db
from db.neo4j import driver

def delete_user_account(user_id, role="investor"):
    # PostgreSQL — Delete user + investments
    conn = connect_postgres()
    cur = conn.cursor()

    if role == "investor":
        cur.execute("DELETE FROM investments WHERE investor_id = %s", (user_id,))
        cur.execute("DELETE FROM investors WHERE id = %s", (user_id,))
    else:
        cur.execute("DELETE FROM investments WHERE entrepreneur_id = %s", (user_id,))
        cur.execute("DELETE FROM entrepreneurs WHERE id = %s", (user_id,))

    conn.commit()
    cur.close()
    conn.close()
    print(" PostgreSQL cleanup complete.")

    # MongoDB — Delete all meetings where user is involved
    db.meetings.delete_many({f"{role}_id": user_id})
    print(" MongoDB cleanup complete.")

    # Neo4j — Delete the node and its relationships
    with driver.session() as session:
        label = "Investor" if role == "investor" else "Entrepreneur"
        session.run(f"""
            MATCH (n:{label} {{id: $id}})
            DETACH DELETE n
        """, id=user_id)

    print(" Neo4j node + relationships removed.")

    return True
