# `tap-twitter`

Twitter tap class.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`

## Settings

| Setting     | Required | Default | Description |
|:------------|:--------:|:-------:|:------------|
| bearer_token| True     | None    | The bearer token to authenticate against the Twitter API using the OAuth 2.0 flow outlined here - https://developer.twitter.com/en/docs/authentication/oauth-2-0/application-only  |
| user_ids    | True     | None    | List of user IDs of Twitter accounts for which to fetch data |
| url_patterns| False    | None    | List of URL patterns for which to fetch tweets |
| start_date  | False    | None    | The earliest record date to sync |

A full list of supported settings and capabilities is available by running: `tap-twitter --about`

## Installation

```bash
pipx install git+https://github.com/voxmedia/tap-twitter.git
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-twitter --about
```

### Source Authentication and Authorization

This tap requires a Twitter developer account. Visit [Twitter Apps](https://apps.twitter.com/) to set one up and get credentials.


## Usage

You can easily run `tap-twitter` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-twitter --version
tap-twitter --help
tap-twitter --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_twitter/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-twitter` CLI interface directly using `poetry run`:

```bash
poetry run tap-twitter --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-twitter
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-twitter --version
# OR run a test `elt` pipeline:
meltano elt tap-twitter target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
