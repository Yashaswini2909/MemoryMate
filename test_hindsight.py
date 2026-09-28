import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load .env
load_dotenv()

# Read configuration
API_KEY = os.getenv("HINDSIGHT_API_KEY")
BASE_URL = os.getenv(
    "HINDSIGHT_API_URL",
    "https://api.hindsight.vectorize.io"
)

# Check API key
if not API_KEY:
    raise ValueError(
        "HINDSIGHT_API_KEY not found. Check your .env file."
    )

# Connect to Hindsight
client = Hindsight(
    base_url=BASE_URL,
    api_key=API_KEY
)

BANK_ID = "memorymate-demo"

print("================================")
print(" MemoryMate - Hindsight Test")
print("================================")

try:
    # 1. Create memory bank
    print("\n[1] Creating memory bank...")

    try:
        bank = client.create_bank(
            bank_id=BANK_ID,
            name="MemoryMate Demo",
            mission=(
                "Remember meeting information, "
                "customer priorities, preferences, "
                "concerns, and unresolved commitments."
            )
        )

        print(f"✓ Bank created: {bank.bank_id}")

    except Exception as e:
        print("✓ Bank already exists, continuing...")

    # 2. Store meeting memory
    print("\n[2] Storing meeting memory...")

    meeting = """
    Meeting with Sarah from Acme Corporation.

    Sarah needs an analytics dashboard before October 15.

    Sarah prefers communication through email rather than
    frequent meetings.

    Sarah is concerned about the implementation timeline.

    Our team promised to send Sarah a revised proposal.

    Sarah wants the dashboard to include sales and revenue
    analytics.
    """

    client.retain(
        bank_id=BANK_ID,
        content=meeting,
        context="Client meeting"
    )

    print("✓ Meeting memory stored!")

    # 3. Recall
    print("\n[3] Recalling Sarah's information...")

    results = client.recall(
        bank_id=BANK_ID,
        query=(
            "What do we know about Sarah, "
            "her priorities, preferences, concerns, "
            "and our commitments?"
        )
    )

    if results.results:
        print(f"✓ Found {len(results.results)} memories:\n")

        for memory in results.results:
            print("-", memory.text)
    else:
        print("No memories returned.")

    # 4. Reflect
    print("\n[4] Generating meeting briefing...")

    response = client.reflect(
        bank_id=BANK_ID,
        query="""
        Prepare a concise briefing for my next meeting with Sarah.

        Include:
        1. Sarah's priorities
        2. Her communication preference
        3. Her concerns
        4. Our unresolved commitments
        5. Suggested follow-up topics

        Use only information available in memory.
        """
    )

    print("\n========== MEETING BRIEF ==========\n")
    print(response.text)

    print("\n================================")
    print(" SUCCESS - Hindsight is working!")
    print("================================")

except Exception as e:
    print("\n❌ ERROR:")
    print(type(e).__name__)
    print(e)

finally:
    client.close()