"""REST client handling, including TwitterStream base class."""

import backoff
import copy
import requests
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional

from singer_sdk.exceptions import FatalAPIError
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator


SCHEMAS_DIR: Path = Path(__file__).parent / Path("./schemas")


class TwitterStream(RESTStream):
    """Twitter stream class."""

    url_base: str = "https://api.twitter.com/2"

    records_jsonpath: str = "$.data[*]"  # Or override `parse_response`.
    next_page_token_jsonpath: str = "$.meta.next_token"  # Or override `get_next_page_token`.

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        return BearerTokenAuthenticator.create_for_stream(
            self,
            token=self.config.get("bearer_token")
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def request_decorator(self, func: Callable) -> Callable:
        """Instantiate a decorator for handling request failures.

        Developers may override this method to provide custom backoff or retry
        handling.

        Args:
            func: Function to decorate.

        Returns:
            A decorated method.
        """
        decorator: Callable = backoff.on_exception(
            backoff.expo,
            (
                FatalAPIError,
                requests.exceptions.HTTPError,
            ),
            max_tries=9,
            max_time=1950,
            base=9,
            factor=5,
        )(func)
        return decorator

    def request_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Request records from REST endpoint(s), returning response records.

        If pagination is detected, pages will be recursed automatically.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            An item for every record in the response.

        Raises:
            RuntimeError: If a loop in pagination is detected. That is, when two
                consecutive pagination tokens are identical.
        """
        next_page_token: Any = None
        finished = False
        decorated_request = self.request_decorator(self._request)

        while not finished:
            prepared_request = self.prepare_request(
                context, next_page_token=next_page_token
            )
            resp = decorated_request(prepared_request, context)
            for row in self.parse_response(resp):
                yield row
            previous_token = copy.deepcopy(next_page_token)
            next_page_token = self.get_next_page_token(
                response=resp, previous_token=previous_token
            )
            if next_page_token and next_page_token == previous_token:
                raise RuntimeError(
                    f"Loop detected in pagination. "
                    f"Pagination token {next_page_token} is identical to prior token."
                )
            # Cycle until get_next_page_token() no longer returns a value
            finished = not next_page_token

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            next_page_token = first_match
        else:
            next_page_token = response.headers.get("X-Next-Page", None)

        return next_page_token

    def get_additional_url_params(self) -> Dict:
        pass

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["next_token"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        if self.get_additional_url_params():
            params.update(self.get_additional_url_params())
        return params

    # def prepare_request_payload(
    #     self, context: Optional[dict], next_page_token: Optional[Any]
    # ) -> Optional[dict]:
    #     """Prepare the data payload for the REST API request.
    #
    #     By default, no payload will be sent (return None).
    #     """
    #     # TODO: Delete this method if no payload is required. (Most REST APIs.)
    #     return None

    # def parse_response(self, response: requests.Response) -> Iterable[dict]:
    #     """Parse the response and return an iterator of result rows."""
    #     # TODO: Parse response body and return a set of records.
    #     yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    # def post_process(self, row: dict, context: Optional[dict]) -> dict:
    #     """As needed, append or transform raw data to match expected structure."""
    #     # TODO: Delete this method if not needed.
    #     return row
