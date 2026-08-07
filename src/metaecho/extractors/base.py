import pathlib
from abc import ABC, abstractmethod


class MetadataExtractor(ABC):
    @abstractmethod
    def supports(self, file_type: str) -> bool:
        """
        Check if the extractor supports the given file type.

        Args:
            file_type (str): The MIME type of the file.

        Returns:
            bool: True if the extractor supports the file type, False otherwise.
        """

    @abstractmethod
    def extract(self, path: pathlib.Path) -> dict[str, str]:
        """
        Extract metadata from the file.

        Returns:
            dict[str, str]: A dictionary containing the extracted metadata.

        Raises:
            Implementation-specific exceptions from the underlying parsing library
            (e.g. a decryption error, a malformed-file error) when the file cannot
            be read. The caller is responsible for catching these and recording
            them as a FileError in the FileRecord — this method does not catch
            them itself.       
        """
