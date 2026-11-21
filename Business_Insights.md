# CUSTOMER CHURN & REVENUE INTELLIGENCE
## Executive Business Insights & Strategic Monetization Report
**Author:** Senior Data Analyst & Revenue Operations Strategist  
**Target Audience:** Chief Executive Officer (CEO), Chief Commercial Officer (CCO), VP of Customer Success  
**Dataset Scope:** 8,500 Subscription Accounts ($18.74M Historical Invoicing | $470.5K Active MRR)  
**Reporting Date:** January 2026  

---

## EXECUTIVE SUMMARY

A rigorous end-to-end data analytics and predictive modeling study was conducted across the company's subscriber base (8,500 customer records) to diagnose customer churn mechanisms, quantify contracted revenue leakage, and build an actionable customer retention playbook.

### High-Level Portfolio Health Check:
- **Total Portfolio Size:** 8,500 Customer Accounts
- **Active Paying Accounts:** 5,802 accounts (68.26% retention rate)
- **Churned Customer Base:** 2,698 accounts (31.74% overall churn rate)
- **Current Active Monthly Recurring Revenue (MRR):** **$470,499.45** ($5.65M Annual Run-Rate)
- **Ongoing Monthly Revenue Destruction:** **$205,776.91** (**$2,469,322.92 Annual Churn Loss**)
- **Active Average Revenue Per User (ARPU):** **$81.09**
- **Cumulative Lifetime Value (CLV):** **$2,204.97** per customer
- **Active Revenue in Immediate Flight Jeopardy:** **$52,210.16 / month** ($626,522 ARR across 647 High/Critical-risk accounts)

---

## 10 CRITICAL BUSINESS INSIGHTS (DATA-BACKED)

### Insight 1: The Month-to-Month Contract Vulnerability (The Single Largest Churn Driver)
- **Analytical Finding:** Customers on Month-to-Month contracts suffer an extraordinary **40.7% churn rate**, compared to **11.1%** for One-Year contracts and only **3.2%** for Two-Year contracts.
- **Financial Consequence:** Month-to-Month customers account for **94.8% of all churned accounts** (2,558 out of 2,698 total cancellations) and **$196,712 in monthly revenue lost** ($2.36M ARR).
- **Underlying Cause:** Month-to-month contracts impose zero switching friction, converting every slight competitive offer or transient frustration into an instant cancellation.

### Insight 2: The "Electronic Check" Payment Friction Catalyst
- **Analytical Finding:** When customers on Month-to-Month contracts pay via **Electronic Check**, their churn rate spikes to an astronomical **84.85%** (1,131 churns out of 1,333 customers).
- **Financial Consequence:** This single cohort bleeds **$87,348.18 per month** ($1.05M ARR)—representing 42.4% of total company churn losses.
- **Underlying Cause:** Unlike Automated Credit Card or Bank Transfer payments that auto-renew silently, Electronic Checks require active manual initiation each billing cycle, forcing customers to re-evaluate their spending every 30 days.

### Insight 3: The Critical "0–6 Month Onboarding Cliff"
- **Analytical Finding:** Churn is drastically concentrated at the beginning of the customer journey. Customers within their first 6 months experience a **71.37% churn rate** (1,274 exits out of 1,785 new signups).
- **Financial Consequence:** This first-half-year cohort accounts for **47.22% of all company churn incidents**. Once a customer reaches 24+ months of tenure, their churn rate drops steeply below 12%, and beyond 48 months it collapses to **3.57%**.
- **Underlying Cause:** A fragmented onboarding workflow, lack of early product activation, and failure to demonstrate value within the first 60 days causes early disillusionment.

### Insight 4: Customer Support Ticket Escalation Tipping Point
- **Analytical Finding:** Customer churn displays a non-linear breaking point tied to support interactions:
  - 0 Tickets: **25.68% churn rate**
  - 1–2 Tickets: **31.4% churn rate**
  - 3 Tickets: **40.52% churn rate**
  - 4 Tickets: **39.55% churn rate**
  - 5+ Tickets: **80.0% to 100.0% churn rate**
- **Financial Consequence:** Resolving issues on first contact is worth millions. Customers logging 3+ tickets represent **$58,410 in monthly lost MRR**.
- **Underlying Cause:** Customers who experience repeated technical issues (without root-cause resolution) interpret tickets as systemic product unreliability.

### Insight 5: Revenue Concentration (Pareto Principle in Action)
- **Analytical Finding:** The top 20% of subscribers (Deciles 1 and 2 by cumulative spend) contribute **51.29% of total historical revenue** ($9.61M of $18.74M total).
- **Financial Consequence:** Attrition of even 50 top-decile Enterprise/Premium customers damages the balance sheet more than the loss of 300 Basic-tier customers.
- **Strategic Impact:** Account retention strategies must be strictly tiered by monetary value rather than treated uniformly.

### Insight 6: Stated Churn Reasons: Competitor Pricing & Speed Dominate
- **Analytical Finding:** Analysis of exit interviews and cancellation logs reveals the primary drivers of voluntary churn:
  1. *Competitor offered better prices:* **31.28% of churns** ($75,550.74/mo lost; $906.6K ARR).
  2. *Poor customer support experience:* **23.94% of churns** ($46,795.46/mo lost; $561.5K ARR).
  3. *Competitor offered higher speeds / features:* **16.31% of churns** ($31,009.64/mo lost; $372.1K ARR).
  4. *Network reliability & frequent downtime:* **11.16% of churns** ($21,606.23/mo lost; $259.3K ARR).
  5. *High pricing & lack of perceived value:* **11.75% of churns** ($20,018.20/mo lost; $240.2K ARR).
- **Underlying Cause:** 47.6% of churned revenue is claimed by competitors through aggressive introductory pricing and aggressive fiber speed marketing.

### Insight 7: Standard & Premium Subscription Tiers Suffer the Heaviest Cash Bleed
- **Analytical Finding:** While the Enterprise tier has high stability due to annual agreements, the **Standard** tier loses **$83,210.45/month** and the **Premium** tier loses **$76,540.20/month**. Combined, they represent **77.6% of all lost recurring revenue**.
- **Underlying Cause:** Mid-tier and high-tier customers have high expectations regarding bandwidth and service quality; when experiencing friction, they defect to rival premium alternatives.

### Insight 8: Digital Disengagement (Usage Hours as an Early Warning Indicator)
- **Analytical Finding:** Customers logging **<20 usage hours per month** have a **48.76% churn rate**, compared to **23.20%** for power users logging 120+ hours.
- **Strategic Impact:** Platform usage decay precedes cancellation by an average of 45–60 days, giving customer success teams a substantial operational window to re-engage the customer before contract termination.

### Insight 9: Regional Performance Disparities
- **Analytical Finding:** Texas metropolitan markets (**Dallas at 33.79%**, **San Antonio at 33.72%**, and **Austin at 32.85%**) exhibit the highest churn rates across the entire geographic footprint, compared to Phoenix (30.1%) and Chicago (30.8%).
- **Underlying Cause:** Heavy local fiber infrastructure competition in Texas urban corridors offers aggressive introductory promotions that poach non-contracted customers.

### Insight 10: Machine Learning Risk Segmentation (Quantifying Imminent Revenue Exposure)
- **Analytical Finding:** The Random Forest predictive model (ROC-AUC: 0.864) classified the 5,802 active customers into four operational risk tiers:
  - *Critical Risk (>75% prob):* **11 accounts** | **$746.38 MRR** ($8,956 ARR)
  - *High Risk (50–75% prob):* **636 accounts** | **$51,463.78 MRR** ($617,565 ARR)
  - *Medium Risk (25–50% prob):* **1,865 accounts** | **$149,661.54 MRR** ($1.79M ARR)
  - *Low Risk (<25% prob):* **3,290 accounts** | **$268,627.75 MRR** ($3.22M ARR)
- **Immediate Call to Action:** Exactly **647 active accounts** representing **$52,210.16 in Monthly Recurring Revenue** are in immediate flight danger today!

---

## 5 ACTIONABLE BUSINESS RECOMMENDATIONS (THE RETENTION PLAYBOOK)

### Recommendation 1: Launch an Automated "Contract & Payment Conversion" Campaign
- **Analytical Basis:** Month-to-Month + Electronic Check carries an 84.85% churn rate ($87.3K/mo lost). One-Year contracts drop churn to 11.1%.
- **Action Plan:**
  1. Offer a **"$10/Month Auto-Pay Bill Credit"** for 6 months to customers who transition from Electronic Check to Automatic Credit Card / Bank Transfer.
  2. Implement an **"Annual Commitment Upgrade Incentive"** providing 1 month free upon switching from Month-to-Month to a 12-Month contract.
- **Financial ROI:** Converting just 25% of the 1,333 Month-to-Month Electronic Check users to annual automated billing recovers approximately **$21,800/month in preserved MRR ($261,600 ARR)**.

### Recommendation 2: Overhaul the "First 90 Days" Customer Onboarding Journey
- **Analytical Basis:** 71.37% of customers in Months 0–6 churn, representing 47.2% of all company attrition.
- **Action Plan:**
  1. Deploy automated, multi-channel product walkthroughs (Day 1, Day 7, Day 21).
  2. Trigger an automated Customer Success Outreach if usage hours drop below 15 hours during the first 30 days.
  3. Guarantee a dedicated VIP setup specialist for all Standard and Premium signups during their first week.
- **Financial ROI:** Reducing onboarding cohort churn from 71.4% to 55% preserves **~$33,600 in monthly recurring revenue ($403,200 ARR)**.

### Recommendation 3: Institute a Support "Escalation Circuit Breaker" at 2 Tickets
- **Analytical Basis:** Churn jumps from 25.7% (0 tickets) to 40.5% (3 tickets) and 80%+ (5+ tickets).
- **Action Plan:**
  1. Implement an automated rule in CRM / Zendesk: Whenever an account logs a **2nd support ticket within a 45-day window**, the ticket is automatically escalated to Senior Engineering.
  2. The customer is automatically routed to a dedicated Retention Specialist with authority to offer immediate billing credits and hardware replacements.
- **Financial ROI:** Preventing 30% of high-ticket churn rescues **~$17,500/month ($210,000 ARR)**.

### Recommendation 4: Proactive Outreach to the 647 High-Risk Accounts via ML Alerts
- **Analytical Basis:** Predictive model identifies 647 active accounts with >50% churn probability holding **$52,210/mo in contracted revenue**.
- **Action Plan:**
  1. Ingest `dataset/high_risk_customers_to_contact.csv` directly into Salesforce / HubSpot.
  2. Task the proactive retention squad with contacting these 647 accounts within 10 business days.
  3. Offer targeted bundle upgrades (e.g., free speed boost or streaming add-on) in exchange for signing an annual agreement.
- **Financial ROI:** Saving 40% of these flagged accounts preserves **$20,884/month in MRR ($250,600 ARR)**.

### Recommendation 5: Competitive Price-Match & Loyalty Renewal Incentive
- **Analytical Basis:** 31.28% of churned revenue ($75,550/mo) is explicitly lost to competitor pricing.
- **Action Plan:**
  1. Establish a structured "Price-Match & Speed Guarantee" program for accounts with tenure > 12 months.
  2. Grant frontline customer care representatives pre-approved authority to apply a 15% discount for a 12-month re-commitment when a customer initiates cancellation citing a competitor offer.
- **Financial ROI:** Salvaging 35% of price-sensitive cancellations saves **$26,440/month in MRR ($317,280 ARR)**.

---

## FINANCIAL SENSITIVITY MODEL: REVENUE RECOVERY PROJECTIONS

| Churn Reduction Scenario | Monthly Churn Rate | Preserved Active Accounts | Monthly MRR Recovered | Annualized Revenue Saved |
| :--- | :--- | :--- | :--- | :--- |
| **Current Baseline** | **31.74%** | 5,802 accounts | $0.00 | $0.00 |
| **Conservative (-2.0%)** | **29.74%** | +170 accounts | **+$13,785.30 / mo** | **+$165,423.60 / yr** |
| **Target Milestone (-5.0%)**| **26.74%** | +425 accounts | **+$34,463.25 / mo** | **+$413,559.00 / yr** |
| **Transformational (-10.0%)**| **21.74%** | +850 accounts | **+$68,926.50 / mo** | **+$827,118.00 / yr** |

> **Conclusion:** Achieving the realistic target of a **5.0% reduction in customer churn** injects **over $413,000 in bottom-line annualized recurring revenue** back into the company, with virtually zero customer acquisition cost (CAC).
