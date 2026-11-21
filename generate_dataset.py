"""
Customer Churn & Revenue Intelligence - Dataset Generator
Creates a realistic 8,500-record dataset for a subscription-based business with
statistically validated relationships between customer behavior, contracts,
pricing, and churn.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_telecom_churn_dataset(n_records=8500, random_seed=42):
    np.random.seed(random_seed)
    
    # 1. Customer Identifiers
    customer_ids = [f"CUST-{10000 + i}" for i in range(1, n_records + 1)]
    
    # 2. Demographics
    genders = np.random.choice(['Female', 'Male'], size=n_records, p=[0.495, 0.505])
    
    # Age distribution: slightly skewed towards working professionals (22-68)
    age_raw = np.random.normal(loc=41, scale=14, size=n_records)
    ages = np.clip(age_raw, 18, 76).astype(int)
    
    cities = [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin'
    ]
    city_weights = [0.18, 0.15, 0.12, 0.10, 0.09, 0.08, 0.07, 0.07, 0.07, 0.07]
    customer_cities = np.random.choice(cities, size=n_records, p=city_weights)
    
    # 3. Tenure (Months): Bi-modal distribution (new signups & long-term loyalists)
    # 35% early tenure (0-12 mos), 30% mid (13-36 mos), 35% long term (37-72 mos)
    tenure_group = np.random.choice([1, 2, 3], size=n_records, p=[0.35, 0.30, 0.35])
    tenures = np.zeros(n_records, dtype=int)
    for i in range(n_records):
        if tenure_group[i] == 1:
            tenures[i] = int(np.random.uniform(0, 12))
        elif tenure_group[i] == 2:
            tenures[i] = int(np.random.uniform(13, 36))
        else:
            tenures[i] = int(np.random.uniform(37, 72))
            
    # Reference Snapshot Date: 2026-01-15
    ref_date = datetime(2026, 1, 15)
    
    signup_dates = [
        (ref_date - timedelta(days=int(t * 30.4375) + np.random.randint(0, 20))).strftime('%Y-%m-%d')
        for t in tenures
    ]
    
    # 4. Subscription Plans and Contract Types
    plans = ['Basic', 'Standard', 'Premium', 'Enterprise']
    plan_weights = [0.25, 0.38, 0.25, 0.12]
    subscription_plans = np.random.choice(plans, size=n_records, p=plan_weights)
    
    # Contract Types: correlated with tenure (new users more often month-to-month)
    contracts = []
    for t in tenures:
        if t < 12:
            p_contract = [0.72, 0.20, 0.08]
        elif t < 36:
            p_contract = [0.45, 0.35, 0.20]
        else:
            p_contract = [0.22, 0.38, 0.40]
        contracts.append(np.random.choice(['Month-to-Month', 'One Year', 'Two Year'], p=p_contract))
    contracts = np.array(contracts)
    
    # 5. Services & Add-ons
    internet_services = []
    for plan in subscription_plans:
        if plan == 'Basic':
            p_int = [0.20, 0.50, 0.15, 0.15] # Fiber, DSL, Cable, None
        elif plan == 'Standard':
            p_int = [0.45, 0.35, 0.15, 0.05]
        elif plan == 'Premium':
            p_int = [0.75, 0.15, 0.10, 0.00]
        else: # Enterprise
            p_int = [0.90, 0.05, 0.05, 0.00]
        internet_services.append(np.random.choice(['Fiber Optic', 'DSL', 'Cable', 'None'], p=p_int))
    internet_services = np.array(internet_services)
    
    # 6. Payment Methods
    payment_methods = np.random.choice(
        ['Electronic Check', 'Bank Transfer (Automatic)', 'Credit Card (Automatic)', 'Mailed Check'],
        size=n_records,
        p=[0.34, 0.26, 0.27, 0.13]
    )
    
    # 7. Discounts Applied
    discounts = np.random.choice(['Yes', 'No'], size=n_records, p=[0.32, 0.68])
    
    # 8. Monthly Charges calculation (Realistic tiered pricing)
    # Basic: $29-45, Standard: $55-75, Premium: $85-110, Enterprise: $120-145
    monthly_charges = []
    for i in range(n_records):
        plan = subscription_plans[i]
        net = internet_services[i]
        disc = discounts[i]
        
        if plan == 'Basic':
            base = np.random.uniform(29.0, 42.0)
        elif plan == 'Standard':
            base = np.random.uniform(55.0, 75.0)
        elif plan == 'Premium':
            base = np.random.uniform(85.0, 110.0)
        else: # Enterprise
            base = np.random.uniform(120.0, 148.0)
            
        if net == 'Fiber Optic':
            base += np.random.uniform(10.0, 18.0)
        elif net == 'DSL':
            base += np.random.uniform(4.0, 8.0)
        elif net == 'None':
            base -= np.random.uniform(8.0, 14.0)
            
        if disc == 'Yes':
            base *= np.random.uniform(0.82, 0.92) # 8-18% discount
            
        monthly_charges.append(round(base, 2))
    monthly_charges = np.array(monthly_charges)
    
    # 9. Support Tickets & Usage Hours
    # Support tickets: 0 to 8. Poisson-like distribution, but frustated customers have more
    support_tickets = np.random.choice(
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        size=n_records,
        p=[0.38, 0.28, 0.16, 0.08, 0.04, 0.03, 0.018, 0.008, 0.004]
    )
    
    # Usage Hours (monthly hours logged in / consuming bandwidth)
    usage_hours = []
    for i in range(n_records):
        plan = subscription_plans[i]
        if plan == 'Basic':
            hrs = np.random.gamma(shape=3.0, scale=12.0) # ~36 hrs avg
        elif plan == 'Standard':
            hrs = np.random.gamma(shape=4.5, scale=14.0) # ~63 hrs avg
        elif plan == 'Premium':
            hrs = np.random.gamma(shape=6.0, scale=16.0) # ~96 hrs avg
        else:
            hrs = np.random.gamma(shape=8.0, scale=18.0) # ~144 hrs avg
        usage_hours.append(round(float(np.clip(hrs, 5.0, 240.0)), 1))
    usage_hours = np.array(usage_hours)
    
    # 10. Churn Probability Model (Realistic Multi-factor Logit)
    churn_log_odds = np.zeros(n_records)
    
    # Base intercept
    churn_log_odds += -1.45
    
    # Contract impact
    for i in range(n_records):
        if contracts[i] == 'Month-to-Month':
            churn_log_odds[i] += 1.65
        elif contracts[i] == 'One Year':
            churn_log_odds[i] += -0.55
        elif contracts[i] == 'Two Year':
            churn_log_odds[i] += -1.85
            
        # Tenure impact
        if tenures[i] <= 6:
            churn_log_odds[i] += 0.85
        elif tenures[i] <= 12:
            churn_log_odds[i] += 0.35
        elif tenures[i] <= 24:
            churn_log_odds[i] += -0.15
        elif tenures[i] <= 48:
            churn_log_odds[i] += -0.75
        else:
            churn_log_odds[i] += -1.40
            
        # Payment method impact
        if payment_methods[i] == 'Electronic Check':
            churn_log_odds[i] += 0.70
        elif payment_methods[i] == 'Mailed Check':
            churn_log_odds[i] += 0.20
        elif payment_methods[i] == 'Bank Transfer (Automatic)':
            churn_log_odds[i] += -0.45
        elif payment_methods[i] == 'Credit Card (Automatic)':
            churn_log_odds[i] += -0.55
            
        # Support tickets impact (dissatisfaction trigger)
        if support_tickets[i] >= 5:
            churn_log_odds[i] += 1.85
        elif support_tickets[i] >= 3:
            churn_log_odds[i] += 0.85
        elif support_tickets[i] == 0:
            churn_log_odds[i] += -0.30
            
        # Usage hours impact (disengagement trigger)
        if usage_hours[i] < 20.0:
            churn_log_odds[i] += 1.10
        elif usage_hours[i] < 45.0:
            churn_log_odds[i] += 0.30
        elif usage_hours[i] > 110.0:
            churn_log_odds[i] += -0.65
            
        # Price sensitivity on Fiber Optic without discount
        if internet_services[i] == 'Fiber Optic' and monthly_charges[i] > 95.0 and discounts[i] == 'No':
            churn_log_odds[i] += 0.45
            
        # Age-related digital friction (seniors with high tickets)
        if ages[i] > 60 and support_tickets[i] >= 3:
            churn_log_odds[i] += 0.40
            
    # Add small Gaussian noise for natural stochasticity
    churn_log_odds += np.random.normal(0, 0.45, size=n_records)
    
    # Calculate probabilities
    churn_probs = 1.0 / (1.0 + np.exp(-churn_log_odds))
    churn_status = np.where(churn_probs > 0.48, 'Yes', 'No')
    
    # 11. Churn Reasons & Last Login Date
    churn_reasons_pool = [
        ('Competitor offered better prices', 0.28),
        ('Competitor offered higher speeds / features', 0.22),
        ('Poor customer support experience', 0.18),
        ('Network reliability & frequent downtime', 0.14),
        ('High pricing & lack of perceived value', 0.10),
        ('Moved out of service area', 0.05),
        ('Product bugs & lack of feature updates', 0.03)
    ]
    reasons, r_probs = zip(*churn_reasons_pool)
    
    churn_reasons = []
    last_login_dates = []
    
    for i in range(n_records):
        if churn_status[i] == 'Yes':
            # Support tickets >= 4 correlates with support reason
            if support_tickets[i] >= 4 and np.random.rand() < 0.65:
                churn_reasons.append('Poor customer support experience')
            elif usage_hours[i] < 20.0 and np.random.rand() < 0.50:
                churn_reasons.append('High pricing & lack of perceived value')
            elif internet_services[i] == 'Fiber Optic' and monthly_charges[i] > 90 and np.random.rand() < 0.45:
                churn_reasons.append('Competitor offered better prices')
            else:
                churn_reasons.append(np.random.choice(reasons, p=r_probs))
                
            # Churned customers logged in between 25 and 180 days ago
            days_ago = np.random.randint(25, 180)
            last_login_dates.append((ref_date - timedelta(days=days_ago)).strftime('%Y-%m-%d'))
        else:
            churn_reasons.append('Active Customer')
            # Active customers logged in between 0 and 24 days ago
            days_ago = np.random.randint(0, 24)
            last_login_dates.append((ref_date - timedelta(days=days_ago)).strftime('%Y-%m-%d'))
            
    # 12. Total Charges calculation (Monthly_Charges * Tenure with slight noise)
    total_charges = []
    for i in range(n_records):
        t = tenures[i]
        m = monthly_charges[i]
        if t == 0:
            # New customer signed up in last few days
            total_charges.append(round(m * np.random.uniform(0.1, 0.4), 2))
        else:
            # Historical tenure with slight price adjustments
            tot = t * m * np.random.uniform(0.97, 1.02)
            total_charges.append(round(tot, 2))
            
    # Introduce real-world raw data quirks for data cleaning demonstration:
    # 14 records with blank/whitespace in Total_Charges (simulate onboarding records with unbilled status)
    total_charges_raw = [str(tc) for tc in total_charges]
    quirk_indices = np.random.choice(np.where(tenures == 0)[0], size=min(12, len(np.where(tenures == 0)[0])), replace=False)
    for q_idx in quirk_indices:
        total_charges_raw[q_idx] = " "  # Whitespace to be handled in SQL & Python cleaning
        
    df = pd.DataFrame({
        'CustomerID': customer_ids,
        'Gender': genders,
        'Age': ages,
        'City': customer_cities,
        'Tenure_Months': tenures,
        'Contract_Type': contracts,
        'Subscription_Plan': subscription_plans,
        'Monthly_Charges': monthly_charges,
        'Total_Charges': total_charges_raw,
        'Payment_Method': payment_methods,
        'Internet_Service': internet_services,
        'Support_Tickets': support_tickets,
        'Last_Login_Date': last_login_dates,
        'Usage_Hours': usage_hours,
        'Discount_Applied': discounts,
        'Churn_Status': churn_status,
        'Churn_Reason': churn_reasons,
        'Signup_Date': signup_dates
    })
    
    return df

if __name__ == '__main__':
    print("Generating telecom subscription customer churn dataset...")
    df = generate_telecom_churn_dataset(n_records=8500, random_seed=42)
    output_path = 'dataset/customer_churn.csv'
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully saved to '{output_path}'")
    print(f"Total Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nChurn Distribution:")
    print(df['Churn_Status'].value_counts(normalize=True).round(4) * 100)
    print("\nContract Type Distribution:")
    print(df['Contract_Type'].value_counts())
    print("\nSubscription Plan Breakdown:")
    print(df['Subscription_Plan'].value_counts())
