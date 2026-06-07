"""
Employee Attrition Intelligence Dashboard — Kayfa Executive HR Analytics (v3)
Premium Executive BI Platform · Question-based Navigation · Insight Cards
"""
import base64
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(
    page_title="Kayfa · Employee Attrition Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  PREMIUM CSS — Executive Dark Navy Theme
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def _css_string():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer { visibility: hidden; }
/* Keep the header transparent but DO NOT hide it — hiding it also hides the
   sidebar expand/collapse arrow, leaving no way to reopen a closed sidebar. */
header[data-testid="stHeader"] { background: transparent !important; }
/* Always allow re-opening a collapsed sidebar */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] { visibility: visible !important; display: flex !important; }
section[data-testid="stSidebar"] { visibility: visible !important; }

.stApp {
    background: linear-gradient(135deg, #0A1430 0%, #14224A 50%, #0B1A38 100%);
    min-height: 100vh;
}

/* ─── SIDEBAR ────────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060F22 0%, #0F1C3C 100%) !important;
    border-right: 1px solid rgba(33, 150, 243, 0.2);
    min-width: 320px !important;
}
section[data-testid="stSidebar"] * { color: #E8EAF6 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #FFFFFF !important; font-size: 14px !important; font-weight: 500; }
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(33, 150, 243, 0.08) !important;
    border: 1px dashed rgba(33, 150, 243, 0.4) !important;
    border-radius: 10px !important;
    padding: 8px !important;
}

/* Logo in sidebar — 2x larger */
.kayfa-sidebar-logo {
    text-align: center;
    padding: 18px 0 22px 0;
}
.kayfa-sidebar-logo .logo-mark {
    font-size: 5.2rem;
    line-height: 1;
    text-shadow: 0 0 40px rgba(33,150,243,0.55);
    margin-bottom: 6px;
}
/* Real logo image / built-in SVG emblem (sidebar) */
.kayfa-sidebar-logo img.logo-mark,
.kayfa-sidebar-logo svg.logo-mark {
    width: 130px;
    max-width: 70%;
    height: auto;
    display: block;
    margin: 0 auto 10px auto;
    filter: drop-shadow(0 0 22px rgba(33,150,243,0.45));
}
.kayfa-sidebar-logo .logo-name {
    font-family: 'Cairo', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #FFFFFF !important;
    letter-spacing: 3px;
    margin: 4px 0 2px 0;
    text-shadow: 0 0 30px rgba(33,150,243,0.6);
}
.kayfa-sidebar-logo .logo-tag {
    font-size: 0.78rem;
    color: #90CAF9 !important;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    font-weight: 600;
}

.sidebar-section-title {
    font-family: 'Cairo', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    color: #64B5F6 !important;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin: 18px 0 10px 0;
}
.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(33,150,243,0.4), transparent);
    margin: 14px 0;
}

/* ─── MAIN CONTAINER ─────────────────────────────────────────────────────── */
.main .block-container { padding: 1.5rem 2.5rem 2rem 2.5rem; max-width: 1500px; }

/* ─── HOMEPAGE HEADER ────────────────────────────────────────────────────── */
.hero-header {
    background: linear-gradient(135deg, rgba(33,150,243,0.12) 0%, rgba(13,71,161,0.18) 100%);
    border: 1px solid rgba(33,150,243,0.25);
    border-radius: 22px;
    padding: 38px 44px;
    margin-bottom: 28px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06);
}
.hero-logo-row {
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 18px;
}
.hero-logo-mark {
    font-size: 4.5rem;
    line-height: 1;
    text-shadow: 0 0 40px rgba(33,150,243,0.6);
}
img.hero-logo-mark { width: 260px; }
svg.hero-logo-mark { width: 100px; }
img.hero-logo-mark, svg.hero-logo-mark {
    height: auto;
    filter: drop-shadow(0 0 26px rgba(33,150,243,0.5));
}
.hero-logo-text {
    font-family: 'Cairo', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: 4px;
    line-height: 1;
    text-shadow: 0 0 30px rgba(33,150,243,0.5);
    min-width: 280px;
}
.hero-logo-tag {
    font-size: 0.9rem;
    color: #90CAF9;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 6px;
}
.hero-header .hero-title,
.hero-title {
    font-family: 'Cairo', sans-serif;
    font-size: 2.3rem;
    font-weight: 900;
    color: #FFFFFF !important;
    margin: 14px 0 8px 0;
    line-height: 1.2;
    letter-spacing: -0.5px;
    text-shadow: 0 1px 12px rgba(0,0,0,0.35);
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #B0BEC5;
    margin: 0;
    font-weight: 400;
    line-height: 1.6;
}

/* Page-level header (per question) */
.page-header {
    background: linear-gradient(135deg, rgba(33,150,243,0.10) 0%, rgba(13,71,161,0.14) 100%);
    border: 1px solid rgba(33,150,243,0.22);
    border-radius: 18px;
    padding: 26px 32px;
    margin-bottom: 24px;
}
.page-tag {
    display: inline-block;
    background: linear-gradient(135deg, #2196F3, #1565C0);
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 18px;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}
.page-header .page-title,
.page-title {
    font-family: 'Cairo', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    color: #FFFFFF !important;
    margin: 4px 0 8px 0;
    letter-spacing: -0.3px;
    text-shadow: 0 1px 12px rgba(0,0,0,0.35);
}
.page-question {
    font-size: 1.05rem;
    color: #90CAF9;
    margin: 0;
    line-height: 1.55;
    font-style: italic;
}

/* ─── KPI CARDS ──────────────────────────────────────────────────────────── */
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 24px 22px;
    text-align: center;
    backdrop-filter: blur(8px);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 18px 18px 0 0;
}
.kpi-card.blue::before  { background: linear-gradient(90deg, #2196F3, #42A5F5); }
.kpi-card.red::before   { background: linear-gradient(90deg, #EF5350, #EF9A9A); }
.kpi-card.amber::before { background: linear-gradient(90deg, #FF8F00, #FFC107); }
.kpi-card.green::before { background: linear-gradient(90deg, #43A047, #81C784); }
.kpi-card.purple::before{ background: linear-gradient(90deg, #7E57C2, #B39DDB); }
.kpi-label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFFFFF;
    margin-bottom: 10px;
    opacity: 0.85;
}
.kpi-value {
    font-family: 'Cairo', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-value.red    { color: #EF9A9A; }
.kpi-value.amber  { color: #FFC107; }
.kpi-value.green  { color: #81C784; }
.kpi-value.purple { color: #B39DDB; }
.kpi-sub { font-size: 13px; color: #B0BEC5; }

/* ─── CHART SECTION ──────────────────────────────────────────────────────── */
.chart-section {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 26px 28px;
    margin-bottom: 22px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
.chart-subtitle {
    font-size: 0.95rem;
    color: #B0BEC5;
    margin: -8px 0 14px 0;
    font-weight: 400;
    line-height: 1.55;
    font-style: italic;
}

/* ─── INSIGHT CARDS (4 colored cards) ────────────────────────────────────── */
.insight-cards-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin: 22px 0 8px 0;
}
.icard {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 20px 22px;
    backdrop-filter: blur(6px);
    border-left: 4px solid var(--accent);
}
.icard.critical    { --accent: #EF5350; }
.icard.keyinsight  { --accent: #2196F3; }
.icard.action      { --accent: #FF8F00; }
.icard.solution    { --accent: #43A047; }

.icard-title {
    font-family: 'Cairo', sans-serif;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    color: var(--accent);
}
.icard-text {
    font-size: 14.5px;
    color: #FFFFFF;
    line-height: 1.65;
    margin: 0;
}
.icard-text strong { color: #FFD54F; font-weight: 700; }

/* ─── SOLUTION PAGE ──────────────────────────────────────────────────────── */
.solution-section {
    background: linear-gradient(135deg, rgba(33,150,243,0.08) 0%, rgba(13,71,161,0.12) 100%);
    border: 1px solid rgba(33,150,243,0.3);
    border-radius: 22px;
    padding: 36px 42px;
    margin-bottom: 24px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 32px rgba(0,0,0,0.25);
}
.solution-header {
    font-family: 'Cairo', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: #FFFFFF;
    margin-bottom: 6px;
    letter-spacing: -0.3px;
}
.solution-subheader {
    font-size: 1rem;
    color: #90CAF9;
    margin-bottom: 28px;
    font-style: italic;
}
.exec-summary {
    background: linear-gradient(135deg, rgba(255,143,0,0.10) 0%, rgba(255,193,7,0.05) 100%);
    border: 1px solid rgba(255,143,0,0.28);
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 26px;
}
.exec-summary-title {
    font-family: 'Cairo', sans-serif;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #FFB300;
    margin-bottom: 12px;
}
.exec-summary-text { font-size: 15px; color: #FFFFFF; line-height: 1.85; }
.exec-summary-text strong { color: #FFD54F; }

.priorities-title {
    font-family: 'Cairo', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 8px 0 18px 0;
}
.priority-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 18px;
    border-left: 4px solid var(--c);
}
.priority-card.p1 { --c: #EF5350; }
.priority-card.p2 { --c: #FF8F00; }
.priority-card.p3 { --c: #2196F3; }
.priority-number {
    font-family: 'Cairo', sans-serif;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
    color: var(--c);
}
.priority-title {
    font-family: 'Cairo', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 8px;
}
.priority-impact {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 18px;
    font-size: 12.5px;
    font-weight: 700;
    margin-bottom: 14px;
    background: rgba(67,160,71,0.18);
    color: #81C784;
    border: 1px solid rgba(67,160,71,0.35);
    letter-spacing: 0.5px;
}
.priority-desc {
    font-size: 14px;
    color: #B0BEC5;
    line-height: 1.7;
    margin-bottom: 14px;
}
.priority-actions-title {
    font-size: 11.5px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.priority-actions { list-style: none; padding: 0; margin: 0; }
.priority-actions li {
    font-size: 14px;
    color: #FFFFFF;
    padding: 7px 0 7px 22px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    position: relative;
    line-height: 1.55;
}
.priority-actions li:last-child { border-bottom: none; }
.priority-actions li::before {
    content: "→"; position: absolute; left: 0;
    color: var(--c); font-weight: 800;
}

.action-plan {
    background: rgba(67,160,71,0.08);
    border: 1px solid rgba(67,160,71,0.28);
    border-radius: 14px;
    padding: 26px 30px;
    margin-top: 22px;
}
.action-plan-title {
    font-family: 'Cairo', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #81C784;
    margin-bottom: 20px;
}
.phase-row {
    display: flex; gap: 18px; margin-bottom: 18px;
    align-items: flex-start;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.phase-row:last-child { border-bottom: none; padding-bottom: 0; margin-bottom: 0; }
.phase-badge {
    background: rgba(67,160,71,0.22);
    border: 1px solid rgba(67,160,71,0.45);
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 800;
    padding: 7px 16px;
    border-radius: 18px;
    white-space: nowrap;
    margin-top: 2px;
    letter-spacing: 0.5px;
}
.phase-content { font-size: 14px; color: #FFFFFF; line-height: 1.75; }
.phase-content strong { color: #FFD54F; font-weight: 700; }

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(33,150,243,0.3), transparent);
    margin: 8px 0 20px 0;
}
</style>
</style>"""

def inject_css():
    st.markdown(_css_string(), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PALETTE & HELPERS — White axis labels, larger fonts everywhere
# ══════════════════════════════════════════════════════════════════════════════
C = dict(
    stayed="#2196F3", left="#EF5350",
    avg="#FFD54F",          # yellow dashed company-average line
    grid="#1E2D4D",
    paper="rgba(0,0,0,0)",
    text="#FFFFFF",
)
BLUE_SEQ  = [[0, "#1A2D5A"], [0.5, "#1E88E5"], [1, "#64B5F6"]]
DIVERGING = [[0, "#EF5350"], [0.5, "#263238"], [1, "#2196F3"]]

def layout(title, subtitle="", h=480):
    """Standard chart layout — white left-aligned title (24px) + optional subtitle."""
    title_text = f"<b>{title}</b>"
    if subtitle:
        title_text = (
            f"<b>{title}</b>"
            f"<br><span style='font-size:13px;color:#B0BEC5;font-weight:400;'>{subtitle}</span>"
        )
    return dict(
        title=dict(
            text=title_text,
            x=0.0, xanchor="left",
            font=dict(size=24, color="#FFFFFF", family="Cairo, sans-serif"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,27,61,0.6)",
        font=dict(family="IBM Plex Sans, sans-serif", color="#FFFFFF", size=14),
        height=h,
        margin=dict(t=100 if subtitle else 88, b=70, l=70, r=50),
        legend=dict(
            orientation="h", y=-0.22, x=0.5, xanchor="center",
            bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF", size=13)
        )
    )

def ax(**kw):
    """Standard axis styling — WHITE labels, larger font."""
    defaults = dict(
        gridcolor=C["grid"],
        linecolor="#1E3A5F",
        zeroline=False,
        tickfont=dict(size=13, color="#FFFFFF"),
        title_font=dict(size=15, color="#FFFFFF", family="IBM Plex Sans, sans-serif"),
    )
    defaults.update(kw)
    return defaults

def add_company_avg(fig, value, orientation="h", text="Company Average", row=None, col=None):
    """Add a yellow-dashed Company Average reference line."""
    kw = dict(line=dict(color=C["avg"], width=2.5, dash="dash"),
              annotation_text=f"<b>{text}: {value:.1f}%</b>",
              annotation_font=dict(color="#FFD54F", size=13),
              annotation_position="top right")
    if row is not None:
        if orientation == "h":
            fig.add_hline(y=value, row=row, col=col, **kw)
        else:
            fig.add_vline(x=value, row=row, col=col, **kw)
    else:
        if orientation == "h":
            fig.add_hline(y=value, **kw)
        else:
            fig.add_vline(x=value, **kw)
    return fig

def show(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def H(s):
    """Collapse multi-line HTML to a single line.
    Streamlit's markdown renderer treats blank / whitespace-only lines as block
    separators and any 4-space-indented line that follows as a CODE block —
    which is why large HTML strings were rendering as raw text. Stripping each
    line and joining with a single space removes both triggers."""
    return " ".join(line.strip() for line in s.splitlines() if line.strip())

def _logo_file():
    """Return (mime, base64) of a logo file if present in the repo, else None.
    Intentionally NOT cached: the file is tiny, and caching a 'missing' result
    would keep the logo hidden after the file is later added."""
    candidates = [
        ("image/png",     "assets/kayfa_logo.png"),
        ("image/png",     "kayfa_logo.png"),
        ("image/png",     "logo.png"),
        ("image/png",     "assets/logo.png"),
        ("image/svg+xml", "kayfa_logo.svg"),
        ("image/svg+xml", "logo.svg"),
        ("image/jpeg",    "logo.jpg"),
    ]
    for mime, p in candidates:
        if os.path.exists(p):
            with open(p, "rb") as fh:
                return mime, base64.b64encode(fh.read()).decode()
    return None

def logo_mark(css_class):
    """Real logo <img> if a file exists, otherwise a built-in Kayfa SVG emblem
    (analytics hexagon) — never a flat emoji. Same CSS class for sizing."""
    f = _logo_file()
    if f:
        mime, data = f
        return f'<img class="{css_class}" src="data:{mime};base64,{data}" alt="Kayfa logo"/>'
    # Recreation of the Kayfa faceted-hexagon emblem (bright azure + deep navy gem)
    gb = f"kgb_{css_class}"   # bright facet gradient
    gn = f"kgn_{css_class}"   # navy facet gradient
    return (
        f'<svg class="{css_class}" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Kayfa">'
        f'<defs>'
        f'<linearGradient id="{gb}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#4D9BFF"/><stop offset="1" stop-color="#2563EB"/></linearGradient>'
        f'<linearGradient id="{gn}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#1E407F"/><stop offset="1" stop-color="#102A57"/></linearGradient>'
        f'</defs>'
        # six alternating facets radiating from centre (60,60)
        f'<path d="M60 60 L60 8 L105 34 Z" fill="url(#{gb})"/>'
        f'<path d="M60 60 L105 34 L105 86 Z" fill="url(#{gn})"/>'
        f'<path d="M60 60 L105 86 L60 112 Z" fill="url(#{gb})"/>'
        f'<path d="M60 60 L60 112 L15 86 Z" fill="url(#{gn})"/>'
        f'<path d="M60 60 L15 86 L15 34 Z" fill="url(#{gb})"/>'
        f'<path d="M60 60 L15 34 L60 8 Z" fill="url(#{gn})"/>'
        # crisp outer hexagon edge
        f'<path d="M60 8 L105 34 L105 86 L60 112 L15 86 L15 34 Z" fill="none" '
        f'stroke="#7FB4FF" stroke-width="2.5" stroke-linejoin="round"/>'
        # subtle centre highlight for the gem facet
        f'<circle cx="60" cy="60" r="3.5" fill="#BBD9FF"/>'
        f'</svg>'
    )

@st.cache_data
def load_data(f=None):
    if f is not None:
        try:    return pd.read_excel(f)
        except: return pd.read_csv(f)
    import os
    for path in ["final_dataset.csv", "final_dataset.xlsx"]:
        if os.path.exists(path):
            return pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    return None

# ══════════════════════════════════════════════════════════════════════════════
#  CHARTS — All values single-label, all text white, company avg in yellow dash
# ══════════════════════════════════════════════════════════════════════════════
def chart1(df):
    c = df["Attrition"].value_counts()
    fig = go.Figure(go.Pie(
        labels=c.index, values=c.values, hole=0.6,
        marker=dict(colors=[C["stayed"], C["left"]], line=dict(color="#0F1B3D", width=3)),
        textinfo="percent+label", textfont=dict(size=17, color="#FFFFFF"),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    ))
    fig.update_layout(
        **layout("Attrition Overview", "Total workforce split between current and departed employees", 440),
        annotations=[dict(
            text=f"<b>{len(df):,}</b><br><span style='font-size:12px'>Total</span>",
            x=0.5, y=0.5, showarrow=False, font=dict(size=20, color="#FFFFFF"))]
    )
    show(fig)

def chart2(df):
    g  = df.groupby(["Gender","Attrition"]).size().unstack()
    gp = df.groupby("Gender")["Attrition"].value_counts(normalize=True).unstack()*100
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index, y=g["Stayed"], marker_color=C["stayed"],
               text=[f"{v:,}" for v in g["Stayed"]], textposition="outside",
               textfont=dict(color="#FFFFFF", size=14)),
        go.Bar(name="Left",   x=g.index, y=g["Left"],   marker_color=C["left"],
               text=[f"{v:,}" for v in g["Left"]],   textposition="outside",
               textfont=dict(color="#FFFFFF", size=14)),
    ])
    for gen in g.index:
        fig.add_annotation(x=gen, y=g.loc[gen].max()+4000,
                           text=f"<b>{gp.loc[gen,'Left']:.1f}%</b>",
                           showarrow=False, font=dict(size=15, color="#FFFFFF"))
    fig.update_layout(**layout("Attrition by Gender",
                               "Do men and women leave the organization at different rates?"),
                      barmode="group")
    fig.update_xaxes(**ax(title_text="Gender"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart3(df):
    df = df.copy()
    df["AG"] = pd.cut(df["Age"],[17,25,35,45,55,65],
                      labels=["18-25","26-35","36-45","46-55","56-65"])
    g  = df.groupby(["AG","Attrition"],observed=False).size().unstack()
    gp = df.groupby("AG",observed=False)["Attrition"].value_counts(normalize=True).unstack()*100
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index.astype(str), y=g["Stayed"], marker_color=C["stayed"]),
        go.Bar(name="Left",   x=g.index.astype(str), y=g["Left"],   marker_color=C["left"]),
    ])
    fig.add_trace(go.Scatter(name="Attrition Rate %", x=g.index.astype(str), y=gp["Left"], yaxis="y2",
        mode="lines+markers+text", line=dict(color="#FF8F00", width=3),
        marker=dict(size=11, color="#FF8F00"),
        text=[f"{v:.1f}%" for v in gp["Left"]], textposition="top center",
        textfont=dict(color="#FFFFFF", size=13)))
    fig.update_layout(**layout("Attrition by Age Group",
                               "Which generations face the highest attrition risk?"),
        barmode="group",
        yaxis2=dict(overlaying="y", side="right", range=[0,100], showgrid=False,
                    title="Attrition Rate (%)", tickfont=dict(color="#FFFFFF", size=13),
                    title_font=dict(color="#FFFFFF", size=15)))
    fig.update_xaxes(**ax(title_text="Age Group"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    add_company_avg(fig, overall)
    show(fig)

def chart4(df):
    pct = df.groupby("Job Role")["Attrition"].apply(lambda x:(x=="Left").mean()*100).sort_values()
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure(go.Bar(x=pct.values, y=pct.index, orientation="h",
        marker=dict(color=pct.values, colorscale=BLUE_SEQ, showscale=True,
                    colorbar=dict(title=dict(text="Rate %", font=dict(color="#FFFFFF", size=13)),
                                  tickfont=dict(color="#FFFFFF", size=12))),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#FFFFFF", size=14)))
    fig.update_layout(**layout("Attrition by Job Role",
                               "Is attrition concentrated in specific roles?", 460))
    fig.update_xaxes(**ax(title_text="Attrition Rate (%)"))
    fig.update_yaxes(**ax(title_text="Job Role"))
    add_company_avg(fig, overall, orientation="v")
    show(fig)

def chart5(df):
    fig = go.Figure()
    for label, color in [("Stayed", C["stayed"]), ("Left", C["left"])]:
        sub = df[df["Attrition"]==label]["Monthly Income"]
        fig.add_trace(go.Box(y=sub, name=label, marker_color=color, boxmean=True,
                             line=dict(color=color)))
        fig.add_annotation(x=label, y=sub.mean()+1500,
                           text=f"<b>Mean: ${sub.mean():,.0f}</b>",
                           showarrow=False, font=dict(size=14, color="#FFFFFF"))
    fig.update_layout(**layout("Monthly Income by Attrition Status",
                               "Are leavers paid less than those who stay?"))
    fig.update_xaxes(**ax(title_text="Attrition Status"))
    fig.update_yaxes(**ax(title_text="Monthly Income (USD)"))
    show(fig)

def chart6(df):
    order = ["Poor","Fair","Good","Excellent"]
    g  = df.groupby(["Work-Life Balance","Attrition"],observed=False).size().unstack().reindex(order)
    gp = df.groupby("Work-Life Balance",observed=False)["Attrition"].value_counts(normalize=True).unstack().reindex(order)*100
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index, y=g["Stayed"], marker_color=C["stayed"],
               text=[f"{v:,}" for v in g["Stayed"]], textposition="inside",
               textfont=dict(color="#FFFFFF", size=13)),
        go.Bar(name="Left",   x=g.index, y=g["Left"],   marker_color=C["left"],
               text=[f"{v:,}" for v in g["Left"]],   textposition="inside",
               textfont=dict(color="#FFFFFF", size=13)),
    ])
    for wl in order:
        fig.add_annotation(x=wl, y=g.loc[wl].sum()+1500,
                           text=f"<b>{gp.loc[wl,'Left']:.1f}%</b>",
                           showarrow=False, font=dict(size=14, color="#FFFFFF"))
    fig.update_layout(**layout("Attrition by Work-Life Balance",
                               "How much does work-life balance affect retention?"),
                      barmode="stack")
    fig.update_xaxes(**ax(title_text="Work-Life Balance"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart7(df):
    ot = df.groupby("Overtime")["Attrition"].value_counts(normalize=True).unstack()*100
    oy = df[df["Overtime"]=="Yes"]["Attrition"].value_counts()
    fig = make_subplots(1, 2,
        specs=[[{"type":"pie"}, {"type":"bar"}]],
        subplot_titles=("Overtime Employee Distribution", "Attrition Rate by Overtime"))
    fig.add_trace(go.Pie(
        labels=["Stayed","Left"], values=[oy.get("Stayed",0), oy.get("Left",0)],
        marker=dict(colors=[C["stayed"], C["left"]]), hole=0.5,
        textinfo="percent+label", textfont=dict(color="#FFFFFF", size=15)), 1, 1)
    fig.add_trace(go.Bar(
        x=["No Overtime","With Overtime"], y=ot["Left"],
        marker=dict(color=[C["stayed"], C["left"]]),
        text=[f"{v:.1f}%" for v in ot["Left"]], textposition="outside",
        textfont=dict(color="#FFFFFF", size=15)), 1, 2)
    fig.update_layout(**layout("Overtime Impact on Attrition",
                               "Does working overtime push employees to leave?", 480),
                      showlegend=False)
    for ann in fig.layout.annotations:
        ann.font.size = 15
        ann.font.color = "#FFFFFF"
    show(fig)

def chart8(df):
    df2 = df.copy()
    df2["Education Level"] = df2["Education Level"].str.replace("'","'").str.replace("'","'")
    order = ["High School","Associate Degree","Bachelor's Degree","Master's Degree","PhD"]
    short = ["High School","Associate Degree","Bachelor's Degree","Master's Degree","PhD"]
    pct = df2.groupby("Education Level")["Attrition"].apply(lambda x:(x=="Left").mean()*100).reindex(order)
    pct_vals = [v if not pd.isna(v) else 0 for v in pct.values]
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure(go.Bar(
        x=short, y=pct_vals,
        marker=dict(color=pct_vals, colorscale=BLUE_SEQ, showscale=True,
                    colorbar=dict(title=dict(text="Rate %", font=dict(color="#FFFFFF", size=13)),
                                  tickfont=dict(color="#FFFFFF", size=12))),
        text=[f"{v:.1f}%" if v>0 else "N/A" for v in pct_vals],
        textposition="outside", textfont=dict(color="#FFFFFF", size=15)))
    fig.update_layout(**layout("Attrition by Education Level",
                               "Do higher-educated employees stay longer?", 500))
    fig.update_xaxes(**ax(title_text="Education Level"))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)", range=[0,60]))
    add_company_avg(fig, overall)
    show(fig)

def chart9(df):
    cols = ["Age","Years at Company","Monthly Income","Number of Promotions",
            "Distance from Home","Number of Dependents","Company Tenure"]
    df2 = df.copy()
    df2["Attrition_Bin"] = (df2["Attrition"]=="Left").astype(int)
    corr = df2[cols+["Attrition_Bin"]].corr()
    labels = ["Age","Years","Income","Promotions","Distance","Dependents","Tenure","Attrition"]
    fig = go.Figure(go.Heatmap(z=corr.values, x=labels, y=labels, colorscale=DIVERGING,
        zmin=-1, zmax=1,
        text=corr.round(2).values, texttemplate="%{text:.2f}", textfont=dict(size=13, color="#FFFFFF"),
        colorbar=dict(title=dict(text="r", font=dict(color="#FFFFFF", size=13)),
                      tickfont=dict(color="#FFFFFF", size=12))))
    fig.update_layout(**layout("Correlation Heatmap — Numeric Drivers",
                               "Which numeric factors correlate most with attrition?", 540))
    fig.update_xaxes(**ax(tickfont=dict(size=13, color="#FFFFFF")))
    fig.update_yaxes(**ax(tickfont=dict(size=13, color="#FFFFFF")))
    show(fig)

def chart10(df):
    df = df.copy()
    bins = list(range(0,55,5))
    df["YG"] = pd.cut(df["Years at Company"], bins=bins,
                      labels=[f"{i}-{i+4}" for i in bins[:-1]], include_lowest=True)
    g  = df.groupby("YG",observed=True)["Attrition"].value_counts().unstack(fill_value=0)
    gp = df.groupby("YG",observed=True)["Attrition"].value_counts(normalize=True).unstack(fill_value=0)*100
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index.astype(str), y=g["Stayed"], marker_color=C["stayed"]),
        go.Bar(name="Left",   x=g.index.astype(str), y=g["Left"],   marker_color=C["left"]),
    ])
    fig.add_trace(go.Scatter(name="Attrition Rate %", x=g.index.astype(str), y=gp["Left"], yaxis="y2",
        mode="lines+markers", line=dict(color="#FF8F00", width=3),
        marker=dict(size=10, color="#FF8F00")))
    fig.update_layout(**layout("Attrition by Company Tenure",
                               "When are employees most likely to leave?"),
        barmode="stack",
        yaxis2=dict(overlaying="y", side="right", range=[0,100], showgrid=False,
                    title="Attrition Rate (%)", tickfont=dict(color="#FFFFFF", size=13),
                    title_font=dict(color="#FFFFFF", size=15)))
    fig.update_xaxes(**ax(title_text="Years at Company"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart11(df):
    data = df.groupby(["Marital Status","Gender"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack()
    colors = {"Male": C["stayed"], "Female": "#AB47BC"}
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure([go.Bar(
        name=g, x=data.index, y=data[g], marker_color=colors.get(g,"#78909C"),
        text=[f"{v:.1f}%" for v in data[g]], textposition="outside",
        textfont=dict(color="#FFFFFF", size=14))
        for g in data.columns])
    fig.update_layout(**layout("Attrition by Marital Status & Gender",
                               "How does life stage shape retention?"),
                      barmode="group")
    fig.update_xaxes(**ax(title_text="Marital Status"))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)"))
    add_company_avg(fig, overall)
    show(fig)

def chart12(df):
    data = df.groupby(["Company Size","Remote Work"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack()
    colors = {"Yes":"#26A69A","No":C["left"]}
    labels = {"Yes":"Remote","No":"On-site"}
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure([go.Bar(
        name=labels.get(k,k), x=data.index, y=data[k], marker_color=colors.get(k,"#78909C"),
        text=[f"{v:.1f}%" for v in data[k]], textposition="outside",
        textfont=dict(color="#FFFFFF", size=14))
        for k in data.columns])
    fig.update_layout(**layout("Attrition by Company Size & Remote Work",
                               "Does remote work reduce attrition across all company sizes?"),
                      barmode="group")
    fig.update_xaxes(**ax(title_text="Company Size"))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)"))
    add_company_avg(fig, overall)
    show(fig)

def chart13(df):
    pivot = df.groupby(["Performance Rating","Job Satisfaction"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack()
    fig = go.Figure(go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=BLUE_SEQ,
        text=pivot.round(1).values, texttemplate="%{text:.1f}%",
        textfont=dict(size=15, color="#FFFFFF"),
        colorbar=dict(title=dict(text="Rate %", font=dict(color="#FFFFFF", size=13)),
                      tickfont=dict(color="#FFFFFF", size=12))))
    fig.update_layout(**layout("Performance Rating × Job Satisfaction",
                               "Spotting the High-Performer + Low-Satisfaction risk segment", 460))
    fig.update_xaxes(**ax(title_text="Job Satisfaction"))
    fig.update_yaxes(**ax(title_text="Performance Rating"))
    show(fig)

def chart14(df):
    df = df.copy()
    df["DG"] = pd.cut(df["Distance from Home"],[0,20,40,60,80,100],
                      labels=["0-20","21-40","41-60","61-80","81-100"])
    pct = df.groupby("DG",observed=True)["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure(go.Bar(
        x=pct.index.astype(str), y=pct.values,
        marker=dict(color=pct.values, colorscale=BLUE_SEQ, showscale=True,
                    colorbar=dict(title=dict(text="Rate %", font=dict(color="#FFFFFF", size=13)),
                                  tickfont=dict(color="#FFFFFF", size=12))),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#FFFFFF", size=15)))
    fig.update_layout(**layout("Attrition by Commute Distance",
                               "Are long-commute employees more likely to leave?"))
    fig.update_xaxes(**ax(title_text="Distance from Home (km)"))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)", range=[0,pct.max()*1.3]))
    add_company_avg(fig, overall)
    show(fig)

def chart15(df):
    pct   = df.groupby("Leadership Opportunities")["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    colors = {"No":C["left"],"Yes":C["stayed"]}
    labels = {"No":"No Leadership Opps","Yes":"Has Leadership Opps"}
    fig = go.Figure()
    for val in ["No","Yes"]:
        fig.add_trace(go.Bar(x=[labels[val]], y=[pct[val]], name=labels[val],
            marker_color=colors[val],
            text=[f"{pct[val]:.1f}%"], textposition="outside",
            textfont=dict(color="#FFFFFF", size=17), width=0.45))
    fig.update_layout(**layout("Attrition by Leadership Opportunities",
                               "Do leadership opportunities help retain employees?", 440),
                      showlegend=False,
                      yaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,65])))
    fig.update_xaxes(**ax(title_text=""))
    show(fig)

def chart16(df):
    pct   = df.groupby("Innovation Opportunities")["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    colors = {"No":C["left"],"Yes":C["stayed"]}
    labels = {"No":"No Innovation Opps","Yes":"Has Innovation Opps"}
    fig = go.Figure()
    for val in ["No","Yes"]:
        fig.add_trace(go.Bar(x=[labels[val]], y=[pct[val]], name=labels[val],
            marker_color=colors[val],
            text=[f"{pct[val]:.1f}%"], textposition="outside",
            textfont=dict(color="#FFFFFF", size=17), width=0.45))
    fig.update_layout(**layout("Attrition by Innovation Opportunities",
                               "Do innovation opportunities help retain employees?", 440),
                      showlegend=False,
                      yaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,65])))
    fig.update_xaxes(**ax(title_text=""))
    show(fig)

def chart17(df):
    order = ["Poor","Fair","Good","Excellent"]
    pct   = df.groupby("Company Reputation")["Attrition"].apply(lambda x:(x=="Left").mean()*100).reindex(order)
    overall = (df["Attrition"]=="Left").mean()*100
    fig = go.Figure(go.Bar(x=pct.values, y=pct.index, orientation="h",
        marker=dict(color=pct.values, colorscale=DIVERGING, cmin=35, cmax=60, showscale=True,
                    colorbar=dict(title=dict(text="Rate %", font=dict(color="#FFFFFF", size=13)),
                                  tickfont=dict(color="#FFFFFF", size=12))),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#FFFFFF", size=15)))
    fig.update_layout(**layout("Attrition by Company Reputation",
                               "Does the company's reputation affect retention?", 440),
        xaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,75])),
        yaxis=dict(**ax(title_text="Reputation Level")))
    add_company_avg(fig, overall, orientation="v")
    show(fig)

def chart18(df):
    order = ["Low","Medium","High","Very High"]
    pct   = df.groupby("Employee Recognition",observed=False)["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).reindex(order)
    count = df["Employee Recognition"].value_counts().reindex(order)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=pct.index, y=pct.values,
        marker=dict(color=pct.values, colorscale=BLUE_SEQ, showscale=True,
                    colorbar=dict(title=dict(text="Rate %", font=dict(color="#FFFFFF", size=13)),
                                  tickfont=dict(color="#FFFFFF", size=12))),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#FFFFFF", size=15), name="Attrition Rate"))
    fig.add_trace(go.Scatter(x=order, y=count.values, yaxis="y2",
        mode="lines+markers", line=dict(color="#FF8F00", width=3, dash="dot"),
        marker=dict(size=11, color="#FF8F00"), name="Employee Count"))
    fig.update_layout(**layout("Attrition by Employee Recognition",
                               "Does verbal recognition translate into retention?", 500),
        yaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,65])),
        yaxis2=dict(overlaying="y", side="right", showgrid=False,
                    title="Employee Count",
                    tickfont=dict(color="#FFFFFF", size=13),
                    title_font=dict(color="#FFFFFF", size=15)))
    fig.update_xaxes(**ax(title_text="Recognition Level"))
    show(fig)

def chart19(df):
    order_jl = ["Entry","Mid","Senior"]
    g  = df.groupby("Job Level")["Attrition"].value_counts().unstack().reindex(order_jl)
    gp = df.groupby("Job Level")["Attrition"].value_counts(normalize=True).unstack().reindex(order_jl)*100
    pivot = df.groupby(["Job Level","Remote Work"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack().reindex(order_jl)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.6,0.4],
        subplot_titles=("Attrition Count & Rate by Job Level","Rate % — Job Level × Remote Work"),
        specs=[[{"type":"bar"},{"type":"heatmap"}]])
    fig.add_trace(go.Bar(name="Stayed", x=order_jl, y=g["Stayed"], marker_color=C["stayed"],
        text=[f"{v:,}" for v in g["Stayed"]], textposition="inside",
        textfont=dict(color="#FFFFFF", size=13)), row=1, col=1)
    fig.add_trace(go.Bar(name="Left", x=order_jl, y=g["Left"], marker_color=C["left"],
        text=[f"{v:,}" for v in g["Left"]], textposition="inside",
        textfont=dict(color="#FFFFFF", size=13)), row=1, col=1)
    fig.add_trace(go.Scatter(name="Rate %", x=order_jl, y=gp["Left"], yaxis="y2",
        mode="lines+markers", line=dict(color="#FF8F00", width=3),
        marker=dict(size=12, color="#FF8F00")), row=1, col=1)
    fig.add_trace(go.Heatmap(z=pivot.values, x=pivot.columns.tolist(), y=order_jl,
        colorscale=BLUE_SEQ,
        text=pivot.round(1).values, texttemplate="%{text:.1f}%",
        textfont=dict(size=15, color="#FFFFFF"),
        colorbar=dict(title=dict(text="Rate %", font=dict(color="#FFFFFF", size=13)),
                      tickfont=dict(color="#FFFFFF", size=12),
                      x=1.02),
        showscale=True), row=1, col=2)
    fig.update_layout(**layout("Job Level Impact × Remote Work",
                               "Who are the highest-risk employees in the entire organization?", 520),
        barmode="group",
        yaxis2=dict(overlaying="y", side="right", range=[0,100], showgrid=False,
                    title="Rate (%)", tickfont=dict(color="#FFFFFF", size=13),
                    title_font=dict(color="#FFFFFF", size=15)))
    for ann in fig.layout.annotations:
        ann.font.size = 15
        ann.font.color = "#FFFFFF"
    fig.update_xaxes(title_text="Job Level", row=1, col=1,
                     tickfont=dict(size=13, color="#FFFFFF"),
                     title_font=dict(size=15, color="#FFFFFF"))
    fig.update_yaxes(title_text="Headcount", row=1, col=1,
                     tickfont=dict(size=13, color="#FFFFFF"),
                     title_font=dict(size=15, color="#FFFFFF"))
    fig.update_xaxes(title_text="Remote Work", row=1, col=2,
                     tickfont=dict(size=13, color="#FFFFFF"),
                     title_font=dict(size=15, color="#FFFFFF"))
    fig.update_yaxes(tickfont=dict(size=13, color="#FFFFFF"), row=1, col=2)
    show(fig)

# ══════════════════════════════════════════════════════════════════════════════
#  QUESTION STRUCTURE — Maps each Q to its charts + insight cards
# ══════════════════════════════════════════════════════════════════════════════
CHARTS = {
    1: chart1, 2: chart2, 3: chart3, 4: chart4, 5: chart5,
    6: chart6, 7: chart7, 8: chart8, 9: chart9, 10: chart10,
    11: chart11, 12: chart12, 13: chart13, 14: chart14, 15: chart15,
    16: chart16, 17: chart17, 18: chart18, 19: chart19,
}

# Each question: title, question_text, chart_ids, and 4 insight cards
QUESTIONS = {
    "Q1": {
        "title": "Headline Overview",
        "question": "What's the overall scale of the attrition problem?",
        "charts": [1, 2, 4],
        "cards": {
            "critical":   "Attrition rate sits at <strong>47.5%</strong> — more than <strong>3× the global benchmark</strong> of 10–15%. Roughly <strong>1 in every 2 employees</strong> leaves the organization.",
            "keyinsight": "The problem is <strong>organization-wide</strong>, not role-specific. Variation between roles is under <strong>2 percentage points</strong>, pointing to a structural / cultural issue.",
            "action":     "Treat this as a <strong>board-level priority</strong>. Stand up a cross-functional retention task force with HR, Operations, and Finance representatives within 14 days.",
            "solution":   "Establish a <strong>monthly attrition KPI dashboard</strong> reported to the C-suite. Target a 5-point reduction in 90 days and 15-point reduction within 12 months.",
        }
    },
    "Q2": {
        "title": "Overtime Impact",
        "question": "Does working overtime push employees out the door?",
        "charts": [7, 6],
        "cards": {
            "critical":   "Overtime workers leave at <strong>51.5%</strong> vs <strong>45.5%</strong> for non-overtime — and <strong>~33% of the workforce (24,341 employees)</strong> is currently doing overtime.",
            "keyinsight": "Combined with Work-Life Balance data: <strong>Poor WLB → 60.2% attrition</strong> vs <strong>Excellent WLB → 35.7%</strong>. Burnout is a primary driver, not pay.",
            "action":     "Set <strong>hard overtime caps</strong> per team (e.g., max 5 hrs/week sustained). Automatic HR escalation when thresholds are breached.",
            "solution":   "Pilot a <strong>4-day work week</strong> for high-overtime teams. Track WLB scores monthly — target 80%+ in Good/Excellent within 6 months.",
        }
    },
    "Q3": {
        "title": "Remote Work Impact",
        "question": "Does remote work meaningfully reduce attrition?",
        "charts": [12, 19],
        "cards": {
            "critical":   "On-site Entry-level employees leave at <strong>69.3%</strong>. Remote Senior employees leave at <strong>5.2%</strong>. The gap is <strong>64 percentage points</strong>.",
            "keyinsight": "Remote work cuts attrition by ~<strong>28 points across all company sizes</strong> (53% on-site → 24% remote). This is the single highest-leverage variable in the entire dataset.",
            "action":     "<strong>Immediately</strong> offer hybrid/remote to all Entry-level employees and to anyone with a commute &gt; 40 km (currently 52.9% attrition).",
            "solution":   "Publish a formal <strong>remote work policy</strong> with transparent eligibility within 30 days. Project a 8–12 pt drop in overall attrition.",
        }
    },
    "Q4": {
        "title": "Pay Fairness",
        "question": "Is salary the real reason employees leave?",
        "charts": [5, 9],
        "cards": {
            "critical":   "Mean income gap between leavers and stayers is only <strong>$46</strong> — and income's correlation with attrition is <strong>0.011</strong> (essentially zero).",
            "keyinsight": "<strong>Salary is NOT the root cause.</strong> The strongest retention driver is <strong>Promotions (−0.081)</strong>; the strongest attrition driver is <strong>Commute distance (+0.094)</strong>.",
            "action":     "Stop using <strong>blanket salary increases</strong> as the primary retention lever. They're expensive and ineffective.",
            "solution":   "Redirect compensation budget into <strong>career growth, flexibility, and recognition</strong> programs — proven, higher-ROI levers.",
        }
    },
    "Q5": {
        "title": "Retention Timeline",
        "question": "When in their tenure are employees most likely to leave?",
        "charts": [10, 3],
        "cards": {
            "critical":   "The <strong>first 5 years</strong> are the most dangerous — attrition peaks at <strong>51–53%</strong>. Employees aged <strong>18–25 leave at 53.1%</strong>.",
            "keyinsight": "After <strong>10 years</strong>, attrition drops sharply. The window for impact is <strong>onboarding through year 3</strong> — that's where retention dollars deliver the most.",
            "action":     "Redesign onboarding into a <strong>12-month structured mentorship program</strong>. Assign a senior 'retention champion' to every new hire.",
            "solution":   "Replace exit interviews with <strong>30/60/90-day stay interviews</strong> for all sub-2-year employees. Catch concerns before they harden into resignations.",
        }
    },
    "Q6": {
        "title": "Engagement Signals",
        "question": "Which engagement signals predict who will stay?",
        "charts": [13, 18, 17],
        "cards": {
            "critical":   "The most dangerous segment: <strong>High Performance + Low Satisfaction</strong>. Top performers find new jobs fastest — and they're <strong>actively unhappy</strong>.",
            "keyinsight": "Recognition level alone changes attrition by only <strong>1.8%</strong> — verbal praise without <strong>tangible rewards or promotions</strong> has near-zero effect.",
            "action":     "Identify all <strong>High-Perf + Low-Sat</strong> employees this week. Run 1:1 retention conversations led by skip-level managers.",
            "solution":   "Tie recognition programs to <strong>concrete rewards</strong> — bonuses, promotions, public visibility. Audit company reputation perception quarterly.",
        }
    },
    "Q7": {
        "title": "Life Stage Analysis",
        "question": "How do age, gender, and marital status shape retention?",
        "charts": [3, 2, 11],
        "cards": {
            "critical":   "<strong>Single employees</strong> leave at staggering rates — <strong>72.2% for women</strong>, <strong>62.3% for men</strong>. Female overall attrition is <strong>53%</strong> vs 42.9% male.",
            "keyinsight": "<strong>Married employees</strong> are dramatically more stable. Family commitments correlate with retention — but the takeaway is <strong>community and belonging</strong>, not marital status itself.",
            "action":     "Launch <strong>community-building programs</strong> for single employees: peer groups, social events, affinity networks.",
            "solution":   "Run targeted <strong>female-employee focus groups</strong> to surface the unique barriers driving the 10-point gender gap.",
        }
    },
    "Q8": {
        "title": "Career Stagnation",
        "question": "Are employees leaving because they see no path forward?",
        "charts": [15, 16, 8],
        "cards": {
            "critical":   "<strong>95% of employees have ZERO leadership opportunities</strong>. <strong>83%</strong> have no innovation opportunities. The talent pipeline is essentially blocked.",
            "keyinsight": "Promotions show the <strong>strongest negative correlation with attrition (−0.081)</strong> — stronger than salary, age, or any other variable measured.",
            "action":     "Mandate <strong>quarterly career-path conversations</strong> for every manager with each direct report. Document expected next role and timeline.",
            "solution":   "Launch a <strong>Leadership Accelerator cohort</strong> for high-performers with &lt;5 yrs tenure. Allocate 10–20% of work time to innovation projects for non-senior staff.",
        }
    },
    "Q9": {
        "title": "Highest Risk Profile",
        "question": "Who is the single highest-risk employee profile?",
        "charts": [19, 14],
        "cards": {
            "critical":   "The deadliest combination: <strong>Entry-level + On-site + Long commute</strong>. Entry-level on-site = <strong>69.3% attrition</strong>. Long commute (&gt;80km) = <strong>52.9%</strong>.",
            "keyinsight": "Conversely, <strong>Senior + Remote = 5.2% attrition</strong>. The variance across the workforce is enormous — meaning targeted interventions can deliver outsized returns.",
            "action":     "Build an <strong>attrition risk score</strong> using: Job Level, Remote/On-site, Commute Distance, WLB, Overtime. Run nightly; alert managers on score &gt; threshold.",
            "solution":   "Triage the top 500 highest-risk employees. Offer <strong>remote work + accelerated career conversation</strong> within 30 days. Track 90-day retention impact.",
        }
    },
    "Q10": {
        "title": "Top Drivers",
        "question": "Across all variables, what truly drives attrition?",
        "charts": [9, 17, 14],
        "cards": {
            "critical":   "Top drivers (in order): <strong>Lack of flexibility, Career stagnation, Poor WLB, Commute distance, Single/Young life stage</strong>. Salary is <strong>not</strong> in the top 5.",
            "keyinsight": "All top drivers are <strong>structurally addressable</strong> — they require <strong>policy changes</strong>, not budget. The highest-impact intervention (remote work) has <strong>zero direct cost</strong>.",
            "action":     "Sequence interventions by <strong>impact × ease</strong>: (1) Remote/Hybrid, (2) Career conversations, (3) Overtime caps, (4) Stay-interview program, (5) Mentorship.",
            "solution":   "See the <strong>Solution</strong> page for the full Top-3 priorities and 90-day action plan with expected impact estimates.",
        }
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — Kayfa logo (2x) + Navigation
# ══════════════════════════════════════════════════════════════════════════════
# Sidebar branding is rendered inside each page via render_sidebar_brand()

# ══════════════════════════════════════════════════════════════════════════════
#  LOAD DATA  (pure Python — no st.* calls at module level)
# ══════════════════════════════════════════════════════════════════════════════
df = load_data()

def _check_data():
    """Call this at the top of every page to guard against missing data."""
    if df is None:
        st.error("❌ Data file not found — ensure final_dataset.csv is in the repo")
        st.stop()

# Pre-compute summary stats (safe — pure pandas, no st.*)
if df is not None:
    total      = len(df)
    left       = (df["Attrition"]=="Left").sum()
    stayed     = total - left
    rate       = left/total*100
    avg_tenure = df["Years at Company"].mean()
else:
    total = left = stayed = rate = avg_tenure = 0

# ══════════════════════════════════════════════════════════════════════════════
#  RENDER HELPERS
# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR BRANDING — called once at the top of every page function
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar_brand():
    inject_css()
    _check_data()
    with st.sidebar:
        st.markdown(f"""
        <div class="kayfa-sidebar-logo">
            {logo_mark("logo-mark")}
            <div class="logo-name">KAYFA</div>
            <div class="logo-tag">Employee Analytics</div>
        </div>
        <div class="sidebar-divider"></div>
        <div style="background:rgba(33,150,243,0.08);border:1px solid rgba(33,150,243,0.22);
                    border-radius:10px;padding:14px 16px;margin-top:12px;">
            <p style="font-size:12px;color:#FFFFFF;margin:0;text-align:center;line-height:2;font-weight:500;">
                📊 19 Interactive Charts<br>
                💡 10 Strategic Questions<br>
                🚀 Executive Action Plan
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_hero():
    """Premium homepage hero with large Kayfa logo top-left."""
    st.markdown(f"""
    <div class="hero-header">
        <div class="hero-logo-row">
            {logo_mark("hero-logo-mark")}
            <div>
                <div class="hero-logo-text">KAYFA</div>
                <div class="hero-logo-tag">Employee Analytics Platform</div>
            </div>
        </div>
        <h1 class="hero-title">Week #1 Task: Employee Attrition Intelligence Dashboard</h1>
        <p class="hero-subtitle">Understand why employees leave and what actions HR should take to improve retention.</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpis():
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card amber">
            <div class="kpi-label">Overall Attrition Rate</div>
            <div class="kpi-value amber">{rate:.1f}%</div>
            <div class="kpi-sub">Company Average</div>
        </div>
        <div class="kpi-card blue">
            <div class="kpi-label">Total Employees</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">100% of Workforce</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Employees Left</div>
            <div class="kpi-value red">{left:,}</div>
            <div class="kpi-sub">Left the Company</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Employees Stayed</div>
            <div class="kpi-value green">{stayed:,}</div>
            <div class="kpi-sub">Still with Company</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-label">Avg. Tenure (Years)</div>
            <div class="kpi-value purple">{avg_tenure:.1f}</div>
            <div class="kpi-sub">Company Average</div>
        </div>
    </div>
    <div class="section-divider"></div>
    """, unsafe_allow_html=True)

def render_page_header(q_key, q):
    st.markdown(f"""
    <div class="page-header">
        <span class="page-tag">{q_key} · Analysis Question</span>
        <h2 class="page-title">{q['title']}</h2>
        <p class="page-question">{q['question']}</p>
    </div>
    """, unsafe_allow_html=True)

def render_insight_cards(cards):
    st.markdown(f"""
    <div class="insight-cards-grid">
        <div class="icard critical">
            <div class="icard-title">🚨 Critical Finding</div>
            <p class="icard-text">{cards['critical']}</p>
        </div>
        <div class="icard keyinsight">
            <div class="icard-title">💡 Key Insight</div>
            <p class="icard-text">{cards['keyinsight']}</p>
        </div>
        <div class="icard action">
            <div class="icard-title">✅ Recommended Action</div>
            <p class="icard-text">{cards['action']}</p>
        </div>
        <div class="icard solution">
            <div class="icard-title">🚀 Solution</div>
            <p class="icard-text">{cards['solution']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Wide charts (multi-panel subplots / heatmaps) always span the full width
WIDE_CHARTS = {7, 9, 13, 19}

def _render_chart(chart_id):
    with st.container():
        CHARTS[chart_id](df)

def render_question_page(q_key):
    render_sidebar_brand()
    q = QUESTIONS[q_key]
    render_page_header(q_key, q)
    render_kpis()
    pending = []  # narrow charts queued to render two-per-row

    def flush():
        while pending:
            row = pending[:2]
            del pending[:2]
            for col, cid in zip(st.columns(len(row)), row):
                with col:
                    _render_chart(cid)

    for chart_id in q["charts"]:
        if chart_id in WIDE_CHARTS:
            flush()
            _render_chart(chart_id)
        else:
            pending.append(chart_id)
    flush()
    render_insight_cards(q["cards"])

def render_home():
    render_sidebar_brand()
    render_hero()
    render_kpis()
    # Homepage shows the headline overview chart
    with st.container():
        chart1(df)

    # Quick-navigation card grid
    st.markdown("""
    <div style="margin-top:8px;">
        <h3 style="font-family:'Cairo',sans-serif;font-size:1.4rem;font-weight:800;
                   color:#FFFFFF;margin:24px 0 14px 0;">📋 Explore the 10 Analysis Questions</h3>
    </div>
    """, unsafe_allow_html=True)

    cards_html = '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;">'
    for k, v in QUESTIONS.items():
        cards_html += f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.10);
                    border-radius:14px;padding:18px 22px;border-left:4px solid #2196F3;">
            <div style="font-size:11px;font-weight:800;letter-spacing:2px;color:#64B5F6;
                        text-transform:uppercase;margin-bottom:6px;">{k}</div>
            <div style="font-family:'Cairo',sans-serif;font-size:1.1rem;font-weight:800;
                        color:#FFFFFF;margin-bottom:4px;">{v['title']}</div>
            <div style="font-size:13px;color:#B0BEC5;line-height:1.5;font-style:italic;">{v['question']}</div>
        </div>
        """
    cards_html += '</div>'
    st.markdown(H(cards_html), unsafe_allow_html=True)

def render_solution():
    render_sidebar_brand()
    st.markdown(f"""
    <div class="hero-header">
        <div class="hero-logo-row">
            {logo_mark("hero-logo-mark")}
            <div>
                <div class="hero-logo-text">KAYFA</div>
                <div class="hero-logo-tag">Executive Action Plan</div>
            </div>
        </div>
        <h1 class="hero-title">Solution — Top Priorities to Reduce Attrition</h1>
        <p class="hero-subtitle">Top 3 priorities · 90-Day action plan · Projected impact</p>
    </div>
    """, unsafe_allow_html=True)

    render_kpis()

    st.markdown(H("""
    <div class="solution-section">

        <div class="exec-summary">
            <div class="exec-summary-title">📋 Executive Summary</div>
            <p class="exec-summary-text">
                With an attrition rate of <strong>47.5%</strong> — more than 3× the global benchmark —
                this organization faces a critical retention crisis. The data shows salary is <em>not</em> the root cause
                ($46 mean gap between leavers and stayers). The true drivers are
                <strong>work-life balance, lack of career growth, and absence of flexible work</strong>.
                The highest-risk segment is <strong>Entry-level on-site employees in their first 5 years</strong>,
                who leave at 69.3%. Addressing the Top 3 Priorities below is projected to reduce overall attrition by
                <strong>15–22 percentage points within 12 months</strong>.
            </p>
        </div>

        <div class="priorities-title">🎯 Top 3 Priorities To Reduce Attrition</div>

        <div class="priority-card p1">
            <div class="priority-number">⚠️ Priority #1 — Highest Impact</div>
            <div class="priority-title">Implement Flexible & Remote Work Policy</div>
            <span class="priority-impact">Expected Impact: −8 to −12 pts attrition</span>
            <p class="priority-desc">
                Remote work cuts attrition from ~53% (on-site) to ~24% (remote) — a 28-point gap across all company sizes.
                Entry-level on-site employees sit at 69.3% attrition; remote entry-level at 24.1%.
                This is the highest-ROI intervention in the entire dataset.
            </p>
            <div class="priority-actions-title">Actions</div>
            <ul class="priority-actions">
                <li>Immediately offer hybrid/remote options to all Entry-level employees</li>
                <li>Prioritize remote access for employees with commutes &gt; 40 km (currently 52.9% attrition)</li>
                <li>Publish a formal remote work policy with transparent eligibility within 30 days</li>
                <li>Pilot a 4-day work week for high-overtime teams to address burnout</li>
                <li>Enforce overtime caps with automatic HR escalation alerts</li>
                <li>Target Work-Life Balance scores 80%+ in Good or Excellent category</li>
            </ul>
        </div>

        <div class="priority-card p2">
            <div class="priority-number">📈 Priority #2 — High Impact</div>
            <div class="priority-title">Build Visible Career Growth Infrastructure</div>
            <span class="priority-impact">Expected Impact: −5 to −8 pts attrition</span>
            <p class="priority-desc">
                95% of employees have zero leadership opportunities. 83% have no innovation opportunities.
                Promotions show the strongest negative correlation with attrition (−0.081) of any variable measured.
                Employees in their first 5 years — when attrition peaks at 51–53% — leave because they see no path forward.
            </p>
            <div class="priority-actions-title">Actions</div>
            <ul class="priority-actions">
                <li>Launch a formal internal mobility program with role transparency</li>
                <li>Require quarterly documented career-path conversations between every manager and direct report</li>
                <li>Allocate 10–20% of work hours to innovation projects for non-senior employees</li>
                <li>Open a Leadership Accelerator cohort for high-performers with &lt;5 years tenure</li>
                <li>Audit promotion timelines — ensure annual reviews have clear measurable criteria</li>
                <li>Fast-track High Performance + Low Satisfaction employees before they resign</li>
            </ul>
        </div>

        <div class="priority-card p3">
            <div class="priority-number">🎯 Priority #3 — Medium-High Impact</div>
            <div class="priority-title">Strengthen Early-Tenure & Onboarding Experience</div>
            <span class="priority-impact">Expected Impact: −4 to −6 pts attrition</span>
            <p class="priority-desc">
                The first 5 years are the most dangerous window — attrition peaks at 51–53%.
                Young employees (18–25) leave at 53.1%. Single employees leave at 62–72%.
                These cohorts need targeted retention programs in their first 18 months.
            </p>
            <div class="priority-actions-title">Actions</div>
            <ul class="priority-actions">
                <li>Redesign onboarding into a 12-month structured mentorship program</li>
                <li>Assign senior "retention champions" to every new hire for the first year</li>
                <li>Run 30/60/90-day stay interviews — not exit interviews — for all new hires</li>
                <li>Build community programs for single employees (social events, peer groups)</li>
                <li>Deploy an attrition risk score using Distance, Tenure, Job Level, WLB, Overtime</li>
                <li>Launch female-employee focus groups to surface unique 53%-attrition barriers</li>
            </ul>
        </div>

        <div class="action-plan">
            <div class="action-plan-title">📅 90-Day Action Plan</div>

            <div class="phase-row">
                <span class="phase-badge">Days 1–30</span>
                <div class="phase-content">
                    <strong>Immediate Wins:</strong> Announce hybrid/remote pilot for Entry-level teams.
                    Identify top 500 High-Performance + Low-Satisfaction employees and schedule 1:1 retention conversations.
                    Freeze overtime in departments exceeding 35% overtime penetration.
                    Launch stay-interview program for all employees with &lt;2 years tenure.
                </div>
            </div>

            <div class="phase-row">
                <span class="phase-badge">Days 31–60</span>
                <div class="phase-content">
                    <strong>Policy & Program Launch:</strong> Publish formal remote work eligibility policy.
                    Roll out quarterly career-path conversation framework to all managers (training required).
                    Open first cohort of Leadership Accelerator. Establish monthly attrition dashboarding cadence
                    for C-suite review. Introduce overtime cap policy with automated HR alerts.
                </div>
            </div>

            <div class="phase-row">
                <span class="phase-badge">Days 61–90</span>
                <div class="phase-content">
                    <strong>Measurement & Scale:</strong> Measure 30-day impact on Work-Life Balance survey scores.
                    Run focus groups with female and single employees on retention barriers.
                    Deploy attrition risk scoring model (Distance, Tenure, Job Level, WLB, Overtime).
                    Present first retention KPI report to C-suite: target 5% reduction in monthly departures within 90 days.
                </div>
            </div>
        </div>

        <div style="background:rgba(33,150,243,0.10); border:1px solid rgba(33,150,243,0.28);
                    border-radius:14px; padding:22px 26px; margin-top:24px;">
            <div style="font-family:'Cairo',sans-serif;font-size:12px;font-weight:800;
                        letter-spacing:2.5px;text-transform:uppercase;
                        color:#64B5F6;margin-bottom:12px;">✅ Recommended Action — Immediate</div>
            <p style="font-size:15px;color:#FFFFFF;line-height:1.85;margin:0;">
                The <strong style="color:#FFD54F;">highest-leverage decision</strong> available today requires no budget:
                approve remote/hybrid work for Entry-level employees. This single policy change is projected to reduce
                Entry-level attrition from <strong style="color:#EF9A9A;">69.3% → ~24%</strong>.
                Every month of delay costs the organization approximately
                <strong style="color:#FFD54F;">1,400+ additional departures</strong> from this cohort alone.
                Pair this with a mandatory career-path conversation program, and the combined impact on total attrition
                rate could reach <strong style="color:#81C784;">−15 percentage points within 12 months</strong>.
            </p>
        </div>
    </div>
    """), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  NAVIGATION — version-safe: st.navigation (≥1.36) or st.radio fallback
# ══════════════════════════════════════════════════════════════════════════════
import streamlit as _st_version_check
_ST_VER = tuple(int(x) for x in _st_version_check.__version__.split(".")[:2])
_HAS_NAV = _ST_VER >= (1, 36)

if _HAS_NAV:
    # Named wrapper functions required — lambdas share __name__="<lambda>",
    # causing duplicate url_path hashes and a StreamlitAPIException.
    def _page_home():        render_home()
    def _page_q1():         render_question_page("Q1")
    def _page_q2():         render_question_page("Q2")
    def _page_q3():         render_question_page("Q3")
    def _page_q4():         render_question_page("Q4")
    def _page_q5():         render_question_page("Q5")
    def _page_q6():         render_question_page("Q6")
    def _page_q7():         render_question_page("Q7")
    def _page_q8():         render_question_page("Q8")
    def _page_q9():         render_question_page("Q9")
    def _page_q10():        render_question_page("Q10")
    def _page_solution():   render_solution()

    _q_funcs = [_page_q1, _page_q2, _page_q3, _page_q4, _page_q5,
                _page_q6, _page_q7, _page_q8, _page_q9, _page_q10]

    _pages = [st.Page(_page_home, title="Home", icon="🏠", default=True)]
    for (_k, _v), _fn in zip(QUESTIONS.items(), _q_funcs):
        _pages.append(st.Page(_fn, title=f"{_k} – {_v['title']}", icon="📊"))
    _pages.append(st.Page(_page_solution, title="Solution", icon="🚀"))

    pg = st.navigation(_pages, position="sidebar", expanded=True)
    pg.run()
else:
    # ── Fallback: native st.radio sidebar nav (works on all Streamlit versions) ──
    render_sidebar_brand()
    with st.sidebar:
        st.markdown('<div class="sidebar-section-title">📋 Analysis Questions</div>',
                    unsafe_allow_html=True)
        _nav_options = ["🏠 Home"] + [f"{k} – {v['title']}" for k, v in QUESTIONS.items()] + ["🚀 Solution"]
        _selected = st.radio("Navigation", _nav_options, label_visibility="collapsed", index=0)

    if _selected == "🏠 Home":
        render_home()
    elif _selected == "🚀 Solution":
        render_solution()
    else:
        _q_key = _selected.split(" – ")[0]
        if _q_key in QUESTIONS:
            render_question_page(_q_key)
        else:
            render_home()
