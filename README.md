<div align="center">

# 📊 Employee Attrition Dashboard
### تحليل دوران الموظفين — لوحة تحكم تفاعلية

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://attrition-dashboard-cvavrzwtzf8rrejc6pxhfa.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat)

<br/>

> **A professional HR Analytics dashboard built with Streamlit & Plotly, analyzing employee attrition patterns across 74,498 employees and 24 variables.**
>
> **لوحة تحليل احترافية مبنية بـ Streamlit و Plotly لتحليل أسباب مغادرة الموظفين عبر 74,498 موظف و 24 متغير.**

**[🚀 Live Demo | عرض مباشر](https://attrition-dashboard-cvavrzwtzf8rrejc6pxhfa.streamlit.app/)**

</div>

---

## 📋 Table of Contents | جدول المحتويات

- [Overview | نظرة عامة](#overview)
- [Key Findings | أهم النتائج](#key-findings)
- [Features | المميزات](#features)
- [Tech Stack | التقنيات المستخدمة](#tech-stack)
- [Project Structure | هيكل المشروع](#project-structure)
- [Getting Started | كيفية التشغيل](#getting-started)
- [Dashboard Sections | أقسام الداشبورد](#dashboard-sections)
- [Dataset | الداتاست](#dataset)
- [Author | المطور](#author)

---

## 🧠 Overview | نظرة عامة <a name="overview"></a>

**EN:** This dashboard provides a deep-dive HR analytics experience, exploring the key drivers behind employee attrition. Built with a dark professional UI theme, it delivers 19 interactive visualizations covering demographics, compensation, work conditions, and organizational factors — each paired with Arabic-language insights and critical findings.

**AR:** يوفر هذا الداشبورد تجربة تحليل HR عميقة، يستكشف فيها المحركات الرئيسية لمغادرة الموظفين. مبني بثيم احترافي داكن، يقدم 19 visualization تفاعلي يغطي الديموغرافيا والرواتب وظروف العمل والعوامل المؤسسية — كل واحدة مرفقة بـ insights وتحليل باللغة العربية.

---

## 🔍 Key Findings | أهم النتائج <a name="key-findings"></a>

| Metric | Value | Insight |
|--------|-------|---------|
| 📉 Overall Attrition Rate | **47.5%** | 3× the global average (10–15%) |
| 👩 Female Attrition | **53%** | vs 42.9% for males — 10pt gap |
| 🧑‍💼 Entry Level (No Remote) | **69.3%** | Highest risk segment |
| 🏠 Remote Work Impact | **−28pts** | On-site 53% → Remote 24% |
| ⚖️ Poor Work-Life Balance | **60.2%** | vs 35.7% Excellent — 24.5pt gap |
| 💰 Salary Difference | **$46 only** | Salary is NOT the main driver |
| 🎓 PhD Holders | **24.4%** | vs ~48% other education levels |
| 📅 First 5 Years | **51–53%** | Highest attrition window |

---

## ✨ Features | المميزات <a name="features"></a>

- 🎨 **Professional Dark UI** — Custom CSS with IBM Plex Sans + Cairo fonts
- 📊 **19 Interactive Charts** — Powered by Plotly (bar, pie, box, heatmap, scatter)
- 💡 **Per-Chart Insights** — Arabic-language KEY INSIGHT & CRITICAL FINDING for every chart
- 🔢 **Live KPI Cards** — Total Employees, Attrition Count, Attrition Rate
- 📂 **Custom Dataset Upload** — Upload your own `.xlsx` or `.csv`
- 🔍 **Selective Chart View** — Show all or pick specific charts from sidebar
- 📱 **Wide Layout** — Optimized for large screens

---

## 🛠️ Tech Stack | التقنيات المستخدمة <a name="tech-stack"></a>

| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat) | Core language |
| ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat) | Web app framework |
| ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?logo=plotly&logoColor=white&style=flat) | Interactive visualizations |
| ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white&style=flat) | Data manipulation |
| ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white&style=flat) | Custom styling & theming |

---

## 📁 Project Structure | هيكل المشروع <a name="project-structure"></a>

```
employee-attrition-dashboard/
│
├── app.py                  # Main Streamlit application
├── final_dataset.csv       # Default dataset (74,498 employees)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 Getting Started | كيفية التشغيل <a name="getting-started"></a>

### Prerequisites | المتطلبات

```bash
Python 3.10+
pip
```

### Installation | التثبيت

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/employee-attrition-dashboard.git
cd employee-attrition-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

### Requirements | المكتبات المطلوبة

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
openpyxl>=3.1.0
```

---

## 📊 Dashboard Sections | أقسام الداشبورد <a name="dashboard-sections"></a>

| # | Chart | Key Insight |
|---|-------|-------------|
| 1 | Attrition Overview (Donut) | 47.5% overall attrition rate |
| 2 | Attrition by Gender | Female attrition 10pts higher |
| 3 | Attrition by Age Group | 18–25 age group at 53.1% |
| 4 | Attrition by Job Role | Problem is organizational, not role-specific |
| 5 | Monthly Income Analysis | $46 salary gap — not the main driver |
| 6 | Work-Life Balance Impact | Poor WLB → 60.2% attrition |
| 7 | Overtime Impact | OT employees leave 6pts more |
| 8 | Education Level | PhD holders leave at 24.4% only |
| 9 | Correlation Heatmap | Distance strongest attrition predictor |
| 10 | Attrition by Tenure | First 5 years = danger zone |
| 11 | Marital Status × Gender | Single females leave at 72.2% |
| 12 | Company Size × Remote Work | Remote cuts attrition by 28pts |
| 13 | Performance × Satisfaction | High performer + low satisfaction = flight risk |
| 14 | Commute Distance | Longer commute → higher attrition |
| 15 | Leadership Opportunities | 95% have zero leadership path |
| 16 | Innovation Opportunities | 83% have no innovation access |
| 17 | Company Reputation | Poor reputation → 56% attrition |
| 18 | Employee Recognition | Recognition alone has 1.8% impact only |
| 19 | Job Level × Remote Work | Entry + No Remote = 69.3% ⚠️ |

---

## 🗃️ Dataset | الداتاست <a name="dataset"></a>

**EN:** The default dataset contains **74,498 employee records** with **24 variables** including:

`Age` · `Gender` · `Attrition` · `Job Role` · `Monthly Income` · `Work-Life Balance` · `Overtime` · `Education Level` · `Years at Company` · `Marital Status` · `Remote Work` · `Company Size` · `Performance Rating` · `Job Satisfaction` · `Distance from Home` · `Leadership Opportunities` · `Innovation Opportunities` · `Company Reputation` · `Employee Recognition` · `Job Level` · `Number of Promotions` · `Number of Dependents` · `Company Tenure`

**AR:** الداتاست الافتراضي يحتوي على **74,498 سجل موظف** بـ **24 متغير** يغطي الديموغرافيا والرواتب وظروف العمل والأداء.

> 💡 You can upload your own dataset via the sidebar — as long as it contains the same column names.

---

## 👨‍💻 Author | المطور <a name="author"></a>

<div align="center">

**Mostafa Nabil**
*AI Engineer | Data Analyst*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR_LINKEDIN)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github&logoColor=white)](https://github.com/YOUR_USERNAME)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-FF6B35?style=flat&logo=firefox&logoColor=white)](https://YOUR_PORTFOLIO_URL)

</div>

---

<div align="center">

⭐ **If you found this useful, give it a star!** | **لو أفادك المشروع، اعمله ستار!** ⭐

*Built with ❤️ using Streamlit & Plotly*

</div>
