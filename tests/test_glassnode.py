from glassnodeapi import Glassnode


def test_glassnode() -> None:
    g = Glassnode.from_env()
    assert isinstance(g, Glassnode)
