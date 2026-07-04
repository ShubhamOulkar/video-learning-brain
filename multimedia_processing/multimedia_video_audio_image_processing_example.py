import asyncio
import os
import pathlib
import requests

import cognee
from cognee import SearchType, visualize_graph
from cognee.shared.logging_utils import ERROR, setup_logging

url = "https://api.cognee.ai/api/v1/sync"

headers = {
    "Authorization": f"Bearer {os.getenv('COGNEE_API_KEY')}",
    "Content-Type": "application/json",
}


async def main():
    # cognee cloud can not load data return from LLM provider, it only passes path strings to cloud.
    # see cognee-cloud-bug.png
    # await cognee.serve()
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    await cognee.forget(everything=True)

    # cognee knowledge graph will be created based on the text and description of these files
    mp3_file_path = os.path.join(pathlib.Path(__file__).parent, "data/text_to_speech.mp3")
    png_file_path = os.path.join(pathlib.Path(__file__).parent, "data/example.png")
    video_file_path = os.path.join(pathlib.Path(__file__).parent, "data/news.mp4")

    # Remember the files and create knowledge graph memory
    remeber_results = await cognee.remember(
        [mp3_file_path, png_file_path, video_file_path],
        dataset_name="multimedia_processing",
        self_improvement=False,
    )

    # Query cognee for summaries of the data in the multimedia files
    search_results = await cognee.recall(
        query_text="What media files are in the permanent memory?",
        datasets=["multimedia_processing"],
        query_type=SearchType.SUMMARIES,
    )

    # Display search results
    for result_text in search_results:
        print(result_text.text)  # type: ignore
        print()

    # visualise locally
    visualize_graph_path = os.path.join(
        os.path.dirname(__file__), "artifacts", "multimedia_processing.html"
    )

    await visualize_graph(visualize_graph_path, dataset="multimedia_processing")

    # await cognee.disconnect()

    # sync local dataset to cognee cloud
    # payload = {"datasetIds": [remeber_results.dataset_id]}
    # response = requests.post(url, json=payload, headers=headers)
    # print(response.text)


if __name__ == "__main__":
    logger = setup_logging(log_level=ERROR)
    asyncio.run(main())
