import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx
import iso8601
import pandas as pd
from dotenv import find_dotenv
from dotenv import load_dotenv

from .enums import Format
from .enums import FrequencyInterval
from .enums import TimestampFormat

ENDPOINT = "https://api.glassnode.com"


def flatten_options(d: dict) -> dict:
    options = d.get("o")
    if options:
        d.update(options)
        del d["o"]
    return d


def convert_to_dataframe(data) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df["t"] = pd.to_datetime(df["t"], unit="s")
    df = df.sort_values("t")
    return df


@dataclass
class Parameters:
    asset: str
    since: datetime | None = None
    until: datetime | None = None
    frequency_interval: FrequencyInterval | None = None
    format: Format | None = None
    currency: str | None = None
    exchange: str | None = None
    timestamp_format: TimestampFormat | None = None

    def to_dict(self) -> dict:
        params: dict[str, Any] = {"a": self.asset}

        if self.since is not None:
            params["s"] = int(self.since.timestamp())

        if self.until is not None:
            params["u"] = int(self.until.timestamp())

        if self.frequency_interval is not None:
            params["i"] = self.frequency_interval.value

        if self.format is not None:
            params["f"] = self.format.value

        if self.currency is not None:
            params["c"] = self.currency

        if self.exchange is not None:
            params["e"] = self.exchange

        if self.timestamp_format is not None:
            params["timestamp_format"] = self.timestamp_format.value

        return params


class Glassnode:
    def __init__(self, api_key: str) -> None:
        self.headers = {}

        # attach API key
        self.headers["X-Api-Key"] = api_key

    def build_url(self, category: str, metric: str):
        return os.path.join(ENDPOINT, "v1", "metrics", category, metric)

    def _get(self, category: str, metric: str, params: Parameters) -> dict:
        url = self.build_url(category, metric)

        res = httpx.get(url, params=params.to_dict(), headers=self.headers)
        res.raise_for_status()

        return json.loads(res.text)

    def get(
        self,
        category: str,
        metric: str,
        asset: str,
        since: str | datetime | None = None,
        until: str | datetime | None = None,
        frequency_interval: str | None = None,
        format: str | None = None,
        currency: str | None = None,
        exchange: str | None = None,
        timestamp_format: str | None = None,
    ) -> dict:
        if isinstance(since, str):
            since = iso8601.parse_date(since)

        if isinstance(until, str):
            until = iso8601.parse_date(until)

        if frequency_interval is not None:
            frequency_interval = FrequencyInterval(frequency_interval)

        if format is not None:
            format = Format(format)

        if timestamp_format is not None:
            timestamp_format = TimestampFormat(timestamp_format)

        params = Parameters(
            asset=asset,
            since=since,
            until=until,
            frequency_interval=frequency_interval,
            format=format,
            currency=currency,
            exchange=exchange,
            timestamp_format=timestamp_format,
        )

        return self._get(category, metric, params)

    @classmethod
    def from_env(cls):
        load_dotenv(find_dotenv())
        api_key = os.environ.get("GLASSNODE_API_KEY")
        return cls(api_key)
