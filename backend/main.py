from db.postgres import import_csv_to_postgres, get_entrepreneur_by_id
from db.mongo import seed_meeting_logs, get_declined_investors
from db.neo4j import seed_neo4j_graph, find_investors_by_industry
from functions.match import match_investors_to_entrepreneur
from functions.log import log_meeting
from functions.dashboard import get_dashboard_summary
from functions.search import search_startups_by_industry
from functions.insights import aggregate_platform_insights
from functions.delete import delete_user_account

# This script serves as the main entry point for the backend application.
# It imports data from CSV files into PostgreSQL, seeds MongoDB and Neo4j,
if __name__ == "__main__":
    print(" Importing PostgreSQL CSV data...")
    import_csv_to_postgres()

    print(" Seeding MongoDB...")
    seed_meeting_logs()

    print(" Seeding Neo4j graph...")
    seed_neo4j_graph()

    print("\n TESTING individual data access...\n")

    # Example entrepreneur ID to test (copy one from entrepreneurs.csv or output)
    entrepreneur_id = "52dd3352-4b7a-4c86-8712-d75635f5f10f"

    # Get entrepreneur profile from Postgres
    entrepreneur = get_entrepreneur_by_id(entrepreneur_id)
    print("PostgreSQL → Entrepreneur Profile:\n", entrepreneur)

    # Get investors that declined this entrepreneur from MongoDB
    declined = get_declined_investors(entrepreneur_id)
    print("\nMongoDB → Declined Investor IDs:\n", declined)

    # Get investors from Neo4j who invested in same industry
    if entrepreneur:
        matching_investors = find_investors_by_industry(entrepreneur["industry"])
        print("\nNeo4j → Investors linked to industry:\n", matching_investors)



    print("\n Final Matching Investors:\n")
    matches = match_investors_to_entrepreneur("52dd3352-4b7a-4c86-8712-d75635f5f10f")
    print(matches)
    

    # Test logging a meeting
    print("\n\n TESTING meeting logging...\n")
    # Log a meeting in MongoDB and update Neo4j relationship
    log_meeting(
        investor_id="test-investor-health",
        entrepreneur_id="52dd3352-4b7a-4c86-8712-d75635f5f10f",
        notes="Great alignment on health sector goals.",
        next_steps="Schedule second call next week",
        rating=5
    )
    print("Meeting logged successfully.")
    print("\n\n TESTING dashboard summary...\n")
    # Get dashboard summary for an investor
    summary = get_dashboard_summary("d79f9392-3c24-4691-a1f6-e04f7fed8767", role="investor")
    print(summary)

    # Get startup recommendations based on industry
    print("\n\n TESTING startup search...\n")
    results = search_startups_by_industry("health")
    print("\n Startup Recommendations:\n", results)

    # Get platform insights
    print("\n\n Give the platform owner admin-level stats ...\n")
    admin_data = aggregate_platform_insights()
    print("\n Platform Insights:\n", admin_data)


    # Delete a user account
    print("\n\n TESTING user account deletion...\n")
    delete_user_account("52dd3352-4b7a-4c86-8712-d75635f5f10f", role="entrepreneur")


    
