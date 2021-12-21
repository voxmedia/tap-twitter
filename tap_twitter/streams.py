"""Stream type classes for tap-twitter."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

import requests

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
    user_fields: List[str] = [
        "id",
        "name",
        "username",
        "public_metrics",
    ]
    expansions: List[str] = ["author_id"]

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        record = response.json()
        users_lookup = {user["id"]: user for user in record["includes"]["users"]}
        for i, tweet in enumerate(record["data"]):
            tweet["expansion__author_id"] = users_lookup[tweet["author_id"]]
            yield tweet

    def make_query(self) -> str:
        user_ids = self.config.get("user_ids")
        url_patterns = self.config.get("url_patterns")
        from_filter = " OR ".join([f"from:{user_id}" for user_id in user_ids])
        to_filter = " OR ".join([f"to:{user_id}" for user_id in user_ids])
        retweet_filter = " OR ".join([f"retweets_of:{user_id}" for user_id in user_ids])

        if url_patterns:
            url_filter = " OR ".join([f"url:{url_pattern}" for url_pattern in url_patterns])
            query_elements = [from_filter, to_filter, retweet_filter, url_filter]
        else:
            query_elements = [from_filter, to_filter, retweet_filter]

        return f" OR ".join(query_elements)

    def get_additional_url_params(self):
        return {
            "max_results": self.max_results,
            "query": self.make_query(),
            "tweet.fields": ",".join(self.tweet_fields),
            "expansions": ",".join(self.expansions),
            "user.fields": ",".join(self.user_fields)
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
            "ids": ",".join(self.config.get("user_ids")),
            "user.fields": ",".join(self.user_fields)
        }
