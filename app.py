import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PSE Valuation Dashboard",
    page_icon="🇵🇭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

h1, h2, h3, .big-title {
    font-family: 'Syne', sans-serif !important;
}

/* Dark background */
.stApp {
    background-color: #0a0e1a;
    color: #e2e8f0;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0d1220;
    border-right: 1px solid #1e2d4a;
}

[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #111827 0%, #1a2540 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    font-family: 'DM Mono', monospace;
    margin-bottom: 0.3rem;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    line-height: 1;
}

.metric-positive { color: #34d399; }
.metric-negative { color: #f87171; }
.metric-neutral  { color: #60a5fa; }

/* Value spread badge */
.spread-positive {
    display: inline-block;
    background: #052e16;
    color: #34d399;
    border: 1px solid #166534;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    margin-top: 0.4rem;
}
.spread-negative {
    display: inline-block;
    background: #2d0f0f;
    color: #f87171;
    border: 1px solid #7f1d1d;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    margin-top: 0.4rem;
}

/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #475569;
    border-bottom: 1px solid #1e2d4a;
    padding-bottom: 0.5rem;
    margin: 2rem 0 1rem 0;
}

/* Company selector */
.company-pill {
    display: inline-block;
    background: #1e3a5f;
    color: #93c5fd;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    margin: 2px;
}

/* Rating badge */
.rating-badge {
    display: inline-block;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    color: #fbbf24;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    overflow: hidden;
}

/* Divider */
hr {
    border-color: #1e2d4a !important;
    margin: 2rem 0;
}

/* Selectbox & sidebar widgets */
[data-testid="stSelectbox"] > div > div {
    background-color: #111827;
    border: 1px solid #1e3a5f;
    color: #e2e8f0;
}

.breakdown-box {
    background: #0d1220;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #94a3b8;
    white-space: pre-wrap;
    line-height: 1.7;
    max-height: 500px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# ── Data loading ──────────────────────────────────────────────────────────────
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

# ── Header ────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 5])
with col_title:
    st.markdown("""
    <div style='margin-bottom:0.2rem'>
        <span style='font-family:Syne,sans-serif;font-size:2.2rem;font-weight:800;
        color:#e2e8f0;letter-spacing:-0.02em;'>PSE Valuation Dashboard</span>
        <span style='font-family:DM Mono,monospace;font-size:0.8rem;color:#475569;
        margin-left:1rem;vertical-align:middle;'>🇵🇭 Philippine Stock Exchange</span>
    </div>
    <div style='font-family:DM Mono,monospace;font-size:0.75rem;color:#475569;margin-bottom:1rem;'>
        FCFF · ROIC · WACC &nbsp;|&nbsp; Sources: Yahoo Finance & Reuters &nbsp;|&nbsp;
        Rf: 7.706% &nbsp;·&nbsp; Tax: 25% &nbsp;·&nbsp; ERP: 6.69%
    </div>
    """, unsafe_allow_html=True)

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;"
                "color:#e2e8f0;margin-bottom:1.5rem;'>FILTERS</div>", unsafe_allow_html=True)

    sectors = ["All Sectors"] + sorted(df["sector"].dropna().unique().tolist())
    selected_sector = st.selectbox("Sector", sectors)

    # Filter df for subsector (if you add subsector later, plug it in here)
    if selected_sector != "All Sectors":
        filtered_df = df[df["sector"] == selected_sector].copy()
    else:
        filtered_df = df.copy()

    st.markdown("---")

    # ROIC vs WACC toggle
    show_value_creators = st.checkbox("Only show ROIC > WACC", value=False,
                                      help="Value creators: companies where ROIC exceeds WACC")
    if show_value_creators:
        filtered_df = filtered_df[filtered_df["roic_pct"] > filtered_df["wacc_pct"]]

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.7rem;color:#475569;font-family:DM Mono,monospace;'>"
                f"Showing <b style='color:#60a5fa'>{len(filtered_df)}</b> of "
                f"<b style='color:#60a5fa'>{len(df)}</b> companies</div>", unsafe_allow_html=True)

# ── OVERVIEW TABLE ────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>ALL COMPANIES</div>", unsafe_allow_html=True)

display_df = filtered_df[[
    "symbol", "company", "sector", "source",
    "fcff_2025_m", "fcff_2024_m", "fcff_2023_m",
    "roic_pct", "wacc_pct", "rating", "beta", "market_cap_b"
]].copy()

display_df["ROIC>WACC"] = display_df["roic_pct"] > display_df["wacc_pct"]
display_df["Spread (ROIC-WACC)"] = display_df["roic_pct"] - display_df["wacc_pct"]

display_df = display_df.rename(columns={
    "symbol": "Ticker",
    "company": "Company",
    "sector": "Sector",
    "source": "Source",
    "fcff_2025_m": "FCFF 2025 (₱M)",
    "fcff_2024_m": "FCFF 2024 (₱M)",
    "fcff_2023_m": "FCFF 2023 (₱M)",
    "roic_pct": "ROIC (%)",
    "wacc_pct": "WACC (%)",
    "rating": "Rating",
    "beta": "Beta",
    "market_cap_b": "Mkt Cap (₱B)",
})

st.dataframe(
    display_df.style
    .format({
        "FCFF 2025 (₱M)": "{:,.1f}",
        "FCFF 2024 (₱M)": "{:,.1f}",
        "FCFF 2023 (₱M)": "{:,.1f}",
        "ROIC (%)": "{:.2f}%",
        "WACC (%)": "{:.2f}%",
        "Spread (ROIC-WACC)": "{:+.2f}%",
        "Beta": "{:.3f}",
        "Mkt Cap (₱B)": "{:,.3f}",
    })
    .map(lambda v: "color: #34d399" if isinstance(v, bool) and v else
              ("color: #f87171" if isinstance(v, bool) else ""), subset=["ROIC>WACC"])
    .map(lambda v: "color: #34d399" if isinstance(v, float) and v > 0 else
              ("color: #f87171" if isinstance(v, float) and v < 0 else ""), subset=["Spread (ROIC-WACC)"]),
    use_container_width=True,
    height=320,
)

# ── CHARTS ROW ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>ROIC vs WACC COMPARISON</div>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # ROIC vs WACC grouped bar
    bar_data = filtered_df.sort_values("roic_pct", ascending=False)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="ROIC", x=bar_data["symbol"], y=bar_data["roic_pct"],
        marker_color="#34d399", opacity=0.85,
    ))
    fig_bar.add_trace(go.Bar(
        name="WACC", x=bar_data["symbol"], y=bar_data["wacc_pct"],
        marker_color="#f87171", opacity=0.85,
    ))
    fig_bar.update_layout(
        barmode="group", paper_bgcolor="#0a0e1a", plot_bgcolor="#0a0e1a",
        font=dict(family="DM Mono, monospace", color="#94a3b8", size=11),
        legend=dict(orientation="h", y=1.1, font=dict(size=10)),
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(ticksuffix="%", gridcolor="#1e2d4a"),
        xaxis=dict(gridcolor="#1e2d4a"),
        height=320,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    # 3-year FCFF trend lines
    fcff_cols = ["fcff_2023_m", "fcff_2024_m", "fcff_2025_m"]
    years = [2023, 2024, 2025]
    fig_fcff = go.Figure()
    colors = ["#60a5fa", "#34d399", "#fbbf24", "#f472b6", "#a78bfa",
              "#fb923c", "#2dd4bf", "#e879f9"]
    for i, row in filtered_df.iterrows():
        color = colors[i % len(colors)]
        fig_fcff.add_trace(go.Scatter(
            x=years, y=[row["fcff_2023_m"], row["fcff_2024_m"], row["fcff_2025_m"]],
            mode="lines+markers", name=row["symbol"],
            line=dict(color=color, width=2),
            marker=dict(size=6, color=color),
        ))
    fig_fcff.update_layout(
        title=dict(text="3-Year FCFF Trend (₱M)", font=dict(size=12, color="#94a3b8")),
        paper_bgcolor="#0a0e1a", plot_bgcolor="#0a0e1a",
        font=dict(family="DM Mono, monospace", color="#94a3b8", size=11),
        legend=dict(orientation="h", y=1.15, font=dict(size=10)),
        margin=dict(l=10, r=10, t=50, b=10),
        yaxis=dict(gridcolor="#1e2d4a", tickformat=",.0f"),
        xaxis=dict(gridcolor="#1e2d4a", tickvals=years),
        height=320,
    )
    st.plotly_chart(fig_fcff, use_container_width=True)

# ── COMPANY DEEP DIVE ─────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>COMPANY DEEP DIVE</div>", unsafe_allow_html=True)

ticker_options = filtered_df["symbol"].tolist()
selected_ticker = st.selectbox(
    "Select company",
    ticker_options,
    format_func=lambda t: f"{t} — {df[df['symbol']==t]['company'].values[0]}"
)

company = filtered_df[filtered_df["symbol"] == selected_ticker].iloc[0]
spread = company["roic_pct"] - company["wacc_pct"]

# KPI cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    fcff_color = "metric-positive" if company["fcff_2025_m"] > 0 else "metric-negative"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>FCFF 2025</div>
        <div class='metric-value {fcff_color}'>₱{company['fcff_2025_m']:,.0f}M</div>
    </div>""", unsafe_allow_html=True)

with kpi2:
    roic_color = "metric-positive" if company["roic_pct"] > company["wacc_pct"] else "metric-negative"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>ROIC</div>
        <div class='metric-value {roic_color}'>{company['roic_pct']:.2f}%</div>
    </div>""", unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>WACC</div>
        <div class='metric-value metric-neutral'>{company['wacc_pct']:.2f}%</div>
    </div>""", unsafe_allow_html=True)

with kpi4:
    spread_color = "metric-positive" if spread > 0 else "metric-negative"
    spread_label = "Value Creator ✓" if spread > 0 else "Value Destroyer ✗"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>ROIC − WACC Spread</div>
        <div class='metric-value {spread_color}'>{spread:+.2f}%</div>
        <div style='font-size:0.72rem;color:{"#34d399" if spread>0 else "#f87171"};
        font-family:DM Mono,monospace;margin-top:0.3rem;'>{spread_label}</div>
    </div>""", unsafe_allow_html=True)

# Company detail row
det1, det2 = st.columns(2)

with det1:
    # WACC build-up
    st.markdown(f"""
    <div class='metric-card' style='margin-top:0.5rem;'>
        <div class='metric-label' style='margin-bottom:0.8rem;'>WACC Components</div>
        <table style='width:100%;font-family:DM Mono,monospace;font-size:0.78rem;
        color:#94a3b8;border-collapse:collapse;'>
            <tr><td style='padding:3px 0;'>Risk-Free Rate (Rf)</td>
                <td style='text-align:right;color:#e2e8f0;'>{company['rf_pct']:.3f}%</td></tr>
            <tr><td style='padding:3px 0;'>Beta (β)</td>
                <td style='text-align:right;color:#e2e8f0;'>{company['beta']:.3f}</td></tr>
            <tr><td style='padding:3px 0;'>ERP</td>
                <td style='text-align:right;color:#e2e8f0;'>{company['erp_pct']:.3f}%</td></tr>
            <tr><td style='padding:3px 0;'>Ke (Cost of Equity)</td>
                <td style='text-align:right;color:#60a5fa;'>{company['ke_pct']:.3f}%</td></tr>
            <tr style='border-top:1px solid #1e2d4a;'>
                <td style='padding:5px 0 3px;'>Credit Rating</td>
                <td style='text-align:right;color:#fbbf24;'>{company['rating']}</td></tr>
            <tr><td style='padding:3px 0;'>Spread</td>
                <td style='text-align:right;color:#e2e8f0;'>{company['spread_pct']:.3f}%</td></tr>
            <tr><td style='padding:3px 0;'>Kd after-tax</td>
                <td style='text-align:right;color:#f87171;'>{company['kd_aftertax_pct']:.3f}%</td></tr>
            <tr style='border-top:1px solid #1e2d4a;'>
                <td style='padding:5px 0 3px;'>E/V weight</td>
                <td style='text-align:right;color:#e2e8f0;'>{company['equity_weight_pct']:.1f}%</td></tr>
            <tr><td style='padding:3px 0;'>D/V weight</td>
                <td style='text-align:right;color:#e2e8f0;'>{company['debt_weight_pct']:.1f}%</td></tr>
            <tr style='border-top:1px solid #334155;font-weight:bold;'>
                <td style='padding:6px 0 3px;color:#e2e8f0;'>WACC</td>
                <td style='text-align:right;color:#60a5fa;font-size:1rem;'>{company['wacc_pct']:.3f}%</td></tr>
        </table>
    </div>""", unsafe_allow_html=True)

with det2:
    # FCFF 3-year chart for selected company
    fig_single = go.Figure()
    fcff_vals = [company["fcff_2023_m"], company["fcff_2024_m"], company["fcff_2025_m"]]
    bar_colors = ["#34d399" if v > 0 else "#f87171" for v in fcff_vals]
    fig_single.add_trace(go.Bar(
        x=[2023, 2024, 2025], y=fcff_vals,
        marker_color=bar_colors, text=[f"₱{v:,.0f}M" for v in fcff_vals],
        textposition="outside", textfont=dict(size=10, color="#94a3b8"),
    ))
    fig_single.add_hline(y=0, line_dash="dot", line_color="#475569")
    fig_single.update_layout(
        title=dict(text=f"{selected_ticker} — 3-Year FCFF (₱M)",
                   font=dict(size=12, color="#94a3b8")),
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font=dict(family="DM Mono, monospace", color="#94a3b8", size=11),
        margin=dict(l=10, r=10, t=50, b=10),
        yaxis=dict(gridcolor="#1e2d4a", tickformat=",.0f"),
        xaxis=dict(tickvals=[2023, 2024, 2025]),
        showlegend=False, height=290,
    )
    st.plotly_chart(fig_single, use_container_width=True)

    # ROIC vs WACC gauge-style bar
    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Bar(
        x=["ROIC", "WACC"], y=[company["roic_pct"], company["wacc_pct"]],
        marker_color=["#34d399" if company["roic_pct"] > company["wacc_pct"] else "#f87171", "#f87171"],
        text=[f"{company['roic_pct']:.2f}%", f"{company['wacc_pct']:.2f}%"],
        textposition="outside", textfont=dict(size=12, color="#e2e8f0"),
        width=0.4,
    ))
    fig_gauge.update_layout(
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font=dict(family="DM Mono, monospace", color="#94a3b8", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis=dict(gridcolor="#1e2d4a", ticksuffix="%"),
        showlegend=False, height=180,
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# ── COMPUTATION BREAKDOWN ─────────────────────────────────────────────────────
with st.expander("📋 View Full Computation Breakdown", expanded=False):
    # Extract the section for the selected company
    import re
    pattern = rf"={{{5,}}}\s+{re.escape(selected_ticker)} —.*?={{{5,}}}"
    sections = re.split(r"(?=={5,}\s+\w+ —)", breakdown_text)
    company_section = ""
    for section in sections:
        if section.strip().startswith("=" * 5) and f"  {selected_ticker} —" in section:
            company_section = section.strip()
            break

    if company_section:
        st.markdown(f"<div class='breakdown-box'>{company_section}</div>",
                    unsafe_allow_html=True)
    else:
        st.text(breakdown_text)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='font-family:DM Mono,monospace;font-size:0.7rem;color:#334155;text-align:center;'>
    PSE Valuation Dashboard &nbsp;·&nbsp; Data from Yahoo Finance & Reuters &nbsp;·&nbsp;
    FCFF = NOPAT + D&A − ΔNWC − CapEx &nbsp;·&nbsp;
    ROIC = NOPAT / Avg IC &nbsp;·&nbsp;
    WACC = (E/V)×Ke + (D/V)×Kd(1−t)
</div>
""", unsafe_allow_html=True)
