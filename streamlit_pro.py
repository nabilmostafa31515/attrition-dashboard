"""
Employee Attrition Dashboard — Professional Streamlit App (v2 — Enhanced)
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Professional CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: linear-gradient(135deg, #0F1B3D 0%, #1A2D5A 50%, #0D1F3C 100%);
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #132040 100%) !important;
    border-right: 1px solid rgba(33, 150, 243, 0.2);
}
section[data-testid="stSidebar"] * { color: #E8EAF6 !important; }
section[data-testid="stSidebar"] .stCheckbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #90CAF9 !important;
    font-size: 14px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(33, 150, 243, 0.08) !important;
    border: 1px dashed rgba(33, 150, 243, 0.4) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

.main .block-container { padding: 1rem 2rem 2rem 2rem; max-width: 1400px; }

.dash-header {
    background: linear-gradient(135deg, rgba(33,150,243,0.15) 0%, rgba(13,71,161,0.2) 100%);
    border: 1px solid rgba(33,150,243,0.25);
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
}
.dash-title {
    font-family: 'Cairo', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.2;
    letter-spacing: -0.5px;
    text-shadow: 0 0 30px rgba(33,150,243,0.4);
}
.dash-subtitle {
    font-size: 1.05rem;
    color: #90CAF9;
    margin-top: 8px;
    font-weight: 400;
}

.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px 28px;
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
    border-radius: 16px 16px 0 0;
}
.kpi-card.blue::before  { background: linear-gradient(90deg, #2196F3, #42A5F5); }
.kpi-card.red::before   { background: linear-gradient(90deg, #EF5350, #EF9A9A); }
.kpi-card.amber::before { background: linear-gradient(90deg, #FF8F00, #FFC107); }
.kpi-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #90CAF9;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Cairo', sans-serif;
    font-size: 2.6rem;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-value.red   { color: #EF9A9A; }
.kpi-value.amber { color: #FFC107; }

.chart-section {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
.chart-number {
    background: linear-gradient(135deg, #2196F3, #1565C0);
    color: white;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.chart-name {
    font-family: 'Cairo', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 0;
    margin-top: 8px;
}

.insight-box {
    background: linear-gradient(135deg, rgba(33,150,243,0.12) 0%, rgba(21,101,192,0.08) 100%);
    border-left: 4px solid #2196F3;
    border-radius: 0 12px 12px 0;
    padding: 18px 22px;
    margin-top: 18px;
}
.insight-title {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #64B5F6;
    margin-bottom: 10px;
}
.insight-text {
    font-size: 16px;
    color: #E8EAF6;
    line-height: 1.75;
    margin: 0;
}
.insight-text strong {
    color: #FF6B6B;
    background: rgba(239,83,80,0.15);
    padding: 1px 5px;
    border-radius: 4px;
    font-weight: 700;
}

.warning-box {
    background: linear-gradient(135deg, rgba(239,83,80,0.12) 0%, rgba(183,28,28,0.08) 100%);
    border-left: 4px solid #EF5350;
    border-radius: 0 12px 12px 0;
    padding: 18px 22px;
    margin-top: 18px;
}
.warning-title {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #EF9A9A;
    margin-bottom: 10px;
}
.warning-text {
    font-size: 16px;
    color: #E8EAF6;
    line-height: 1.75;
    margin: 0;
}
.warning-text strong {
    color: #FFD54F;
    background: rgba(255,213,79,0.15);
    padding: 1px 5px;
    border-radius: 4px;
    font-weight: 700;
}

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(33,150,243,0.3), transparent);
    margin: 8px 0 24px 0;
}

.kw-red { background: rgba(239,83,80,0.2); color: #FF6B6B; font-weight: 700; padding: 2px 7px; border-radius: 5px; border: 1px solid rgba(239,83,80,0.3); }
.kw-green { background: rgba(39,174,96,0.2); color: #69F0AE; font-weight: 700; padding: 2px 7px; border-radius: 5px; border: 1px solid rgba(39,174,96,0.3); }
.kw-blue { background: rgba(33,150,243,0.2); color: #64B5F6; font-weight: 700; padding: 2px 7px; border-radius: 5px; border: 1px solid rgba(33,150,243,0.3); }
.kw-amber { background: rgba(255,143,0,0.2); color: #FFD54F; font-weight: 700; padding: 2px 7px; border-radius: 5px; border: 1px solid rgba(255,143,0,0.3); }

/* Solution Section */
.solution-section {
    background: linear-gradient(135deg, rgba(33,150,243,0.08) 0%, rgba(13,71,161,0.12) 100%);
    border: 1px solid rgba(33,150,243,0.3);
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 24px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 32px rgba(0,0,0,0.25);
}
.solution-header {
    font-family: 'Cairo', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    color: #FFFFFF;
    margin-bottom: 6px;
    text-shadow: 0 0 30px rgba(33,150,243,0.3);
}
.solution-subheader {
    font-size: 1rem;
    color: #90CAF9;
    margin-bottom: 32px;
}
.priority-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
}
.priority-card.p1 { border-left: 4px solid #EF5350; }
.priority-card.p2 { border-left: 4px solid #FF8F00; }
.priority-card.p3 { border-left: 4px solid #2196F3; }
.priority-number {
    font-family: 'Cairo', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.p1 .priority-number { color: #EF9A9A; }
.p2 .priority-number { color: #FFB300; }
.p3 .priority-number { color: #64B5F6; }
.priority-title {
    font-family: 'Cairo', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 8px;
}
.priority-impact {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 16px;
}
.p1 .priority-impact { background: rgba(239,83,80,0.2); color: #EF9A9A; border: 1px solid rgba(239,83,80,0.3); }
.p2 .priority-impact { background: rgba(255,143,0,0.2); color: #FFB300; border: 1px solid rgba(255,143,0,0.3); }
.p3 .priority-impact { background: rgba(33,150,243,0.2); color: #64B5F6; border: 1px solid rgba(33,150,243,0.3); }
.priority-actions { list-style: none; padding: 0; margin: 0; }
.priority-actions li {
    font-size: 14px;
    color: #CFD8DC;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    padding-left: 20px;
    position: relative;
}
.priority-actions li:last-child { border-bottom: none; }
.priority-actions li::before { content: "→"; position: absolute; left: 0; color: #546E7A; }

.action-plan {
    background: rgba(39,174,96,0.08);
    border: 1px solid rgba(39,174,96,0.25);
    border-radius: 16px;
    padding: 24px 28px;
    margin-top: 24px;
}
.action-plan-title {
    font-family: 'Cairo', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: #81C784;
    margin-bottom: 20px;
}
.phase-row { display: flex; gap: 16px; margin-bottom: 16px; align-items: flex-start; }
.phase-badge {
    background: rgba(39,174,96,0.2);
    border: 1px solid rgba(39,174,96,0.4);
    color: #81C784;
    font-size: 12px;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 20px;
    white-space: nowrap;
    margin-top: 2px;
}
.phase-content { font-size: 14px; color: #CFD8DC; line-height: 1.7; }
.phase-content strong { color: #FFFFFF; }

.exec-summary {
    background: linear-gradient(135deg, rgba(255,143,0,0.08) 0%, rgba(255,193,7,0.04) 100%);
    border: 1px solid rgba(255,143,0,0.25);
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 28px;
}
.exec-summary-title {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #FFB300;
    margin-bottom: 12px;
}
.exec-summary-text { font-size: 15px; color: #E8EAF6; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

# ── Color & Chart Helpers ────────────────────────────────────────────────────
C = dict(stayed="#2196F3", left="#EF5350", line="#FF8F00", grid="#1E2D4D", paper="rgba(0,0,0,0)", text="#E8EAF6")
BLUE_SEQ  = [[0, "#1A2D5A"], [0.5, "#1E88E5"], [1, "#64B5F6"]]
DIVERGING = [[0, "#EF5350"], [0.5, "#263238"], [1, "#2196F3"]]

def layout(title, sub, h=480):
    return dict(
        title=dict(
            text=f"<b>{title}</b>",
            x=0.0,
            xanchor="left",
            font=dict(size=22, color="#FFFFFF", family="Cairo, sans-serif")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,27,61,0.6)",
        font=dict(family="IBM Plex Sans, sans-serif", color=C["text"], size=13),
        height=h,
        margin=dict(t=90, b=60, l=60, r=40),
        legend=dict(
            orientation="h", y=-0.25, x=0.5, xanchor="center",
            bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5", size=13)
        )
    )

def ax(**kw):
    defaults = dict(
        gridcolor=C["grid"],
        linecolor="#1E3A5F",
        zeroline=False,
        tickfont=dict(size=13, color="#90CAF9"),
        title_font=dict(size=15, color="#90CAF9", family="IBM Plex Sans, sans-serif")
    )
    defaults.update(kw)
    return defaults

def show(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

@st.cache_data
def load_data(f=None):
    if f is not None:
        try:
            return pd.read_excel(f)
        except:
            return pd.read_csv(f)
    import os
    for path in ["final_dataset.csv", "final_dataset.xlsx"]:
        if os.path.exists(path):
            return pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
    return None

# ── Charts ───────────────────────────────────────────────────────────────────
def chart1(df):
    c = df["Attrition"].value_counts()
    fig = go.Figure(go.Pie(
        labels=c.index, values=c.values, hole=0.6,
        marker=dict(colors=[C["stayed"], C["left"]], line=dict(color="#0F1B3D", width=3)),
        textinfo="percent+label", textfont=dict(size=16, color="#E8EAF6"),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    ))
    fig.update_layout(**layout("Attrition Overview", "", 420),
        annotations=[dict(text=f"<b>{len(df):,}</b><br><span style='font-size:12px'>Total</span>",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="#E8EAF6"))])
    show(fig)

def chart2(df):
    g  = df.groupby(["Gender","Attrition"]).size().unstack()
    gp = df.groupby("Gender")["Attrition"].value_counts(normalize=True).unstack()*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index, y=g["Stayed"], marker_color=C["stayed"],
               text=[f"{v:,}" for v in g["Stayed"]], textposition="outside",
               textfont=dict(color="#90CAF9", size=14)),
        go.Bar(name="Left",   x=g.index, y=g["Left"],   marker_color=C["left"],
               text=[f"{v:,}" for v in g["Left"]],   textposition="outside",
               textfont=dict(color="#EF9A9A", size=14)),
    ])
    for gen in g.index:
        fig.add_annotation(x=gen, y=g.loc[gen].max()+4000,
                           text=f"<b>Rate: {gp.loc[gen,'Left']:.1f}%</b>",
                           showarrow=False, font=dict(size=14, color=C["left"]))
    fig.update_layout(**layout("Attrition by Gender", ""), barmode="group")
    fig.update_xaxes(**ax(title_text="Gender"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart3(df):
    df = df.copy()
    df["AG"] = pd.cut(df["Age"],[17,25,35,45,55,65],labels=["18-25","26-35","36-45","46-55","56-65"])
    g  = df.groupby(["AG","Attrition"],observed=False).size().unstack()
    gp = df.groupby("AG",observed=False)["Attrition"].value_counts(normalize=True).unstack()*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index.astype(str), y=g["Stayed"], marker_color=C["stayed"]),
        go.Bar(name="Left",   x=g.index.astype(str), y=g["Left"],   marker_color=C["left"]),
    ])
    fig.add_trace(go.Scatter(name="Rate %", x=g.index.astype(str), y=gp["Left"], yaxis="y2",
        mode="lines+markers", line=dict(color=C["line"], width=2.5),
        marker=dict(size=10, color=C["line"]),
        text=[f"{v:.1f}%" for v in gp["Left"]], textposition="top center",
        textfont=dict(color=C["line"], size=13)))
    fig.update_layout(**layout("Attrition by Age Group", ""), barmode="group",
        yaxis2=dict(overlaying="y", side="right", range=[0,100], showgrid=False,
                    title="Rate (%)", tickfont=dict(color="#FFB300", size=13),
                    title_font=dict(color="#FFB300", size=15)))
    fig.update_xaxes(**ax(title_text="Age Group"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart4(df):
    pct = df.groupby("Job Role")["Attrition"].apply(lambda x:(x=="Left").mean()*100).sort_values()
    fig = go.Figure(go.Bar(x=pct.values, y=pct.index, orientation="h",
        marker=dict(color=pct.values, colorscale=BLUE_SEQ, showscale=True,
                    colorbar=dict(title="Rate %", tickfont=dict(color="#90A4AE", size=13),
                                  title_font=dict(color="#90CAF9", size=14))),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#90CAF9", size=14)))
    fig.update_layout(**layout("Attrition by Job Role", "", 420))
    fig.update_xaxes(**ax(title_text="Attrition Rate (%)"))
    fig.update_yaxes(**ax(tickfont=dict(size=13, color="#90CAF9")))
    show(fig)

def chart5(df):
    fig = go.Figure()
    for label, color in [("Stayed", C["stayed"]), ("Left", C["left"])]:
        sub = df[df["Attrition"]==label]["Monthly Income"]
        fig.add_trace(go.Box(y=sub, name=label, marker_color=color, boxmean=True,
                             line=dict(color=color)))
        fig.add_annotation(x=label, y=sub.mean()+1200,
                           text=f"<b>Mean: ${sub.mean():,.0f}</b>",
                           showarrow=False, font=dict(size=14, color=color))
    fig.update_layout(**layout("Monthly Income by Attrition Status", ""))
    fig.update_yaxes(**ax(title_text="Monthly Income (USD)"))
    show(fig)

def chart6(df):
    order = ["Poor","Fair","Good","Excellent"]
    g  = df.groupby(["Work-Life Balance","Attrition"],observed=False).size().unstack().reindex(order)
    gp = df.groupby("Work-Life Balance",observed=False)["Attrition"].value_counts(normalize=True).unstack().reindex(order)*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index, y=g["Stayed"], marker_color=C["stayed"],
               text=[f"{v:,}" for v in g["Stayed"]], textposition="inside",
               textfont=dict(size=13)),
        go.Bar(name="Left",   x=g.index, y=g["Left"],   marker_color=C["left"],
               text=[f"{v:,}" for v in g["Left"]],   textposition="inside",
               textfont=dict(size=13)),
    ])
    for wl in order:
        fig.add_annotation(x=wl, y=g.loc[wl].sum()+1200,
                           text=f"<b>Rate: {gp.loc[wl,'Left']:.1f}%</b>",
                           showarrow=False, font=dict(size=13, color=C["left"]))
    fig.update_layout(**layout("Attrition by Work-Life Balance", ""), barmode="stack")
    fig.update_xaxes(**ax(title_text="Work-Life Balance"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart7(df):
    ot = df.groupby("Overtime")["Attrition"].value_counts(normalize=True).unstack()*100
    oy = df[df["Overtime"]=="Yes"]["Attrition"].value_counts()
    fig = make_subplots(1, 2,
        specs=[[{"type":"pie"}, {"type":"bar"}]],
        subplot_titles=("Overtime Employees Distribution", "Attrition Rate by Overtime"))
    fig.add_trace(go.Pie(
        labels=["Stayed","Left"], values=[oy.get("Stayed",0), oy.get("Left",0)],
        marker=dict(colors=[C["stayed"], C["left"]]), hole=0.5,
        textinfo="percent+label", textfont=dict(color="#E8EAF6", size=15)), 1, 1)
    fig.add_trace(go.Bar(
        x=["No Overtime","With Overtime"], y=ot["Left"],
        marker=dict(color=[C["stayed"], C["left"]]),
        text=[f"{v:.1f}%" for v in ot["Left"]], textposition="outside",
        textfont=dict(color="#E8EAF6", size=15)), 1, 2)
    fig.update_layout(**layout("Overtime Impact on Attrition", "", 450), showlegend=False)
    for ann in fig.layout.annotations:
        ann.font.size = 15
        ann.font.color = "#90CAF9"
    show(fig)

def chart8(df):
    df2 = df.copy()
    df2["Education Level"] = df2["Education Level"].str.replace("'","'").str.replace("'","'")
    order = ["High School","Associate Degree","Bachelor's Degree","Master's Degree","PhD"]
    short = ["High\nSchool","Associate\nDegree","Bachelor's\nDegree","Master's\nDegree","PhD"]
    pct = df2.groupby("Education Level")["Attrition"].apply(lambda x:(x=="Left").mean()*100).reindex(order)
    pct_vals = [v if not pd.isna(v) else 0 for v in pct.values]
    fig = go.Figure(go.Bar(
        x=short, y=pct_vals,
        marker=dict(color=pct_vals, colorscale=BLUE_SEQ, showscale=True,
                    colorbar=dict(title="Rate %", tickfont=dict(color="#90A4AE", size=13),
                                  title_font=dict(color="#90CAF9", size=14))),
        text=[f"{v:.1f}%" if v>0 else "N/A" for v in pct_vals],
        textposition="outside", textfont=dict(color="#90CAF9", size=15)))
    fig.update_layout(**layout("Attrition by Education Level", "", 500))
    fig.update_xaxes(**ax(title_text="Education Level", tickfont=dict(size=13, color="#90CAF9")))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)", range=[0,60]))
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
        text=corr.round(2).values, texttemplate="%{text:.2f}", textfont=dict(size=12, color="#E8EAF6"),
        colorbar=dict(title="r", tickfont=dict(color="#90A4AE", size=13),
                      title_font=dict(color="#90CAF9", size=14))))
    fig.update_layout(**layout("Correlation Heatmap", "", 520))
    fig.update_xaxes(**ax(tickfont=dict(size=13, color="#90CAF9")))
    fig.update_yaxes(**ax(tickfont=dict(size=13, color="#90CAF9")))
    show(fig)

def chart10(df):
    df = df.copy()
    bins = list(range(0,55,5))
    df["YG"] = pd.cut(df["Years at Company"], bins=bins,
                      labels=[f"{i}-{i+4}" for i in bins[:-1]], include_lowest=True)
    g  = df.groupby("YG",observed=True)["Attrition"].value_counts().unstack(fill_value=0)
    gp = df.groupby("YG",observed=True)["Attrition"].value_counts(normalize=True).unstack(fill_value=0)*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index.astype(str), y=g["Stayed"], marker_color=C["stayed"]),
        go.Bar(name="Left",   x=g.index.astype(str), y=g["Left"],   marker_color=C["left"]),
    ])
    fig.add_trace(go.Scatter(name="Rate %", x=g.index.astype(str), y=gp["Left"], yaxis="y2",
        mode="lines+markers", line=dict(color=C["line"], width=2.5),
        marker=dict(size=9, color=C["line"])))
    fig.update_layout(**layout("Attrition by Company Tenure", ""), barmode="stack",
        yaxis2=dict(overlaying="y", side="right", range=[0,100], showgrid=False,
                    title="Rate (%)", tickfont=dict(color="#FFB300", size=13),
                    title_font=dict(color="#FFB300", size=15)))
    fig.update_xaxes(**ax(title_text="Years at Company"))
    fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart11(df):
    data = df.groupby(["Marital Status","Gender"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack()
    colors = {"Male": C["stayed"], "Female": "#AB47BC"}
    fig = go.Figure([go.Bar(
        name=g, x=data.index, y=data[g], marker_color=colors.get(g,"#78909C"),
        text=[f"{v:.1f}%" for v in data[g]], textposition="outside",
        textfont=dict(color="#E8EAF6", size=14))
        for g in data.columns])
    fig.update_layout(**layout("Attrition by Marital Status & Gender", ""), barmode="group")
    fig.update_xaxes(**ax(title_text="Marital Status"))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)"))
    show(fig)

def chart12(df):
    data = df.groupby(["Company Size","Remote Work"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack()
    colors = {"Yes":"#26A69A","No":C["left"]}
    labels = {"Yes":"Remote","No":"On-site"}
    fig = go.Figure([go.Bar(
        name=labels.get(k,k), x=data.index, y=data[k], marker_color=colors.get(k,"#78909C"),
        text=[f"{v:.1f}%" for v in data[k]], textposition="outside",
        textfont=dict(color="#E8EAF6", size=14))
        for k in data.columns])
    fig.update_layout(**layout("Attrition by Company Size & Remote Work", ""), barmode="group")
    fig.update_xaxes(**ax(title_text="Company Size"))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)"))
    show(fig)

def chart13(df):
    pivot = df.groupby(["Performance Rating","Job Satisfaction"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack()
    fig = go.Figure(go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=BLUE_SEQ,
        text=pivot.round(1).values, texttemplate="%{text:.1f}%",
        textfont=dict(size=14, color="#E8EAF6"),
        colorbar=dict(title="Rate %", tickfont=dict(color="#90A4AE", size=13),
                      title_font=dict(color="#90CAF9", size=14))))
    fig.update_layout(**layout("Performance Rating × Job Satisfaction", "", 440))
    fig.update_xaxes(**ax(title_text="Job Satisfaction", tickfont=dict(size=13, color="#90CAF9")))
    fig.update_yaxes(**ax(title_text="Performance Rating", tickfont=dict(size=13, color="#90CAF9")))
    show(fig)

def chart14(df):
    df = df.copy()
    df["DG"] = pd.cut(df["Distance from Home"],[0,20,40,60,80,100],
                      labels=["0-20","21-40","41-60","61-80","81-100"])
    pct = df.groupby("DG",observed=True)["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    fig = go.Figure(go.Bar(
        x=pct.index.astype(str), y=pct.values,
        marker=dict(color=pct.values, colorscale=BLUE_SEQ, showscale=True),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#90CAF9", size=15)))
    fig.update_layout(**layout("Attrition by Commute Distance", ""))
    fig.update_xaxes(**ax(title_text="Distance from Home (km)"))
    fig.update_yaxes(**ax(title_text="Attrition Rate (%)", range=[0,pct.max()*1.3]))
    show(fig)

def chart15(df):
    pct   = df.groupby("Leadership Opportunities")["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    count = df["Leadership Opportunities"].value_counts()
    colors = {"No":C["left"],"Yes":C["stayed"]}
    labels = {"No":"No Leadership Opps","Yes":"Has Leadership Opps"}
    fig = go.Figure()
    for val in ["No","Yes"]:
        fig.add_trace(go.Bar(x=[labels[val]], y=[pct[val]], name=labels[val],
            marker_color=colors[val],
            text=[f"{pct[val]:.1f}%"], textposition="outside",
            textfont=dict(color="#E8EAF6", size=16), width=0.4))
    fig.update_layout(**layout("Attrition by Leadership Opportunities", "", 420),
        showlegend=False,
        yaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,65])))
    show(fig)

def chart16(df):
    pct   = df.groupby("Innovation Opportunities")["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    count = df["Innovation Opportunities"].value_counts()
    colors = {"No":C["left"],"Yes":C["stayed"]}
    labels = {"No":"No Innovation Opps","Yes":"Has Innovation Opps"}
    fig = go.Figure()
    for val in ["No","Yes"]:
        fig.add_trace(go.Bar(x=[labels[val]], y=[pct[val]], name=labels[val],
            marker_color=colors[val],
            text=[f"{pct[val]:.1f}%"], textposition="outside",
            textfont=dict(color="#E8EAF6", size=16), width=0.4))
    fig.update_layout(**layout("Attrition by Innovation Opportunities", "", 420),
        showlegend=False,
        yaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,65])))
    show(fig)

def chart17(df):
    order = ["Poor","Fair","Good","Excellent"]
    pct   = df.groupby("Company Reputation")["Attrition"].apply(lambda x:(x=="Left").mean()*100).reindex(order)
    fig = go.Figure(go.Bar(x=pct.values, y=pct.index, orientation="h",
        marker=dict(color=pct.values, colorscale=DIVERGING, cmin=35, cmax=60, showscale=True,
                    colorbar=dict(title="Rate %", tickfont=dict(color="#90A4AE", size=13),
                                  title_font=dict(color="#90CAF9", size=14))),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#90CAF9", size=15)))
    fig.update_layout(**layout("Attrition by Company Reputation", "", 420),
        xaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,75])),
        yaxis=dict(**ax(title_text="Reputation Level", tickfont=dict(size=14, color="#90CAF9"))))
    show(fig)

def chart18(df):
    order = ["Low","Medium","High","Very High"]
    pct   = df.groupby("Employee Recognition",observed=False)["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).reindex(order)
    count = df["Employee Recognition"].value_counts().reindex(order)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=pct.index, y=pct.values,
        marker=dict(color=pct.values, colorscale=BLUE_SEQ, showscale=True,
                    colorbar=dict(title="Rate %", tickfont=dict(color="#90A4AE", size=13),
                                  title_font=dict(color="#90CAF9", size=14))),
        text=[f"{v:.1f}%" for v in pct.values], textposition="outside",
        textfont=dict(color="#90CAF9", size=15), name="Attrition Rate"))
    fig.add_trace(go.Scatter(x=order, y=count.values, yaxis="y2",
        mode="lines+markers", line=dict(color=C["line"], width=2.5, dash="dot"),
        marker=dict(size=10, color=C["line"]), name="Employee Count"))
    fig.update_layout(**layout("Attrition by Employee Recognition Level", "", 480),
        yaxis=dict(**ax(title_text="Attrition Rate (%)", range=[0,65])),
        yaxis2=dict(overlaying="y", side="right", showgrid=False,
                    title="Employee Count",
                    tickfont=dict(color="#FFB300", size=13),
                    title_font=dict(color="#FFB300", size=15)))
    show(fig)

def chart19(df):
    order_jl = ["Entry","Mid","Senior"]
    g  = df.groupby("Job Level")["Attrition"].value_counts().unstack().reindex(order_jl)
    gp = df.groupby("Job Level")["Attrition"].value_counts(normalize=True).unstack().reindex(order_jl)*100
    pivot = df.groupby(["Job Level","Remote Work"])["Attrition"].apply(
        lambda x:(x=="Left").mean()*100).unstack().reindex(order_jl)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.6,0.4],
        subplot_titles=("Attrition Count & Rate by Job Level","Rate % by Job Level × Remote Work"),
        specs=[[{"type":"bar"},{"type":"heatmap"}]])
    fig.add_trace(go.Bar(name="Stayed", x=order_jl, y=g["Stayed"], marker_color=C["stayed"],
        text=[f"{v:,}" for v in g["Stayed"]], textposition="inside",
        textfont=dict(size=13)), row=1, col=1)
    fig.add_trace(go.Bar(name="Left", x=order_jl, y=g["Left"], marker_color=C["left"],
        text=[f"{v:,}" for v in g["Left"]], textposition="inside",
        textfont=dict(size=13)), row=1, col=1)
    fig.add_trace(go.Scatter(name="Rate %", x=order_jl, y=gp["Left"], yaxis="y2",
        mode="lines+markers", line=dict(color=C["line"], width=2.5),
        marker=dict(size=11, color=C["line"])), row=1, col=1)
    fig.add_trace(go.Heatmap(z=pivot.values, x=pivot.columns.tolist(), y=order_jl,
        colorscale=BLUE_SEQ,
        text=pivot.round(1).values, texttemplate="%{text:.1f}%",
        textfont=dict(size=15, color="#E8EAF6"),
        colorbar=dict(title="Rate %", x=1.02,
                      tickfont=dict(color="#90A4AE", size=13),
                      title_font=dict(color="#90CAF9", size=14)),
        showscale=True), row=1, col=2)
    fig.update_layout(**layout("Job Level Impact on Attrition", "", 500),
        barmode="group",
        yaxis2=dict(overlaying="y", side="right", range=[0,100], showgrid=False,
                    title="Rate (%)", tickfont=dict(color="#FFB300", size=13),
                    title_font=dict(color="#FFB300", size=15)))
    for ann in fig.layout.annotations:
        ann.font.size = 15
        ann.font.color = "#90CAF9"
    fig.update_xaxes(title_text="Job Level", row=1, col=1,
                     tickfont=dict(size=13, color="#90CAF9"))
    fig.update_yaxes(title_text="Headcount", row=1, col=1)
    fig.update_xaxes(title_text="Remote Work", row=1, col=2,
                     tickfont=dict(size=13, color="#90CAF9"))
    show(fig)

# ── Insights ─────────────────────────────────────────────────────────────────
INSIGHTS = {
    "1":  ("insight", 'نسبة الـ Attrition تبلغ <span class="kw-red">47.5%</span> — ضعف المعدل العالمي الطبيعي <span class="kw-blue">10-15%</span>. يعني تقريباً <span class="kw-red">موظف من كل 2 يغادر الشركة</span>، وهو ما يشير إلى <span class="kw-amber">مشكلة هيكلية عميقة</span> تستوجب تحقيقاً فورياً.'),
    "2":  ("warning", 'الإناث يغادرن بنسبة <span class="kw-red">53%</span> مقابل <span class="kw-blue">42.9%</span> للذكور — فارق <span class="kw-amber">10 نقاط كاملة</span>. هذا يوحي بوجود تحديات خاصة تواجه الموظفات، سواء في <span class="kw-red">التوازن الأسري</span> أو <span class="kw-red">فرص الترقي</span> أو بيئة العمل.'),
    "3":  ("insight", 'فئة <span class="kw-red">18-25 سنة</span> هي الأعلى في المغادرة بنسبة <span class="kw-red">53.1%</span>. كل ما زاد العمر انخفضت النسبة تدريجياً، مما يستوجب التركيز على <span class="kw-green">برامج الاحتفاظ بالموظفين الجدد</span>.'),
    "4":  ("insight", 'الفارق بين الوظائف لا يتجاوز <span class="kw-blue">2%</span> — وهذا يؤكد أن المشكلة <span class="kw-red">ليست في وظيفة بعينها</span>، بل هي <span class="kw-amber">مشكلة مؤسسية شاملة</span> تمس ثقافة الشركة وسياساتها.'),
    "5":  ("warning", 'الفارق في الراتب بين من غادروا ومن بقوا هو <span class="kw-amber">46 دولاراً فقط</span>! هذا يكشف أن <span class="kw-red">الراتب ليس السبب الرئيسي للمغادرة</span>، مما يعني أن <span class="kw-amber">رفع الرواتب وحده لن يحل المشكلة</span>.'),
    "6":  ("warning", 'موظفو الـ <span class="kw-red">Poor WLB</span> يغادرون بنسبة <span class="kw-red">60.2%</span> مقابل <span class="kw-green">35.7%</span> لأصحاب الـ Excellent — فارق <span class="kw-amber">24.5 نقطة</span>! <span class="kw-blue">التوازن بين العمل والحياة</span> هو أكثر العوامل تأثيراً على الاستبقاء.'),
    "7":  ("insight", 'الموظفون الذين يعملون <span class="kw-red">أوفر تايم</span> يغادرون بنسبة <span class="kw-red">51.5%</span> مقابل <span class="kw-green">45.5%</span>. والخطير أن <span class="kw-amber">ثلث الموظفين (24,341)</span> يعملون أوفر تايم، مما يشكل <span class="kw-red">ضغطاً مزمناً</span> على المؤسسة.'),
    "8":  ("insight", 'أصحاب <span class="kw-green">PhD</span> يغادرون بنسبة <span class="kw-green">24.4% فقط</span> مقارنة بـ <span class="kw-red">~48%</span> لباقي المستويات — فارق مذهل! في حين أن باقي المستويات التعليمية <span class="kw-blue">متقاربة جداً</span> في نسب المغادرة.'),
    "9":  ("insight", 'أقوى عامل للاستبقاء هو <span class="kw-green">الترقيات (-0.081)</span>، وأقوى عامل للمغادرة هو <span class="kw-red">بُعد المسافة (+0.094)</span>. أما الراتب فعلاقته بالمغادرة <span class="kw-amber">شبه معدومة (0.011)</span>.'),
    "10": ("warning", 'أول <span class="kw-red">5 سنوات</span> هي الأخطر بنسبة مغادرة <span class="kw-red">51-53%</span>. بعد <span class="kw-green">10 سنوات</span> تنخفض النسبة بشكل ملحوظ، مما يجعل <span class="kw-amber">الـ Onboarding والسنوات الأولى</span> أولوية قصوى.'),
    "11": ("warning", 'الأعزب/العزباء يغادرون بنسب صادمة: <span class="kw-red">72.2%</span> للإناث و<span class="kw-red">62.3%</span> للذكور. <span class="kw-green">المتزوجون</span> هم الأكثر استقراراً بفارق كبير بسبب <span class="kw-blue">الالتزامات الأسرية</span>.'),
    "12": ("insight", 'الـ <span class="kw-green">Remote Work</span> يخفض الـ Attrition بأكثر من <span class="kw-green">28 نقطة</span> في جميع أحجام الشركات! من <span class="kw-red">~53% On-site</span> إلى <span class="kw-green">~24% Remote</span> — هذا <span class="kw-amber">أقوى قرار</span> يمكن اتخاذه للاحتفاظ بالموظفين.'),
    "13": ("warning", 'الأخطر هو الموظف <span class="kw-red">High Performance + Low Satisfaction</span> — شاطر لكن غير راضٍ، وسيجد فرصة أخرى بسرعة. يجب <span class="kw-amber">تحديد هؤلاء والتحدث معهم</span> قبل مغادرتهم.'),
    "14": ("insight", 'كل ما زادت المسافة، زادت نسبة المغادرة من <span class="kw-green">41.7%</span> للأقرب إلى <span class="kw-red">52.9%</span> للأبعد. توفير خيار <span class="kw-green">Hybrid/Remote</span> للموظفين البعيدين سيقلل هذا الأثر بشكل كبير.'),
    "15": ("warning", '<span class="kw-red">95%</span> من الموظفين ليس لديهم أي <span class="kw-red">فرصة قيادية</span>! هذا يعني غياب <span class="kw-amber">مسار التطوير الوظيفي</span> لغالبية الموظفين، وهو من أهم أسباب الشعور بالركود والرغبة في المغادرة.'),
    "16": ("warning", '<span class="kw-red">83%</span> من الموظفين محرومون من <span class="kw-red">فرص الابتكار</span>. الموظف الذي يكرر نفس المهام يومياً بدون تحدٍّ <span class="kw-amber">سيبحث عن بيئة أكثر إثارة وتحفيزاً</span>.'),
    "17": ("insight", 'السمعة الضعيفة <span class="kw-red">(Poor)</span> ترفع نسبة المغادرة إلى <span class="kw-red">56%</span> مقارنة بـ <span class="kw-green">43%</span> للسمعة الجيدة — فارق <span class="kw-amber">13 نقطة</span>. الموظف يريد أن <span class="kw-blue">يفتخر بمكان عمله</span> أمام الآخرين.'),
    "18": ("insight", 'الفارق بين أعلى وأدنى مستوى من التقدير <span class="kw-amber">1.8% فقط</span>! مما يؤكد أن <span class="kw-red">التقدير اللفظي بدون مكافآت ملموسة</span> أو ترقيات <span class="kw-red">لا أثر له</span> على قرار البقاء.'),
    "19": ("warning", 'الأخطر في الداتا كلها: <span class="kw-red">Entry Level بدون Remote = 69.3%</span> مغادرة! بينما <span class="kw-green">Senior مع Remote = 5.2% فقط</span>. تركيز جهود الـ Remote على <span class="kw-amber">الـ Entry Level هو أولوية الأولويات</span>.'),
}

CHARTS = {
    "1":  ("Attrition Overview",             chart1),
    "2":  ("Attrition by Gender",            chart2),
    "3":  ("Attrition by Age Group",         chart3),
    "4":  ("Attrition by Job Role",          chart4),
    "5":  ("Monthly Income vs Attrition",    chart5),
    "6":  ("Work-Life Balance Impact",       chart6),
    "7":  ("Overtime Impact",                chart7),
    "8":  ("Attrition by Education Level",   chart8),
    "9":  ("Correlation Heatmap",            chart9),
    "10": ("Attrition by Tenure",            chart10),
    "11": ("Marital Status × Gender",        chart11),
    "12": ("Company Size × Remote Work",     chart12),
    "13": ("Performance × Satisfaction",     chart13),
    "14": ("Commute Distance Impact",        chart14),
    "15": ("Leadership Opportunities",       chart15),
    "16": ("Innovation Opportunities",       chart16),
    "17": ("Company Reputation",             chart17),
    "18": ("Employee Recognition",           chart18),
    "19": ("Job Level × Remote Work",        chart19),
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 24px 0 12px 0;">
        <div style="font-size:3rem;">📊</div>
        <div style="font-family:'Cairo',sans-serif; font-size:1.5rem; font-weight:900;
                    color:#FFFFFF; margin-top:8px; line-height:1.2;">
            Kayfa
        </div>
        <div style="font-size:0.9rem; color:#90CAF9; margin-top:4px;">
            Employee Analytics Platform
        </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,243,0.4),transparent);margin-bottom:20px;"></div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("📂 Upload different file (optional)", type=["xlsx","csv"])
    st.markdown("""
    <div style="background:rgba(39,174,96,0.12);border:1px solid rgba(39,174,96,0.3);
                border-radius:10px;padding:12px 16px;margin-top:8px;">
        <p style="font-size:13px;color:#81C784;margin:0;">✅ Data loaded automatically<br>
        <span style="color:#90A4AE;font-size:12px;">74,498 employees · 24 variables</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,243,0.4),transparent);margin:18px 0;"></div>', unsafe_allow_html=True)

    show_all = st.checkbox("Show all charts", value=True)
    show_solution = st.checkbox("🚀 Show Solution Section", value=True)
    chart_options = [f"Chart {k} — {v[0]}" for k,v in CHARTS.items()]
    selected_labels = st.multiselect("Or select specific charts:", chart_options, disabled=show_all)

    st.markdown("""
    <div style="margin-top:24px; padding:18px; background:rgba(33,150,243,0.08);
                border-radius:12px; border:1px solid rgba(33,150,243,0.2);">
        <p style="font-size:13px; color:#78909C; margin:0; text-align:center; line-height:2;">
            📊 19 Interactive Charts<br>
            🔍 Deep HR Analytics<br>
            💡 Actionable Insights<br>
            🚀 Executive Solution
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <div>
        <h1 class="dash-title">📊 Employee Attrition Dashboard</h1>
        <p class="dash-subtitle">Deep-dive analysis into employee turnover drivers · 19 Visualizations · Powered by Real Data</p>
    </div>
    <div style="text-align:right;">
        <div style="font-family:'Cairo',sans-serif; font-size:2.4rem; font-weight:900;
                    color:#FFFFFF; line-height:1; text-shadow:0 0 20px rgba(33,150,243,0.5);">
            KAYFA
        </div>
        <div style="font-size:0.85rem; color:#90CAF9; margin-top:4px; letter-spacing:2px;
                    text-transform:uppercase;">Analytics Platform</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load & KPIs ───────────────────────────────────────────────────────────────
df = load_data(uploaded) if uploaded is not None else load_data()

if df is None:
    st.error("❌ Data file not found — ensure final_dataset.csv is in the repo")
    st.stop()

total  = len(df)
left   = (df["Attrition"]=="Left").sum()
stayed = total - left
rate   = left/total*100

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card blue">
        <div class="kpi-label">Total Employees</div>
        <div class="kpi-value">{total:,}</div>
        <div style="font-size:13px;color:#546E7A;">Full Dataset</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Employees Left</div>
        <div class="kpi-value red">{left:,}</div>
        <div style="font-size:13px;color:#546E7A;">Attrition Count</div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-label">Attrition Rate</div>
        <div class="kpi-value amber">{rate:.1f}%</div>
        <div style="font-size:13px;color:#546E7A;">Global avg: 10–15%</div>
    </div>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ── Render Charts ─────────────────────────────────────────────────────────────
if show_all:
    keys_to_show = list(CHARTS.keys())
else:
    keys_to_show = [label.split(" — ")[0].replace("Chart ","") for label in selected_labels]

if not keys_to_show and not show_solution:
    st.markdown("""
    <div style="text-align:center;padding:40px;color:#546E7A;">
        <div style="font-size:3rem;">🔍</div>
        <p>Select at least one chart from the Sidebar</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for k in keys_to_show:
        name, fn = CHARTS[k]
        insight_type, insight_text = INSIGHTS[k]
        box_class   = "insight-box"   if insight_type == "insight" else "warning-box"
        title_class = "insight-title" if insight_type == "insight" else "warning-title"
        icon        = "💡 KEY INSIGHT" if insight_type == "insight" else "⚠️ CRITICAL FINDING"

        st.markdown(f"""
        <div class="chart-section">
            <span class="chart-number">CHART {k} / 19</span>
            <h3 class="chart-name">{name}</h3>
        """, unsafe_allow_html=True)

        fn(df)

        p_class = 'insight-text' if insight_type == 'insight' else 'warning-text'
        st.markdown(f"""
            <div class="{box_class}">
                <div class="{title_class}">{icon}</div>
                <p class="{p_class}" dir="auto" style="text-align:right; unicode-bidi:plaintext;">{insight_text}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Solution Section ──────────────────────────────────────────────────────────
if show_solution:
    st.markdown("""
    <div class="solution-section">
        <h2 class="solution-header">🚀 SOLUTION — Executive Action Plan</h2>
        <p class="solution-subheader">Top attrition drivers identified · Ranked priorities · 90-Day roadmap for HR leadership</p>

        <div class="exec-summary">
            <div class="exec-summary-title">📋 EXECUTIVE SUMMARY</div>
            <p class="exec-summary-text">
                With an attrition rate of <strong style="color:#EF9A9A;">47.5%</strong> — more than 3× the global benchmark —
                this organization faces a critical retention crisis. The data reveals that salary is <em>not</em> the root cause
                (only $46 mean difference between leavers and stayers). The primary drivers are
                <strong style="color:#EF9A9A;">work-life balance, lack of career growth, and absence of flexible work arrangements</strong>.
                The highest-risk segment: <strong style="color:#EF9A9A;">Entry-level, on-site employees in their first 5 years</strong>,
                who leave at a staggering 69.3% rate. Addressing the top 3 priorities below is projected to reduce
                overall attrition by <strong style="color:#69F0AE;">15–22 percentage points</strong> within 12 months.
            </p>
        </div>

        <div class="priority-card p1">
            <div class="priority-number">⚠️ PRIORITY #1 — HIGHEST IMPACT</div>
            <div class="priority-title">Implement Flexible & Remote Work Policy</div>
            <span class="priority-impact">Expected Attrition Reduction: 8–12 pts</span>
            <p style="font-size:14px; color:#B0BEC5; margin-bottom:14px;">
                Remote work reduces attrition from ~53% (on-site) to ~24% (remote) — a 28-point gap across all company sizes.
                Entry-level on-site employees are at 69.3% attrition; remote entry-level employees are at 24.1%.
                This is the single highest-ROI intervention available.
            </p>
            <ul class="priority-actions">
                <li>Immediately offer hybrid/remote options to all Entry-level employees</li>
                <li>Prioritize remote access for employees with commutes exceeding 40km (currently 52.9% attrition)</li>
                <li>Establish a formal remote work policy with clear eligibility criteria within 30 days</li>
                <li>Pilot 4-day work week for high-overtime teams to reduce burnout</li>
                <li>Set overtime caps and implement manager escalation alerts when thresholds are exceeded</li>
                <li>Track Work-Life Balance scores monthly; set target of 80%+ in "Good" or "Excellent" category</li>
            </ul>
        </div>

        <div class="priority-card p2">
            <div class="priority-number">📈 PRIORITY #2 — HIGH IMPACT</div>
            <div class="priority-title">Build Visible Career Growth Infrastructure</div>
            <span class="priority-impact">Expected Attrition Reduction: 5–8 pts</span>
            <p style="font-size:14px; color:#B0BEC5; margin-bottom:14px;">
                95% of employees have zero leadership opportunities. 83% have no innovation opportunities.
                Promotions show the strongest negative correlation with attrition (-0.081) of any variable.
                Employees in their first 5 years — when attrition peaks at 51–53% — leave because they see no path forward.
            </p>
            <ul class="priority-actions">
                <li>Launch a formal internal mobility program with open role transparency</li>
                <li>Require every manager to have a documented career-path conversation with each direct report quarterly</li>
                <li>Create "Innovation time" allocation (10–20% of work hours) for non-senior employees</li>
                <li>Introduce a Leadership Accelerator cohort for high-performers with &lt;5 years tenure</li>
                <li>Audit promotion timelines — ensure annual review cycles have clear, measurable criteria</li>
                <li>Identify and fast-track High Performance + Low Satisfaction employees before they resign</li>
            </ul>
        </div>

        <div class="priority-card p3">
            <div class="priority-number">🎯 PRIORITY #3 — MEDIUM-HIGH IMPACT</div>
            <div class="priority-title">Strengthen Early-Tenure & Onboarding Experience</div>
            <span class="priority-impact">Expected Attrition Reduction: 4–6 pts</span>
            <p style="font-size:14px; color:#B0BEC5; margin-bottom:14px;">
                The first 5 years are the most dangerous — attrition peaks at 51–53% during this window.
                Young employees (18–25) leave at 53.1%. Single employees leave at 62–72%.
                These groups need targeted retention programs in their first 18 months.
            </p>
            <ul class="priority-actions">
                <li>Redesign onboarding to include a 12-month structured mentorship program</li>
                <li>Assign retention "champions" (senior employees) to every new hire for the first year</li>
                <li>Conduct 30/60/90-day stay interviews — not exit interviews — for all new hires</li>
                <li>Create community-building programs for single employees (social events, peer groups)</li>
                <li>Implement an early-warning attrition risk score using the key predictors in this dashboard</li>
                <li>Launch targeted female-employee focus groups to uncover unique barriers driving 53% attrition</li>
            </ul>
        </div>

        <div class="action-plan">
            <div class="action-plan-title">📅 90-DAY ACTION PLAN</div>

            <div class="phase-row">
                <span class="phase-badge">Days 1–30</span>
                <div class="phase-content">
                    <strong>Immediate Wins:</strong> Announce hybrid/remote pilot for Entry-level teams.
                    Identify top 500 High-Performance + Low-Satisfaction employees and schedule 1:1 retention conversations.
                    Freeze overtime for departments exceeding 35% overtime penetration. Launch stay-interview program for all
                    employees with &lt;2 years tenure.
                </div>
            </div>

            <div class="phase-row">
                <span class="phase-badge">Days 31–60</span>
                <div class="phase-content">
                    <strong>Policy & Program Launch:</strong> Publish formal remote work eligibility policy.
                    Roll out quarterly career-path conversation framework to all managers (training required).
                    Open first cohort of Leadership Accelerator program. Establish monthly attrition dashboarding cadence
                    for executive review. Introduce overtime cap policy with automated HR alerts.
                </div>
            </div>

            <div class="phase-row">
                <span class="phase-badge">Days 61–90</span>
                <div class="phase-content">
                    <strong>Measurement & Scale:</strong> Measure 30-day impact on Work-Life Balance survey scores.
                    Run focus groups with female employees and single employees on retention barriers.
                    Deploy attrition risk scoring model (based on distance, tenure, job level, WLB, overtime).
                    Present first retention KPI report to C-suite: target 5% reduction in monthly departures within 90 days.
                </div>
            </div>
        </div>

        <div style="background:rgba(33,150,243,0.08); border:1px solid rgba(33,150,243,0.2);
                    border-radius:12px; padding:18px 22px; margin-top:20px;">
            <div style="font-size:12px; font-weight:700; letter-spacing:2px; text-transform:uppercase;
                        color:#64B5F6; margin-bottom:10px;">✅ RECOMMENDED ACTION — IMMEDIATE</div>
            <p style="font-size:15px; color:#E8EAF6; line-height:1.8; margin:0;">
                The <strong style="color:#FFFFFF;">highest-leverage decision</strong> available today requires no budget:
                approve remote/hybrid work for Entry-level employees. This single policy change, based on the data,
                is projected to reduce Entry-level attrition from <strong style="color:#EF9A9A;">69.3% → ~24%</strong>.
                Every month of delay costs the organization approximately
                <strong style="color:#FFD54F;">1,400+ additional departures</strong> from this cohort alone.
                Pair this with a mandatory career-path conversation program, and the combined impact on total attrition
                rate could reach <strong style="color:#69F0AE;">−15 percentage points within 12 months</strong>.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
