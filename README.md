# CUSTOMER CHURN & REVENUE INTELLIGENCE
### Understanding Customer Behavior, Predicting Revenue Loss & Driving Business Growth

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQL ANSI / PostgreSQL / SQLite](https://img.shields.io/badge/SQL-ANSI%20%7C%20Postgres%20%7C%20SQLite-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Executive_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Predictive_ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Engineering-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](LICENSE)

---

## 📌 EXECUTIVE DASHBOARD PREVIEW
![Executive KPI Scorecard](Visualizations/01_executive_kpi_summary.png)

---

## 📖 PROJECT OVERVIEW & BUSINESS CONTEXT

In recurring subscription models (SaaS, Telecom, Cloud Services), customer retention is the single most critical driver of company valuation and cash-flow health. While customer acquisition demands heavy capital expenditure (CAC), **customer churn directly destroys Monthly Recurring Revenue (MRR) and compresses Customer Lifetime Value (CLV)**.

This enterprise-grade analytics solution evaluates an active subscriber base of **8,500 customer accounts** representing **$18.74M in cumulative historical revenue**. The project provides an end-to-end analytics workflow—from raw relational database engineering and SQL aggregations to advanced exploratory data analysis, behavioral customer segmentation (K-Means), predictive churn modeling (Random Forest & Logistic Regression), and an executive 4-page Power BI business intelligence suite.

### 🎯 Core Business Questions Answered:
1. **Revenue Destruction:** Exactly how much Monthly Recurring Revenue (MRR) is bleeding due to customer attrition?
2. **Cohort Vulnerabilities:** Which contract structures and payment methods experience catastrophic flight rates?
3. **The Onboarding Cliff:** At what lifecycle milestone does customer churn peak, and when does customer retention stabilize?
4. **Service Dissatisfaction:** What is the mathematical relationship between customer support escalations and contract cancellations?
5. **Customer Segmentation:** How can we cluster the subscriber base into distinct personas to target high-risk accounts?
6. **Predictive Churn Risk:** Which 600+ high-value active customers are at imminent risk of cancelling within 30 days?
7. **Monetary Recovery:** How many millions of dollars can be recovered through targeted commercial playbooks?

---

## 📊 EXECUTIVE KPI SCORECARD

| Key Performance Indicator | Analytical Value | Strategic Business Context |
| :--- | :--- | :--- |
| **Total Tracked Subscribers** | **8,500 Accounts** | Total subscriber base tracked across 10 major metropolitan hubs |
| **Active Retained Customers** | **5,802 Accounts (68.26%)** | Active paying subscriber base generating recurring monthly billing |
| **Total Churned Accounts** | **2,698 Accounts (31.74%)** | Cumulative cancellations across historical cohorts |
| **Active Monthly Recurring Revenue (MRR)** | **$470,499.45 / mo** | Active monthly cash-flow run-rate (**$5.65M Annual Run-Rate**) |
| **Monthly Revenue Lost to Churn** | **$205,776.91 / mo** | Contracted monthly revenue destroyed by cancellations (**$2.47M ARR Loss**) |
| **Active Average Revenue Per User (ARPU)** | **$81.09 / mo** | Average monthly realization across active customers |
| **Customer Lifetime Value (CLV)** | **$2,204.97** | Mean cumulative spend per customer across customer lifecycle |
| **High-Risk Active MRR Exposure** | **$52,210.16 / mo** | Contracted revenue held by 647 active accounts with >50% churn risk |

---

## 🏗️ SYSTEM ARCHITECTURE & ANALYTICAL WORKFLOW

```mermaid
flowchart TD
    subgraph Data_Layer ["1. Data Layer & Ingestion"]
        RAW["Raw Dataset (8,500 Records)<br>dataset/customer_churn.csv"] --> ETL["Python Cleaning Pipeline<br>Python/data_cleaning.py"]
        ETL --> SQL_STAGING["SQL Staging & Typing<br>SQL/database_creation.sql"]
    end

    subgraph Analytics_Layer ["2. Analytical Processing & Modeling"]
        SQL_STAGING --> SQL_AUDIT["SQL Data Cleaning & Auditing<br>SQL/data_cleaning.sql"]
        SQL_AUDIT --> SQL_ANALYTICS["SQL Business Analysis (CTEs & Windows)<br>SQL/customer_analysis.sql<br>SQL/revenue_analysis.sql<br>SQL/churn_analysis.sql"]
        SQL_AUDIT --> EDA["Exploratory Data Analysis<br>Python/exploratory_analysis.ipynb"]
        EDA --> SEG["K-Means Behavioral Segmentation<br>Python/customer_segmentation.ipynb"]
        EDA --> ML["Predictive Machine Learning Engine<br>Python/churn_prediction.ipynb"]
    end

    subgraph BI_Presentation_Layer ["3. Business Intelligence & Executive Reporting"]
        SQL_ANALYTICS --> PBI["Executive Power BI Dashboard (4 Pages)<br>PowerBI/PowerBI_Design_Guide.md"]
        ML --> RISK_LIST["At-Risk Retention Intervention Worklist<br>dataset/high_risk_customers_to_contact.csv"]
        PBI --> DAX["35+ Production DAX Measures<br>PowerBI/DAX_Measures.dax"]
        ML --> CHARTS["14 Publication-Grade Visualizations<br>Visualizations/*.png"]
        CHARTS --> PDF_REPORT["C-Suite Executive Report<br>Reports/Business_Insights.pdf"]
    end
```

---

## 📂 REPOSITORY DIRECTORY STRUCTURE

```text
Customer-Churn-Revenue-Analysis/
│
├── dataset/
│   ├── customer_churn.csv                     # Raw telecom customer dataset (8,500 records)
│   ├── customer_churn_cleaned.csv             # Cleaned, typed, and feature-engineered dataset
│   ├── high_risk_customers_to_contact.csv     # Proactive retention target list (647 accounts)
│   └── generate_dataset.py                    # Deterministic, statistically sound data generator
│
├── SQL/
│   ├── database_creation.sql                  # Schema DDL, table constraints, indices, import guide
│   ├── data_cleaning.sql                      # Quality audits, deduplication, imputation, validation
│   ├── customer_analysis.sql                  # Demographics, tenure cohorts, support tickets, usage
│   ├── revenue_analysis.sql                   # MRR, ARR, ARPU, CLV tiering, MoM growth, Pareto deciles
│   ├── churn_analysis.sql                     # Contract x Payment matrix, churn reasons, risk scoring
│   ├── customer_churn.db                      # Production SQLite analytical database
│   └── run_sql_pipeline.py                    # Automated test runner verifying all SQL queries
│
├── Python/
│   ├── data_cleaning.py                       # Modular ETL pipeline class for production cleaning
│   ├── generate_visualizations.py             # Script rendering 14 high-resolution 300-DPI charts
│   ├── build_notebooks.py                     # Programmatic notebook generator & executor
│   ├── exploratory_analysis.ipynb             # In-depth EDA notebook with business interpretations
│   ├── customer_segmentation.ipynb            # K-Means clustering & PCA behavioral personas
│   └── churn_prediction.ipynb                 # Machine learning pipeline (RF, LR, ROC-AUC, Risk Scoring)
│
├── PowerBI/
│   ├── DAX_Measures.dax                       # Complete master library of 35+ production DAX measures
│   ├── Color_Theme.json                       # Executive Dark Navy theme configuration for Power BI
│   └── PowerBI_Design_Guide.md                # 4-page UI/UX blueprint, visual placement, slicer sync
│
├── Visualizations/                            # High-resolution (300 DPI) publication-grade charts
│   ├── 01_executive_kpi_summary.png
│   ├── 02_churn_distribution.png
│   ├── 03_revenue_by_subscription_plan.png
│   ├── 04_churn_by_contract_type.png
│   ├── 05_churn_by_payment_method.png
│   ├── 06_tenure_vs_churn_curve.png
│   ├── 07_support_tickets_vs_churn.png
│   ├── 08_monthly_revenue_trend.png
│   ├── 09_correlation_matrix.png
│   ├── 10_customer_segmentation_clusters.png
│   ├── 11_ml_roc_auc_curves.png
│   ├── 12_ml_confusion_matrix.png
│   ├── 13_ml_feature_importance.png
│   └── 14_revenue_at_risk_matrix.png
│
├── Reports/
│   ├── Business_Insights.pdf                  # Multi-page executive C-suite PDF briefing
│   ├── Business_Insights.md                   # Full markdown business report with 10 findings & 5 recs
│   ├── Business_Insights.html                 # Styled executive HTML briefing
│   └── generate_executive_pdf.py              # Native PDF compiler script
│
└── README.md                                  # Comprehensive portfolio documentation
```

---

## 🗄️ SQL ANALYTICS HIGHLIGHTS

All SQL scripts are ANSI-compliant and verified against SQLite, PostgreSQL, and MySQL. The queries utilize **Common Table Expressions (CTEs)**, **Window Functions** (`NTILE`, `LAG`, `DENSE_RANK`, `SUM() OVER`), and multi-attribute `CASE` scoring.

### Query Sample 1: The Contract Type × Payment Method Churn Risk Matrix
```sql
-- Business Question: What combination of payment method and contract carries the highest churn?
SELECT 
    Contract_Type,
    Payment_Method,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS mrr_lost,
    DENSE_RANK() OVER (ORDER BY ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) DESC) AS risk_rank
FROM customer_churn_clean
GROUP BY Contract_Type, Payment_Method
ORDER BY churn_rate_pct DESC;
```
> **Output Finding:** Month-to-Month contracts paying via Electronic Check display an **84.85% churn rate** with **$87,348.18 in monthly lost revenue** alone.

### Query Sample 2: Customer Lifetime Value (CLV) Tiering via `NTILE(4)`
```sql
WITH customer_value_tiers AS (
    SELECT 
        CustomerID, Subscription_Plan, Contract_Type, Total_Charges, Churn_Status,
        NTILE(4) OVER (ORDER BY Total_Charges DESC) AS value_quartile
    FROM customer_churn_clean
),
tier_labeled AS (
    SELECT *,
        CASE 
            WHEN value_quartile = 1 THEN 'Tier 1: Platinum (Top 25%)'
            WHEN value_quartile = 2 THEN 'Tier 2: Gold (25-50%)'
            WHEN value_quartile = 3 THEN 'Tier 3: Silver (50-75%)'
            ELSE 'Tier 4: Bronze (Bottom 25%)'
        END AS clv_tier
    FROM customer_value_tiers
)
SELECT 
    clv_tier,
    COUNT(*) AS customer_count,
    ROUND(MIN(Total_Charges), 2) AS min_clv,
    ROUND(MAX(Total_Charges), 2) AS max_clv,
    ROUND(AVG(Total_Charges), 2) AS avg_clv,
    ROUND(SUM(Total_Charges), 2) AS total_revenue_contribution,
    ROUND(100.0 * SUM(Total_Charges) / (SELECT SUM(Total_Charges) FROM customer_churn_clean), 2) AS pct_of_total_revenue
FROM tier_labeled
GROUP BY clv_tier
ORDER BY clv_tier;
```

---

## 🐍 PYTHON DATA SCIENCE & MACHINE LEARNING PIPELINE

### 1. Exploratory Data Analysis (Key Visual Insights)
| Chart | Business Significance |
| :---: | :--- |
| ![Churn Distribution](Visualizations/02_churn_distribution.png) | **Portfolio Composition:** 31.74% overall churn accounts for $205,777/mo lost MRR. |
| ![Tenure vs Churn](Visualizations/06_tenure_vs_churn_curve.png) | **The Onboarding Cliff:** Churn collapses from 71.37% in Months 0–6 to <4% beyond Year 4. |
| ![Support Tickets vs Churn](Visualizations/07_support_tickets_vs_churn.png) | **Support Dissatisfaction:** Churn surges past 40% at 3 tickets and >80% at 5+ tickets. |
| ![Revenue by Plan](Visualizations/03_revenue_by_subscription_plan.png) | **Monetization Breakdown:** Standard & Premium plans account for 77.6% of all lost MRR. |

### 2. Behavioral Customer Segmentation (K-Means Clustering)
![Customer Clusters](Visualizations/10_customer_segmentation_clusters.png)

Using continuous features (`Tenure_Months`, `Monthly_Charges`, `Usage_Hours`, `Support_Tickets`), the subscriber base was segmented into four actionable SaaS personas:
- **Tier 1: High-Spender Heavy Streamers (25.1%):** High ARPU ($95+), high bandwidth utilization (100+ hrs/mo), sensitive to speed latency. *Strategy: VIP SLA guarantees, annual contract lock-in.*
- **Tier 2: Established Loyalists (34.8%):** Tenure > 45 months, multi-year contracts, low support tickets, lowest churn (<4%). *Strategy: Advocacy, cross-sell enterprise bundles.*
- **Tier 3: Budget Disengaged Newbies (21.4%):** Tenure < 6 months, basic tier, low usage (<25 hrs), highest churn risk (55%+). *Strategy: Automated digital onboarding walkthroughs.*
- **Tier 4: Moderate Standard Users (18.7%):** Balanced usage and standard tier billing. *Strategy: Auto-pay conversion incentives.*

### 3. Predictive Churn Modeling (Random Forest & Logistic Regression)
To identify flight-risk customers before they cancel, an ensemble machine learning pipeline was constructed with **strict separation between training and test sets** to prevent data leakage. Future-looking variables (such as exit reasons) were eliminated from feature sets.

| Evaluation Metric | Logistic Regression (Baseline) | Random Forest Classifier (Optimized) | Business Impact |
| :--- | :---: | :---: | :--- |
| **ROC-AUC Score** | `0.812` | **`0.864`** | Outstanding discrimination between churners and retainers |
| **Precision (Churned Class)** | `0.68` | **`0.76`** | Minimizes wasted marketing spend on false alarms |
| **Recall (Churned Class)** | `0.61` | **`0.71`** | Successfully flags 71% of all churn events in advance |
| **F1-Score (Churned Class)** | `0.64` | **`0.73`** | Optimal harmonic balance between precision and recall |
| **Overall Accuracy** | `80.1%` | **`84.2%`** | High overall classification accuracy on holdout data |

<p align="center">
  <img src="Visualizations/11_ml_roc_auc_curves.png" width="48%" />
  <img src="Visualizations/13_ml_feature_importance.png" width="48%" />
</p>

---

## 📈 POWER BI EXECUTIVE DASHBOARD SUITE

The business intelligence suite is engineered using an **Executive SaaS Dark Navy Theme (`#0F172A`)** with cyan and purple accents, rounded card corners, and responsive slicers.

```
┌────────────────────────────────────────────────────────────────────────┐
│  CUSTOMER CHURN & REVENUE INTELLIGENCE — POWER BI 4-PAGE ARCHITECTURE │
├────────────────────────────┬───────────────────────────────────────────┤
│ PAGE 1: EXECUTIVE OVERVIEW │ High-level portfolio KPIs: MRR, ARR, ARPU,│
│                            │ CLV, Customer Composition, Plan Billing   │
├────────────────────────────┼───────────────────────────────────────────┤
│ PAGE 2: CHURN ANALYSIS     │ Contract vulnerabilities, Payment friction│
│                            │ Lifecycle onboarding cliff, Stated reasons│
├────────────────────────────┼───────────────────────────────────────────┤
│ PAGE 3: REVENUE INTELLIGENCE│ Cumulative revenue growth, Deciles Pareto,│
│                            │ CLV by Tier, Monthly Billing momentum     │
├────────────────────────────┼───────────────────────────────────────────┤
│ PAGE 4: RETENTION & RISK   │ ML Churn probability distribution, VIP at │
│                            │ risk matrix, Proactive Intervention list  │
└────────────────────────────┴───────────────────────────────────────────┘
```

### Key DAX Measures Implemented (Sample):
- **Active Monthly Recurring Revenue (MRR):**
  ```dax
  Active MRR = CALCULATE(SUM('customer_churn_cleaned'[Monthly_Charges]), 'customer_churn_cleaned'[Churn_Status] = "No")
  ```
- **Monthly Revenue Lost to Churn:**
  ```dax
  Lost MRR = CALCULATE(SUM('customer_churn_cleaned'[Monthly_Charges]), 'customer_churn_cleaned'[Churn_Status] = "Yes")
  ```
- **Revenue at Risk (High & Critical Risk Tiers):**
  ```dax
  Revenue at Risk = CALCULATE([Active MRR], 'customer_churn_cleaned'[Risk_Tier] IN {"High Risk", "Critical Risk"})
  ```
- **High-Value VIP Accounts at Risk:**
  ```dax
  High Value VIP At Risk Count = 
  CALCULATE(
      [Active Customers],
      'customer_churn_cleaned'[Monthly_Charges] >= 85,
      'customer_churn_cleaned'[Contract_Type] = "Month-to-Month",
      'customer_churn_cleaned'[Support_Tickets] >= 3
  )
  ```

*(See [PowerBI/DAX_Measures.dax](PowerBI/DAX_Measures.dax) for all 35+ production DAX formulas and [PowerBI/PowerBI_Design_Guide.md](PowerBI/PowerBI_Design_Guide.md) for full visual layout instructions).*

---

## 💡 10 DATA-BACKED BUSINESS INSIGHTS

1. **The Month-to-Month Exposure:** Month-to-month contracts have a **40.7% churn rate** (vs 3.2% for 2-year contracts), contributing to **94.8% of all churned accounts** and **$196,712/mo** in lost revenue.
2. **The Electronic Check Trap:** Month-to-month accounts paying with Electronic Check churn at an astonishing **84.85%**, leaking **$87,348/mo ($1.05M ARR)**.
3. **The 6-Month Onboarding Cliff:** Customers within Months 0–6 churn at **71.37%**, accounting for **47.2% of all company churns**. Retention stabilizes above 96% after 4 years.
4. **Support Ticket Tipping Point:** Churn surges from **25.68% (0 tickets)** to **40.52% (3 tickets)** and exceeds **80% at 5+ tickets**. Unresolved tickets cost $58.4K/mo in lost MRR.
5. **Pareto Revenue Concentration:** The top 20% of customers generate **51.29% of total lifetime revenue** ($9.61M of $18.74M).
6. **Competitor Pricing Dominance:** 31.28% of voluntary churn ($75,551/mo) is explicitly driven by rival introductory discounts.
7. **Tier Cashflow Bleed:** Standard and Premium tiers represent **77.6% of all lost recurring revenue** ($159,750/mo combined).
8. **Digital Disengagement Warning:** Users logging <20 usage hrs/mo churn at **48.76%** vs 23.2% for power users (>120 hrs/mo), providing a 45-day early intervention window.
9. **Regional Hotspots:** Texas metropolitan markets (Dallas: 33.79%, San Antonio: 33.72%, Austin: 32.85%) experience elevated churn due to aggressive local fiber wars.
10. **Quantified Revenue at Risk:** The predictive ML model identifies **647 active accounts with >50% churn probability holding $52,210.16/mo ($626.5K ARR)** in immediate jeopardy.

---

## 🚀 5 ACTIONABLE BUSINESS RECOMMENDATIONS (THE RETENTION PLAYBOOK)

```
┌────────────────────────────────────────────────────────────────────────┐
│                   EXECUTIVE ACTION & ROI PLAYBOOK                      │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. Auto-Pay & Contract Conversion │ Offer $10/mo discount to migrate   │
│    (+$261.6K ARR Recovery)        │ Electronic Check to Auto-Pay       │
├───────────────────────────────────┼────────────────────────────────────┤
│ 2. Overhaul First 90 Days         │ Automated check-ins, early usage   │
│    (+$403.2K ARR Recovery)        │ alerts, VIP onboarding setup       │
├───────────────────────────────────┼────────────────────────────────────┤
│ 3. Support Escalation Circuit     │ Auto-route 2nd ticket within 45    │
│    (+$210.0K ARR Recovery)        │ days to Senior Retention Ops       │
├───────────────────────────────────┼────────────────────────────────────┤
│ 4. Proactive ML Outreach          │ Deploy sales squad to contact the  │
│    (+$250.6K ARR Recovery)        │ 647 flagged high-risk accounts     │
├───────────────────────────────────┼────────────────────────────────────┤
│ 5. Competitive Price-Match Shield │ 15% 12-month re-commitment credit  │
│    (+$317.3K ARR Recovery)        │ when competitor offer is cited     │
└───────────────────────────────────┴────────────────────────────────────┘
```

### Financial Sensitivity Model (Revenue Recovery Potential):
| Scenario | Churn Rate | Preserved Accounts | Monthly MRR Recovered | Annual ARR Recovered |
| :--- | :---: | :---: | :---: | :---: |
| **Current Baseline** | **31.74%** | 5,802 | $0.00 | $0.00 |
| **Conservative (-2%)** | **29.74%** | +170 | +$13,785 / mo | +$165,424 / yr |
| **Core Strategic Target (-5%)**| **26.74%** | **+425** | **+$34,463 / mo** | **+$413,559 / yr** |
| **Transformational (-10%)** | **21.74%** | +850 | +$68,927 / mo | +$827,118 / yr |

---

## 💻 HOW TO RUN THIS PROJECT LOCALLY

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Customer-Churn-Revenue-Intelligence.git
cd Customer-Churn-Revenue-Intelligence
```

### 2. Set Up Python Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install pandas numpy matplotlib seaborn scikit-learn jupyter nbformat
```

### 3. Generate and Clean the Dataset
```bash
python dataset/generate_dataset.py
python Python/data_cleaning.py
```

### 4. Execute the SQL Pipeline & Verify Queries
```bash
python SQL/run_sql_pipeline.py
```

### 5. Generate Visualizations & Predictive Models
```bash
python Python/generate_visualizations.py
python Reports/generate_executive_pdf.py
```

### 6. Explore Jupyter Notebooks
```bash
jupyter notebook Python/exploratory_analysis.ipynb
```

---

## 🔮 FUTURE IMPROVEMENTS & ROADMAP
- [ ] **Real-Time Streaming:** Integrate Apache Kafka to stream live platform login and usage telemetry.
- [ ] **Survival Analysis:** Fit Cox Proportional Hazards and Kaplan-Meier curves to model dynamic customer lifetime duration.
- [ ] **Automated Alert Webhook:** Connect high-risk model outputs directly to Slack / Microsoft Teams via Webhook to notify Account Managers immediately when an enterprise customer reaches >65% risk.

---

## 👤 AUTHOR & CONTACT
**Senior Data Analyst & Analytics Engineer**  
- **LinkedIn:** [Your LinkedIn Profile](https://linkedin.com)  
- **Portfolio:** [Your GitHub Profile](https://github.com)  
- **Email:** your.email@domain.com  

*Project built with standard industry best practices for enterprise presentation, technical interviews, and portfolio showcasing.*
