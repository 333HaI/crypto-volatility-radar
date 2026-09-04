# Crypto Volatility Radar

This repo is me trying out Google's TimesFM-3 model on crypto data. The main
question is whether its multivariate setup can learn anything useful from BTC,
ETH, and SOL moving together.

The planned targets are 24-hour realized volatility and trading volume. I also
want to try time-of-day, scheduled macro events, funding rates, and open interest
as covariates where the data is good enough.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/333HaI/crypto-volatility-radar/blob/main/notebooks/crypto_volatility_radar.ipynb)

## What works so far

The notebook can load TimesFM-3 and make a joint 24-hour forecast for six
synthetic series: volatility and volume for each coin. It returns a point
forecast plus p10-p90 quantiles. I checked the same call locally with the real
`timesfm==3.0.1` model and got the expected `(6, 24)` and `(6, 24, 9)` arrays.

There is also a downloader for 180 days of hourly BTC-USD, ETH-USD, and SOL-USD
candles from Coinbase Exchange. My latest run returned 4,315 rows per asset with
no duplicates or broken OHLCV rows.

## Notebook

The notebook is easiest to run in Colab with a T4 GPU. Since this repo is
private, first open [Colab's GitHub browser](https://colab.research.google.com/github),
check **Include Private Repos**, and authorize the `333HaI` GitHub account. Then
open `notebooks/crypto_volatility_radar.ipynb` and use **Runtime > Run all**.

The first model run downloads the public TimesFM-3 checkpoint to Colab's
temporary cache. No Hugging Face token is needed. The small synthetic example
also works on CPU, although the actual forecasting experiments will use a GPU.

## Downloading the data locally

From the project root:

```bash
python -m pip install -r requirements.txt
python -m crypto_radar.data --days 180
```

This creates `data/hourly_market_data.csv`. The file is ignored by Git because it
can be downloaded again.

Coinbase's candle API sometimes has gaps. The current data is missing five shared
hours on May 8, 2026; a second request returned the same gap. I leave those rows
missing for now instead of quietly filling them. Volume is reported in the base
asset, so BTC, ETH, and SOL volumes are not directly comparable yet.

## Project layout

```text
crypto_radar/data.py                  Coinbase candle downloader
notebooks/crypto_volatility_radar.ipynb
requirements.txt
data/                                 downloaded data (ignored)
outputs/                              generated forecasts (ignored)
```

## Still to add

- Return, realized-volatility, and volume features
- Forecasts on the real series
- A rolling-average baseline
- A small Streamlit/Plotly dashboard
- Funding, open interest, and macro-event covariates if they are practical

## Model license

The [TimesFM source](https://github.com/google-research/timesfm) is Apache-2.0.
The [TimesFM-3 weights](https://huggingface.co/google/timesfm-3.0-pytorch) use a
separate non-commercial, non-production license. This is an exploratory project.
