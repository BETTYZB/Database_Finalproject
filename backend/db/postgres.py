import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv


load_dotenv()

def connect_postgres():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

def import_csv_to_postgres():
    conn = connect_postgres()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS investments")
    cur.execute("DROP TABLE IF EXISTS entrepreneurs")
    cur.execute("DROP TABLE IF EXISTS investors")

    with open("sql/create_tables.sql", "r") as f:
        cur.execute(f.read())

    tables = {
        "investors": "investors.csv",
        "entrepreneurs": "entrepreneurs.csv",
        "investments": "investments.csv"
    }

    csv_dir = os.path.join(os.getcwd(), "data")
    for table, filename in tables.items():
        filepath = os.path.join(csv_dir, filename)
        with open(filepath, "r") as f:
            next(f)
            cur.copy_expert(f"COPY {table} FROM STDIN WITH CSV", f)
        print(f" Imported {filename} into {table}")

    conn.commit()
    cur.close()
    conn.close()

def get_entrepreneur_by_id(entrepreneur_id):
    try:
        conn = connect_postgres()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM entrepreneurs WHERE id = %s", (entrepreneur_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return dict(result) if result else None
    except Exception as e:
        print(" Error fetching entrepreneur:", e)
        return None
