import pytest

from glassnodeapi import Glassnode


@pytest.fixture
def glassnode() -> Glassnode:
    return Glassnode.from_env()


def test_glassnode_market_marketcap_usd(glassnode: Glassnode):
    s = glassnode.get(
        category='market',
        metric='marketcap_usd',
        asset='btc',
        since='2022-01-01 00:00:00',
        until='2022-03-01 00:00:00',
        frequency_interval='24h',
    )

    assert len(s) > 0


def test_glassnode_derivatives_marketcap_usd(glassnode: Glassnode):
    s = glassnode.get(
        category='derivatives',
        metric='options_atm_implied_volatility_all',
        asset='btc',
    )

    assert len(s) > 0
