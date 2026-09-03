# Crypto Volatility Radar

A small Python learning project for jointly forecasting realized volatility and
trading volume for **BTC, ETH, and SOL** with Google's **TimesFM-3**. The planned
forecast horizon is 24 hourly steps. GPU inference will run in Google Colab; a
Streamlit dashboard with Plotly charts will follow later.

**Current stage: step 1 — repository and Colab notebook setup.**
The notebook runs environment checks only. Forecasts and a dashboard are not yet
implemented.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/333HaI/crypto-volatility-radar/blob/main/notebooks/crypto_volatility_radar.ipynb)

## Run step 1

1. Open [Colab's GitHub browser](https://colab.research.google.com/github) and
   sign in to Google.
2. Check **Include Private Repos**. In the popup, sign in to GitHub as `333HaI`
   and authorize Colab to read private repositories. Being signed in to GitHub
   in another tab does not replace this authorization.
3. Search for `333HaI/crypto-volatility-radar`, choose branch `main`, and open
   `notebooks/crypto_volatility_radar.ipynb`. After authorization, the **Open in
   Colab** badge above should also work.
4. Connect to a Python runtime. A **CPU runtime is sufficient for step 1**.
5. Select **Runtime → Run all**.
6. Check that the final cell prints:

   ```text
   Step 1 setup OK.
   Assets: BTC, ETH, SOL
   Planned targets: 6 channels; horizon: 24 hourly steps.
   Stop here. Step 2 will add the synthetic TimesFM-3 inference check.
   ```

If the direct Colab link reports GitHub `404 Not Found`, complete steps 1–2
first. GitHub hides private resources from unauthenticated requests with a 404;
this can happen even when the notebook exists. See
[Google's private-notebook instructions](https://github.com/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb)
and [GitHub's authentication explanation](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api#404-not-found-for-an-existing-resource).

If Colab cannot access the private repository, download
[`notebooks/crypto_volatility_radar.ipynb`](notebooks/crypto_volatility_radar.ipynb)
from GitHub and use **File → Upload notebook** in Colab. Step 1 is self-contained:
it needs no repository clone, package installation, API key, or model download.

An unavailable GPU is an expected result on a CPU runtime. We will select a GPU
and verify its suitability in step 2. This setup check does not verify TimesFM-3
inference.

Validation on 2026-09-03: the notebook format and all four code cells passed a
top-to-bottom local Jupyter run on Python 3.13.13. Git ignore checks also passed
for credentials, data, outputs, and model weights. A Colab runtime run remains
the user check above; GPU inference has not been attempted.

**Stop after these checks. Proceed to step 2 only when ready.**

## Project layout

```text
crypto-volatility-radar/
├── README.md
├── .gitignore
├── requirements.txt                     # Dependencies added as steps need them
├── notebooks/
│   └── crypto_volatility_radar.ipynb     # Colab walkthrough, extended each step
├── crypto_radar/
│   └── __init__.py                      # Home for reusable Python code later
├── data/
│   └── .gitkeep                         # Downloaded data is ignored by Git
└── outputs/
    └── .gitkeep                         # Generated forecasts/results are ignored
```

The first notebook uses only Python's standard library (Python 3.10+).
There is nothing to install from `requirements.txt` yet. TimesFM-3 dependencies
and the source revision will be pinned after the synthetic inference check in
step 2. Streamlit and Plotly will be added when we build the dashboard.

## Build plan

We implement and test one step at a time, then pause.

1. **Repository and Colab notebook setup** — current step.
2. Run TimesFM-3 on a small synthetic multivariate example using a Colab GPU.
3. Download hourly BTC, ETH, and SOL market data from a free source.
4. Calculate returns, realized volatility, and volume features.
5. Produce joint 24-hour forecasts with quantile intervals.
6. Compare forecasts with a rolling-average baseline on held-out observations.
7. Build a Streamlit dashboard with Plotly uncertainty bands and asset risk ranking.
8. Add screenshots, methodology, limitations, and complete run instructions.

## Planned scope

- Use a shared UTC hourly grid and six target channels: volatility and volume
  for each of the three assets. Final target definitions and units come in step 4.
- Try hour-of-day and day-of-week as known-future covariates after the basic model
  path works. Add scheduled CPI/FOMC/NFP event indicators if a reliable calendar
  is practical; event outcomes must not be treated as known in advance.
- Consider funding rates and open interest as historical-only covariates if free
  data coverage is adequate. Never supply their observed future values to a forecast.
- Keep inference in Colab and let the later dashboard read exported results.
  Quantile coverage and baseline performance still need empirical evaluation.

## Model reference and use limits

Checked on **2026-09-03**:

- [Google's TimesFM-3 announcement](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/)
  describes native multivariate targets, historical and known-future covariates,
  and quantiles from 0.1 through 0.9.
- [Official source and examples](https://github.com/google-research/timesfm)
  use `timesfm3` and the checkpoint `google/timesfm-3.0-pytorch`.
- [Official model card](https://huggingface.co/google/timesfm-3.0-pytorch)
  links the TimesFM Non-Commercial License v1.0. The pretrained weights currently
  restrict use to non-commercial, non-production purposes. This repository is a
  learning/research prototype. The source code's Apache-2.0 license is separate
  from the weights' license.

## Save changes safely

The notebook is versioned in GitHub. After editing in Colab, use
**File → Save a copy in GitHub** and choose this repository and notebook path.
Select **Omit code cell output when saving this notebook**, and review the diff.
Avoid creating an extra Drive copy unless you need one.

Keep credentials in Colab Secrets or environment variables, never in notebook
cells or outputs. Store future model downloads in the runtime cache outside the
repository. `.gitignore` excludes common credential files, weights, data, and
generated outputs; always inspect files before committing because ignore rules
cannot detect every secret.

For a local checkout, inspect changes with:

```bash
git status --short
git diff
```
