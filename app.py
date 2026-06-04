import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re as _re

st.set_page_config(
    page_title="PSE-listed Companies Valuation",
    page_icon="🇵🇭",
    layout="wide",
    initial_sidebar_state="collapsed",
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
}

/* Hide sidebar completely */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }

.stApp { background: #f5f6fa; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Force table white - override Streamlit dark theme */
.stDataFrame, .stDataFrame > div, iframe { background: white !important; }
div[data-testid="stDataFrame"] > div { background: white !important; }

/* TOP NAV BAR */
.topbar {
    background: linear-gradient(135deg, #1d3a4f 0%, #122535 100%);
    padding: 1.2rem 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #2a4f68;
}
.topbar-left { display: flex; align-items: center; gap: 2rem; }
.topbar-title { font-size: 1.15rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; white-space: nowrap; }
.topbar-sub { font-size: 0.75rem; color: #6a96ae; font-weight: 400; }
.topbar-stats { display: flex; gap: 2.5rem; align-items: center; }
.bstat-label { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #6a96ae; margin-bottom: 0.2rem; }
.bstat-val { font-size: 1.3rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; }
.bstat-val.g { color: #4cd964; }
.bstat-val.r { color: #ff6b6b; }
.bstat-val.b { color: #5ac8fa; }

/* FILTER BAR */
.filterbar {
    background: #ffffff;
    padding: 1rem 3rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    border-bottom: 1px solid #e2e6ed;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.filter-label {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #8a9faf; white-space: nowrap;
}

/* NAV TABS */
.navtab-wrap { display: flex; gap: 0.3rem; }
.navtab {
    padding: 0.45rem 1.1rem; border-radius: 8px;
    font-size: 0.88rem; font-weight: 600; color: #6b7f93;
    cursor: pointer; border: 1px solid transparent;
    text-decoration: none; background: transparent;
}
.navtab.active {
    background: #eaf3f8; color: #1d3a4f;
    border-color: #b8d4e4;
}

/* CONTENT */
.content { padding: 2rem 7rem 3.5rem 7rem; }

/* SECTION LABEL */
.sec-label {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #8a9faf;
    margin-bottom: 1.1rem; padding-bottom: 0.65rem;
    border-bottom: 1px solid #e2e6ed;
}

/* CARDS */
.card {
    background: #fff; border-radius: 14px; padding: 1.6rem 1.9rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 2px 10px rgba(0,0,0,0.04);
}
.card-label { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #8a9faf; margin-bottom: 0.65rem; }
.card-val { font-size: 2rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1; color: #1a2e3b; }
.card-val.g { color: #27ae60; }
.card-val.r { color: #e74c3c; }
.card-val.b { color: #0066cc; }
.card-sub { font-size: 0.84rem; color: #8a9faf; margin-top: 0.55rem; line-height: 1.5; }

/* TABLE - white with teal gridlines */
[data-testid="stDataFrame"] {
    border-radius: 14px !important; overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: 1px solid #b8d4e4 !important;
    margin-right: 2rem !important;
}
[data-testid="stDataFrame"] table { background: #ffffff !important; border-collapse: collapse !important; }
[data-testid="stDataFrame"] thead tr th {
    background: #eaf3f8 !important; color: #2a6080 !important;
    font-size: 0.75rem !important; font-weight: 700 !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    border-bottom: 2px solid #b8d4e4 !important;
    border-right: 1px solid #b8d4e4 !important;
    padding: 0.75rem 0.9rem !important;
}
[data-testid="stDataFrame"] tbody tr td {
    background: #ffffff !important; color: #1a2e3b !important;
    font-size: 0.92rem !important;
    border-bottom: 1px solid #d0e8f2 !important;
    border-right: 1px solid #d0e8f2 !important;
    padding: 0.65rem 0.9rem !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td { background: #f7fbfd !important; }
[data-testid="stDataFrame"] tbody tr:hover td { background: #eaf3f8 !important; }

/* WACC ROWS */
.drow {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.72rem 0; border-bottom: 1px solid #f0f3f6;
    font-size: 0.92rem; gap: 1rem;
}
.drow:last-child { border-bottom: none; }
.dkey { color: #6b7f93; font-weight: 500; }
.dval { font-weight: 600; color: #1a2e3b; white-space: nowrap; }
.dval.g { color: #27ae60; }
.dval.r { color: #e74c3c; }
.dval.b { color: #0066cc; }

/* BADGES */
.badge-g { background: #eafaf2; color: #27ae60; border-radius: 20px; padding: 4px 14px; font-size: 0.78rem; font-weight: 700; }
.badge-n { background: #fff4e0; color: #e67e22; border-radius: 20px; padding: 4px 14px; font-size: 0.78rem; font-weight: 700; }

/* BREAKDOWN */
.bkdown {
    background: #f8f9fc !important; border-radius: 12px;
    border: 1px solid #dce8f0; padding: 1.6rem 1.8rem;
    font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 0.84rem; color: #2c3e50; white-space: pre-wrap;
    line-height: 1.9; max-height: 580px; overflow-y: auto;
}

/* EXPANDER */
[data-testid="stExpander"],
[data-testid="stExpander"] > details,
[data-testid="stExpander"] details[open],
[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
    background: #ffffff !important;
    border: 1px solid #dce8f0 !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary {
    font-size: 1rem !important; font-weight: 600 !important;
    color: #1a2e3b !important; padding: 1.2rem 1.5rem !important;
    background: #ffffff !important; border-radius: 14px !important;
}
[data-testid="stExpander"] summary:hover {
    background: #f0f7fb !important; color: #1a2e3b !important;
}

/* SELECTBOX */
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important; border: 1px solid #b8d4e4 !important;
    border-radius: 10px !important; font-size: 0.95rem !important;
    color: #1a2e3b !important;
}
[data-testid="stSelectbox"] > div > div * { color: #1a2e3b !important; }
[data-testid="stSelectbox"] svg { fill: #5a8fa8 !important; }

/* DOWNLOAD BUTTON */
[data-testid="stDownloadButton"] button {
    background: #0066cc !important; color: #fff !important;
    border: none !important; border-radius: 10px !important;
    font-size: 0.9rem !important; font-weight: 600 !important;
    padding: 0.55rem 1.5rem !important;
}

/* ABOUT */
.about-wrap { max-width: 780px; margin: 0 auto; padding: 2.5rem 0 4rem 0; }
.about-h1 { font-size: 1.9rem; font-weight: 800; color: #1a2e3b; letter-spacing: -0.03em; margin-bottom: 0.5rem; }
.about-lead { font-size: 1.05rem; color: #4a6070; line-height: 1.75; margin-bottom: 2.5rem; }
.about-section { margin-bottom: 2.5rem; }
.about-h2 { font-size: 1.1rem; font-weight: 700; color: #1a2e3b; margin-bottom: 0.9rem; padding-bottom: 0.5rem; border-bottom: 2px solid #dce8f0; }
.about-p { font-size: 0.97rem; color: #4a6070; line-height: 1.75; margin-bottom: 1rem; }
.about-formula { background: #f0f7fb; border-left: 3px solid #0066cc; border-radius: 0 10px 10px 0; padding: 1rem 1.4rem; font-family: 'SF Mono','Fira Code','Courier New',monospace; font-size: 0.92rem; color: #1a2e3b; margin: 1rem 0; }
.about-ul { margin: 0.8rem 0 1rem 0; padding-left: 0; list-style: none; }
.about-ul li { font-size: 0.95rem; color: #4a6070; line-height: 1.75; padding: 0.3rem 0 0.3rem 1.2rem; position: relative; }
.about-ul li::before { content: ""; position: absolute; left: 0; top: 0.75rem; width: 6px; height: 6px; border-radius: 50%; background: #0066cc; }
.about-ul li b { color: #1a2e3b; }
.about-note { background: #fff8ed; border-radius: 10px; padding: 1rem 1.4rem; font-size: 0.88rem; color: #7a5c20; line-height: 1.65; margin-top: 2rem; border: 1px solid #f5dfa0; }

[data-testid="stToggle"] label { color: #1a2e3b !important; font-size: 0.95rem !important; font-weight: 600 !important; }
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

# ── Filter bar ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div>
            <div class="topbar-title">🇵🇭 PSE Valuation Dashboard</div>
            <div class="topbar-sub">FCFF · ROIC · WACC &nbsp;·&nbsp; Yahoo Finance & Reuters &nbsp;·&nbsp; Rf 7.706% · Tax 25% · ERP 6.69%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Filter row
col_sector, col_vc, col_space, col_about = st.columns([2, 1.8, 4, 1])

with col_about:
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    if st.button("ℹ About", use_container_width=True):
        st.session_state["page"] = "About"
    if "page" not in st.session_state:
        st.session_state["page"] = "Dashboard"

page = st.session_state.get("page", "Dashboard")

with col_sector:
    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
    sectors = ["All Sectors"] + sorted(df["sector"].dropna().unique().tolist())
    sel_sector = st.selectbox("Sector", sectors, label_visibility="collapsed")
    if sel_sector != st.session_state.get("_last_sector", sel_sector):
        st.session_state["page"] = "Dashboard"
    st.session_state["_last_sector"] = sel_sector

with col_vc:
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    only_vc = st.toggle("Value creators only", value=False)
    if only_vc != st.session_state.get("_last_vc", only_vc):
        st.session_state["page"] = "Dashboard"
    st.session_state["_last_vc"] = only_vc

# Apply filters
fdf = df.copy()
if sel_sector != "All Sectors":
    fdf = fdf[fdf["sector"] == sel_sector]
if only_vc:
    fdf = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna()
              & (fdf["roic_pct"] > fdf["wacc_pct"])]

valid = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna()]
creators = int((valid["roic_pct"] > valid["wacc_pct"]).sum())
avg_roic   = robust_mean(valid["roic_pct"])
avg_wacc   = robust_mean(valid["wacc_pct"])
avg_spread = (avg_roic - avg_wacc) if avg_roic is not None and avg_wacc is not None else None

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# Stats bar
s1, s2, s3, s4, s5 = st.columns(5)
for col, label, val, color in [
    (s1, "Companies", str(len(fdf)), "#1a2e3b"),
    (s2, "Value Creators", str(creators), "#27ae60"),
    (s3, "Avg ROIC", pct(avg_roic), "#0066cc"),
    (s4, "Avg WACC", pct(avg_wacc), "#1a2e3b"),
    (s5, "Avg Spread", pct(avg_spread, sign=True), "#27ae60" if avg_spread and avg_spread > 0 else "#e74c3c"),
]:
    col.markdown(f"""
    <div style='background:#fff;border-radius:12px;padding:1rem 1.4rem;text-align:center;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);'>
        <div style='font-size:1.3rem;font-weight:700;letter-spacing:0.1em;
        text-transform:uppercase;color:#003d7a;margin-bottom:0.3rem;'>{label}</div>
        <div style='font-size:1.5rem;font-weight:700;color:{color};
        letter-spacing:-0.02em;'>{val}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="content">', unsafe_allow_html=True)


# ════════════════════════════════
#  DASHBOARD
# ════════════════════════════════
if page == "Dashboard":

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

    def fmt(v, typ):
        if pd.isna(v) or v is None: return "—"
        if typ == "m": return f"{v:,.1f}"
        if typ == "pct": return f"{v:.2f}%"
        if typ == "spct": return f"{v:+.2f}%"
        if typ == "b": return f"{v:,.3f}"
        return str(v)

    rows_html = ""
    for i, r in tbl.iterrows():
        sp_val = r["Spread"]
        sp_color = "#27ae60" if pd.notna(sp_val) and sp_val > 0 else ("#e74c3c" if pd.notna(sp_val) and sp_val < 0 else "#1a2e3b")
        bg = "#f7fbfd" if i % 2 == 0 else "#ffffff"
        rows_html += f"""<tr style='background:{bg};'>
            <td>{r['Ticker']}</td>
            <td>{r['Company']}</td>
            <td>{r['Sector']}</td>
            <td style='text-align:right'>{fmt(r['FCFF 2025 (₱M)'],'m')}</td>
            <td style='text-align:right'>{fmt(r['FCFF 2024 (₱M)'],'m')}</td>
            <td style='text-align:right'>{fmt(r['FCFF 2023 (₱M)'],'m')}</td>
            <td style='text-align:right'>{fmt(r['ROIC (%)'],'pct')}</td>
            <td style='text-align:right'>{fmt(r['WACC (%)'],'pct')}</td>
            <td>{r['Rating'] if pd.notna(r['Rating']) else '—'}</td>
            <td style='text-align:right'>{fmt(r['Mkt Cap (₱B)'],'b')}</td>
            <td style='text-align:right;color:{sp_color};font-weight:600'>{fmt(sp_val,'spct')}</td>
        </tr>"""

    table_html = f"""
    <div style='overflow-x:auto;overflow-y:auto;max-height:420px;max-width:75%;margin:0 auto;border-radius:14px;border:1px solid #b8d4e4;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-right:2rem;margin-bottom:1rem;'>
    <table style='width:100%;border-collapse:collapse;background:#ffffff;font-family:Inter,sans-serif;font-size:0.88rem;'>
        <thead>
            <tr style='background:#eaf3f8;'>
                <th style='padding:0.75rem 0.9rem;text-align:left;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>Ticker</th>
                <th style='padding:0.75rem 0.9rem;text-align:left;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>Company</th>
                <th style='padding:0.75rem 0.9rem;text-align:left;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>Sector</th>
                <th style='padding:0.75rem 0.9rem;text-align:right;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>FCFF 2025 (₱M)</th>
                <th style='padding:0.75rem 0.9rem;text-align:right;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>FCFF 2024 (₱M)</th>
                <th style='padding:0.75rem 0.9rem;text-align:right;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>FCFF 2023 (₱M)</th>
                <th style='padding:0.75rem 0.9rem;text-align:right;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>ROIC (%)</th>
                <th style='padding:0.75rem 0.9rem;text-align:right;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>WACC (%)</th>
                <th style='padding:0.75rem 0.9rem;text-align:left;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>Rating</th>
                <th style='padding:0.75rem 0.9rem;text-align:right;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;border-right:1px solid #b8d4e4;'>Mkt Cap (₱B)</th>
                <th style='padding:0.75rem 0.9rem;text-align:right;color:#2a6080;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-bottom:2px solid #b8d4e4;'>Spread</th>
            </tr>
        </thead>
        <tbody style='color:#1a2e3b;'>
            {rows_html}
        </tbody>
    </table>
    </div>"""
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)
    csv_data = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇  Export to CSV",
        data=csv_data,
        file_name=f"pse_valuation_{sel_sector.lower().replace(' ','_')}.csv",
        mime="text/csv",
    )

    st.markdown('<div style="height:2.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Company Deep Dive</div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.88rem;color:#6b7f93;font-weight:600;margin-bottom:0.5rem;'>Select a company</div>", unsafe_allow_html=True)

    tickers = fdf["symbol"].tolist()
    sel = st.selectbox(
        "Select a company", tickers,
        format_func=lambda t: f"{t}  —  {df[df['symbol']==t]['company'].values[0]}",
        label_visibility="collapsed"
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
        bdg = f"<span class='badge-{'g' if is_vc else 'n'}'>ROIC {'above' if is_vc else 'below'} WACC</span>" if sp is not None else ""
        st.markdown(f"""<div class="card">
            <div class="card-label">ROIC - WACC Spread</div>
            <div class="card-val {clr(sp)}">{pct(sp, sign=True)}</div>
            <div class="card-sub" style="margin-top:0.65rem">{bdg}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        wv = row["wacc_pct"]          if pd.notna(row["wacc_pct"])          else None
        ke = row["ke_pct"]            if pd.notna(row["ke_pct"])            else None
        kd = row["kd_aftertax_pct"]   if pd.notna(row["kd_aftertax_pct"])   else None
        ew = row["equity_weight_pct"] if pd.notna(row["equity_weight_pct"]) else None
        dw = row["debt_weight_pct"]   if pd.notna(row["debt_weight_pct"])   else None
        st.markdown(f"""<div class="card">
            <div style="font-size:1rem;font-weight:700;color:#1a2e3b;margin-bottom:1.3rem;">WACC Components</div>
            <div class="drow"><span class="dkey">Risk-Free Rate (Rf)</span><span class="dval">{pct(row['rf_pct'])}</span></div>
            <div class="drow"><span class="dkey">Beta (β)</span><span class="dval">{f"{row['beta']:.3f}" if pd.notna(row['beta']) else '—'}</span></div>
            <div class="drow"><span class="dkey">Equity Risk Premium</span><span class="dval">{pct(row['erp_pct'])}</span></div>
            <div class="drow"><span class="dkey">Cost of Equity (Ke)</span><span class="dval b">{pct(ke)}</span></div>
            <div class="drow"><span class="dkey">Credit Rating</span><span class="dval">{row['rating'] if pd.notna(row['rating']) else '—'}</span></div>
            <div class="drow"><span class="dkey">Credit Spread</span><span class="dval">{pct(row['spread_pct'])}</span></div>
            <div class="drow"><span class="dkey">Kd after-tax</span><span class="dval r">{pct(kd)}</span></div>
            <div class="drow"><span class="dkey">Equity Weight (E/V)</span><span class="dval">{pct(ew)}</span></div>
            <div class="drow"><span class="dkey">Debt Weight (D/V)</span><span class="dval">{pct(dw)}</span></div>
            <div class="drow" style="border-top:2px solid #dce8f0;margin-top:0.5rem;padding-top:1rem;">
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
            textfont=dict(size=12, color="#1a2e3b", family="Inter"), width=0.55,
        ))
        fig1.add_hline(y=0, line_color="#dce8f0", line_width=1.5)
        fig1.update_layout(
            title=dict(text=f"<b>{sel}</b> — 3-Year FCFF",
                       font=dict(size=13, color="#1a2e3b", family="Inter"), x=0),
            paper_bgcolor="#fff", plot_bgcolor="#fff",
            font=dict(family="Inter", color="#8a9faf", size=12),
            margin=dict(l=8, r=8, t=50, b=8),
            yaxis=dict(gridcolor="#f0f3f6", zeroline=False, tickformat=",.0f",
                       tickfont=dict(size=11, color="#8a9faf")),
            xaxis=dict(tickvals=yrs, tickfont=dict(size=12, color="#1a2e3b")),
            bargap=0.15, showlegend=False, height=255,
        )

        rv2 = row["roic_pct"] if pd.notna(row["roic_pct"]) else 0
        wv2 = row["wacc_pct"] if pd.notna(row["wacc_pct"]) else 0
        fig2 = go.Figure(go.Bar(
            x=["ROIC", "WACC"], y=[rv2, wv2],
            marker_color=["#27ae60" if rv2 >= wv2 else "#e74c3c", "#0066cc"],
            marker_line_width=0,
            text=[pct(rv2), pct(wv2)], textposition="outside",
            textfont=dict(size=13, color="#1a2e3b", family="Inter"), width=0.45,
        ))
        fig2.update_layout(
            paper_bgcolor="#fff", plot_bgcolor="#fff",
            font=dict(family="Inter", color="#8a9faf", size=12),
            margin=dict(l=8, r=8, t=12, b=8),
            yaxis=dict(gridcolor="#f0f3f6", ticksuffix="%", zeroline=False,
                       tickfont=dict(size=11, color="#8a9faf")),
            xaxis=dict(tickfont=dict(size=13, color="#1a2e3b")),
            bargap=0.4, showlegend=False, height=210,
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


# ════════════════════════════════
#  ABOUT PAGE
# ════════════════════════════════
else:
    if st.button("← Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()
    st.markdown("<div style='max-width:780px;margin:0 3rem;padding:2.5rem 3rem 4rem 3rem;background:#fff;border-radius:14px;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-top:1rem;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.9rem;font-weight:800;color:#1a2e3b;letter-spacing:-0.03em;margin-bottom:0.5rem;line-height:1.2;'>About This Project</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:1.05rem;color:#4a6070;line-height:1.75;margin-bottom:2.5rem;'>A free, open-access fundamental valuation dashboard for Philippine Stock Exchange-listed companies. Built for the everyday Filipino investor.</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:1.1rem;font-weight:700;color:#1a2e3b;margin:2rem 0 0.9rem 0;padding-bottom:0.5rem;border-bottom:2px solid #dce8f0;'>Why This Exists</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>Only 2% of Filipinos, or possibly less, invest in the stock market. For a country of 115 million people, that reach is strikingly narrow, and it points to something more than just a lack of interest.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>One of the biggest barriers is data. Fundamental financial data, the kind that serious investors use to evaluate whether a company is actually creating value, exists, but it is fragmented, paywalled, or buried in dense annual reports. Subscribing to a financial data terminal costs more per month than many Filipinos earn in a week. For someone who wants to invest P5,000, paying P3,000 for data defeats the purpose.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>This dashboard was built to change that. Every metric here, FCFF, ROIC, and WACC, is computed from publicly available sources and made available for free.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>This is a personal contribution to financial inclusion, the belief that the tools of fundamental analysis should not be reserved for institutions and professionals. They belong to every Filipino who wants to build long-term wealth.</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>This is a work in progress. The methodology, coverage, and presentation will continue to improve over time as more data becomes available and the framework is refined.</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:1.1rem;font-weight:700;color:#1a2e3b;margin:2rem 0 0.9rem 0;padding-bottom:0.5rem;border-bottom:2px solid #dce8f0;'>FCFF — Free Cash Flow to the Firm</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>FCFF measures how much real cash a company generates from its operations after accounting for the investments needed to sustain and grow the business. Unlike reported earnings, FCFF is harder to distort through accounting choices.</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#f0f7fb;border-left:3px solid #0066cc;border-radius:0 10px 10px 0;padding:1rem 1.4rem;font-family:monospace;font-size:0.92rem;color:#1a2e3b;margin:1rem 0;'>FCFF = NOPAT + D&A - Change in NWC - CapEx</div>", unsafe_allow_html=True)
    st.markdown("<ul style='margin:0.8rem 0 1rem 1.2rem;'><li><b>NOPAT</b> = EBIT x (1 - Tax Rate), operating profit after tax, before financing costs</li><li><b>D&A</b> = Depreciation and Amortization, a non-cash charge added back</li><li><b>Change in NWC</b> = Change in Net Working Capital, cash tied up or released by operations</li><li><b>CapEx</b> = Capital Expenditures, cash spent on maintaining and growing assets</li></ul>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>Three years of FCFF are shown (2023, 2024, 2025) to reveal the trend, not just a snapshot.</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:1.1rem;font-weight:700;color:#1a2e3b;margin:2rem 0 0.9rem 0;padding-bottom:0.5rem;border-bottom:2px solid #dce8f0;'>ROIC — Return on Invested Capital</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>ROIC answers one fundamental question: for every peso of capital entrusted to this company, how much annual operating profit does it generate?</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#f0f7fb;border-left:3px solid #0066cc;border-radius:0 10px 10px 0;padding:1rem 1.4rem;font-family:monospace;font-size:0.92rem;color:#1a2e3b;margin:1rem 0;'>ROIC = NOPAT / Average Invested Capital</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>Where Invested Capital = Total Debt + Book Equity - Cash</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>A ROIC of 12% means the company generates P12 of annual operating profit for every P100 of capital deployed. Its power comes when compared to WACC.</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:1.1rem;font-weight:700;color:#1a2e3b;margin:2rem 0 0.9rem 0;padding-bottom:0.5rem;border-bottom:2px solid #dce8f0;'>WACC — Weighted Average Cost of Capital</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>WACC is the minimum annual return a company must earn to satisfy both its shareholders and its lenders.</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#f0f7fb;border-left:3px solid #0066cc;border-radius:0 10px 10px 0;padding:1rem 1.4rem;font-family:monospace;font-size:0.92rem;color:#1a2e3b;margin:1rem 0;'>WACC = (E/V) x Ke + (D/V) x Kd x (1 - Tax Rate)</div>", unsafe_allow_html=True)
    st.markdown("<ul style='margin:0.8rem 0 1rem 1.2rem;'><li><b>Ke</b> = Cost of Equity: Rf + Beta x ERP</li><li><b>Kd</b> = Cost of Debt from Damodaran's synthetic rating table</li><li><b>Rf</b> = 7.706%, 25-year BVAL rate from Bureau of the Treasury</li><li><b>ERP</b> = 6.69%, Philippines Equity Risk Premium from Damodaran</li><li><b>E/V and D/V</b> = market-value weights using live market capitalization</li></ul>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:1.1rem;font-weight:700;color:#1a2e3b;margin:2rem 0 0.9rem 0;padding-bottom:0.5rem;border-bottom:2px solid #dce8f0;'>The ROIC vs. WACC Spread</div>", unsafe_allow_html=True)
    st.markdown("<ul style='margin:0.8rem 0 1rem 1.2rem;'><li><b>ROIC above WACC</b> means the company generates returns above its cost of capital. Every peso deployed produces more than it costs.</li><li><b>ROIC below WACC</b> means the company earns less than its capital costs. Even with a reported profit, it is not generating sufficient returns relative to risk.</li></ul>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:1.1rem;font-weight:700;color:#1a2e3b;margin:2rem 0 0.9rem 0;padding-bottom:0.5rem;border-bottom:2px solid #dce8f0;'>How the Data Was Collected</div>", unsafe_allow_html=True)
    st.markdown("<ul style='margin:0.8rem 0 1rem 1.2rem;'><li><b>Yahoo Finance</b>, for companies with OTC tickers, via the yfinance Python library</li><li><b>Reuters</b>, for PSE-only (.PS) tickers, via Selenium and Chrome browser scripts</li></ul>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>The pipeline is fully automated in Python. Results are pushed to GitHub and served via Streamlit Community Cloud. The entire stack runs on open-source tools.</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:1.1rem;font-weight:700;color:#1a2e3b;margin:2rem 0 0.9rem 0;padding-bottom:0.5rem;border-bottom:2px solid #dce8f0;'>On Sustainability and Financial Inclusion</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.97rem;color:#4a6070;line-height:1.75;margin-bottom:1rem;'>Markets work better when more people participate in them. A stock market where participation is limited to a small fraction of the population constrains liquidity, price discovery, and capital allocation. This project sits at the intersection of financial literacy, open data, and sustainability. It will be updated every quarter.</div>", unsafe_allow_html=True)

    st.markdown("<div style='background:#fff8ed;border-radius:10px;padding:1rem 1.4rem;font-size:0.88rem;color:#7a5c20;line-height:1.65;margin-top:2rem;border:1px solid #f5dfa0;'><b>Limitations.</b> This dashboard is for informational and educational purposes only. It is not investment advice. Always do your own research before making investment decisions.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)



st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='background:#1d3a4f;padding:1.3rem 3rem;margin-top:2rem;text-align:center;
font-size:0.78rem;color:#6a96ae;letter-spacing:0.03em;line-height:1.7;'>
    PSE Valuation Dashboard &nbsp;·&nbsp;
    FCFF = NOPAT + D&A - Change in NWC - CapEx &nbsp;·&nbsp;
    ROIC = NOPAT / Avg IC &nbsp;·&nbsp;
    WACC = (E/V)Ke + (D/V)Kd(1-t)
</div>
""", unsafe_allow_html=True)
