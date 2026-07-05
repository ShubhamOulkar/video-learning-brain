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
    print("🎥 Cognee Video Memory Demo")
    print("=" * 70)

    print("\n🧹 Cleaning previous memory...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    print("✅ Previous memory removed.")

    # ------------------------------------------------------------------
    # Meeting videos
    # ------------------------------------------------------------------

    intro_path = os.path.join(
        pathlib.Path(__file__).parent,
        "metting_data",
        "metting introdution january.mp4",
    )

    taxo_path = os.path.join(
        pathlib.Path(__file__).parent,
        "metting_data",
        "product taxonomy march.mp4",
    )

    print("\n📂 Videos to ingest:")
    print(f"   • {os.path.basename(intro_path)}")
    print(f"   • {os.path.basename(taxo_path)}")

    print("\n🧠 Building persistent memory...")
    print("   • Extracting multimodal information")
    print("   • Creating knowledge graph")
    print("   • Linking entities and relationships")
    print("   • Enabling self-improving memory")

    start = time.perf_counter()

    remember_results = await cognee.remember(
        [intro_path, taxo_path],
        dataset_name="meetings",
        self_improvement=True,
    )

    elapsed = time.perf_counter() - start

    print(f"\n✅ Memory successfully created in {elapsed:.1f} seconds.")
    print(f"📚 Dataset: {remember_results.dataset_name}")

    # ------------------------------------------------------------------
    # Visualize graph
    # ------------------------------------------------------------------

    print("\n🕸️ Generating knowledge graph visualization...")

    visualize_graph_path = os.path.join(
        os.path.dirname(__file__),
        "artifacts",
        "mettings.html",
    )

    await visualize_graph(
        visualize_graph_path,
        dataset=remember_results.dataset_name,
    )

    print("✅ Knowledge graph saved.")
    print(f"📍 {visualize_graph_path}")

    print("\n🚀 Memory is ready for querying!")
    print("=" * 70)

    await cognee.disconnect()


if __name__ == "__main__":
    logger = setup_logging(log_level=ERROR)
    asyncio.run(main())
