import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re

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
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 14px;
    -webkit-font-smoothing: antialiased;
}

/* ── Background ── */
.stApp { background: #f0f2f5; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a3a4a !important;
    border-right: none;
    min-width: 220px !important;
    max-width: 220px !important;
}
[data-testid="stSidebar"] * { color: #cde0e8 !important; }
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem !important; }
[data-testid="stSidebar"] label {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #7aa8bc !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #0f2535 !important;
    border: 1px solid #2a5570 !important;
    border-radius: 8px !important;
    color: #e0f0f8 !important;
    font-size: 0.85rem !important;
}
[data-testid="stSidebar"] p {
    color: #7aa8bc !important;
    font-size: 0.78rem !important;
}

/* ── Top banner ── */
.top-banner {
    background: linear-gradient(135deg, #1a3a4a 0%, #0f2535 100%);
    padding: 1.4rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #2a5570;
}
.banner-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.01em;
}
.banner-sub {
    font-size: 0.75rem;
    color: #7aa8bc;
    margin-top: 0.2rem;
    font-weight: 400;
}
.banner-stats {
    display: flex;
    gap: 2.5rem;
    align-items: center;
}
.banner-stat-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7aa8bc;
    margin-bottom: 0.2rem;
}
.banner-stat-val {
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
}
.banner-stat-val.green { color: #4cd964; }
.banner-stat-val.red   { color: #ff6b6b; }
.banner-stat-val.blue  { color: #5ac8fa; }

/* ── Content wrapper ── */
.content-wrap { padding: 1.8rem 2.5rem; }

/* ── Section label ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8a9bb0;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #dde3ec;
}

/* ── Cards ── */
.card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.card-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8a9bb0;
    margin-bottom: 0.5rem;
}
.card-val {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1a2e3b;
    letter-spacing: -0.02em;
    line-height: 1;
}
.card-val.green { color: #28a745; }
.card-val.red   { color: #dc3545; }
.card-val.blue  { color: #0075c9; }
.card-sub {
    font-size: 0.75rem;
    color: #8a9bb0;
    margin-top: 0.35rem;
    font-weight: 400;
}

/* ── Table ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07) !important;
    border: none !important;
}

/* ── Detail rows ── */
.drow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #f0f2f5;
    font-size: 0.85rem;
}
.drow:last-child { border-bottom: none; }
.dkey { color: #6b7f93; font-weight: 500; }
.dval { font-weight: 600; color: #1a2e3b; }
.dval.green { color: #28a745; }
.dval.red   { color: #dc3545; }
.dval.blue  { color: #0075c9; }

/* ── Badge ── */
.badge-g { background:#eafaf0; color:#28a745; border-radius:20px; padding:2px 10px; font-size:0.72rem; font-weight:600; }
.badge-r { background:#fdf0f0; color:#dc3545; border-radius:20px; padding:2px 10px; font-size:0.72rem; font-weight:600; }

/* ── Breakdown box ── */
.bkdown {
    background: #1a2e3b;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 0.74rem;
    color: #9bb8c9;
    white-space: pre-wrap;
    line-height: 1.8;
    max-height: 500px;
    overflow-y: auto;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #fff;
    border: 1px solid #dde3ec;
    border-radius: 10px;
    font-size: 0.88rem;
}

/* ── Toggle ── */
[data-testid="stToggle"] label { color: #cde0e8 !important; font-size:0.82rem !important; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def pct(v, sign=False):
    if pd.isna(v): return "—"
    s = f"{v:+.2f}%" if sign else f"{v:.2f}%"
    return s

def money(v):
    if pd.isna(v): return "—"
    if abs(v) >= 1_000_000: return f"₱{v/1_000_000:.2f}T"
    if abs(v) >= 1_000:     return f"₱{v/1_000:.1f}B"
    return f"₱{v:,.0f}M"

def clr(v, reverse=False):
    if pd.isna(v): return ""
    if reverse: return "red" if v > 0 else "green"
    return "green" if v > 0 else "red"


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("data/pse_valuation.csv")
    return df

@st.cache_data
def load_txt():
    with open("data/pse_valuation_breakdown.txt") as f:
        return f.read()

df = load()
txt = load_txt()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:2rem;padding-bottom:1.2rem;border-bottom:1px solid #2a5570;'>
        <div style='font-size:1.15rem;font-weight:700;color:#fff;letter-spacing:-0.01em;'>
            🇵🇭 PSE Valuation
        </div>
        <div style='font-size:0.72rem;color:#7aa8bc;margin-top:0.25rem;'>Fundamental Screener</div>
    </div>
    """, unsafe_allow_html=True)

    sectors = ["All Sectors"] + sorted(df["sector"].dropna().unique().tolist())
    sel_sector = st.selectbox("Sector", sectors)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    only_creators = st.toggle("Value creators only", value=False)

    # Apply filters
    fdf = df.copy()
    if sel_sector != "All Sectors":
        fdf = fdf[fdf["sector"] == sel_sector]
    if only_creators:
        fdf = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna() & (fdf["roic_pct"] > fdf["wacc_pct"])]

    valid = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna()]
    creators = (valid["roic_pct"] > valid["wacc_pct"]).sum()

    st.markdown(f"""
    <div style='margin-top:1.5rem;padding-top:1.2rem;border-top:1px solid #2a5570;'>
        <div style='font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
        color:#7aa8bc;margin-bottom:1rem;'>Summary</div>
        <div style='display:flex;justify-content:space-between;margin-bottom:0.6rem;'>
            <span style='font-size:0.82rem;color:#7aa8bc;'>Showing</span>
            <span style='font-size:0.82rem;font-weight:700;color:#fff;'>{len(fdf)} of {len(df)}</span>
        </div>
        <div style='display:flex;justify-content:space-between;margin-bottom:0.6rem;'>
            <span style='font-size:0.82rem;color:#7aa8bc;'>With data</span>
            <span style='font-size:0.82rem;font-weight:700;color:#5ac8fa;'>{len(valid)}</span>
        </div>
        <div style='display:flex;justify-content:space-between;'>
            <span style='font-size:0.82rem;color:#7aa8bc;'>Value creators</span>
            <span style='font-size:0.82rem;font-weight:700;color:#4cd964;'>{creators}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Banner ────────────────────────────────────────────────────────────────────
avg_roic = valid["roic_pct"].mean() if len(valid) else None
avg_wacc = valid["wacc_pct"].mean() if len(valid) else None
avg_spread = (avg_roic - avg_wacc) if avg_roic and avg_wacc else None
spread_c = "green" if avg_spread and avg_spread > 0 else "red"

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
        <div>
            <div class="banner-stat-label">Companies</div>
            <div class="banner-stat-val">{len(fdf)}</div>
        </div>
        <div>
            <div class="banner-stat-label">Value Creators</div>
            <div class="banner-stat-val green">{creators}</div>
        </div>
        <div>
            <div class="banner-stat-label">Avg ROIC</div>
            <div class="banner-stat-val blue">{pct(avg_roic)}</div>
        </div>
        <div>
            <div class="banner-stat-label">Avg WACC</div>
            <div class="banner-stat-val">{pct(avg_wacc)}</div>
        </div>
        <div>
            <div class="banner-stat-label">Avg Spread</div>
            <div class="banner-stat-val {spread_c}">{pct(avg_spread, sign=True)}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">All Companies</div>', unsafe_allow_html=True)

tbl = fdf[["symbol","company","sector","fcff_2025_m","fcff_2024_m","fcff_2023_m",
           "roic_pct","wacc_pct","rating","market_cap_b"]].copy()
tbl["Spread"] = tbl["roic_pct"] - tbl["wacc_pct"]
tbl = tbl.rename(columns={
    "symbol":"Ticker","company":"Company","sector":"Sector",
    "fcff_2025_m":"FCFF 2025 (₱M)","fcff_2024_m":"FCFF 2024 (₱M)","fcff_2023_m":"FCFF 2023 (₱M)",
    "roic_pct":"ROIC (%)","wacc_pct":"WACC (%)","rating":"Rating","market_cap_b":"Mkt Cap (₱B)",
})

styled = tbl.style.format({
    "FCFF 2025 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
    "FCFF 2024 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
    "FCFF 2023 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
    "ROIC (%)":        lambda v: f"{v:.2f}%" if pd.notna(v) else "—",
    "WACC (%)":        lambda v: f"{v:.2f}%" if pd.notna(v) else "—",
    "Spread":          lambda v: f"{v:+.2f}%" if pd.notna(v) else "—",
    "Mkt Cap (₱B)":   lambda v: f"{v:,.3f}" if pd.notna(v) else "—",
}).map(lambda v: "color:#28a745;font-weight:600" if isinstance(v,float) and pd.notna(v) and v>0
       else ("color:#dc3545;font-weight:600" if isinstance(v,float) and pd.notna(v) and v<0 else ""),
       subset=["Spread"])

st.dataframe(styled, use_container_width=True, height=360)

# ── Deep Dive ─────────────────────────────────────────────────────────────────
st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">Company Deep Dive</div>', unsafe_allow_html=True)

tickers = fdf["symbol"].tolist()
sel = st.selectbox(
    "Select company",
    tickers,
    format_func=lambda t: f"{t}  —  {df[df['symbol']==t]['company'].values[0]}"
)

row = fdf[fdf["symbol"] == sel].iloc[0]
sp = (row["roic_pct"] - row["wacc_pct"]) if pd.notna(row["roic_pct"]) and pd.notna(row["wacc_pct"]) else None
is_vc = sp is not None and sp > 0

# 4 KPI cards
k1, k2, k3, k4 = st.columns(4)
with k1:
    fc = "green" if pd.notna(row["fcff_2025_m"]) and row["fcff_2025_m"] > 0 else "red"
    st.markdown(f"""<div class="card">
        <div class="card-label">FCFF 2025</div>
        <div class="card-val {fc}">{money(row['fcff_2025_m'])}</div>
        <div class="card-sub">{row['sector']}</div>
    </div>""", unsafe_allow_html=True)

with k2:
    rc = clr(sp)
    st.markdown(f"""<div class="card">
        <div class="card-label">ROIC</div>
        <div class="card-val {rc}">{pct(row['roic_pct'])}</div>
        <div class="card-sub">Return on Invested Capital</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="card">
        <div class="card-label">WACC</div>
        <div class="card-val blue">{pct(row['wacc_pct'])}</div>
        <div class="card-sub">Weighted Avg Cost of Capital</div>
    </div>""", unsafe_allow_html=True)

with k4:
    sc = clr(sp)
    sp_str = pct(sp, sign=True)
    bdg = f"<span class='badge-{'g' if is_vc else 'r'}'>{'Value Creator ✓' if is_vc else 'Value Destroyer ✗'}</span>"
    st.markdown(f"""<div class="card">
        <div class="card-label">ROIC − WACC Spread</div>
        <div class="card-val {sc}">{sp_str}</div>
        <div class="card-sub" style="margin-top:0.5rem">{bdg}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    st.markdown(f"""<div class="card">
        <div style="font-size:0.95rem;font-weight:700;color:#1a2e3b;margin-bottom:1rem;">WACC Components</div>
        <div class="drow"><span class="dkey">Risk-Free Rate (Rf)</span><span class="dval">{pct(row['rf_pct'])}</span></div>
        <div class="drow"><span class="dkey">Beta (β)</span><span class="dval">{f"{row['beta']:.3f}" if pd.notna(row['beta']) else '—'}</span></div>
        <div class="drow"><span class="dkey">Equity Risk Premium</span><span class="dval">{pct(row['erp_pct'])}</span></div>
        <div class="drow"><span class="dkey">Cost of Equity (Ke)</span><span class="dval blue">{pct(row['ke_pct'])}</span></div>
        <div class="drow"><span class="dkey">Credit Rating</span><span class="dval">{row['rating'] if pd.notna(row['rating']) else '—'}</span></div>
        <div class="drow"><span class="dkey">Spread</span><span class="dval">{pct(row['spread_pct'])}</span></div>
        <div class="drow"><span class="dkey">Kd after-tax</span><span class="dval red">{pct(row['kd_aftertax_pct'])}</span></div>
        <div class="drow"><span class="dkey">Equity Weight (E/V)</span><span class="dval">{pct(row['equity_weight_pct'])}</span></div>
        <div class="drow"><span class="dkey">Debt Weight (D/V)</span><span class="dval">{pct(row['debt_weight_pct'])}</span></div>
        <div class="drow" style="border-top:2px solid #dde3ec;margin-top:0.3rem;padding-top:0.8rem;">
            <span style="font-weight:700;color:#1a2e3b;font-size:0.95rem;">WACC</span>
            <span style="font-weight:800;font-size:1.15rem;color:#0075c9;">{pct(row['wacc_pct'])}</span>
        </div>
    </div>""", unsafe_allow_html=True)

with right:
    # FCFF bar chart
    yrs = [2023, 2024, 2025]
    vals = [row["fcff_2023_m"], row["fcff_2024_m"], row["fcff_2025_m"]]
    bcolors = ["#28a745" if v > 0 else "#dc3545" for v in vals]

    fig1 = go.Figure(go.Bar(
        x=yrs, y=vals,
        marker_color=bcolors, marker_line_width=0,
        text=[money(v) for v in vals],
        textposition="outside",
        textfont=dict(size=11, color="#1a2e3b", family="Inter"),
        width=0.4,
    ))
    fig1.add_hline(y=0, line_color="#dde3ec", line_width=1)
    fig1.update_layout(
        title=dict(text=f"<b>{sel}</b> — 3-Year FCFF",
                   font=dict(size=12, color="#1a2e3b", family="Inter"), x=0, xanchor="left"),
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter", color="#8a9bb0", size=11),
        margin=dict(l=8, r=8, t=45, b=8),
        yaxis=dict(gridcolor="#f0f2f5", zeroline=False, tickformat=",.0f",
                   tickfont=dict(size=10)),
        xaxis=dict(tickvals=yrs, tickfont=dict(size=11, color="#1a2e3b")),
        showlegend=False, height=230,
    )
    st.markdown('<div class="card" style="padding:1rem 1.2rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)

    # ROIC vs WACC
    rv = row["roic_pct"] if pd.notna(row["roic_pct"]) else 0
    wv = row["wacc_pct"] if pd.notna(row["wacc_pct"]) else 0
    fig2 = go.Figure(go.Bar(
        x=["ROIC", "WACC"], y=[rv, wv],
        marker_color=["#28a745" if rv >= wv else "#dc3545", "#0075c9"],
        marker_line_width=0,
        text=[pct(rv), pct(wv)],
        textposition="outside",
        textfont=dict(size=12, color="#1a2e3b", family="Inter"),
        width=0.3,
    ))
    fig2.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter", color="#8a9bb0", size=11),
        margin=dict(l=8, r=8, t=8, b=8),
        yaxis=dict(gridcolor="#f0f2f5", ticksuffix="%", zeroline=False,
                   tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=12, color="#1a2e3b")),
        showlegend=False, height=190,
    )
    st.markdown('<div class="card" style="padding:1rem 1.2rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ── Breakdown ─────────────────────────────────────────────────────────────────
st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
with st.expander("📋 View Full Computation Breakdown"):
    sections = txt.split("=" * 70)
    found = ""
    for s in sections:
        if f"  {sel} —" in s:
            found = ("=" * 70 + s).strip()
            break
    if found:
        st.markdown(f'<div class="bkdown">{found}</div>', unsafe_allow_html=True)
    else:
        st.info("Breakdown not available for this company.")

st.markdown('</div>', unsafe_allow_html=True)  # close content-wrap

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#1a3a4a;padding:1rem 2.5rem;margin-top:2rem;
text-align:center;font-size:0.72rem;color:#7aa8bc;font-weight:400;'>
    PSE Valuation Dashboard &nbsp;·&nbsp;
    FCFF = NOPAT + D&A − ΔNWC − CapEx &nbsp;·&nbsp;
    ROIC = NOPAT / Avg IC &nbsp;·&nbsp;
    WACC = (E/V)Ke + (D/V)Kd(1−t) &nbsp;·&nbsp;
    Data: Yahoo Finance & Reuters
</div>
""", unsafe_allow_html=True)
