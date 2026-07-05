import asyncio
import os
import pathlib
import time

import cognee
from cognee import visualize_graph
from cognee.shared.logging_utils import ERROR, setup_logging


async def main():
    print("Connecting to cognee cloud.....")

    await cognee.serve()

    print("✅ Connected to cognee cloud")

    print("\n" + "=" * 70)
    print("🆕 Updating Cognee Persistent Memory")
    print("=" * 70)

    # ------------------------------------------------------------------
    # New meeting video
    # ------------------------------------------------------------------

    bug_path = os.path.join(
        pathlib.Path(__file__).parent,
        "metting_data",
        "bug and security may.mp4",
    )

    print("\n📂 New meeting received:")
    print(f"   • {os.path.basename(bug_path)}")

    print("\n🧠 Updating existing memory...")
    print("   • Processing new meeting")
    print("   • Discovering new entities")
    print("   • Updating relationships")
    print("   • Preserving existing knowledge")
    print("   • Refreshing persistent memory")

    start = time.perf_counter()

    remember_results = await cognee.remember(
        [bug_path],
        dataset_name="meetings",
        self_improvement=True,
    )

    elapsed = time.perf_counter() - start

    print(f"\n✅ Memory updated successfully in {elapsed:.1f} seconds.")
    print(f"📚 Dataset: {remember_results.dataset_name}")

    # ------------------------------------------------------------------
    # Visualize updated graph
    # ------------------------------------------------------------------

    print("\n🕸️ Regenerating knowledge graph visualization...")

    visualize_graph_path = os.path.join(
        os.path.dirname(__file__),
        "artifacts",
        "mettings.html",
    )

    await visualize_graph(
        visualize_graph_path,
        dataset=remember_results.dataset_name,
    )

    print("✅ Knowledge graph updated.")
    print(f"📍 {visualize_graph_path}")

    print("\n🤖 Agents can now answer questions using the latest meeting context.")
    print("=" * 70)

    await cognee.disconnect()


if __name__ == "__main__":
    logger = setup_logging(log_level=ERROR)
    asyncio.run(main())
