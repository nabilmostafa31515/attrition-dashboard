"""
Employee Attrition Dashboard — Professional Streamlit App
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import base64

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

/* Global */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Hide default streamlit header */
#MainMenu, footer, header { visibility: hidden; }

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0F1B3D 0%, #1A2D5A 50%, #0D1F3C 100%);
    min-height: 100vh;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #132040 100%) !important;
    border-right: 1px solid rgba(33, 150, 243, 0.2);
}
section[data-testid="stSidebar"] * {
    color: #E8EAF6 !important;
}
section[data-testid="stSidebar"] .stCheckbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #90CAF9 !important;
    font-size: 13px !important;
}

/* File uploader */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(33, 150, 243, 0.08) !important;
    border: 1px dashed rgba(33, 150, 243, 0.4) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

/* Main content area */
.main .block-container {
    padding: 1rem 2rem 2rem 2rem;
    max-width: 1400px;
}

/* Custom header */
.dash-header {
    background: linear-gradient(135deg, rgba(33,150,243,0.15) 0%, rgba(13,71,161,0.2) 100%);
    border: 1px solid rgba(33,150,243,0.25);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
}
.dash-title {
    font-family: 'Cairo', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.2;
    letter-spacing: -0.5px;
}
.dash-subtitle {
    font-size: 0.9rem;
    color: #90CAF9;
    margin-top: 6px;
    font-weight: 300;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px 28px;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: transform 0.2s, border-color 0.2s;
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
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #90CAF9;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Cairo', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #FFFFFF;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-value.red   { color: #EF9A9A; }
.kpi-value.amber { color: #FFC107; }

/* Chart container */
.chart-section {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
.chart-title-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 8px;
}
.chart-number {
    background: linear-gradient(135deg, #2196F3, #1565C0);
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.chart-name {
    font-family: 'Cairo', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #E8EAF6;
    margin-bottom: 0;
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, rgba(33,150,243,0.12) 0%, rgba(21,101,192,0.08) 100%);
    border-left: 4px solid #2196F3;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin-top: 18px;
}
.insight-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #64B5F6;
    margin-bottom: 8px;
}
.insight-text {
    font-size: 14px;
    color: #CFD8DC;
    line-height: 1.7;
    margin: 0;
}
.insight-text strong { color: #EF9A9A; }

/* Warning box */
.warning-box {
    background: linear-gradient(135deg, rgba(239,83,80,0.12) 0%, rgba(183,28,28,0.08) 100%);
    border-left: 4px solid #EF5350;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin-top: 18px;
}
.warning-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #EF9A9A;
    margin-bottom: 8px;
}
.warning-text {
    font-size: 14px;
    color: #CFD8DC;
    line-height: 1.7;
    margin: 0;
}
.warning-text strong { color: #FFF176; }

/* Upload placeholder */
.upload-placeholder {
    text-align: center;
    padding: 80px 40px;
    color: #546E7A;
}
.upload-placeholder h2 {
    font-family: 'Cairo', sans-serif;
    font-size: 1.8rem;
    color: #78909C;
    margin-bottom: 12px;
}
.upload-placeholder p {
    font-size: 15px;
    color: #546E7A;
}

/* Divider */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(33,150,243,0.3), transparent);
    margin: 8px 0 24px 0;
}

/* Metric overrides */
[data-testid="metric-container"] {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ── Color & Chart Helpers ────────────────────────────────────────────────────
C = dict(stayed="#2196F3", left="#EF5350", line="#FF8F00", grid="#1E2D4D", paper="rgba(0,0,0,0)", text="#E8EAF6")
BLUE_SEQ  = [[0, "#1A2D5A"], [0.5, "#1E88E5"], [1, "#64B5F6"]]
DIVERGING = [[0, "#EF5350"], [0.5, "#263238"], [1, "#2196F3"]]

def layout(title, sub, h=480):
    return dict(
        title=dict(text=f"<b>{title}</b><br><sub>{sub}</sub>", x=0.5,
                   font=dict(size=18, color=C["text"])),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,27,61,0.6)",
        font=dict(family="IBM Plex Sans, sans-serif", color=C["text"]),
        height=h,
        margin=dict(t=80, b=50, l=50, r=30),
        legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center",
                    bgcolor="rgba(0,0,0,0)", font=dict(color="#B0BEC5"))
    )

def ax(**kw):
    return dict(gridcolor=C["grid"], linecolor="#1E3A5F", zeroline=False,
                tickfont=dict(size=11, color="#90A4AE"),
                title_font=dict(size=12, color="#90CAF9"), **kw)

def show(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

@st.cache_data
def load_data(f):
    return pd.read_excel(f)

# ── Charts ───────────────────────────────────────────────────────────────────
def chart1(df):
    c = df["Attrition"].value_counts()
    fig = go.Figure(go.Pie(
        labels=c.index, values=c.values, hole=0.6,
        marker=dict(colors=[C["stayed"], C["left"]], line=dict(color="#0F1B3D", width=3)),
        textinfo="percent+label", textfont=dict(size=14, color="#E8EAF6"),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    ))
    fig.update_layout(**layout("Attrition Overview", "Stayed vs. Left", 420),
        annotations=[dict(text=f"<b style='font-size:16px'>{len(df):,}</b><br><span style='font-size:11px'>Total</span>",
                          x=0.5, y=0.5, showarrow=False, font=dict(size=15, color="#E8EAF6"))])
    show(fig)

def chart2(df):
    g  = df.groupby(["Gender","Attrition"]).size().unstack()
    gp = df.groupby("Gender")["Attrition"].value_counts(normalize=True).unstack()*100
    fig = go.Figure([
        go.Bar(name="Stayed", x=g.index, y=g["Stayed"], marker_color=C["stayed"],
               text=[f"{v:,}" for v in g["Stayed"]], textposition="outside", textfont=dict(color="#90CAF9")),
        go.Bar(name="Left",   x=g.index, y=g["Left"],   marker_color=C["left"],
               text=[f"{v:,}" for v in g["Left"]],   textposition="outside", textfont=dict(color="#EF9A9A")),
    ])
    for gen in g.index:
        fig.add_annotation(x=gen, y=g.loc[gen].max()+2000,
                           text=f"<b>Rate: {gp.loc[gen,'Left']:.1f}%</b>",
                           showarrow=False, font=dict(size=11, color=C["left"]))
    fig.update_layout(**layout("Attrition by Gender", "Comparing turnover between genders"), barmode="group")
    fig.update_xaxes(**ax(title_text="Gender")); fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart3(df):
    df=df.copy()
    df["AG"]=pd.cut(df["Age"],[17,25,35,45,55,65],labels=["18-25","26-35","36-45","46-55","56-65"])
    g =df.groupby(["AG","Attrition"],observed=False).size().unstack()
    gp=df.groupby("AG",observed=False)["Attrition"].value_counts(normalize=True).unstack()*100
    fig=go.Figure([
        go.Bar(name="Stayed",x=g.index.astype(str),y=g["Stayed"],marker_color=C["stayed"]),
        go.Bar(name="Left",  x=g.index.astype(str),y=g["Left"],  marker_color=C["left"]),
    ])
    fig.add_trace(go.Scatter(name="Rate %",x=g.index.astype(str),y=gp["Left"],yaxis="y2",
        mode="lines+markers",line=dict(color=C["line"],width=2.5),marker=dict(size=9, color=C["line"])))
    fig.update_layout(**layout("Attrition by Age Group","How attrition shifts across age brackets"),barmode="group",
        yaxis2=dict(overlaying="y",side="right",range=[0,100],showgrid=False,title="Rate (%)",
                    tickfont=dict(color="#FFB300"), title_font=dict(color="#FFB300")))
    fig.update_xaxes(**ax(title_text="Age group")); fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart4(df):
    pct=df.groupby("Job Role")["Attrition"].apply(lambda x:(x=="Left").mean()*100).sort_values()
    fig=go.Figure(go.Bar(x=pct.values,y=pct.index,orientation="h",
        marker=dict(color=pct.values,colorscale=BLUE_SEQ,showscale=True,
                    colorbar=dict(title="Rate %", tickfont=dict(color="#90A4AE"), title_font=dict(color="#90CAF9"))),
        text=[f"{v:.1f}%" for v in pct.values],textposition="outside",textfont=dict(color="#90CAF9")))
    fig.update_layout(**layout("Attrition by Job Role","Which roles have highest turnover?",420))
    fig.update_xaxes(**ax(title_text="Attrition rate (%)"))
    show(fig)

def chart5(df):
    fig=go.Figure()
    for label,color in [("Stayed",C["stayed"]),("Left",C["left"])]:
        sub=df[df["Attrition"]==label]["Monthly Income"]
        fig.add_trace(go.Box(y=sub,name=label,marker_color=color,boxmean=True,
                             line=dict(color=color), fillcolor=color.replace(")", ",0.3)").replace("rgb","rgba") if "rgb" in color else color))
        fig.add_annotation(x=label,y=sub.mean()+800,text=f"<b>Mean: ${sub.mean():,.0f}</b>",
                           showarrow=False,font=dict(size=11,color=color))
    fig.update_layout(**layout("Monthly Income by Attrition","Do lower earners leave more?"))
    fig.update_yaxes(**ax(title_text="Monthly income (USD)"))
    show(fig)

def chart6(df):
    order=["Poor","Fair","Good","Excellent"]
    g =df.groupby(["Work-Life Balance","Attrition"],observed=False).size().unstack().reindex(order)
    gp=df.groupby("Work-Life Balance",observed=False)["Attrition"].value_counts(normalize=True).unstack().reindex(order)*100
    fig=go.Figure([
        go.Bar(name="Stayed",x=g.index,y=g["Stayed"],marker_color=C["stayed"],
               text=[f"{v:,}" for v in g["Stayed"]],textposition="inside"),
        go.Bar(name="Left",  x=g.index,y=g["Left"],  marker_color=C["left"],
               text=[f"{v:,}" for v in g["Left"]],  textposition="inside"),
    ])
    for wl in order:
        fig.add_annotation(x=wl,y=g.loc[wl].sum()+800,
                           text=f"<b>Rate: {gp.loc[wl,'Left']:.1f}%</b>",
                           showarrow=False,font=dict(size=10,color=C["left"]))
    fig.update_layout(**layout("Attrition by Work-Life Balance","Does poor WLB drive attrition?"),barmode="stack")
    fig.update_xaxes(**ax(title_text="WLB")); fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart7(df):
    ot=df.groupby("Overtime")["Attrition"].value_counts(normalize=True).unstack()*100
    oy=df[df["Overtime"]=="Yes"]["Attrition"].value_counts()
    fig=make_subplots(1,2,specs=[[{"type":"pie"},{"type":"bar"}]],
                      subplot_titles=("Overtime Employees Distribution","Attrition Rate by Overtime"))
    fig.add_trace(go.Pie(labels=["Stayed","Left"],values=[oy.get("Stayed",0),oy.get("Left",0)],
        marker=dict(colors=[C["stayed"],C["left"]]),hole=0.5,textinfo="percent+label",
        textfont=dict(color="#E8EAF6")),1,1)
    fig.add_trace(go.Bar(x=["No OT","With OT"],y=ot["Left"],
        marker=dict(color=[C["stayed"],C["left"]]),
        text=[f"{v:.1f}%" for v in ot["Left"]],textposition="outside",
        textfont=dict(color="#E8EAF6")),1,2)
    fig.update_layout(**layout("Overtime Impact on Attrition","Overtime employees leave significantly more",450),showlegend=False)
    show(fig)

def chart8(df):
    order=["High School","Associate Degree","Bachelor's Degree","Master's Degree","PhD"]
    pct=df.groupby("Education Level")["Attrition"].apply(lambda x:(x=="Left").mean()*100).reindex(order)
    counts=df["Education Level"].value_counts().reindex(order)
    fig=go.Figure(go.Bar(x=pct.index,y=pct.values,
        marker=dict(color=pct.values,colorscale=BLUE_SEQ,showscale=True),
        text=[f"{v:.1f}%" for v in pct.values],textposition="outside",textfont=dict(color="#90CAF9")))
    for edu,p in zip(pct.index,pct.values):
        fig.add_annotation(x=edu,y=p+3,text=f"n={counts[edu]:,}",
                           showarrow=False,font=dict(size=10,color="#78909C"))
    fig.update_layout(**layout("Attrition by Education","Does education correlate with turnover?"))
    fig.update_xaxes(**ax(title_text="Education")); fig.update_yaxes(**ax(title_text="Rate (%)",range=[0,pct.max()*1.35]))
    show(fig)

def chart9(df):
    cols=["Age","Years at Company","Monthly Income","Number of Promotions","Distance from Home","Number of Dependents","Company Tenure"]
    df2=df.copy(); df2["Attrition_Bin"]=(df2["Attrition"]=="Left").astype(int)
    corr=df2[cols+["Attrition_Bin"]].corr()
    labels=["Age","Years","Income","Promotions","Distance","Dependents","Tenure","Attrition"]
    fig=go.Figure(go.Heatmap(z=corr.values,x=labels,y=labels,colorscale=DIVERGING,zmin=-1,zmax=1,
        text=corr.round(2).values,texttemplate="%{text:.2f}",textfont=dict(size=10,color="#E8EAF6"),
        colorbar=dict(title="r", tickfont=dict(color="#90A4AE"), title_font=dict(color="#90CAF9"))))
    fig.update_layout(**layout("Correlation Heatmap","Which variables correlate with attrition?",500))
    show(fig)

def chart10(df):
    df=df.copy(); bins=list(range(0,55,5))
    df["YG"]=pd.cut(df["Years at Company"],bins=bins,labels=[f"{i}-{i+4}" for i in bins[:-1]],include_lowest=True)
    g =df.groupby("YG",observed=True)["Attrition"].value_counts().unstack(fill_value=0)
    gp=df.groupby("YG",observed=True)["Attrition"].value_counts(normalize=True).unstack(fill_value=0)*100
    fig=go.Figure([
        go.Bar(name="Stayed",x=g.index.astype(str),y=g["Stayed"],marker_color=C["stayed"]),
        go.Bar(name="Left",  x=g.index.astype(str),y=g["Left"],  marker_color=C["left"]),
    ])
    fig.add_trace(go.Scatter(name="Rate %",x=g.index.astype(str),y=gp["Left"],yaxis="y2",
        mode="lines+markers",line=dict(color=C["line"],width=2.5),marker=dict(size=8,color=C["line"])))
    fig.update_layout(**layout("Attrition by Tenure","Early employees have higher turnover"),barmode="stack",
        yaxis2=dict(overlaying="y",side="right",range=[0,100],showgrid=False,title="Rate (%)",
                    tickfont=dict(color="#FFB300"), title_font=dict(color="#FFB300")))
    fig.update_xaxes(**ax(title_text="Years")); fig.update_yaxes(**ax(title_text="Headcount"))
    show(fig)

def chart11(df):
    data=df.groupby(["Marital Status","Gender"])["Attrition"].apply(lambda x:(x=="Left").mean()*100).unstack()
    colors={"Male":C["stayed"],"Female":"#AB47BC"}
    fig=go.Figure([go.Bar(name=g,x=data.index,y=data[g],marker_color=colors.get(g,"#78909C"),
        text=[f"{v:.1f}%" for v in data[g]],textposition="outside",textfont=dict(color="#E8EAF6"))
        for g in data.columns])
    fig.update_layout(**layout("Attrition by Marital Status & Gender","Single employees show highest turnover"),barmode="group")
    fig.update_xaxes(**ax(title_text="Marital status")); fig.update_yaxes(**ax(title_text="Rate (%)"))
    show(fig)

def chart12(df):
    data=df.groupby(["Company Size","Remote Work"])["Attrition"].apply(lambda x:(x=="Left").mean()*100).unstack()
    colors={"Yes":"#26A69A","No":C["left"]}; labels={"Yes":"Remote","No":"On-site"}
    fig=go.Figure([go.Bar(name=labels.get(k,k),x=data.index,y=data[k],marker_color=colors.get(k,"#78909C"),
        text=[f"{v:.1f}%" for v in data[k]],textposition="outside",textfont=dict(color="#E8EAF6"))
        for k in data.columns])
    fig.update_layout(**layout("Attrition by Size & Remote Work","How size and remote work affect turnover"),barmode="group")
    fig.update_xaxes(**ax(title_text="Company size")); fig.update_yaxes(**ax(title_text="Rate (%)"))
    show(fig)

def chart13(df):
    pivot=df.groupby(["Performance Rating","Job Satisfaction"])["Attrition"].apply(lambda x:(x=="Left").mean()*100).unstack()
    fig=go.Figure(go.Heatmap(z=pivot.values,x=pivot.columns,y=pivot.index,colorscale=BLUE_SEQ,
        text=pivot.round(1).values,texttemplate="%{text:.1f}%",textfont=dict(size=11,color="#E8EAF6"),
        colorbar=dict(title="Rate %",tickfont=dict(color="#90A4AE"),title_font=dict(color="#90CAF9"))))
    fig.update_layout(**layout("Performance x Satisfaction","Interaction effects on attrition",420))
    show(fig)

def chart14(df):
    df=df.copy()
    df["DG"]=pd.cut(df["Distance from Home"],[0,20,40,60,80,100],labels=["0-20","21-40","41-60","61-80","81-100"])
    pct=df.groupby("DG",observed=True)["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    fig=go.Figure(go.Bar(x=pct.index.astype(str),y=pct.values,
        marker=dict(color=pct.values,colorscale=BLUE_SEQ,showscale=True),
        text=[f"{v:.1f}%" for v in pct.values],textposition="outside",textfont=dict(color="#90CAF9")))
    fig.update_layout(**layout("Attrition by Commute Distance","Does longer commute drive attrition?"))
    fig.update_xaxes(**ax(title_text="Distance (km)")); fig.update_yaxes(**ax(title_text="Rate (%)",range=[0,pct.max()*1.25]))
    show(fig)

def chart15(df):
    pct   = df.groupby("Leadership Opportunities")["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    count = df["Leadership Opportunities"].value_counts()
    colors = {"No":C["left"],"Yes":C["stayed"]}
    labels = {"No":"No Leadership Opps","Yes":"Has Leadership Opps"}
    fig = go.Figure()
    for val in ["No","Yes"]:
        fig.add_trace(go.Bar(x=[labels[val]],y=[pct[val]],name=labels[val],
            marker_color=colors[val],text=[f"{pct[val]:.1f}%"],textposition="outside",
            textfont=dict(color="#E8EAF6"),width=0.4))
        fig.add_annotation(x=labels[val],y=pct[val]+3,text=f"n={count[val]:,}",
                           showarrow=False,font=dict(size=11,color="#78909C"))
    fig.update_layout(**layout("Attrition by Leadership Opportunities",
                 f"Only {count.get('Yes',0)/len(df)*100:.1f}% of employees have leadership opportunities",420),
        showlegend=False, yaxis=dict(**ax(title_text="Attrition Rate (%)",range=[0,60])))
    show(fig)

def chart16(df):
    pct   = df.groupby("Innovation Opportunities")["Attrition"].apply(lambda x:(x=="Left").mean()*100)
    count = df["Innovation Opportunities"].value_counts()
    colors = {"No":C["left"],"Yes":C["stayed"]}
    labels = {"No":"No Innovation Opps","Yes":"Has Innovation Opps"}
    fig = go.Figure()
    for val in ["No","Yes"]:
        fig.add_trace(go.Bar(x=[labels[val]],y=[pct[val]],name=labels[val],
            marker_color=colors[val],text=[f"{pct[val]:.1f}%"],textposition="outside",
            textfont=dict(color="#E8EAF6"),width=0.4))
        fig.add_annotation(x=labels[val],y=pct[val]+3,text=f"n={count[val]:,}",
                           showarrow=False,font=dict(size=11,color="#78909C"))
    fig.update_layout(**layout("Attrition by Innovation Opportunities",
                 f"{count.get('No',0)/len(df)*100:.1f}% of employees have no innovation opportunities",420),
        showlegend=False, yaxis=dict(**ax(title_text="Attrition Rate (%)",range=[0,60])))
    show(fig)

def chart17(df):
    order = ["Poor","Fair","Good","Excellent"]
    pct   = df.groupby("Company Reputation")["Attrition"].apply(lambda x:(x=="Left").mean()*100).reindex(order)
    count = df["Company Reputation"].value_counts().reindex(order)
    fig = go.Figure(go.Bar(x=pct.values,y=pct.index,orientation="h",
        marker=dict(color=pct.values,colorscale=DIVERGING,cmin=35,cmax=60,showscale=True,
                    colorbar=dict(title="Rate %",tickfont=dict(color="#90A4AE"),title_font=dict(color="#90CAF9"))),
        text=[f"{v:.1f}%" for v in pct.values],textposition="outside",textfont=dict(color="#90CAF9")))
    for rep,p in zip(pct.index,pct.values):
        fig.add_annotation(x=p+2,y=rep,text=f"n={count[rep]:,}",
                           showarrow=False,font=dict(size=10,color="#78909C"),xanchor="left")
    fig.update_layout(**layout("Attrition by Company Reputation","Poor reputation drives significantly higher turnover",420),
        xaxis=dict(**ax(title_text="Attrition Rate (%)",range=[0,70])),
        yaxis=dict(**ax(title_text="Company Reputation")))
    show(fig)

def chart18(df):
    order = ["Low","Medium","High","Very High"]
    pct   = df.groupby("Employee Recognition",observed=False)["Attrition"].apply(
                lambda x:(x=="Left").mean()*100).reindex(order)
    count = df["Employee Recognition"].value_counts().reindex(order)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=pct.index,y=pct.values,
        marker=dict(color=pct.values,colorscale=BLUE_SEQ,showscale=True,
                    colorbar=dict(title="Rate %",tickfont=dict(color="#90A4AE"),title_font=dict(color="#90CAF9"))),
        text=[f"{v:.1f}%" for v in pct.values],textposition="outside",
        textfont=dict(color="#90CAF9"),name="Attrition Rate"))
    fig.add_trace(go.Scatter(x=order,y=count.values,yaxis="y2",mode="lines+markers",
        line=dict(color=C["line"],width=2.5,dash="dot"),marker=dict(size=9,color=C["line"]),
        name="Employee Count"))
    fig.update_layout(**layout("Attrition by Employee Recognition",
                 "Recognition level has minimal impact — only 1.8% difference across all levels",480),
        yaxis=dict(**ax(title_text="Attrition Rate (%)",range=[0,60])),
        yaxis2=dict(overlaying="y",side="right",showgrid=False,title="Employee Count",
                    tickfont=dict(color="#FFB300"),title_font=dict(color="#FFB300")))
    show(fig)

def chart19(df):
    order_jl=["Entry","Mid","Senior"]
    g  = df.groupby("Job Level")["Attrition"].value_counts().unstack().reindex(order_jl)
    gp = df.groupby("Job Level")["Attrition"].value_counts(normalize=True).unstack().reindex(order_jl)*100
    pivot = df.groupby(["Job Level","Remote Work"])["Attrition"].apply(
                lambda x:(x=="Left").mean()*100).unstack().reindex(order_jl)
    fig = make_subplots(rows=1,cols=2,column_widths=[0.6,0.4],
        subplot_titles=("Attrition Count & Rate by Job Level","Rate % by Job Level x Remote Work"),
        specs=[[{"type":"bar"},{"type":"heatmap"}]])
    fig.add_trace(go.Bar(name="Stayed",x=order_jl,y=g["Stayed"],marker_color=C["stayed"],
        text=[f"{v:,}" for v in g["Stayed"]],textposition="inside"),row=1,col=1)
    fig.add_trace(go.Bar(name="Left",x=order_jl,y=g["Left"],marker_color=C["left"],
        text=[f"{v:,}" for v in g["Left"]],textposition="inside"),row=1,col=1)
    fig.add_trace(go.Scatter(name="Rate %",x=order_jl,y=gp["Left"],yaxis="y2",
        mode="lines+markers",line=dict(color=C["line"],width=2.5),marker=dict(size=10,color=C["line"])),row=1,col=1)
    fig.add_trace(go.Heatmap(z=pivot.values,x=pivot.columns.tolist(),y=order_jl,
        colorscale=BLUE_SEQ,text=pivot.round(1).values,texttemplate="%{text:.1f}%",
        textfont=dict(size=13,color="#E8EAF6"),
        colorbar=dict(title="Rate %",x=1.02,tickfont=dict(color="#90A4AE"),title_font=dict(color="#90CAF9")),
        showscale=True),row=1,col=2)
    fig.update_layout(**layout("Job Level Impact on Attrition",
                 "Entry-level employees leave at 63.3% — Senior at only 20.3%",500),
        barmode="group",
        yaxis2=dict(overlaying="y",side="right",range=[0,100],showgrid=False,title="Rate (%)",
                    tickfont=dict(color="#FFB300"),title_font=dict(color="#FFB300")))
    fig.update_xaxes(title_text="Job Level",row=1,col=1)
    fig.update_yaxes(title_text="Headcount",row=1,col=1)
    fig.update_xaxes(title_text="Remote Work",row=1,col=2)
    show(fig)

# ── Insights per chart ───────────────────────────────────────────────────────
INSIGHTS = {
    "1":  ("insight", "نسبة الـ Attrition تبلغ <strong>47.5%</strong> — ضعف المعدل العالمي الطبيعي (10-15%). يعني تقريباً <strong>موظف من كل 2 يغادر الشركة</strong>، وهو ما يشير إلى مشكلة هيكلية عميقة تستوجب تحقيقاً فورياً."),
    "2":  ("warning", "الإناث يغادرن بنسبة <strong>53%</strong> مقابل <strong>42.9%</strong> للذكور — فارق <strong>10 نقاط كاملة</strong>. هذا يوحي بوجود تحديات خاصة تواجه الموظفات، سواء في التوازن الأسري أو فرص الترقي أو بيئة العمل."),
    "3":  ("insight", "فئة <strong>18-25 سنة</strong> هي الأعلى في المغادرة بنسبة <strong>53.1%</strong>. كل ما زاد العمر انخفضت النسبة تدريجياً، مما يستوجب التركيز على <strong>برامج الاحتفاظ بالموظفين الجدد</strong>."),
    "4":  ("insight", "الفارق بين الوظائف لا يتجاوز <strong>2%</strong> — وهذا يؤكد أن المشكلة <strong>ليست في وظيفة بعينها</strong>، بل هي مشكلة مؤسسية شاملة تمس ثقافة الشركة وسياساتها."),
    "5":  ("warning", "الفارق في الراتب بين من غادروا ومن بقوا هو <strong>46 دولاراً فقط</strong>! هذا يكشف أن <strong>الراتب ليس السبب الرئيسي للمغادرة</strong>، مما يعني أن رفع الرواتب وحده لن يحل المشكلة."),
    "6":  ("warning", "موظفو الـ <strong>Poor WLB</strong> يغادرون بنسبة <strong>60.2%</strong> مقابل <strong>35.7%</strong> لأصحاب الـ Excellent — فارق <strong>24.5 نقطة</strong>! التوازن بين العمل والحياة هو أكثر العوامل تأثيراً على الاستبقاء."),
    "7":  ("insight", "الموظفون الذين يعملون أوفر تايم يغادرون بنسبة <strong>51.5%</strong> مقابل <strong>45.5%</strong>. والخطير أن <strong>ثلث الموظفين</strong> (24,341) يعملون أوفر تايم، مما يشكل ضغطاً مزمناً على المؤسسة."),
    "8":  ("insight", "أصحاب <strong>PhD</strong> يغادرون بنسبة <strong>24.4% فقط</strong> مقارنة بـ ~48% لباقي المستويات — فارق مذهل! في حين أن باقي المستويات التعليمية متقاربة جداً في نسب المغادرة."),
    "9":  ("insight", "أقوى عامل للاستبقاء هو <strong>الترقيات (-0.081)</strong>، وأقوى عامل للمغادرة هو <strong>بُعد المسافة (+0.094)</strong>. أما الراتب فعلاقته بالمغادرة <strong>شبه معدومة (0.011)</strong>."),
    "10": ("warning", "أول <strong>5 سنوات</strong> هي الأخطر بنسبة مغادرة <strong>51-53%</strong>. بعد <strong>10 سنوات</strong> تنخفض النسبة بشكل ملحوظ، مما يجعل الـ Onboarding والسنوات الأولى أولوية قصوى."),
    "11": ("warning", "الأعزب/العزباء يغادرون بنسب صادمة: <strong>72.2%</strong> للإناث و<strong>62.3%</strong> للذكور. المتزوجون هم الأكثر استقراراً بفارق كبير بسبب الالتزامات الأسرية."),
    "12": ("insight", "الـ <strong>Remote Work</strong> يخفض الـ Attrition بأكثر من <strong>28 نقطة</strong> في جميع أحجام الشركات! من ~53% On-site إلى ~24% Remote — هذا أقوى قرار يمكن اتخاذه للاحتفاظ بالموظفين."),
    "13": ("warning", "الأخطر هو الموظف <strong>High Performance + Low Satisfaction</strong> — شاطر لكن غير راضٍ، وسيجد فرصة أخرى بسرعة. يجب تحديد هؤلاء والتحدث معهم قبل مغادرتهم."),
    "14": ("insight", "كل ما زادت المسافة، زادت نسبة المغادرة من <strong>41.7%</strong> للأقرب إلى <strong>52.9%</strong> للأبعد. توفير خيار <strong>Hybrid/Remote</strong> للموظفين البعيدين سيقلل هذا الأثر بشكل كبير."),
    "15": ("warning", "<strong>95%</strong> من الموظفين ليس لديهم أي فرصة قيادية! هذا يعني غياب مسار التطوير الوظيفي لغالبية الموظفين، وهو من أهم أسباب الشعور بالركود والرغبة في المغادرة."),
    "16": ("warning", "<strong>83%</strong> من الموظفين محرومون من فرص الابتكار. الموظف الذي يكرر نفس المهام يومياً بدون تحدٍّ سيبحث عن بيئة أكثر إثارة وتحفيزاً."),
    "17": ("insight", "السمعة الضعيفة <strong>(Poor)</strong> ترفع نسبة المغادرة إلى <strong>56%</strong> مقارنة بـ <strong>43%</strong> للسمعة الجيدة — فارق <strong>13 نقطة</strong>. الموظف يريد أن يفتخر بمكان عمله أمام الآخرين."),
    "18": ("insight", "الفارق بين أعلى وأدنى مستوى من التقدير <strong>1.8% فقط</strong>! مما يؤكد أن التقدير اللفظي بدون مكافآت ملموسة أو ترقيات <strong>لا أثر له على قرار البقاء</strong>."),
    "19": ("warning", "الأخطر في الداتا كلها: <strong>Entry Level بدون Remote = 69.3%</strong> مغادرة! بينما <strong>Senior مع Remote = 5.2% فقط</strong>. تركيز جهود الـ Remote على الـ Entry Level هو أولوية الأولويات."),
}

# ── Registry ─────────────────────────────────────────────────────────────────
CHARTS = {
    "1":  ("Attrition Overview",             chart1),
    "2":  ("Attrition by Gender",            chart2),
    "3":  ("Attrition by Age Group",         chart3),
    "4":  ("Attrition by Job Role",          chart4),
    "5":  ("Monthly Income",                 chart5),
    "6":  ("Work-Life Balance",              chart6),
    "7":  ("Overtime Impact",                chart7),
    "8":  ("Education Level",                chart8),
    "9":  ("Correlation Heatmap",            chart9),
    "10": ("Attrition by Tenure",            chart10),
    "11": ("Marital Status x Gender",        chart11),
    "12": ("Company Size x Remote Work",     chart12),
    "13": ("Performance x Satisfaction",     chart13),
    "14": ("Commute Distance",               chart14),
    "15": ("Leadership Opportunities",       chart15),
    "16": ("Innovation Opportunities",       chart16),
    "17": ("Company Reputation",             chart17),
    "18": ("Employee Recognition",           chart18),
    "19": ("Job Level x Remote Work",        chart19),
}

LOGO_B64 = "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"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 20px 0 10px 0;">
        <img src="data:image/png;base64,{LOGO_B64}" style="max-width:160px; border-radius:10px;">
    </div>
    <div style="text-align:center; margin-bottom:20px;">
        <span style="font-family:'Cairo',sans-serif; font-size:1.1rem; font-weight:700; color:#90CAF9;">
            لوحة تحليل دوران الموظفين
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,243,0.4),transparent);margin-bottom:20px;"></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("📂 ارفع ملف الـ Excel", type=["xlsx"])

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,243,0.4),transparent);margin:16px 0;"></div>', unsafe_allow_html=True)

    show_all = st.checkbox("عرض كل الشارتات", value=True)
    chart_options = [f"Chart {k} — {v[0]}" for k,v in CHARTS.items()]
    selected_labels = st.multiselect("أو اختار شارتات محددة:", chart_options, disabled=show_all)

    st.markdown("""
    <div style="margin-top:30px; padding:16px; background:rgba(33,150,243,0.08); border-radius:12px; border:1px solid rgba(33,150,243,0.2);">
        <p style="font-size:12px; color:#78909C; margin:0; text-align:center; line-height:1.6;">
            📊 19 Interactive Chart<br>
            🔍 Deep HR Analytics<br>
            💡 Actionable Insights
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <div>
        <h1 class="dash-title">📊 Employee Attrition Dashboard</h1>
        <p class="dash-subtitle">تحليل معمّق لأسباب مغادرة الموظفين · 19 Visualization · Powered by Real Data</p>
    </div>
    <img src="data:image/png;base64,{LOGO_B64}"
         style="height:60px; border-radius:10px; opacity:0.9;">
</div>
""", unsafe_allow_html=True)

# ── No file state ─────────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div class="upload-placeholder">
        <div style="font-size:5rem; margin-bottom:20px;">📂</div>
        <h2>ارفع ملف الداتا للبدء</h2>
        <p>ارفع ملف <strong style="color:#90CAF9;">final_dataset.xlsx</strong> من الـ Sidebar على اليسار<br>
        وستظهر الـ 19 شارت فوراً مع التحليل الكامل</p>
        <div style="margin-top:40px; display:flex; gap:20px; justify-content:center; flex-wrap:wrap;">
            <div style="background:rgba(33,150,243,0.1);border:1px solid rgba(33,150,243,0.2);border-radius:12px;padding:16px 24px;text-align:center;">
                <div style="font-size:2rem; font-weight:900; color:#2196F3; font-family:'Cairo';">19</div>
                <div style="font-size:12px; color:#546E7A;">Interactive Charts</div>
            </div>
            <div style="background:rgba(239,83,80,0.1);border:1px solid rgba(239,83,80,0.2);border-radius:12px;padding:16px 24px;text-align:center;">
                <div style="font-size:2rem; font-weight:900; color:#EF5350; font-family:'Cairo';">74K+</div>
                <div style="font-size:12px; color:#546E7A;">Employee Records</div>
            </div>
            <div style="background:rgba(255,143,0,0.1);border:1px solid rgba(255,143,0,0.2);border-radius:12px;padding:16px 24px;text-align:center;">
                <div style="font-size:2rem; font-weight:900; color:#FF8F00; font-family:'Cairo';">15+</div>
                <div style="font-size:12px; color:#546E7A;">Key Variables</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load & KPIs ───────────────────────────────────────────────────────────────
df = load_data(uploaded)
total = len(df)
left  = (df["Attrition"]=="Left").sum()
stayed = total - left
rate = left/total*100

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card blue">
        <div class="kpi-label">Total Employees</div>
        <div class="kpi-value">{total:,}</div>
        <div style="font-size:12px;color:#546E7A;">Full Dataset</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Employees Left</div>
        <div class="kpi-value red">{left:,}</div>
        <div style="font-size:12px;color:#546E7A;">Attrition Count</div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-label">Attrition Rate</div>
        <div class="kpi-value amber">{rate:.1f}%</div>
        <div style="font-size:12px;color:#546E7A;">Global avg: 10-15%</div>
    </div>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ── Render Charts ─────────────────────────────────────────────────────────────
if show_all:
    keys_to_show = list(CHARTS.keys())
else:
    keys_to_show = [label.split(" — ")[0].replace("Chart ","") for label in selected_labels]

if not keys_to_show:
    st.markdown("""
    <div style="text-align:center;padding:40px;color:#546E7A;">
        <div style="font-size:3rem;">🔍</div>
        <p>اختار شارت واحد على الأقل من الـ Sidebar</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for k in keys_to_show:
        name, fn = CHARTS[k]
        insight_type, insight_text = INSIGHTS[k]
        box_class = "insight-box" if insight_type == "insight" else "warning-box"
        title_class = "insight-title" if insight_type == "insight" else "warning-title"
        icon = "💡 KEY INSIGHT" if insight_type == "insight" else "⚠️ CRITICAL FINDING"

        st.markdown(f"""
        <div class="chart-section">
            <div class="chart-title-row">
                <div>
                    <span class="chart-number">CHART {k} / 19</span>
                    <h3 class="chart-name" style="margin-top:8px;">{name}</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)

        fn(df)

        st.markdown(f"""
            <div class="{box_class}">
                <div class="{title_class}">{icon}</div>
                <p class="{'insight-text' if insight_type == 'insight' else 'warning-text'}">{insight_text}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
