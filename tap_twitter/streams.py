"""Stream type classes for tap-twitter."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_twitter.client import TwitterStream


# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TweetsStream(TwitterStream):
    """Define custom stream."""
    name = "tweets"
    path = "/tweets/search/recent"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "tweets.schema.json"
    tweet_fields: List[str] = [
        "attachments",
        "author_id",
        "context_annotations",
        "conversation_id",
        "created_at",
        "entities",
        "geo",
        "public_metrics",
    ]

    def get_additional_url_params(self):
        return {
            "tweet.fields": ",".join(self.tweet_fields)
        }
