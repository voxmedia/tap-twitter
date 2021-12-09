"""Twitter tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_twitter.streams import (
    TweetsStream,
    UsersStream,
)


STREAM_TYPES = [
    TweetsStream,
    UsersStream,
]


class TapTwitter(Tap):
    """Twitter tap class."""
    name = "tap-twitter"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "bearer_token",
            th.StringType,
            required=True,
            description="The bearer token to authenticate against the Twitter API using the OAuth 2.0 flow outlined "
                        "here - https://developer.twitter.com/en/docs/authentication/oauth-2-0/application-only "
        ),
        th.Property(
            "user_id",
            th.StringType,
            required=True,
            description="User ID of the Twitter account"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
