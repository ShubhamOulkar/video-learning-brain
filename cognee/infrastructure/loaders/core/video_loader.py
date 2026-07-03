import os
from typing import Any

from cognee.infrastructure.files.storage import (
    get_file_storage,
    get_storage_config,
)
from cognee.infrastructure.files.utils.get_file_metadata import (
    get_file_metadata,
)
from cognee.infrastructure.llm.LLMGateway import LLMGateway
from cognee.infrastructure.loaders.LoaderInterface import LoaderInterface


class VideoLoader(LoaderInterface):
    """
    Core video file loader.

    This loader converts supported video files into text using the
    configured multimodal LLM. The generated transcript/description
    is stored as a text document so the rest of Cognee can process
    it exactly like any other text source.
    """

    loader_name = "video_loader"

    @property
    def supported_extensions(self) -> list[str]:
        """Supported video file extensions."""
        return [
            "mp4",
            "mov",
            "avi",
            "mkv",
            "webm",
            "mpeg",
            "mpg",
            "m4v",
        ]

    @property
    def supported_mime_types(self) -> list[str]:
        """Supported MIME types."""
        return [
            "video/mp4",
            "video/quicktime",
            "video/x-msvideo",
            "video/x-matroska",
            "video/webm",
            "video/mpeg",
            "video/x-m4v",
        ]

    def can_handle(self, extension: str, mime_type: str) -> bool:
        """
        Check whether this loader supports the supplied file.
        """
        return extension in self.supported_extensions and mime_type in self.supported_mime_types

    async def load(self, file_path: str, **kwargs: Any) -> str:
        """
        Load and process a video file.

        Args:
            file_path: Path to the video file.
            **kwargs:
                persist (bool): When False, return the generated text
                instead of storing it.

        Returns:
            Either:
            - Path to the stored text file (persist=True)
            - Generated transcript/description (persist=False)

        Raises:
            FileNotFoundError:
                If the supplied file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Compute content hash so duplicate videos produce the same
        # stored filename.
        with open(file_path, "rb") as f:
            file_metadata = await get_file_metadata(f)

        storage_file_name = "text_" + file_metadata["content_hash"] + ".txt"

        # Delegate video understanding to the configured LLM.
        result = await LLMGateway.transcribe_video(file_path)

        if result is None:
            return ""

        # Allow callers to skip persistence.
        if not kwargs.get("persist", True):
            return result.text

        storage_config = get_storage_config()
        data_root_directory = storage_config["data_root_directory"]
        storage = get_file_storage(data_root_directory)

        full_file_path = await storage.store(
            storage_file_name,
            result.text,
        )

        return full_file_path
