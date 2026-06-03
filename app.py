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
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: #f2f2f7;
    color: #1c1c1e;
}

.block-container {
    padding: 2rem 2.5rem 4rem 2.5rem;
    max-width: 1400px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e5ea;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem;
}
[data-testid="stSidebar"] label {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #8e8e93 !important;
}

/* Cards */
.card {
    background: #ffffff;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
}

.kpi-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #8e8e93;
    margin-bottom: 0.5rem;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    color: #1c1c1e;
}

.kpi-sub {
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 0.4rem;
    color: #8e8e93;
}

.green { color: #34c759; }
.red   { color: #ff3b30; }
.blue  { color: #007aff; }
.gray  { color: #8e8e93; }

.badge-green {
    display: inline-block;
    background: #e8fdf0;
    color: #34c759;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-red {
    display: inline-block;
    background: #fff0ef;
    color: #ff3b30;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 600;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #1c1c1e;
    margin: 2rem 0 1rem 0;
}

.table-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #8e8e93;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f2f2f7;
    margin-bottom: 0.3rem;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid #f2f2f7;
    font-size: 0.88rem;
}
.detail-row:last-child { border-bottom: none; }
.detail-key { color: #8e8e93; font-weight: 500; }
.detail-val { font-weight: 600; color: #1c1c1e; }

.breakdown-box {
    background: #1c1c1e;
    border-radius: 14px;
    padding: 1.5rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 0.76rem;
    color: #a0a0a8;
    white-space: pre-wrap;
    line-height: 1.8;
    max-height: 520px;
    overflow-y: auto;
}

/* Override streamlit defaults */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: none !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

div[data-testid="metric-container"] { display: none; }

.stSelectbox > div > div {
    background: #f2f2f7;
    border: none;
    border-radius: 12px;
    color: #1c1c1e;
}

hr { border-color: #e5e5ea !important; }

/* Hide streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_pct(v):
    if pd.isna(v): return "—"
    return f"{v:.2f}%"

def fmt_m(v):
    if pd.isna(v): return "—"
    if abs(v) >= 1000:
        return f"₱{v/1000:,.1f}B"
    return f"₱{v:,.0f}M"

def fmt_b(v):
    if pd.isna(v): return "—"
    return f"₱{v:,.2f}B"

def color_class(v, reverse=False):
    if pd.isna(v): return "gray"
    if reverse:
        return "red" if v > 0 else "green"
    return "green" if v > 0 else "red"


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/pse_valuation.csv")
    return df

@st.cache_data
def load_breakdown():
    with open("data/pse_valuation_breakdown.txt", "r") as f:
        return f.read()

df = load_data()
breakdown_text = load_breakdown()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:2rem;'>
        <div style='font-size:1.3rem;font-weight:800;letter-spacing:-0.02em;color:#1c1c1e;'>
            🇵🇭 PSE Valuation
        </div>
        <div style='font-size:0.75rem;color:#8e8e93;margin-top:0.2rem;font-weight:500;'>
            Fundamental Screener
        </div>
    </div>
    """, unsafe_allow_html=True)

    sectors = ["All Sectors"] + sorted(df["sector"].dropna().unique().tolist())
    selected_sector = st.selectbox("Sector", sectors)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    show_value_creators = st.toggle("Value creators only (ROIC > WACC)", value=False)

    # Apply filters
    filtered = df.copy()
    if selected_sector != "All Sectors":
        filtered = filtered[filtered["sector"] == selected_sector]
    if show_value_creators:
        filtered = filtered[
            filtered["roic_pct"].notna() &
            filtered["wacc_pct"].notna() &
            (filtered["roic_pct"] > filtered["wacc_pct"])
        ]

    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    total = len(df)
    shown = len(filtered)
    has_data = filtered["roic_pct"].notna().sum()

    st.markdown(f"""
    <div style='background:#f2f2f7;border-radius:14px;padding:1rem;'>
        <div style='font-size:0.7rem;font-weight:600;text-transform:uppercase;
        letter-spacing:0.06em;color:#8e8e93;margin-bottom:0.8rem;'>Summary</div>
        <div style='display:flex;justify-content:space-between;margin-bottom:0.5rem;'>
            <span style='font-size:0.85rem;color:#8e8e93;'>Showing</span>
            <span style='font-size:0.85rem;font-weight:700;color:#1c1c1e;'>{shown} of {total}</span>
        </div>
        <div style='display:flex;justify-content:space-between;'>
            <span style='font-size:0.85rem;color:#8e8e93;'>With full data</span>
            <span style='font-size:0.85rem;font-weight:700;color:#007aff;'>{has_data}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:1.5rem;'>
    <div style='font-size:2rem;font-weight:800;letter-spacing:-0.03em;color:#1c1c1e;'>
        PSE Valuation Dashboard
    </div>
    <div style='font-size:0.88rem;color:#8e8e93;margin-top:0.3rem;font-weight:500;'>
        FCFF · ROIC · WACC &nbsp;·&nbsp; Yahoo Finance & Reuters &nbsp;·&nbsp;
        Rf 7.706% &nbsp;·&nbsp; Tax 25% &nbsp;·&nbsp; ERP 6.69%
    </div>
</div>
""", unsafe_allow_html=True)


# ── Summary KPIs ──────────────────────────────────────────────────────────────
valid = filtered[filtered["roic_pct"].notna() & filtered["wacc_pct"].notna()]
value_creators = (valid["roic_pct"] > valid["wacc_pct"]).sum()
avg_roic = valid["roic_pct"].mean()
avg_wacc = valid["wacc_pct"].mean()
avg_spread = avg_roic - avg_wacc if not pd.isna(avg_roic) else None

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Companies</div>
        <div class='kpi-value'>{shown}</div>
        <div class='kpi-sub'>{selected_sector}</div>
    </div>""", unsafe_allow_html=True)

with k2:
    vc_pct = f"{value_creators/len(valid)*100:.0f}%" if len(valid) > 0 else "—"
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Value Creators</div>
        <div class='kpi-value green'>{value_creators}</div>
        <div class='kpi-sub'>{vc_pct} of companies with data</div>
    </div>""", unsafe_allow_html=True)

with k3:
    roic_color = color_class(avg_spread)
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Avg ROIC</div>
        <div class='kpi-value {roic_color}'>{fmt_pct(avg_roic)}</div>
        <div class='kpi-sub'>vs WACC {fmt_pct(avg_wacc)}</div>
    </div>""", unsafe_allow_html=True)

with k4:
    spread_color = color_class(avg_spread)
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Avg ROIC − WACC</div>
        <div class='kpi-value {spread_color}'>{(f"+{avg_spread:.2f}%" if avg_spread and avg_spread > 0 else fmt_pct(avg_spread))}</div>
        <div class='kpi-sub'>Economic value spread</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

# ── Company Table ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>All Companies</div>", unsafe_allow_html=True)

table_df = filtered[[
    "symbol", "company", "sector",
    "fcff_2025_m", "fcff_2024_m", "fcff_2023_m",
    "roic_pct", "wacc_pct", "rating", "market_cap_b"
]].copy()

table_df["Spread"] = table_df["roic_pct"] - table_df["wacc_pct"]

table_df = table_df.rename(columns={
    "symbol": "Ticker",
    "company": "Company",
    "sector": "Sector",
    "fcff_2025_m": "FCFF 2025 (₱M)",
    "fcff_2024_m": "FCFF 2024 (₱M)",
    "fcff_2023_m": "FCFF 2023 (₱M)",
    "roic_pct": "ROIC",
    "wacc_pct": "WACC",
    "rating": "Rating",
    "market_cap_b": "Mkt Cap (₱B)",
})

def style_table(df):
    return df.style.format({
        "FCFF 2025 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
        "FCFF 2024 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
        "FCFF 2023 (₱M)": lambda v: f"{v:,.1f}" if pd.notna(v) else "—",
        "ROIC": lambda v: f"{v:.2f}%" if pd.notna(v) else "—",
        "WACC": lambda v: f"{v:.2f}%" if pd.notna(v) else "—",
        "Spread": lambda v: f"{v:+.2f}%" if pd.notna(v) else "—",
        "Mkt Cap (₱B)": lambda v: f"{v:,.3f}" if pd.notna(v) else "—",
    }).map(
        lambda v: "color: #34c759; font-weight:600" if isinstance(v, float) and not pd.isna(v) and v > 0
        else ("color: #ff3b30; font-weight:600" if isinstance(v, float) and not pd.isna(v) and v < 0 else ""),
        subset=["Spread"]
    )

st.dataframe(style_table(table_df), use_container_width=True, height=380)

# ── Company Deep Dive ─────────────────────────────────────────────────────────
st.markdown("<div class='section-title'>Company Deep Dive</div>", unsafe_allow_html=True)

ticker_list = filtered["symbol"].tolist()
selected_ticker = st.selectbox(
    "Select a company",
    ticker_list,
    format_func=lambda t: f"{t}  —  {df[df['symbol']==t]['company'].values[0]}"
)

row = filtered[filtered["symbol"] == selected_ticker].iloc[0]
spread_val = (row["roic_pct"] - row["wacc_pct"]) if pd.notna(row["roic_pct"]) and pd.notna(row["wacc_pct"]) else None
is_creator = spread_val is not None and spread_val > 0

# KPI row
c1, c2, c3, c4 = st.columns(4)

with c1:
    fcff_color = "green" if pd.notna(row["fcff_2025_m"]) and row["fcff_2025_m"] > 0 else "red"
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>FCFF 2025</div>
        <div class='kpi-value {fcff_color}'>{fmt_m(row["fcff_2025_m"])}</div>
        <div class='kpi-sub'>{row["sector"]}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    roic_c = color_class(spread_val)
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>ROIC</div>
        <div class='kpi-value {roic_c}'>{fmt_pct(row["roic_pct"])}</div>
        <div class='kpi-sub'>Return on Invested Capital</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>WACC</div>
        <div class='kpi-value blue'>{fmt_pct(row["wacc_pct"])}</div>
        <div class='kpi-sub'>Cost of Capital</div>
    </div>""", unsafe_allow_html=True)

with c4:
    sp_color = color_class(spread_val)
    badge = f"<span class='badge-{'green' if is_creator else 'red'}'>{'Value Creator ✓' if is_creator else 'Value Destroyer ✗'}</span>"
    sp_str = f"{spread_val:+.2f}%" if spread_val is not None else "—"
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>ROIC − WACC</div>
        <div class='kpi-value {sp_color}'>{sp_str}</div>
        <div class='kpi-sub' style='margin-top:0.5rem;'>{badge}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    # WACC breakdown table
    st.markdown(f"""
    <div class='card'>
        <div style='font-size:1rem;font-weight:700;color:#1c1c1e;margin-bottom:1rem;letter-spacing:-0.01em;'>
            WACC Components
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Risk-Free Rate (Rf)</span>
            <span class='detail-val'>{fmt_pct(row["rf_pct"])}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Beta (β)</span>
            <span class='detail-val'>{f"{row['beta']:.3f}" if pd.notna(row["beta"]) else "—"}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Equity Risk Premium</span>
            <span class='detail-val'>{fmt_pct(row["erp_pct"])}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Cost of Equity (Ke)</span>
            <span class='detail-val' style='color:#007aff;'>{fmt_pct(row["ke_pct"])}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Credit Rating</span>
            <span class='detail-val'>{row["rating"] if pd.notna(row["rating"]) else "—"}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Spread</span>
            <span class='detail-val'>{fmt_pct(row["spread_pct"])}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Kd after-tax</span>
            <span class='detail-val'>{fmt_pct(row["kd_aftertax_pct"])}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Equity Weight (E/V)</span>
            <span class='detail-val'>{fmt_pct(row["equity_weight_pct"])}</span>
        </div>
        <div class='detail-row'>
            <span class='detail-key'>Debt Weight (D/V)</span>
            <span class='detail-val'>{fmt_pct(row["debt_weight_pct"])}</span>
        </div>
        <div class='detail-row' style='border-top:2px solid #e5e5ea;margin-top:0.3rem;padding-top:0.8rem;'>
            <span style='font-weight:700;color:#1c1c1e;'>WACC</span>
            <span style='font-weight:800;font-size:1.1rem;color:#007aff;'>{fmt_pct(row["wacc_pct"])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    # 3-year FCFF chart
    years = [2023, 2024, 2025]
    fcff_vals = [row["fcff_2023_m"], row["fcff_2024_m"], row["fcff_2025_m"]]
    bar_colors = ["#34c759" if v > 0 else "#ff3b30" for v in fcff_vals]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=fcff_vals,
        marker_color=bar_colors,
        marker_line_width=0,
        text=[fmt_m(v) for v in fcff_vals],
        textposition="outside",
        textfont=dict(size=11, color="#1c1c1e", family="Manrope"),
        width=0.45,
    ))
    fig.add_hline(y=0, line_color="#e5e5ea", line_width=1)
    fig.update_layout(
        title=dict(text=f"{selected_ticker} — 3-Year FCFF",
                   font=dict(size=13, color="#1c1c1e", family="Manrope"), x=0),
        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
        font=dict(family="Manrope", color="#8e8e93", size=11),
        margin=dict(l=10, r=10, t=50, b=10),
        yaxis=dict(gridcolor="#f2f2f7", tickformat=",.0f", zeroline=False,
                   showgrid=True, tickfont=dict(size=10)),
        xaxis=dict(tickvals=years, tickfont=dict(size=11, color="#1c1c1e")),
        showlegend=False, height=220,
    )
    st.markdown("<div class='card' style='padding:1rem;'>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ROIC vs WACC
    fig2 = go.Figure()
    roic_v = row["roic_pct"] if pd.notna(row["roic_pct"]) else 0
    wacc_v = row["wacc_pct"] if pd.notna(row["wacc_pct"]) else 0
    fig2.add_trace(go.Bar(
        x=["ROIC", "WACC"],
        y=[roic_v, wacc_v],
        marker_color=["#34c759" if roic_v > wacc_v else "#ff3b30", "#007aff"],
        marker_line_width=0,
        text=[fmt_pct(roic_v), fmt_pct(wacc_v)],
        textposition="outside",
        textfont=dict(size=12, color="#1c1c1e", family="Manrope"),
        width=0.35,
    ))
    fig2.update_layout(
        paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
        font=dict(family="Manrope", color="#8e8e93", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(gridcolor="#f2f2f7", ticksuffix="%", zeroline=False,
                   tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=12, color="#1c1c1e", family="Manrope")),
        showlegend=False, height=180,
    )
    st.markdown("<div class='card' style='padding:1rem;margin-top:-0.5rem;'>", unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ── Computation Breakdown ─────────────────────────────────────────────────────
with st.expander("View Full Computation Breakdown", expanded=False):
    sections = breakdown_text.split("=" * 70)
    company_section = ""
    for section in sections:
        if f"  {selected_ticker} —" in section:
            company_section = ("=" * 70 + section).strip()
            break

    if company_section:
        st.markdown(f"<div class='breakdown-box'>{company_section}</div>",
                    unsafe_allow_html=True)
    else:
        st.info("Breakdown not available for this company.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;font-size:0.75rem;color:#8e8e93;font-weight:500;'>
    PSE Valuation Dashboard &nbsp;·&nbsp;
    FCFF = NOPAT + D&A − ΔNWC − CapEx &nbsp;·&nbsp;
    ROIC = NOPAT / Avg IC &nbsp;·&nbsp;
    WACC = (E/V)Ke + (D/V)Kd(1−t)
</div>
""", unsafe_allow_html=True)
