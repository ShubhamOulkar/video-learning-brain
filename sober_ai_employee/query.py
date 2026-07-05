import asyncio

import cognee
from cognee import SearchType
from cognee.shared.logging_utils import ERROR, setup_logging


QUERIES = [
    {
        "title": "Query 1 - Engineering Decisions",
        "query": "Summarize all engineering decisions discussed across the meetings.",
    },
    {
        "title": "Query 2 - Action Items",
        "query": "What action items were assigned, and who is responsible for them?",
    },
    {
        "title": "Query 3 - Topics Across Meetings",
        "query": "What topics has the engineering team discussed across all meetings?",
    },
    {
        "title": "Query 4 - Self Improving Memory",
        "query": "What changed since the previous meetings?",
    },
    {
        "title": "Query 5 - AI Employee",
        "query": "What should a new engineer know before joining this project?",
    },
]


async def run_query(title: str, query: str):
    print("\n" + "=" * 80)
    print(f"🔍 {title}")
    print("=" * 80)
    print(f"\nQuestion:\n{query}\n")

    results = await cognee.recall(
        query_text=query,
        datasets=["meetings"],
        query_type=SearchType.GRAPH_COMPLETION,
    )

    print("Answer:\n")

    if not results:
        print("No results returned.")
        return

    for result in results:
        print(result.text) # type: ignore
        print()


async def main():
    print("Connecting to cognee cloud.....")
    
    await cognee.serve()

    print("✅ Connected to cognee cloud")

    print("\n" + "=" * 80)
    print("🤖 Cognee AI Employee Demo")
    print("=" * 80)

    for item in QUERIES:
        await run_query(item["title"], item["query"])

    print("=" * 80)
    print("✅ Demo Complete")
    print("=" * 80)

    await cognee.disconnect()


if __name__ == "__main__":
    logger = setup_logging(log_level=ERROR)
    asyncio.run(main())