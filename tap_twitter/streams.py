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
    max_results = 100
    tweet_fields: List[str] = [
        "id",
        "text",
        "attachments",
        "author_id",
        "context_annotations",
        "conversation_id",
        "created_at",
        "entities",
        "geo",
        "public_metrics",
    ]

    def make_query(self) -> str:
        twitter_handle = self.config.get("user_id")
        return f"from:{twitter_handle} OR to:{twitter_handle} OR retweets_of:{twitter_handle}"

    def get_additional_url_params(self):
        return {
            "max_results": self.max_results,
            "query": self.make_query(),
            "tweet.fields": ",".join(self.tweet_fields)
        }


class UsersStream(TwitterStream):
    """Define custom stream."""
    name = "users"
    path = "/users"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "users.schema.json"
    user_fields: List[str] = [
        "id",
        "name",
        "username",
        "created_at",
        "description",
        "entities",
        "location",
        "pinned_tweet_id",
        "profile_image_url",
        "protected",
        "public_metrics",
        "url",
        "verified",
        "withheld",
    ]

    def get_additional_url_params(self):
        return {
            "ids": self.config.get("user_id"),
            "user.fields": ",".join(self.user_fields)
        }
