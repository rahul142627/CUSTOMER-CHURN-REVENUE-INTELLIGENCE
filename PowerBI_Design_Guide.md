# Executive Power BI Dashboard Implementation Blueprint
## SaaS Customer Churn & Revenue Intelligence Platform

This document serves as the master engineering and design blueprint for constructing the 4-page executive Power BI dashboard for the **Customer Churn & Revenue Intelligence** analytics solution.

---

## 1. Environment & Canvas Setup

### 1.1 Canvas Properties
- **Page Size:** 16:9 Widescreen (`1920 px` width × `1080 px` height).
- **Theme:** Import `PowerBI/Color_Theme.json` via **View > Themes > Browse for themes**.
- **Page Background:** `#0F172A` (Slate 900 Dark Navy), Transparency: `0%`.
- **Card & Container Fill:** `#1E293B` (Slate 800 Charcoal Navy), Border Radius: `10 px`, Border Color: `#334155`.
- **Primary Color Palette:**
  - Cyan Accent (Primary): `#06B6D4`
  - Indigo / Purple Accent (Secondary): `#818CF8`
  - Emerald Green (Retention / Healthy): `#10B981`
  - Rose Coral (Churn / Losses): `#F43F5E`
  - Amber (At Risk / Warnings): `#F59E0B`
  - Off-White Text: `#F8FAFC`
  - Slate Muted Text: `#94A3B8`

### 1.2 Data Source Connection
1. In Power BI Desktop, click **Get Data > Text/CSV** and select `dataset/customer_churn_cleaned.csv`.
2. Confirm the schema types:
   - `CustomerID`: Text
   - `Age`, `Tenure_Months`, `Support_Tickets`: Whole Number
   - `Monthly_Charges`, `Total_Charges`, `Usage_Hours`: Fixed Decimal / Decimal Number
   - `Last_Login_Date`, `Signup_Date`: Date
3. Create a dedicated **Measures Table** named `_DAX_Measures` using Home > Enter Data.
4. Copy and paste all 35+ production DAX formulas from `PowerBI/DAX_Measures.dax`.

---

## 2. Interactive Global Navigation & Slicer Bar (Present on All 4 Pages)

Place a streamlined horizontal top header bar and a left-hand or top slicer bar (`Y: 10 px` to `Y: 120 px`):
- **Logo / Title:** "CUSTOMER CHURN & REVENUE INTELLIGENCE | EXECUTIVE BI" (Segoe UI Semibold, 18 pt, `#F8FAFC`).
- **Dynamic Headline Card:** Measure `[Dynamic Executive Headline]`.
- **Slicers (Dropdown with Search enabled):**
  1. `Signup_Date` (Relative Date / Date Range Slider)
  2. `Subscription_Plan` (`Basic`, `Standard`, `Premium`, `Enterprise`)
  3. `Contract_Type` (`Month-to-Month`, `One Year`, `Two Year`)
  4. `Payment_Method` (`Electronic Check`, `Credit Card`, `Bank Transfer`, `Mailed Check`)
  5. `Age_Group` (`<25`, `25-39`, `40-54`, `55-64`, `65+`)
  6. `Churn_Status` (`Yes`, `No`)
- **Sync Slicers:** Enable **View > Sync Slicers** across all 4 pages so executive filters persist seamlessly across views.

---

## 3. Detailed Page Layouts & Visual Configurations

```
┌────────────────────────────────────────────────────────────────────────┐
│ TOP HEADER: SaaS Revenue Intelligence Platform | Dynamic KPI Headline   │
│ SLICERS: Date Range | Plan | Contract Type | Payment Method | Churn     │
├──────────────┬──────────────┬──────────────┬──────────────┬────────────┤
│ KPI CARD 1   │ KPI CARD 2   │ KPI CARD 3   │ KPI CARD 4   │ KPI CARD 5 │
│ Total Cust   │ Active Cust  │ Churned Cust │ Churn Rate % │ Active MRR │
├──────────────┴──────────────┴──────────────┼──────────────┴────────────┤
│ CHART 1: Monthly Trend / Core Metric       │ CHART 2: Plan Breakdown   │
│ (Area / Line Chart)                        │ (Clustered Bar Chart)     │
├─────────────────────────────┬──────────────┴──────────────┬────────────┤
│ CHART 3: Interaction Matrix │ CHART 4: Lifecycle Breakdown│ TOOLTIPS & │
│ (Horizontal Bar)            │ (Donut / Matrix)            │ DRILLDOWN  │
└─────────────────────────────┴─────────────────────────────┴────────────┘
```

---

### PAGE 1: EXECUTIVE OVERVIEW
**Objective:** Deliver high-level portfolio health, MRR stability, customer retention, and contraction metrics to the C-Suite.

#### 1. Top Executive KPI Cards (Row 1: Y = 130 px, Height = 110 px)
| KPI Card | Measure | Display Format | Accent Color | Subtitle / Target Callout |
| :--- | :--- | :--- | :--- | :--- |
| **Total Customers** | `[Total Customers]` | `#,##0` (8,500) | `#06B6D4` (Cyan) | "Total subscriber database" |
| **Active Customers** | `[Active Customers]` | `#,##0` (5,802) | `#10B981` (Emerald) | "68.3% Retention Rate" |
| **Churned Customers**| `[Churned Customers]` | `#,##0` (2,698) | `#F43F5E` (Rose) | "31.7% Overall Churn Rate" |
| **Active MRR** | `[Active MRR]` | `$#,##0` ($470,499) | `#818CF8` (Purple) | "$5.65M Annual Run-Rate" |
| **Monthly Lost MRR** | `[Lost MRR]` | `$#,##0` ($205,777) | `#F43F5E` (Rose) | "$2.47M Annual Churn Loss" |
| **Active ARPU** | `[ARPU Active]` | `$#,##0.00` ($81.09) | `#06B6D4` (Cyan) | "Monthly spend per active user" |
| **Avg Lifetime Value**| `[Customer Lifetime Value (CLV)]` | `$#,##0.00` ($2,205) | `#F59E0B` (Amber) | "Historical revenue per account" |

#### 2. Visual Layout (Row 2 & 3: Y = 260 px to 1040 px)
- **Visual 1 (Top Left): Monthly Recurring Revenue Trend (2024–2026)**
  - *Type:* Line & Stacked Area Chart.
  - *X-Axis:* `Signup_Date` (Year-Month hierarchy).
  - *Y-Axis:* `[Active MRR]` (Line in Cyan `#06B6D4`), `[Total Revenue]` (Area in Purple `#818CF8`).
  - *Tooltip:* `[MoM MRR Growth %]`, `[New Customer Signups]`.
- **Visual 2 (Top Right): Monthly Revenue by Subscription Plan: Active vs Lost**
  - *Type:* Clustered Column Chart.
  - *X-Axis:* `Subscription_Plan` (`Basic`, `Standard`, `Premium`, `Enterprise`).
  - *Y-Axis:* `[Active MRR]` (Cyan `#06B6D4`), `[Lost MRR]` (Rose `#F43F5E`).
  - *Data Labels:* Enabled (`$#,##0`).
- **Visual 3 (Bottom Left): Active vs Churned Composition**
  - *Type:* Donut Chart.
  - *Legend:* `Churn_Status`.
  - *Values:* `[Total Customers]` (Inner radius: 65%).
  - *Colors:* Active (`#10B981`), Churned (`#F43F5E`).
- **Visual 4 (Bottom Right): Contract Distribution & Retention Security**
  - *Type:* 100% Stacked Bar Chart.
  - *Y-Axis:* `Contract_Type`.
  - *X-Axis:* `[Total Customers]`.
  - *Legend:* `Churn_Status`.
  - *Insight Highlight:* Month-to-month contracts visually dominate churn volume.

---

### PAGE 2: CUSTOMER CHURN ANALYSIS
**Objective:** Dissect behavioral attrition triggers, contract vulnerabilities, payment friction, and stated churn reasons.

#### Visual Layout:
- **Visual 1 (Top Left): Churn Rate by Contract Type (Horizontal Bar)**
  - *Y-Axis:* `Contract_Type`.
  - *X-Axis:* `[Churn Rate %]`.
  - *Data Labels:* `40.7%` Month-to-Month, `11.1%` One Year, `3.2%` Two Year.
  - *Conditional Formatting:* Fill bars based on `[Churn Rate %]` (<15% Green, 15-30% Amber, >30% Rose).
- **Visual 2 (Top Right): The Onboarding Cliff: Churn by Tenure Cohort**
  - *Type:* Area Chart with Markers.
  - *X-Axis:* `Tenure_Cohort` (`0-6 Mos`, `7-12 Mos`, `13-24 Mos`, `25-48 Mos`, `49+ Mos`).
  - *Y-Axis:* `[Churn Rate %]`.
  - *Annotation Callout:* "71.4% of customers churn in Months 0–6!".
- **Visual 3 (Middle Left): Churn Rate by Payment Method (Friction Analysis)**
  - *Type:* Clustered Column Chart.
  - *X-Axis:* `Payment_Method`.
  - *Y-Axis:* `[Churn Rate %]`.
  - *Insight:* Highlights Electronic Check attrition (84.8% on monthly contracts).
- **Visual 4 (Middle Right): Support Ticket Escalation Tipping Point**
  - *Type:* Column Chart.
  - *X-Axis:* `Support_Tickets` (0 to 8).
  - *Y-Axis:* `[Churn Rate %]`.
  - *Insight:* Shows steep escalation from 25.7% (0 tickets) to 40.5% (3 tickets) and 80%+ (5+ tickets).
- **Visual 5 (Bottom Full-Width): Stated Churn Reasons & Lost MRR Waterfall**
  - *Type:* Horizontal Bar Chart sorted by `[Lost MRR]`.
  - *Y-Axis:* `Churn_Reason`.
  - *X-Axis:* `[Lost MRR]`.
  - *Data Label:* Value and `% of Total Lost MRR`.

---

### PAGE 3: REVENUE INTELLIGENCE
**Objective:** Provide deep financial transparency into MRR expansion, unit economics (ARPU/CLV), customer value tiers, and revenue concentration.

#### Visual Layout:
- **Visual 1 (Top Left): Cumulative Revenue Growth & Monthly Invoicing**
  - *Type:* Stacked Area Chart.
  - *X-Axis:* `Signup_Date` (Monthly).
  - *Values:* `[Total Revenue]` ($18.74M cumulative).
- **Visual 2 (Top Right): Customer Lifetime Value (CLV) by Subscription Tier**
  - *Type:* Clustered Bar Chart.
  - *Y-Axis:* `Subscription_Plan`.
  - *Values:* `[Customer Lifetime Value (CLV)]`.
  - *Tooltip:* `[ARPU Active]`, `[Avg Tenure Months]`.
- **Visual 3 (Bottom Left): Pareto Revenue Concentration (Deciles Analysis)**
  - *Type:* Line & Stacked Column Chart.
  - *X-Axis:* `Revenue_Decile` (Top 10% to Bottom 10%).
  - *Column:* `[Decile Revenue]`.
  - *Line:* `[Cumulative Revenue %]`.
  - *Insight:* Confirms top 20% of accounts generate ~51.3% of cumulative revenue.
- **Visual 4 (Bottom Right): MRR at Risk by Customer Value Quartile**
  - *Type:* Matrix / Heatmap Grid.
  - *Rows:* `CLV_Tier` (Platinum, Gold, Silver, Bronze).
  - *Columns:* `Contract_Type`.
  - *Values:* `[Active MRR]`, `[Revenue at Risk]`, `[Churn Rate %]`.

---

### PAGE 4: CUSTOMER RETENTION & RISK (PROACTIVE SUCCESS ENGINE)
**Objective:** Arm Customer Success, Account Managers, and Retention Teams with real-time risk scores and actionable account intervention lists.

#### Visual Layout:
- **Visual 1 (Top Left KPI Cards):**
  - `[High Risk Customer Count]` (636 accounts)
  - `[Critical Risk Customer Count]` (11 accounts)
  - `[Revenue at Risk]` ($52,210 / month)
  - `[Annualized Revenue at Risk]` ($626,522 / year)
- **Visual 2 (Top Center): Active Accounts by Risk Tier**
  - *Type:* Donut Chart.
  - *Legend:* `Risk_Tier` (Low, Medium, High, Critical).
  - *Values:* `[Active Customers]`.
  - *Colors:* Low (`#10B981`), Medium (`#F59E0B`), High (`#FB7185`), Critical (`#F43F5E`).
- **Visual 3 (Top Right): Churn Probability Distribution**
  - *Type:* Histogram / Density Bar.
  - *X-Axis:* Predicted Churn Probability Bins (0–100%).
  - *Y-Axis:* Customer Count.
- **Visual 4 (Bottom Left): High-Value Accounts at Risk Matrix (Scatter Plot)**
  - *X-Axis:* `Monthly_Charges` ($20 to $150).
  - *Y-Axis:* `Risk_Score` (0 to 100).
  - *Bubble Size:* `Total_Charges` (CLV).
  - *Color:* `Contract_Type`.
  - *Quadrant Lines:* X = $85 (VIP spend), Y = 50 (High Risk).
- **Visual 5 (Bottom Right): Proactive Intervention Worklist (Interactive Table)**
  - *Fields:* `CustomerID`, `City`, `Subscription_Plan`, `Contract_Type`, `Monthly_Charges`, `Support_Tickets`, `Usage_Hours`, `Risk_Score`, `Risk_Tier`.
  - *Sort:* `Monthly_Charges` DESC, `Risk_Score` DESC.
  - *Conditional Formatting:* Apply bold red tag if `Risk_Score >= 70`.

---

## 4. Quality Checklist & Verification
- [x] All 35+ DAX measures verified and referencing consistent column names.
- [x] Color theme aligns with SaaS Dark Navy (`#0F172A`) and Cyan/Purple accents.
- [x] Slicers synchronized across all 4 pages.
- [x] Filter contexts tested: selecting `Contract_Type = "Month-to-Month"` instantly updates KPIs, risk charts, and tables across all views.
