# Crypto Volatility Radar

A small forecasting project I am building to learn how TimesFM-3 behaves on
crypto market data. The goal is to jointly forecast 24 hours of realized
volatility and trading volume for BTC, ETH, and SOL, then show the result in a
simple dashboard.

This is being built one step at a time. Right now the data is synthetic. No
trading signal here yet.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/333HaI/crypto-volatility-radar/blob/main/notebooks/crypto_volatility_radar.ipynb)

## Where it is now

- [x] Basic repo and Colab notebook
- [x] TimesFM-3 synthetic forecast (verified locally; Colab GPU run below)
- [ ] Hourly BTC, ETH, and SOL data
- [ ] Returns, realized volatility, and volume features
- [ ] 24-hour forecasts with quantiles
- [ ] Rolling-average baseline
- [ ] Streamlit/Plotly dashboard
- [ ] Screenshots and final write-up

## Run step 2

The repo is private, so authorize it before using the badge:

1. Open [Colab's GitHub browser](https://colab.research.google.com/github).
2. Check **Include Private Repos** and authorize GitHub account `333HaI`.
3. Open `333HaI/crypto-volatility-radar`, branch `main`, then
   `notebooks/crypto_volatility_radar.ipynb`.
4. Choose **Runtime > Change runtime type > T4 GPU**.
5. Choose **Runtime > Run all**.

The first run installs `timesfm==3.0.1` and downloads the public TimesFM-3
checkpoint into Colab's temporary cache. Nothing is downloaded into this repo.
The last cell should print:

```text
Step 2 passed: TimesFM-3 ran a 6-series, 24-hour forecast on the GPU.
Forecast shape: (6, 24)
Quantile shape: (6, 24, 9)
Next: stop here. Real hourly market data comes in step 3.
```

If the notebook link gives a GitHub 404, Colab has not been given access to the
private repo yet. Go back to step 1 above and check **Include Private Repos**.
You can also download the notebook from GitHub and upload it to Colab manually.

## What this test does

The notebook makes six fake hourly series: volatility and volume for each asset.
They have a daily pattern and a fake scheduled event. TimesFM-3 forecasts all six
series together for 24 hours, using hour-of-day and the event flag as
known-future covariates. A few assertions check the output shapes, finite values,
quantile ordering, and the p50 forecast.

Passing this test only proves that the model API and our array shapes work. It
does not say anything about forecast quality on real crypto data.

I also ran the same forecast call locally on September 4, 2026 with
`timesfm==3.0.1`. The real model returned `(6, 24)` point forecasts and
`(6, 24, 9)` quantiles. That run used CPU; the notebook checks the Colab GPU path.

## Files

```text
crypto_radar/                         reusable Python code (added when useful)
data/                                 local downloads; ignored by Git
notebooks/crypto_volatility_radar.ipynb
outputs/                              generated files; ignored by Git
requirements.txt
```

## A couple of project choices

- Everything uses an hourly UTC grid.
- Funding and open interest will be historical covariates if the free data is
  decent enough.
- Hour-of-day, day-of-week, and scheduled CPI/FOMC/NFP flags are candidates for
  known-future covariates. Actual event outcomes will never be future inputs.
- Forecasts run in Colab. The later dashboard will read saved forecast results.

## License note

The [TimesFM source](https://github.com/google-research/timesfm) is Apache-2.0,
but the [TimesFM-3 weights](https://huggingface.co/google/timesfm-3.0-pytorch)
currently have a separate non-commercial, non-production license. This repo is a
learning/research project.

## Saving from Colab

Use **File > Save a copy in GitHub**, pick this repo and notebook path, and omit
cell outputs. Keep secrets in Colab Secrets. Model files, downloaded data,
credentials, and generated outputs are ignored, but it is still worth checking
`git status` before committing.
