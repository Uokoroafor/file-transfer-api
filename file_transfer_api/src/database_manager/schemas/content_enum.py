import enum


class ContentEnum(enum.Enum):
    """Enum for file content types"""

    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    APPLICATION = "application"
    OTHER = "other"

    @staticmethod
    def from_str(content_type: str) -> "ContentEnum":
        """Get the content type enum from a string.

        Args:
            content_type: Content type to get enum from.

        Returns:
            Content type enum.
        """
        content_map = {
            "image": ContentEnum.IMAGE,
            "video": ContentEnum.VIDEO,
            "audio": ContentEnum.AUDIO,
            "text": ContentEnum.TEXT,
            "application": ContentEnum.APPLICATION,
        }

        for key, value in content_map.items():
            if content_type.startswith(key):
                return value
        return ContentEnum.OTHER


if __name__ == '__main__':
    # Test the ContentEnum class
    print(ContentEnum.from_str("image/jpeg"))
    print(ContentEnum.from_str("video/mp4"))
    print(ContentEnum.from_str("audio/mp3"))
    print(ContentEnum.from_str("text/plain"))
    print(ContentEnum.from_str("application/pdf"))
    print(ContentEnum.from_str("application/json"))
