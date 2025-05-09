from db.postgres import get_entrepreneur_by_id
from db.neo4j import find_investors_by_industry
from db.mongo import get_declined_investors

def match_investors_to_entrepreneur(entrepreneur_id):
    # Step 1: Get entrepreneur info from PostgreSQL
    entrepreneur = get_entrepreneur_by_id(entrepreneur_id)
    if not entrepreneur:
        print(" Entrepreneur not found.")
        return []

    industry = entrepreneur["industry"]
    print(f" Matching for industry: {industry}")

    # Step 2: Get investors in that industry from Neo4j
    potential_investors = find_investors_by_industry(industry)
    print(f" Found {len(potential_investors)} potential investors from Neo4j")

    # Step 3: Get declined investors from MongoDB
    declined_investors = get_declined_investors(entrepreneur_id)
    print(f" Excluding {len(declined_investors)} declined investors from MongoDB")

    # Step 4: Filter
    final_matches = [inv for inv in potential_investors if inv not in declined_investors]
    print(f"Final matched investors: {len(final_matches)}")

    return final_matches
