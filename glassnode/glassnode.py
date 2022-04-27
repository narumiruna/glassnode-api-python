import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from requests.utils import default_headers

# /v1/metrics/market/marketcap_usd

ENDPOINT = "https://api.glassnode.com"

from enum import Enum


class FrequencyInterval(Enum):
    TEN_MINUTES = '10m'
    ONE_HOUR = "1h"
    ONE_DAY = "24h"
    ONE_WEEK = "1w"
    ONE_MONTH = '1month'


class Format(Enum):
    JSON = 'json'
    CSV = 'csv'


class TimestampFormat(Enum):
    UNIX = 'unix'
    HUMANIZED = 'humanized'  # RFC 3339


@dataclass
class Parameters:
    asset: str
    since: datetime
    until: datetime
    frequency_interval: FrequencyInterval = FrequencyInterval.ONE_HOUR
    format: Format = Format.JSON
    timestamp_format: TimestampFormat = TimestampFormat.UNIX


class Glassnode(object):

    def __init__(self, api_key: str) -> None:
        self.url = ""
        self.api_key = api_key

    def get_metric_data(self, ref_url: str, params: dict):
        url = urljoin(ENDPOINT, ref_url)

        # attach API key
        headers = default_headers()
        headers['X-Api-Key'] = self.api_key

        res = requests.get(url, params=params, headers=headers)
        return json.loads(res.text)
