import json
import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import requests
from requests.utils import default_headers

from .errors import ResolutionForbidden

ENDPOINT = "https://api.glassnode.com"


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
    since: datetime = datetime.fromtimestamp(0)
    until: datetime = datetime.now()
    frequency_interval: FrequencyInterval = FrequencyInterval.ONE_DAY
    format: Format = Format.JSON
    timestamp_format: TimestampFormat = TimestampFormat.UNIX

    def to_dict(self) -> dict:
        return dict(
            a=self.asset,
            s=int(self.since.timestamp() * 1000),
            u=int(self.until.timestamp() * 1000),
            i=self.frequency_interval.value,
            f=self.format.value,
            timestamp_format=self.timestamp_format.value,
        )


class Glassnode(object):

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def query_metric_data(self, category: str, metric: str, params: Parameters) -> dict:
        url = os.path.join(ENDPOINT, 'v1', 'metrics', category, metric)

        # attach API key
        headers = default_headers()
        headers['X-Api-Key'] = self.api_key

        res = requests.get(url, params=params.to_dict(), headers=headers)

        if res.status_code == 403:
            raise ResolutionForbidden(res.text)

        return json.loads(res.text)
