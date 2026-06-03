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
    font-size: 15px;
    line-height: 1.5;
    letter-spacing: 0.01em;
}

/* 60% dominant — light gray background */
.stApp { background: #f5f6fa; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── SIDEBAR (30% secondary) ── */
[data-testid="stSidebar"] {
    background: #1d3a4f !important;
    border-right: none;
    min-width: 230px !important;
    max-width: 230px !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.4rem !important;
}
[data-testid="stSidebar"] * { color: #b8d0dc !important; }

[data-testid="stSidebar"] label {
    font-size: 0.67rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #6a96ae !important;
    line-height: 2 !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #122535 !important;
    border: 1px solid #2a5570 !important;
    border-radius: 8px !important;
    color: #e8f4f8 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 0.75rem !important;
    letter-spacing: 0.02em !important;
}
[data-testid="stSidebar"] p {
    color: #6a96ae !important;
    font-size: 0.78rem !important;
    line-height: 1.6 !important;
}
[data-testid="stSidebar"] [data-testid="stToggle"] label {
    font-size: 0.84rem !important;
    color: #b8d0dc !important;
    letter-spacing: 0.02em !important;
}

/* ── TOP BANNER ── */
.top-banner {
    background: linear-gradient(135deg, #1d3a4f 0%, #122535 100%);
    padding: 1.6rem 2.8rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #2a4f68;
}
.banner-left { flex: 1; }
.banner-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.banner-sub {
    font-size: 0.75rem;
    color: #6a96ae;
    margin-top: 0.35rem;
    font-weight: 400;
    letter-spacing: 0.03em;
    line-height: 1.5;
}
.banner-stats {
    display: flex;
    gap: 3rem;
    align-items: center;
}
.bstat {}
.bstat-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6a96ae;
    margin-bottom: 0.3rem;
    line-height: 1;
}
.bstat-val {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.03em;
    line-height: 1;
}
.bstat-val.g { color: #4cd964; }
.bstat-val.r { color: #ff6b6b; }
.bstat-val.b { color: #5ac8fa; }

/* ── CONTENT ── */
.content { padding: 2rem 2.8rem 3rem 2.8rem; }

/* ── SECTION LABEL ── */
.sec-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8a9faf;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #e2e6ed;
    line-height: 1;
}

/* ── CARDS ── */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 2px 8px rgba(0,0,0,0.04);
    height: 100%;
}
.card-label {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8a9faf;
    margin-bottom: 0.6rem;
    line-height: 1;
}
.card-val {
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    color: #1a2e3b;
}
.card-val.g { color: #27ae60; }
.card-val.r { color: #e74c3c; }
.card-val.b { color: #0066cc; }
.card-sub {
    font-size: 0.78rem;
    color: #8a9faf;
    margin-top: 0.5rem;
    font-weight: 400;
    letter-spacing: 0.01em;
    line-height: 1.5;
}

/* ── TABLE ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 2px 8px rgba(0,0,0,0.04) !important;
    border: none !important;
}

/* ── DETAIL ROWS ── */
.drow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid #f0f3f6;
    font-size: 0.88rem;
    line-height: 1.4;
    letter-spacing: 0.01em;
}
.drow:last-child { border-bottom: none; }
.dkey { color: #6b7f93; font-weight: 500; }
.dval { font-weight: 600; color: #1a2e3b; }
.dval.g { color: #27ae60; }
.dval.r { color: #e74c3c; }
.dval.b { color: #0066cc; }

/* ── BADGE (10% accent) ── */
.badge-g {
    background: #eafaf2; color: #27ae60;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.03em;
}
.badge-r {
    background: #fdf0ee; color: #e74c3c;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.03em;
}

/* ── BREAKDOWN ── */
.bkdown {
    background: #122535;
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 0.76rem;
    color: #8ab4c8;
    white-space: pre-wrap;
    line-height: 1.9;
    max-height: 520px;
    overflow-y: auto;
    letter-spacing: 0.02em;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: #ffffff;
    border: 1px solid #dde3ec;
    border-radius: 10px;
    font-size: 0.9rem;
    letter-spacing: 0.01em;
    padding: 0.45rem 0.75rem;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    border: 1px solid #e2e6ed !important;
    border-radius: 12px !important;
    background: #fff !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #1a2e3b !important;
    letter-spacing: 0.01em !important;
    padding: 1rem 1.2rem !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def pct(v, sign=False):
    if pd.isna(v): return "—"
    return f"{v:+.2f}%" if sign else f"{v:.2f}%"

def money(v):
    if pd.isna(v): return "—"
    if abs(v) >= 1_000_000: return f"₱{v/1_000_000:.2f}T"
    if abs(v) >= 1_000:     return f"₱{v/1_000:.1f}B"
    return f"₱{v:,.0f}M"

def clr(v):
    if pd.isna(v) or v is None: return ""
    return "g" if v > 0 else "r"


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
        <div style='font-size:1.1rem;font-weight:700;color:#fff;letter-spacing:-0.02em;line-height:1.2;'>
            🇵🇭 PSE Valuation
        </div>
        <div style='font-size:0.75rem;color:#6a96ae;margin-top:0.4rem;
        letter-spacing:0.03em;line-height:1.5;'>Fundamental Screener</div>
    </div>
    """, unsafe_allow_html=True)

    sectors = ["All Sectors"] + sorted(df["sector"].dropna().unique().tolist())
    sel_sector = st.selectbox("Sector", sectors)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    only_vc = st.toggle("Value creators only", value=False)

    fdf = df.copy()
    if sel_sector != "All Sectors":
        fdf = fdf[fdf["sector"] == sel_sector]
    if only_vc:
        fdf = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna() & (fdf["roic_pct"] > fdf["wacc_pct"])]

    valid = fdf[fdf["roic_pct"].notna() & fdf["wacc_pct"].notna()]
    creators = int((valid["roic_pct"] > valid["wacc_pct"]).sum())

    st.markdown(f"""
    <div style='margin-top:2rem;padding-top:1.4rem;border-top:1px solid #2a4f68;'>
        <div style='font-size:0.62rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
        color:#6a96ae;margin-bottom:1.1rem;'>Summary</div>
        <div style='display:flex;justify-content:space-between;align-items:center;
        margin-bottom:0.75rem;'>
            <span style='font-size:0.84rem;color:#6a96ae;letter-spacing:0.01em;'>Showing</span>
            <span style='font-size:0.84rem;font-weight:700;color:#fff;'>{len(fdf)} of {len(df)}</span>
        </div>
        <div style='display:flex;justify-content:space-between;align-items:center;
        margin-bottom:0.75rem;'>
            <span style='font-size:0.84rem;color:#6a96ae;letter-spacing:0.01em;'>With data</span>
            <span style='font-size:0.84rem;font-weight:700;color:#5ac8fa;'>{len(valid)}</span>
        </div>
        <div style='display:flex;justify-content:space-between;align-items:center;'>
            <span style='font-size:0.84rem;color:#6a96ae;letter-spacing:0.01em;'>Value creators</span>
            <span style='font-size:0.84rem;font-weight:700;color:#4cd964;'>{creators}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Banner ────────────────────────────────────────────────────────────────────
avg_roic  = valid["roic_pct"].mean()  if len(valid) else None
avg_wacc  = valid["wacc_pct"].mean()  if len(valid) else None
avg_spread = (avg_roic - avg_wacc)    if avg_roic is not None and avg_wacc is not None else None
sc = clr(avg_spread)

st.markdown(f"""
<div class="top-banner">
    <div class="banner-left">
        <div class="banner-title">PSE Valuation Dashboard</div>
        <div class="banner-sub">
            FCFF · ROIC · WACC &nbsp;·&nbsp; Yahoo Finance & Reuters
            &nbsp;·&nbsp; Rf 7.706% &nbsp;·&nbsp; Tax 25% &nbsp;·&nbsp; ERP 6.69%
        </div>
    </div>
    <div class="banner-stats">
        <div class="bstat">
            <div class="bstat-label">Companies</div>
            <div class="bstat-val">{len(fdf)}</div>
        </div>
        <div class="bstat">
            <div class="bstat-label">Value Creators</div>
            <div class="bstat-val g">{creators}</div>
        </div>
        <div class="bstat">
            <div class="bstat-label">Avg ROIC</div>
            <div class="bstat-val b">{pct(avg_roic)}</div>
        </div>
        <div class="bstat">
            <div class="bstat-label">Avg WACC</div>
            <div class="bstat-val">{pct(avg_wacc)}</div>
        </div>
        <div class="bstat">
            <div class="bstat-label">Avg Spread</div>
            <div class="bstat-val {sc}">{pct(avg_spread, sign=True)}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content">', unsafe_allow_html=True)

# ── All Companies Table ───────────────────────────────────────────────────────
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
}).map(
    lambda v: "color:#27ae60;font-weight:600" if isinstance(v,float) and pd.notna(v) and v > 0
    else ("color:#e74c3c;font-weight:600" if isinstance(v,float) and pd.notna(v) and v < 0 else ""),
    subset=["Spread"]
)

st.dataframe(styled, use_container_width=True, height=370)

# ── Company Deep Dive ─────────────────────────────────────────────────────────
st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
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

st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

# 4 KPI cards
k1, k2, k3, k4 = st.columns(4)
with k1:
    fc = clr(row["fcff_2025_m"] if pd.notna(row["fcff_2025_m"]) else None)
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
        <div class="card-val b">{pct(row['wacc_pct'])}</div>
        <div class="card-sub">Weighted Avg Cost of Capital</div>
    </div>""", unsafe_allow_html=True)

with k4:
    sc2 = clr(sp)
    sp_str = pct(sp, sign=True)
    bdg = f"<span class='badge-{'g' if is_vc else 'r'}'>{'Value Creator ✓' if is_vc else 'Value Destroyer ✗'}</span>"
    st.markdown(f"""<div class="card">
        <div class="card-label">ROIC − WACC Spread</div>
        <div class="card-val {sc2}">{sp_str}</div>
        <div class="card-sub" style="margin-top:0.6rem">{bdg}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    rv = row["roic_pct"] if pd.notna(row["roic_pct"]) else None
    wv = row["wacc_pct"] if pd.notna(row["wacc_pct"]) else None
    ke = row["ke_pct"]   if pd.notna(row["ke_pct"])   else None
    kd = row["kd_aftertax_pct"] if pd.notna(row["kd_aftertax_pct"]) else None
    ew = row["equity_weight_pct"] if pd.notna(row["equity_weight_pct"]) else None
    dw = row["debt_weight_pct"]   if pd.notna(row["debt_weight_pct"])   else None

    st.markdown(f"""<div class="card">
        <div style="font-size:0.95rem;font-weight:700;color:#1a2e3b;
        letter-spacing:-0.01em;margin-bottom:1.2rem;line-height:1;">
            WACC Components
        </div>
        <div class="drow">
            <span class="dkey">Risk-Free Rate (Rf)</span>
            <span class="dval">{pct(row['rf_pct'])}</span>
        </div>
        <div class="drow">
            <span class="dkey">Beta (β)</span>
            <span class="dval">{f"{row['beta']:.3f}" if pd.notna(row['beta']) else '—'}</span>
        </div>
        <div class="drow">
            <span class="dkey">Equity Risk Premium</span>
            <span class="dval">{pct(row['erp_pct'])}</span>
        </div>
        <div class="drow">
            <span class="dkey">Cost of Equity (Ke)</span>
            <span class="dval b">{pct(ke)}</span>
        </div>
        <div class="drow">
            <span class="dkey">Credit Rating</span>
            <span class="dval">{row['rating'] if pd.notna(row['rating']) else '—'}</span>
        </div>
        <div class="drow">
            <span class="dkey">Credit Spread</span>
            <span class="dval">{pct(row['spread_pct'])}</span>
        </div>
        <div class="drow">
            <span class="dkey">Kd after-tax</span>
            <span class="dval r">{pct(kd)}</span>
        </div>
        <div class="drow">
            <span class="dkey">Equity Weight (E/V)</span>
            <span class="dval">{pct(ew)}</span>
        </div>
        <div class="drow">
            <span class="dkey">Debt Weight (D/V)</span>
            <span class="dval">{pct(dw)}</span>
        </div>
        <div class="drow" style="border-top:2px solid #e2e6ed;margin-top:0.5rem;padding-top:1rem;">
            <span style="font-weight:700;color:#1a2e3b;font-size:0.95rem;
            letter-spacing:-0.01em;">WACC</span>
            <span style="font-weight:800;font-size:1.2rem;color:#0066cc;
            letter-spacing:-0.02em;">{pct(wv)}</span>
        </div>
    </div>""", unsafe_allow_html=True)

with right:
    yrs  = [2023, 2024, 2025]
    vals = [row["fcff_2023_m"], row["fcff_2024_m"], row["fcff_2025_m"]]
    bcolors = ["#27ae60" if pd.notna(v) and v > 0 else "#e74c3c" for v in vals]

    fig1 = go.Figure(go.Bar(
        x=yrs, y=vals,
        marker_color=bcolors,
        marker_line_width=0,
        text=[money(v) for v in vals],
        textposition="outside",
        textfont=dict(size=11, color="#1a2e3b", family="Inter"),
        width=0.42,
    ))
    fig1.add_hline(y=0, line_color="#e2e6ed", line_width=1.5)
    fig1.update_layout(
        title=dict(
            text=f"<b>{sel}</b> — 3-Year FCFF",
            font=dict(size=12, color="#1a2e3b", family="Inter"),
            x=0, xanchor="left"
        ),
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter", color="#8a9faf", size=11),
        margin=dict(l=8, r=8, t=48, b=8),
        yaxis=dict(gridcolor="#f5f6fa", zeroline=False, tickformat=",.0f",
                   tickfont=dict(size=10, color="#8a9faf")),
        xaxis=dict(tickvals=yrs, tickfont=dict(size=11, color="#1a2e3b")),
        showlegend=False, height=240,
    )
    st.markdown('<div class="card" style="padding:1.2rem 1.4rem;margin-bottom:1.2rem;">',
                unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    rv2 = rv if rv is not None else 0
    wv2 = wv if wv is not None else 0
    fig2 = go.Figure(go.Bar(
        x=["ROIC", "WACC"],
        y=[rv2, wv2],
        marker_color=["#27ae60" if rv2 >= wv2 else "#e74c3c", "#0066cc"],
        marker_line_width=0,
        text=[pct(rv2), pct(wv2)],
        textposition="outside",
        textfont=dict(size=12, color="#1a2e3b", family="Inter"),
        width=0.32,
    ))
    fig2.update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        font=dict(family="Inter", color="#8a9faf", size=11),
        margin=dict(l=8, r=8, t=12, b=8),
        yaxis=dict(gridcolor="#f5f6fa", ticksuffix="%", zeroline=False,
                   tickfont=dict(size=10, color="#8a9faf")),
        xaxis=dict(tickfont=dict(size=12, color="#1a2e3b", family="Inter")),
        showlegend=False, height=200,
    )
    st.markdown('<div class="card" style="padding:1.2rem 1.4rem;">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ── Breakdown ─────────────────────────────────────────────────────────────────
st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
with st.expander("📋  View Full Computation Breakdown"):
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

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background:#1d3a4f;padding:1.2rem 2.8rem;margin-top:3rem;
text-align:center;font-size:0.73rem;color:#6a96ae;font-weight:400;
letter-spacing:0.03em;line-height:1.6;'>
    PSE Valuation Dashboard &nbsp;·&nbsp;
    FCFF = NOPAT + D&amp;A − ΔNWC − CapEx &nbsp;·&nbsp;
    ROIC = NOPAT / Avg IC &nbsp;·&nbsp;
    WACC = (E/V)Ke + (D/V)Kd(1−t)
</div>
""", unsafe_allow_html=True)
