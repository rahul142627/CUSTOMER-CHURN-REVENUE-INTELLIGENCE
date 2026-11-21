-- ============================================================================
-- CUSTOMER CHURN & REVENUE INTELLIGENCE
-- SCRIPT 04: REVENUE INTELLIGENCE & MONETIZATION METRICS
-- Author: Senior Data Analyst & BI Developer
-- Business Objective: Quantify Monthly Recurring Revenue (MRR), Customer Lifetime
--                     Value (CLV), revenue loss from churn, and MoM cohort trends.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CORE FINANCIAL REVENUE KPIS
-- Business Question: What is the current MRR, ARR, ARPU, and revenue lost to churn?
-- ----------------------------------------------------------------------------
SELECT 
    -- Active Monthly Recurring Revenue
    ROUND(SUM(CASE WHEN Churn_Status = 'No' THEN Monthly_Charges ELSE 0 END), 2) AS active_mrr,
    
    -- Annualized Active Recurring Revenue
    ROUND(SUM(CASE WHEN Churn_Status = 'No' THEN Monthly_Charges ELSE 0 END) * 12, 2) AS active_arr,
    
    -- Monthly Revenue Lost to Churn
    ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS monthly_revenue_lost,
    
    -- Annualized Revenue Lost to Churn
    ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END) * 12, 2) AS annualized_revenue_lost,
    
    -- Total Potential MRR (Active + Churned base)
    ROUND(SUM(Monthly_Charges), 2) AS total_potential_mrr,
    
    -- Percentage of Monthly Revenue Lost
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END) / SUM(Monthly_Charges), 2) AS pct_revenue_lost,
    
    -- Average Revenue Per User (ARPU) - Active Base
    ROUND(AVG(CASE WHEN Churn_Status = 'No' THEN Monthly_Charges ELSE NULL END), 2) AS arpu_active_customers,
    
    -- Average Revenue Per User (ARPU) - Blended Base
    ROUND(AVG(Monthly_Charges), 2) AS arpu_blended_base,
    
    -- Cumulative Historical Revenue Collected
    ROUND(SUM(Total_Charges), 2) AS cumulative_historical_revenue,
    
    -- Overall Customer Lifetime Value (CLV)
    ROUND(AVG(Total_Charges), 2) AS average_customer_lifetime_value
FROM customer_churn_clean;

-- ----------------------------------------------------------------------------
-- 2. REVENUE CONTRIBUTION BY SUBSCRIPTION PLAN
-- Business Question: Which subscription tier generates the most MRR, and which
--                    experiences the highest monetary loss?
-- ----------------------------------------------------------------------------
SELECT 
    Subscription_Plan,
    COUNT(*) AS total_subscribers,
    SUM(CASE WHEN Churn_Status = 'No' THEN 1 ELSE 0 END) AS active_subscribers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_subscribers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS plan_churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn_Status = 'No' THEN Monthly_Charges ELSE 0 END), 2) AS plan_active_mrr,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'No' THEN Monthly_Charges ELSE 0 END) / 
          (SELECT SUM(CASE WHEN Churn_Status = 'No' THEN Monthly_Charges ELSE 0 END) FROM customer_churn_clean), 2) AS pct_of_active_mrr,
    ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS plan_mrr_lost,
    ROUND(AVG(Monthly_Charges), 2) AS plan_avg_monthly_charges,
    ROUND(AVG(Total_Charges), 2) AS plan_avg_clv
FROM customer_churn_clean
GROUP BY Subscription_Plan
ORDER BY plan_active_mrr DESC;

-- ----------------------------------------------------------------------------
-- 3. REVENUE STABILITY BY CONTRACT TYPE
-- Business Question: How does contract structure affect financial predictability?
-- ----------------------------------------------------------------------------
SELECT 
    Contract_Type,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn_Status = 'No' THEN Monthly_Charges ELSE 0 END), 2) AS active_mrr,
    ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS mrr_lost,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(Tenure_Months), 1) AS avg_tenure_months,
    ROUND(AVG(Total_Charges), 2) AS avg_clv
FROM customer_churn_clean
GROUP BY Contract_Type
ORDER BY active_mrr DESC;

-- ----------------------------------------------------------------------------
-- 4. CUSTOMER LIFETIME VALUE (CLV) TIERING VIA NTILE
-- Business Question: How is historical revenue distributed across customer tiers?
-- ----------------------------------------------------------------------------
WITH customer_value_tiers AS (
    SELECT 
        CustomerID,
        Subscription_Plan,
        Contract_Type,
        Tenure_Months,
        Monthly_Charges,
        Total_Charges,
        Churn_Status,
        NTILE(4) OVER (ORDER BY Total_Charges DESC) AS value_quartile
    FROM customer_churn_clean
),
tier_labeled AS (
    SELECT 
        *,
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
    ROUND(100.0 * SUM(Total_Charges) / (SELECT SUM(Total_Charges) FROM customer_churn_clean), 2) AS pct_of_total_revenue,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS tier_churn_rate_pct
FROM tier_labeled
GROUP BY clv_tier
ORDER BY clv_tier;

-- ----------------------------------------------------------------------------
-- 5. MONTH-OVER-MONTH SIGNUP & COHORT REVENUE MOMENTUM
-- Business Question: What is the trend of monthly new customer acquisitions and
--                    associated contracted recurring revenue over recent cohorts?
-- ----------------------------------------------------------------------------
WITH monthly_cohorts AS (
    SELECT 
        SUBSTR(Signup_Date, 1, 7) AS signup_cohort_month,
        COUNT(*) AS new_customers,
        ROUND(SUM(Monthly_Charges), 2) AS cohort_monthly_billing,
        ROUND(AVG(Monthly_Charges), 2) AS cohort_arpu
    FROM customer_churn_clean
    WHERE Signup_Date >= '2024-01-01'
    GROUP BY SUBSTR(Signup_Date, 1, 7)
)
SELECT 
    signup_cohort_month,
    new_customers,
    cohort_monthly_billing,
    cohort_arpu,
    LAG(new_customers, 1) OVER (ORDER BY signup_cohort_month) AS prev_month_customers,
    ROUND(
        100.0 * (new_customers - LAG(new_customers, 1) OVER (ORDER BY signup_cohort_month)) 
        / NULLIF(LAG(new_customers, 1) OVER (ORDER BY signup_cohort_month), 0), 2
    ) AS mom_customer_growth_pct,
    LAG(cohort_monthly_billing, 1) OVER (ORDER BY signup_cohort_month) AS prev_month_billing,
    ROUND(
        100.0 * (cohort_monthly_billing - LAG(cohort_monthly_billing, 1) OVER (ORDER BY signup_cohort_month)) 
        / NULLIF(LAG(cohort_monthly_billing, 1) OVER (ORDER BY signup_cohort_month), 0), 2
    ) AS mom_revenue_growth_pct,
    ROUND(SUM(cohort_monthly_billing) OVER (ORDER BY signup_cohort_month), 2) AS cumulative_cohort_billing
FROM monthly_cohorts
ORDER BY signup_cohort_month DESC;

-- ----------------------------------------------------------------------------
-- 6. REVENUE CONCENTRATION (PARETO 80/20 PRINCIPLE)
-- Business Question: Does the top 20% of customers generate 80% of revenue?
-- ----------------------------------------------------------------------------
WITH deciles AS (
    SELECT 
        CustomerID,
        Total_Charges,
        NTILE(10) OVER (ORDER BY Total_Charges DESC) AS revenue_decile
    FROM customer_churn_clean
)
SELECT 
    revenue_decile,
    COUNT(*) AS customer_count,
    ROUND(SUM(Total_Charges), 2) AS decile_revenue,
    ROUND(100.0 * SUM(Total_Charges) / (SELECT SUM(Total_Charges) FROM customer_churn_clean), 2) AS pct_of_total_revenue,
    ROUND(SUM(SUM(Total_Charges)) OVER (ORDER BY revenue_decile) * 100.0 / 
          (SELECT SUM(Total_Charges) FROM customer_churn_clean), 2) AS cumulative_revenue_pct
FROM deciles
GROUP BY revenue_decile
ORDER BY revenue_decile;
