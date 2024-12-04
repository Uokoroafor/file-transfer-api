from dataclasses import dataclass


@dataclass
class S3Uri:
    """A data class to represent an S3 URI and make it easy to access the different parts of the URI."""

    bucket: str
    name: str

    @property
    def url(self) -> str:
        return f"s3://{self.bucket}/{self.name}"

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url
