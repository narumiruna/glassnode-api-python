from glassnodeapi import Glassnode


def main():
    g = Glassnode.from_env()

    s = g.get(
        category="market",
        metric="marketcap_usd",
        asset="btc",
        since="2022-01-01 00:00:00",
        until="2022-03-01 00:00:00",
        frequency_interval="1h",
    )

    print(s)


if __name__ == "__main__":
    main()
