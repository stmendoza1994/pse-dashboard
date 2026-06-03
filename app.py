import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re as _re

st.set_page_config(
    page_title="PSE Valuation",
    page_icon="🇵🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    font-size: 16px;
    line-height: 1.55;
    letter-spacing: 0.01em;
}

.stApp { background: #f5f6fa; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Hide sidebar collapse button ── */
[data-testid="collapsedControl"] { display: none !important; }
button[kind="header"] { display: none !important; }
.st-emotion-cache-1dr2tuc { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #1d3a4f !important;
    border-right: none;
    min-width: 250px !important;
    max-width: 250px !important;
}
[data-testid="stSidebar"] .block-container { padding: 2rem 1.6rem !important; }
[data-testid="stSidebar"] * { color: #c0d8e4 !important; }
[data-testid="stSidebar"] label {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #6a96ae !important;
    line-height: 2.2 !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #122535 !important;
    border: 1px solid #2a5570 !important;
    border-radius: 10px !important;
    color: #e8f4f8 !important;
    font-size: 0.97rem !important;
    padding: 0.6rem 0.9rem !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] svg {
    fill: #6a96ae !important;
}
[data-testid="stSidebar"] p { color: #6a96ae !important; font-size: 0.88rem !important; }
[data-testid="stSidebar"] [data-testid="stToggle"] label {
    font-size: 0.95rem !important; color: #c0d8e4 !important;
}

/* ── NAV TABS ── */
.nav-tabs {
    display: flex; gap: 0.5rem;
    padding: 0 3rem;
    background: #122535;
    border-bottom: 1px solid #2a4f68;
}
.nav-tab {
    padding: 0.85rem 1.4rem;
    font-size: 0.88rem; font-weight: 600;
    color: #6a96ae; cursor: pointer;
    border-bottom: 2px solid transparent;
    letter-spacing: 0.02em;
    text-decoration: none;
    transition: color 0.15s;
}
.nav-tab:hover { color: #c0d8e4; }
.nav-tab.active { color: #ffffff; border-bottom: 2px solid #5ac8fa; }

/* ── BANNER ── */
.top-banner {
    background: linear-gradient(135deg, #1d3a4f 0%, #122535 100%);
    padding: 1.8rem 3rem;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid #2a4f68;
}
.banner-title {
    font-size: 1.45rem; font-weight: 700; color: #fff;
    letter-spacing: -0.02em; line-height: 1.2;
}
.banner-sub {
    font-size: 0.82rem; color: #6a96ae; margin-top: 0.4rem;
    font-weight: 400; letter-spacing: 0.03em; line-height: 1.5;
}
.banner-stats { display: flex; gap: 3rem; align-items: center; }
.bstat-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #6a96ae; margin-bottom: 0.35rem;
}
.bstat-val {
    font-size: 1.55rem; font-weight: 700; color: #fff; letter-spacing: -0.03em;
}
.bstat-val.g { color: #4cd964; }
.bstat-val.r { color: #ff6b6b; }
.bstat-val.b { color: #5ac8fa; }

/* ── CONTENT ── */
.content { padding: 2.2rem 3rem 3.5rem 3rem; }

/* ── SECTION LABEL ── */
.sec-label {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #8a9faf;
    margin-bottom: 1.1rem; padding-bottom: 0.65rem;
    border-bottom: 1px solid #e2e6ed;
}

/* ── CARDS ── */
.card {
    background: #fff; border-radius: 14px; padding: 1.6rem 1.9rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 2px 10px rgba(0,0,0,0.04);
}
.card-label {
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #8a9faf; margin-bottom: 0.65rem;
}
.card-val {
    font-size: 2rem; font-weight: 700; letter-spacing: -0.03em;
    line-height: 1; color: #1a2e3b;
}
.card-val.g { color: #27ae60; }
.card-val.r { color: #e74c3c; }
.card-val.b { color: #0066cc; }
.card-sub {
    font-size: 0.84rem; color: #8a9faf; margin-top: 0.55rem;
    font-weight: 400; letter-spacing: 0.01em; line-height: 1.5;
}

/* ── TABLE ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important; overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: none !important; margin-right: 1rem;
}

/* ── DETAIL ROWS ── */
.drow {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.72rem 0; border-bottom: 1px solid #f0f3f6;
    font-size: 0.92rem; line-height: 1.4;
}
.drow:last-child { border-bottom: none; }
.dkey { color: #6b7f93; font-weight: 500; flex: 1; }
.dval { font-weight: 600; color: #1a2e3b; text-align: right; min-width: 80px; }
.dval.g { color: #27ae60; }
.dval.r { color: #e74c3c; }
.dval.b { color: #0066cc; }

/* ── BADGE ── */
.badge-g {
    background: #eafaf2; color: #27ae60; border-radius: 20px;
    padding: 4px 14px; font-size: 0.78rem; font-weight: 700;
}
.badge-n {
    background: #fff4e0; color: #e67e22; border-radius: 20px;
    padding: 4px 14px; font-size: 0.78rem; font-weight: 700;
}

/* ── BREAKDOWN ── */
.bkdown {
    background: #f8f9fc; border-radius: 12px; border: 1px solid #e2e6ed;
    padding: 1.6rem 1.8rem;
    font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 0.84rem; color: #2c3e50; white-space: pre-wrap;
    line-height: 1.9; max-height: 580px; overflow-y: auto;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    border: 1px solid #e2e6ed !important; border-radius: 14px !important;
    background: #fff !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}
[data-testid="stExpander"] summary {
    font-size: 1rem !important; font-weight: 600 !important;
    color: #1a2e3b !important; padding: 1.2rem 1.5rem !important;
}
[data-testid="stExpander"] summary:hover {
    background: #f8f9fc !important; border-radius: 14px !important;
}
[data-testid="stExpander"] details[open] summary {
    border-bottom: 1px solid #e2e6ed !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: #fff; border: 1px solid #dde3ec;
    border-radius: 10px; font-size: 0.95rem; color: #1a2e3b;
}
[data-testid="stSelectbox"] svg { fill: #8a9faf !important; }

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
    background: #0066cc !important; color: #fff !important;
    border: none !important; border-radius: 10px !important;
    font-size: 0.9rem !important; font-weight: 600 !important;
    padding: 0.55rem 1.5rem !important; cursor: pointer !important;
}
[data-testid="stDownloadButton"] button:hover { background: #0052a3 !important; }

/* ── ABOUT PAGE ── */
.about-wrap { max-width: 780px; margin: 0 auto; padding: 2.5rem 0 4rem 0; }
.about-h1 {
    font-size: 1.9rem; font-weight: 800; color: #1a2e3b;
    letter-spacing: -0.03em; margin-bottom: 0.5rem; line-height: 1.2;
}
.about-lead {
    font-size: 1.05rem; color: #4a6070; font-weight: 400;
    line-height: 1.7; margin-bottom: 2.5rem; letter-spacing: 0.01em;
}
.about-section {
    margin-bottom: 2.5rem;
}
.about-h2 {
    font-size: 1.1rem; font-weight: 700; color: #1a2e3b;
    letter-spacing: -0.01em; margin-bottom: 0.9rem;
    padding-bottom: 0.5rem; border-bottom: 2px solid #e2e6ed;
}
.about-p {
    font-size: 0.97rem; color: #4a6070; line-height: 1.75;
    margin-bottom: 1rem; letter-spacing: 0.01em;
}
.about-formula {
    background: #f5f6fa; border-left: 3px solid #0066cc;
    border-radius: 0 10px 10px 0; padding: 1rem 1.4rem;
    font-family: 'SF Mono','Fira Code','Courier New',monospace;
    font-size: 0.92rem; color: #1a2e3b; margin: 1rem 0;
    letter-spacing: 0.02em;
}
.about-ul {
    margin: 0.8rem 0 1rem 0; padding-left: 0; list-style: none;
}
.about-ul li {
    font-size: 0.95rem; color: #4a6070; line-height: 1.7;
    padding: 0.3rem 0 0.3rem 1.2rem; position: relative;
}
.about-ul li::before {
    content: ""; position: absolute; left: 0; top: 0.75rem;
    width: 6px; height: 6px; border-radius: 50%; background: #0066cc;
}
.about-ul li b { color: #1a2e3b; }
.about-note {
    background: #fff4e0; border-radius: 10px; padding: 1rem 1.4rem;
    font-size: 0.88rem; color: #7a5c20; line-height: 1.65;
    margin-top: 2rem;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def pct(v, sign=False):
    if pd.isna(v) or v is None: return "—"
    return f"{v:+.2f}%" if sign else f"{v:.2f}%"

def money(v):
    if pd.isna(v) or v is None: return "—"
    if abs(v) >= 1_000_000: return f"₱{v/1_000_000:.2f}T"
    if abs(v) >= 1_000:     return f"₱{v/1_000:.1f}B"
    return f"₱{v:,.0f}M"

def clr(v):
    if v is None or (isinstance(v, float) and pd.isna(v)): return ""
    return "g" if v > 0 else "r"

def robust_mean(series):
    s = series.dropna()
    if len(s) == 0: return None
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    filtered = s[(s >= q1 - 1.5 * iqr) & (s <= q3 + 1.5 * iqr)]
    return filtered.mean() if len(filtered) > 0 else None


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    return pd.read_csv("data/pse_valuation.csv")

@st.cache_data
def load_txt():
    with open("data/pse_valuation_breakdown.txt") as f:
        return f.read()

df = load()
txt = load_txt()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:2rem;padding-bottom:1.4rem;border-bottom:1px solid #2a4f68;'>
        <div style='font-size:1.15rem;font-weight:700;color:#fff;
        letter-spacing:-0.02em;line-height:1.2;'>🇵🇭 PSE Valuation</div>
        <div style='font-size:0.82rem;color:#6a96ae;margin-top:0.4rem;'>
        Fundamental Screener</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", ["Dashboard", "About"], label_visibility="collapsed")

    if page == "Dashboard":
        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.78rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6a96ae;margin-bottom:0.5rem;'>Sector</div>", unsafe_allow_html=True)
        sectors = ["All Sectors"] + sorted(df["sector"].dropna().unique().tolist())
        sel_sector = st.selectbox("Sector", sectors, label_visibility="collapsed")
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        only_vc = st.toggle("Value creators only", value=False)

        fdf = df.copy()
        if sel_sector != "All Sectors":
            fdf = fdf[fdf["sector"] == sel_sector]
        if only_vc:
            fdf = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna()
                      & (fdf["roic_pct"] > fdf["wacc_pct"])]

        valid = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna()]
        creators = int((valid["roic_pct"] > valid["wacc_pct"]).sum())

        st.markdown(f"""
        <div style='margin-top:2rem;padding-top:1.4rem;border-top:1px solid #2a4f68;'>
            <div style='font-size:0.7rem;font-weight:700;letter-spacing:0.12em;
            text-transform:uppercase;color:#6a96ae;margin-bottom:1.2rem;'>Summary</div>
            <div style='display:flex;justify-content:space-between;margin-bottom:0.8rem;'>
                <span style='font-size:0.92rem;color:#6a96ae;'>Showing</span>
                <span style='font-size:0.92rem;font-weight:700;color:#fff;'>{len(fdf)} of {len(df)}</span>
            </div>
            <div style='display:flex;justify-content:space-between;margin-bottom:0.8rem;'>
                <span style='font-size:0.92rem;color:#6a96ae;'>With data</span>
                <span style='font-size:0.92rem;font-weight:700;color:#5ac8fa;'>{len(valid)}</span>
            </div>
            <div style='display:flex;justify-content:space-between;'>
                <span style='font-size:0.92rem;color:#6a96ae;'>Value creators</span>
                <span style='font-size:0.92rem;font-weight:700;color:#4cd964;'>{creators}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        fdf = df.copy()
        valid = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna()]
        creators = int((valid["roic_pct"] > valid["wacc_pct"]).sum())
        sel_sector = "All Sectors"
        only_vc = False


# ════════════════════════════════════════════════════════════
#  DASHBOARD PAGE
# ════════════════════════════════════════════════════════════
if page == "Dashboard":

    avg_roic   = robust_mean(valid["roic_pct"])
    avg_wacc   = robust_mean(valid["wacc_pct"])
    avg_spread = (avg_roic - avg_wacc) if avg_roic is not None and avg_wacc is not None else None
    sc = clr(avg_spread)

    st.markdown(f"""
    <div class="top-banner">
        <div>
            <div class="banner-title">PSE Valuation Dashboard</div>
            <div class="banner-sub">
                FCFF · ROIC · WACC &nbsp;·&nbsp; Yahoo Finance & Reuters
                &nbsp;·&nbsp; Rf 7.706% · Tax 25% · ERP 6.69%
            </div>
        </div>
        <div class="banner-stats">
            <div><div class="bstat-label">Companies</div>
                 <div class="bstat-val">{len(fdf)}</div></div>
            <div><div class="bstat-label">Value Creators</div>
                 <div class="bstat-val g">{creators}</div></div>
            <div><div class="bstat-label">Avg ROIC</div>
                 <div class="bstat-val b">{pct(avg_roic)}</div></div>
            <div><div class="bstat-label">Avg WACC</div>
                 <div class="bstat-val">{pct(avg_wacc)}</div></div>
            <div><div class="bstat-label">Avg Spread</div>
                 <div class="bstat-val {sc}">{pct(avg_spread, sign=True)}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">All Companies</div>', unsafe_allow_html=True)

    tbl = fdf[["symbol","company","sector","fcff_2025_m","fcff_2024_m","fcff_2023_m",
               "roic_pct","wacc_pct","rating","market_cap_b"]].copy()
    tbl["Spread"] = tbl["roic_pct"] - tbl["wacc_pct"]
    tbl = tbl.rename(columns={
        "symbol":"Ticker","company":"Company","sector":"Sector",
        "fcff_2025_m":"FCFF 2025 (₱M)","fcff_2024_m":"FCFF 2024 (₱M)",
        "fcff_2023_m":"FCFF 2023 (₱M)","roic_pct":"ROIC (%)","wacc_pct":"WACC (%)",
        "rating":"Rating","market_cap_b":"Mkt Cap (₱B)",
    })

    styled = tbl.style.format({
        "FCFF 2025 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
        "FCFF 2024 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
        "FCFF 2023 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
        "ROIC (%)":       lambda v: f"{v:.2f}%" if pd.notna(v) else "—",
        "WACC (%)":       lambda v: f"{v:.2f}%" if pd.notna(v) else "—",
        "Spread":         lambda v: f"{v:+.2f}%" if pd.notna(v) else "—",
        "Mkt Cap (₱B)":  lambda v: f"{v:,.3f}" if pd.notna(v) else "—",
    }).set_properties(**{
        "background-color": "#ffffff",
        "color": "#1a2e3b",
        "font-size": "0.92rem",
        "border-color": "#dce8f0",
    }).set_table_styles([
        {"selector": "thead th", "props": [
            ("background-color", "#eaf2f8"),
            ("color", "#2a6080"),
            ("font-size", "0.75rem"),
            ("font-weight", "700"),
            ("letter-spacing", "0.06em"),
            ("text-transform", "uppercase"),
            ("border-bottom", "2px solid #b8d4e4"),
        ]},
        {"selector": "tbody tr:hover td", "props": [("background-color", "#f0f7fb")]},
        {"selector": "td", "props": [("border-bottom", "1px solid #dce8f0")]},
    ]).map(
        lambda v: "color:#27ae60;font-weight:600" if isinstance(v,float) and pd.notna(v) and v > 0
        else ("color:#e74c3c;font-weight:600" if isinstance(v,float) and pd.notna(v) and v < 0 else ""),
        subset=["Spread"]
    )

    st.dataframe(styled, use_container_width=True, height=380)

    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)
    csv_data = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇  Export to CSV",
        data=csv_data,
        file_name=f"pse_valuation_{sel_sector.lower().replace(' ','_')}.csv",
        mime="text/csv",
    )

    # ── Company Deep Dive ──────────────────────────────────────────────────────
    st.markdown('<div style="height:2.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Company Deep Dive</div>', unsafe_allow_html=True)

    tickers = fdf["symbol"].tolist()
    sel = st.selectbox(
        "Select a company",
        tickers,
        format_func=lambda t: f"{t}  —  {df[df['symbol']==t]['company'].values[0]}"
    )

    row = fdf[fdf["symbol"] == sel].iloc[0]
    sp = (row["roic_pct"] - row["wacc_pct"]) if pd.notna(row["roic_pct"]) and pd.notna(row["wacc_pct"]) else None
    is_vc = sp is not None and sp > 0

    st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        fv = row["fcff_2025_m"] if pd.notna(row["fcff_2025_m"]) else None
        st.markdown(f"""<div class="card">
            <div class="card-label">FCFF 2025</div>
            <div class="card-val {clr(fv)}">{money(fv)}</div>
            <div class="card-sub">{row['sector']}</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""<div class="card">
            <div class="card-label">ROIC</div>
            <div class="card-val {clr(sp)}">{pct(row['roic_pct'])}</div>
            <div class="card-sub">Return on Invested Capital</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""<div class="card">
            <div class="card-label">WACC</div>
            <div class="card-val b">{pct(row['wacc_pct'])}</div>
            <div class="card-sub">Weighted Avg Cost of Capital</div>
        </div>""", unsafe_allow_html=True)

    with k4:
        sp_str = pct(sp, sign=True)
        bdg = f"<span class='badge-{'g' if is_vc else 'n'}'>ROIC {'above' if is_vc else 'below'} WACC</span>" if sp is not None else ""
        st.markdown(f"""<div class="card">
            <div class="card-label">ROIC - WACC Spread</div>
            <div class="card-val {clr(sp)}">{sp_str}</div>
            <div class="card-sub" style="margin-top:0.65rem">{bdg}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        wv = row["wacc_pct"]          if pd.notna(row["wacc_pct"])          else None
        ke = row["ke_pct"]            if pd.notna(row["ke_pct"])            else None
        kd = row["kd_aftertax_pct"]   if pd.notna(row["kd_aftertax_pct"])   else None
        ew = row["equity_weight_pct"] if pd.notna(row["equity_weight_pct"]) else None
        dw = row["debt_weight_pct"]   if pd.notna(row["debt_weight_pct"])   else None

        st.markdown(f"""<div class="card">
            <div style="font-size:1rem;font-weight:700;color:#1a2e3b;
            letter-spacing:-0.01em;margin-bottom:1.3rem;">WACC Components</div>
            <div class="drow"><span class="dkey">Risk-Free Rate (Rf)</span><span class="dval">{pct(row['rf_pct'])}</span></div>
            <div class="drow"><span class="dkey">Beta (β)</span><span class="dval">{f"{row['beta']:.3f}" if pd.notna(row['beta']) else '—'}</span></div>
            <div class="drow"><span class="dkey">Equity Risk Premium</span><span class="dval">{pct(row['erp_pct'])}</span></div>
            <div class="drow"><span class="dkey">Cost of Equity (Ke)</span><span class="dval b">{pct(ke)}</span></div>
            <div class="drow"><span class="dkey">Credit Rating</span><span class="dval">{row['rating'] if pd.notna(row['rating']) else '—'}</span></div>
            <div class="drow"><span class="dkey">Credit Spread</span><span class="dval">{pct(row['spread_pct'])}</span></div>
            <div class="drow"><span class="dkey">Kd after-tax</span><span class="dval r">{pct(kd)}</span></div>
            <div class="drow"><span class="dkey">Equity Weight (E/V)</span><span class="dval">{pct(ew)}</span></div>
            <div class="drow"><span class="dkey">Debt Weight (D/V)</span><span class="dval">{pct(dw)}</span></div>
            <div class="drow" style="border-top:2px solid #e2e6ed;margin-top:0.5rem;padding-top:1rem;">
                <span style="font-weight:700;color:#1a2e3b;font-size:1rem;">WACC</span>
                <span style="font-weight:800;font-size:1.25rem;color:#0066cc;">{pct(wv)}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with right:
        yrs  = [2023, 2024, 2025]
        vals = [row["fcff_2023_m"], row["fcff_2024_m"], row["fcff_2025_m"]]
        bcolors = ["#27ae60" if pd.notna(v) and v > 0 else "#e74c3c" for v in vals]

        fig1 = go.Figure(go.Bar(
            x=yrs, y=vals, marker_color=bcolors, marker_line_width=0,
            text=[money(v) for v in vals], textposition="outside",
            textfont=dict(size=12, color="#1a2e3b", family="Inter"), width=0.5,
        ))
        fig1.add_hline(y=0, line_color="#e2e6ed", line_width=1.5)
        fig1.update_layout(
            title=dict(text=f"<b>{sel}</b> — 3-Year FCFF",
                       font=dict(size=13, color="#1a2e3b", family="Inter"), x=0),
            paper_bgcolor="#fff", plot_bgcolor="#fff",
            font=dict(family="Inter", color="#8a9faf", size=12),
            margin=dict(l=8, r=8, t=50, b=8),
            yaxis=dict(gridcolor="#f0f3f6", zeroline=False, tickformat=",.0f",
                       tickfont=dict(size=11, color="#8a9faf")),
            xaxis=dict(tickvals=yrs, tickfont=dict(size=12, color="#1a2e3b")),
            bargap=0.25, showlegend=False, height=250,
        )

        rv2 = row["roic_pct"] if pd.notna(row["roic_pct"]) else 0
        wv2 = row["wacc_pct"] if pd.notna(row["wacc_pct"]) else 0
        fig2 = go.Figure(go.Bar(
            x=["ROIC", "WACC"], y=[rv2, wv2],
            marker_color=["#27ae60" if rv2 >= wv2 else "#e74c3c", "#0066cc"],
            marker_line_width=0,
            text=[pct(rv2), pct(wv2)], textposition="outside",
            textfont=dict(size=13, color="#1a2e3b", family="Inter"), width=0.4,
        ))
        fig2.update_layout(
            paper_bgcolor="#fff", plot_bgcolor="#fff",
            font=dict(family="Inter", color="#8a9faf", size=12),
            margin=dict(l=8, r=8, t=12, b=8),
            yaxis=dict(gridcolor="#f0f3f6", ticksuffix="%", zeroline=False,
                       tickfont=dict(size=11, color="#8a9faf")),
            xaxis=dict(tickfont=dict(size=13, color="#1a2e3b")),
            bargap=0.5, showlegend=False, height=210,
        )

        st.markdown('<div class="card" style="padding:1.3rem 1.5rem;">', unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<hr style="border:none;border-top:1px solid #f0f3f6;margin:0.2rem 0;">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
    with st.expander(f"📋   View Full Computation Breakdown  —  {sel}"):
        parts = _re.split(r'={60,}', txt)
        found = ""
        for i, part in enumerate(parts):
            if _re.search(rf'^\s+{_re.escape(sel)}\s+—', part, _re.MULTILINE):
                section = part
                if i + 1 < len(parts): section += "=" * 70 + parts[i + 1]
                if i + 2 < len(parts): section += "=" * 70 + parts[i + 2]
                found = section.strip()
                break
        if found:
            st.markdown(f'<div class="bkdown">{found}</div>', unsafe_allow_html=True)
        else:
            st.info("Breakdown not available for this company.")

    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  ABOUT PAGE
# ════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-wrap">

        <div class="about-h1">About This Project</div>
        <div class="about-lead">
            A free, open-access fundamental valuation dashboard for all Philippine
            Stock Exchange-listed companies. Built for the everyday Filipino investor.
        </div>

        <div class="about-section">
            <div class="about-h2">Why This Exists</div>
            <div class="about-p">
                Only 2% of Filipinos, or possibly less, invest in the stock market.
                For a country of 115 million people, that reach is strikingly narrow,
                and it points to something more than just a lack of interest.
            </div>
            <div class="about-p">
                One of the biggest barriers is data. Fundamental financial data, the kind
                that serious investors use to evaluate whether a company is actually creating
                value, exists, but it is fragmented, paywalled, or buried in dense annual
                reports. Subscribing to a financial data terminal costs more per month than
                many Filipinos earn in a week. For someone who wants to invest ₱5,000,
                paying ₱3,000 for data defeats the purpose.
            </div>
            <div class="about-p">
                This dashboard was built to change that. Every metric here, FCFF, ROIC,
                and WACC, is computed from publicly available sources and made available
                for free.
            </div>
            <div class="about-p">
                This is a personal contribution to financial inclusion, the belief that
                the tools of fundamental analysis should not be reserved for institutions
                and professionals. They belong to every Filipino who wants to build
                long-term wealth.
            </div>
            <div class="about-p">
                This is a work in progress. The methodology, coverage, and presentation
                will continue to improve over time as more data becomes available and
                the framework is refined.
            </div>
        </div>

        <div class="about-section">
            <div class="about-h2">FCFF — Free Cash Flow to the Firm</div>
            <div class="about-p">
                FCFF measures how much real cash a company generates from its operations
                after accounting for the investments needed to sustain and grow the business.
                Unlike reported earnings, FCFF is harder to distort through accounting
                choices. It is one of the most direct measures of a company's underlying
                economic output.
            </div>
            <div class="about-formula">FCFF = NOPAT + D&A - Change in NWC - CapEx</div>
            <ul class="about-ul">
                <li><b>NOPAT</b> = EBIT x (1 - Tax Rate), operating profit after tax, before financing costs</li>
                <li><b>D&A</b> = Depreciation and Amortization, a non-cash charge added back</li>
                <li><b>Change in NWC</b> = Change in Net Working Capital, cash tied up or released by operations</li>
                <li><b>CapEx</b> = Capital Expenditures, cash spent on maintaining and growing assets</li>
            </ul>
            <div class="about-p">
                Three years of FCFF are shown (2023, 2024, 2025) to reveal the trend,
                not just a snapshot.
            </div>
        </div>

        <div class="about-section">
            <div class="about-h2">ROIC — Return on Invested Capital</div>
            <div class="about-p">
                ROIC answers one fundamental question: for every peso of capital entrusted
                to this company, by shareholders and lenders alike, how much annual
                operating profit does it generate?
            </div>
            <div class="about-formula">ROIC = NOPAT / Average Invested Capital</div>
            <div class="about-p" style="margin-top:0.6rem;">
                Where Invested Capital = Total Debt + Book Equity - Cash
            </div>
            <div class="about-p">
                A ROIC of 12% means the company generates ₱12 of annual operating profit
                for every ₱100 of capital deployed in the business. On its own, this number
                means little. Its power comes when compared to WACC.
            </div>
        </div>

        <div class="about-section">
            <div class="about-h2">WACC — Weighted Average Cost of Capital</div>
            <div class="about-p">
                WACC is the minimum annual return a company must earn to satisfy both its
                shareholders and its lenders. It is the hurdle rate, the floor below which
                a company is not generating sufficient returns relative to the risk taken,
                even if it is reporting a profit.
            </div>
            <div class="about-formula">WACC = (E/V) x Ke + (D/V) x Kd x (1 - Tax Rate)</div>
            <ul class="about-ul">
                <li><b>Ke</b> = Cost of Equity, estimated using CAPM: Ke = Rf + Beta x ERP</li>
                <li><b>Kd</b> = Cost of Debt, estimated from the company's credit rating using Damodaran's synthetic rating table</li>
                <li><b>Rf</b> = 7.706%, the 25-year BVAL risk-free rate from the Bureau of the Treasury</li>
                <li><b>ERP</b> = 6.69%, the Philippines Equity Risk Premium from Damodaran's country risk premium dataset</li>
                <li><b>E/V and D/V</b> = market-value weights, using live market capitalization for equity</li>
            </ul>
        </div>

        <div class="about-section">
            <div class="about-h2">The ROIC vs. WACC Spread</div>
            <div class="about-p">
                The most important signal in this dashboard is the spread between ROIC and WACC.
            </div>
            <ul class="about-ul">
                <li><b>ROIC above WACC</b> means the company is generating annual returns above its cost of capital. Every peso of capital deployed is producing more than it costs to deploy.</li>
                <li><b>ROIC below WACC</b> means the company is earning less than what its capital costs. Even if it reports a profit, it is not generating sufficient returns relative to the risk taken by shareholders and lenders.</li>
            </ul>
            <div class="about-p">
                This spread is the lens through which long-term investors evaluate whether
                a business deserves more capital.
            </div>
        </div>

        <div class="about-section">
            <div class="about-h2">How the Data Was Collected</div>
            <div class="about-p">
                Financial statements for PSE-listed companies were collected from two
                publicly available sources:
            </div>
            <ul class="about-ul">
                <li><b>Yahoo Finance</b>, for companies with OTC tickers available internationally, accessed via the yfinance Python library</li>
                <li><b>Reuters</b>, for companies listed only on the PSE (.PS tickers), collected via automated browser scripts using Selenium and Chrome</li>
            </ul>
            <div class="about-p">
                The scraping, computation, and output generation are fully automated in
                Python. Results are exported to CSV and a narrative breakdown file, then
                pushed to GitHub. The dashboard is hosted on Streamlit Community Cloud,
                a free platform that serves the app directly from the GitHub repository.
                The entire pipeline runs on open-source tools.
            </div>
        </div>

        <div class="about-section">
            <div class="about-h2">On Sustainability and Financial Inclusion</div>
            <div class="about-p">
                Markets work better when more people participate in them. A stock market
                where participation is limited to a small fraction of the population
                constrains liquidity, price discovery, and the efficient allocation of
                capital. These are not abstract concerns. They affect the cost of doing
                business, the availability of financing for small enterprises, and the
                long-term development of the economy.
            </div>
            <div class="about-p">
                This project sits at the intersection of financial literacy, open data,
                and sustainability. It is one small attempt to make fundamental analysis
                more accessible. It will be updated every quarter as companies publish
                new financial statements.
            </div>
        </div>

        <div class="about-note">
            <b>Limitations.</b> This dashboard is for informational and educational purposes
            only. It is not investment advice. The computations follow standard academic
            frameworks but rely on publicly available data that may contain errors or
            omissions. Some companies have incomplete data due to limited disclosures or
            non-standard reporting formats. Always do your own research before making
            investment decisions.
        </div>

    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#1d3a4f;padding:1.3rem 3rem;margin-top:2rem;
text-align:center;font-size:0.78rem;color:#6a96ae;letter-spacing:0.03em;line-height:1.7;'>
    PSE Valuation Dashboard &nbsp;·&nbsp;
    FCFF = NOPAT + D&amp;A - Change in NWC - CapEx &nbsp;·&nbsp;
    ROIC = NOPAT / Avg IC &nbsp;·&nbsp;
    WACC = (E/V)Ke + (D/V)Kd(1-t) &nbsp;·&nbsp;
    Data: Yahoo Finance & Reuters
</div>
""", unsafe_allow_html=True)
