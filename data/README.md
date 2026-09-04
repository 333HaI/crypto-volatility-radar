# Data folder

Run `python -m crypto_radar.data --days 180` from the project root to create
`hourly_market_data.csv` here. The CSV is ignored by Git because it can always be
downloaded again.

The source is Coinbase Exchange's public candle endpoint. Timestamps are UTC and
volume is the amount of the base asset traded during each hour (BTC, ETH, or SOL),
not USD volume. Missing hourly buckets are reported and left missing.
