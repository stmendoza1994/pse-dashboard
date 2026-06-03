# PSE Valuation Dashboard

A Streamlit dashboard for Philippine Stock Exchange (PSE) listed companies showing 3-year FCFF, ROIC, and WACC.

## Project Structure

```
pse-dashboard/
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
├── data/
│   ├── pse_valuation.csv           # ← Replace this each quarter
│   └── pse_valuation_breakdown.txt # ← Replace this each quarter
└── .gitignore
```

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

## Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub (make it Public)
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click **New app** → select your repo → set main file to `app.py`
5. Click **Deploy** — live in ~2 minutes

## Quarterly Update

When TTM data refreshes:

```bash
# 1. Run your scraper and overwrite the data files
cp your_new_pse_valuation.csv data/pse_valuation.csv
cp your_new_breakdown.txt data/pse_valuation_breakdown.txt

# 2. Push to GitHub
git add data/
git commit -m "Q3 2025 data update"
git push
```

Streamlit Cloud auto-redeploys on every push. That's it.

## Data Format

`pse_valuation.csv` must have these columns:
- `symbol`, `company`, `sector`, `source`, `fiscal_year`, `status`
- `fcff_2025_m`, `fcff_2024_m`, `fcff_2023_m`
- `roic_pct`, `wacc_pct`
- `rf_pct`, `beta`, `erp_pct`, `ke_pct`
- `rating`, `spread_pct`, `kd_aftertax_pct`
- `equity_weight_pct`, `debt_weight_pct`
- `market_cap_b`, `total_debt_b`
