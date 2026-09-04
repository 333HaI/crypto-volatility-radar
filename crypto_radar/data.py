"""Download hourly spot candles from Coinbase Exchange."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import requests


API_ROOT = "https://api.exchange.coinbase.com"
PRODUCTS = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD"}
CANDLE_COLUMNS = ["timestamp", "low", "high", "open", "close", "volume"]


def fetch_hourly_candles(
    product_id: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
    session: requests.Session | None = None,
    pause_seconds: float = 0.15,
) -> pd.DataFrame:
    """Fetch one product in chunks small enough for Coinbase's candle limit."""
    client = session or requests.Session()
    rows: list[list[float]] = []
    cursor = start

    while cursor < end:
        chunk_end = min(cursor + pd.Timedelta(hours=299), end)
        params = {
            "start": cursor.isoformat(),
            "end": chunk_end.isoformat(),
            "granularity": 3600,
        }

        for attempt in range(3):
            response = client.get(
                f"{API_ROOT}/products/{product_id}/candles",
                params=params,
                timeout=30,
            )
            if response.status_code != 429 and response.status_code < 500:
                break
            time.sleep(2**attempt)

        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise RuntimeError(f"Unexpected Coinbase response for {product_id}: {payload}")

        rows.extend(payload)
        cursor = chunk_end
        time.sleep(pause_seconds)

    candles = pd.DataFrame(rows, columns=CANDLE_COLUMNS)
    if candles.empty:
        raise RuntimeError(f"Coinbase returned no candles for {product_id}")

    candles["timestamp"] = pd.to_datetime(candles["timestamp"], unit="s", utc=True)
    candles = candles[(candles["timestamp"] >= start) & (candles["timestamp"] < end)]
    candles = candles.drop_duplicates("timestamp").sort_values("timestamp")

    for column in CANDLE_COLUMNS[1:]:
        candles[column] = pd.to_numeric(candles[column], errors="raise")

    return candles.reset_index(drop=True)


def download_hourly_market_data(
    days: int = 180,
    end: pd.Timestamp | None = None,
    output_path: str | Path = "data/hourly_market_data.csv",
) -> pd.DataFrame:
    """Download BTC, ETH, and SOL candles on one UTC hourly window."""
    if days < 1:
        raise ValueError("days must be at least 1")

    end = pd.Timestamp.now(tz="UTC").floor("h") if end is None else pd.Timestamp(end)
    if end.tzinfo is None:
        end = end.tz_localize("UTC")
    else:
        end = end.tz_convert("UTC")
    start = end - pd.Timedelta(days=days)

    session = requests.Session()
    session.headers.update({"User-Agent": "brypt0-vol-radar/0.1"})

    frames = []
    for asset, product_id in PRODUCTS.items():
        print(f"Downloading {product_id}...")
        candles = fetch_hourly_candles(product_id, start, end, session=session)
        candles.insert(0, "product_id", product_id)
        candles.insert(0, "asset", asset)
        frames.append(candles)

    market_data = pd.concat(frames, ignore_index=True)
    market_data = market_data.sort_values(["asset", "timestamp"]).reset_index(drop=True)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    market_data.to_csv(path, index=False)
    print(f"Saved {len(market_data):,} rows to {path}")
    return market_data


def data_quality_summary(
    market_data: pd.DataFrame,
    start: pd.Timestamp | None = None,
    end: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Report coverage and gaps without filling missing candles."""
    rows = []
    for asset, group in market_data.groupby("asset", sort=True):
        timestamps = pd.DatetimeIndex(group["timestamp"])
        expected_start = start if start is not None else timestamps.min()
        expected_end = end if end is not None else timestamps.max() + pd.Timedelta(hours=1)
        expected = pd.date_range(expected_start, expected_end, freq="h", inclusive="left")
        rows.append(
            {
                "asset": asset,
                "rows": len(group),
                "first_hour": timestamps.min(),
                "last_hour": timestamps.max(),
                "missing_hours": len(expected.difference(timestamps)),
                "duplicate_hours": int(timestamps.duplicated().sum()),
            }
        )
    return pd.DataFrame(rows)


def validate_market_data(market_data: pd.DataFrame) -> None:
    """Raise an error if the basic candle rules do not hold."""
    required = {"asset", "product_id", *CANDLE_COLUMNS}
    assert required.issubset(market_data.columns)
    assert set(market_data["asset"]) == set(PRODUCTS)
    assert not market_data.duplicated(["asset", "timestamp"]).any()
    assert market_data[CANDLE_COLUMNS[1:]].notna().all().all()
    assert (market_data[["open", "high", "low", "close"]] > 0).all().all()
    assert (market_data["volume"] >= 0).all()
    assert (market_data["high"] >= market_data[["open", "close", "low"]].max(axis=1)).all()
    assert (market_data["low"] <= market_data[["open", "close", "high"]].min(axis=1)).all()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=180)
    parser.add_argument("--output", default="data/hourly_market_data.csv")
    args = parser.parse_args()

    data = download_hourly_market_data(days=args.days, output_path=args.output)
    validate_market_data(data)
    print(data_quality_summary(data).to_string(index=False))


if __name__ == "__main__":
    main()
