"""
Customer Churn & Revenue Intelligence - Professional Chart Generator
Produces 14 publication-grade, dark-navy themed visualizations for Power BI,
executive reports, and GitHub documentation.
File: Python/generate_visualizations.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

from matplotlib.patches import FancyBboxPatch, Rectangle

# Styling Configuration: Premium Executive Dark Navy Theme
plt.style.use('dark_background')
BG_DARK = '#0F172A'       # Slate 900
PANEL_DARK = '#1E293B'    # Slate 800
BORDER_COLOR = '#334155'  # Slate 700
TEXT_WHITE = '#F8FAFC'
TEXT_MUTED = '#94A3B8'
ACCENT_CYAN = '#06B6D4'
ACCENT_PURPLE = '#818CF8'
COLOR_CHURN = '#F43F5E'   # Rose 500
COLOR_RETAIN = '#10B981'  # Emerald 500
COLOR_WARN = '#F59E0B'    # Amber 500

plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['axes.edgecolor'] = BORDER_COLOR
plt.rcParams['axes.linewidth'] = 1.0

os.makedirs('Visualizations', exist_ok=True)
df = pd.read_csv('dataset/customer_churn_cleaned.csv')

# -----------------------------------------------------------------------------
# CHART 01: EXECUTIVE KPI SUMMARY DASHBOARD
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7), facecolor=BG_DARK)
ax.set_facecolor(BG_DARK)
ax.axis('off')

kpis = [
    ("TOTAL CUSTOMERS", f"{len(df):,}", "Total subscriber database", ACCENT_CYAN),
    ("ACTIVE CUSTOMERS", f"{(df['Churn_Status']=='No').sum():,}", "68.26% retention rate", COLOR_RETAIN),
    ("CHURNED CUSTOMERS", f"{(df['Churn_Status']=='Yes').sum():,}", "31.74% overall churn rate", COLOR_CHURN),
    ("ACTIVE MRR", f"${df[df['Churn_Status']=='No']['Monthly_Charges'].sum():,.0f}", "$5.65M annualized run-rate", ACCENT_PURPLE),
    ("MONTHLY REVENUE LOST", f"${df[df['Churn_Status']=='Yes']['Monthly_Charges'].sum():,.0f}", "$2.47M annualized churn loss", COLOR_CHURN),
    ("AVERAGE ARPU", f"${df[df['Churn_Status']=='No']['Monthly_Charges'].mean():.2f}", "Avg monthly spend per active user", ACCENT_CYAN),
    ("AVG CUSTOMER LIFETIME VALUE", f"${df['Total_Charges'].mean():,.2f}", "Mean cumulative spend per customer", COLOR_WARN),
    ("HIGH-RISK MRR EXPOSURE", "$52,210", "Active revenue in High/Critical risk", COLOR_CHURN),
]

for i, (title, val, subtext, color) in enumerate(kpis):
    row, col = divmod(i, 4)
    x = 0.05 + col * 0.235
    y = 0.55 - row * 0.45
    
    # Card Background
    rect = FancyBboxPatch((x, y), 0.21, 0.36, facecolor=PANEL_DARK, edgecolor=BORDER_COLOR,
                          boxstyle="round,pad=0.015", transform=ax.transAxes, zorder=1)
    ax.add_patch(rect)
    
    # Accent top border
    accent_bar = Rectangle((x + 0.01, y + 0.34), 0.19, 0.012, facecolor=color,
                           edgecolor='none', transform=ax.transAxes, zorder=2)
    ax.add_patch(accent_bar)
    
    ax.text(x + 0.02, y + 0.27, title, transform=ax.transAxes, color=TEXT_MUTED, fontsize=9, fontweight='bold', zorder=3)
    ax.text(x + 0.02, y + 0.12, val, transform=ax.transAxes, color=TEXT_WHITE, fontsize=18, fontweight='bold', zorder=3)
    ax.text(x + 0.02, y + 0.04, subtext, transform=ax.transAxes, color=TEXT_MUTED, fontsize=8, zorder=3)

fig.suptitle("CUSTOMER CHURN & REVENUE INTELLIGENCE — EXECUTIVE KPI SCORECARD",
             fontsize=16, fontweight='bold', color=TEXT_WHITE, y=0.98)
plt.tight_layout()
plt.savefig('Visualizations/01_executive_kpi_summary.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 02: CHURN DISTRIBUTION & REVENUE IMPACT
# -----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=BG_DARK)
for ax in (ax1, ax2):
    ax.set_facecolor(BG_DARK)

# Left: Customer Counts Donut
counts = df['Churn_Status'].value_counts()
colors = [COLOR_RETAIN, COLOR_CHURN]
wedges, texts, autotexts = ax1.pie(
    counts, labels=['Active (5,802)', 'Churned (2,698)'], autopct='%1.1f%%',
    startangle=140, colors=colors, textprops=dict(color=TEXT_WHITE, fontsize=11),
    wedgeprops=dict(width=0.45, edgecolor=BG_DARK, linewidth=3)
)
for at in autotexts:
    at.set_fontsize(13)
    at.set_fontweight('bold')
ax1.set_title("Customer Base Composition", fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)

# Right: Monthly Revenue Breakdown
rev_retained = df[df['Churn_Status'] == 'No']['Monthly_Charges'].sum()
rev_lost = df[df['Churn_Status'] == 'Yes']['Monthly_Charges'].sum()
rev_data = [rev_retained, rev_lost]

wedges2, texts2, autotexts2 = ax2.pie(
    rev_data, labels=[f'Active MRR\n${rev_retained:,.0f}', f'Lost MRR\n${rev_lost:,.0f}'],
    autopct='%1.1f%%', startangle=140, colors=[ACCENT_PURPLE, COLOR_CHURN],
    textprops=dict(color=TEXT_WHITE, fontsize=11),
    wedgeprops=dict(width=0.45, edgecolor=BG_DARK, linewidth=3)
)
for at in autotexts2:
    at.set_fontsize(13)
    at.set_fontweight('bold')
ax2.set_title("Monthly Recurring Revenue (MRR) Distribution", fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)

fig.suptitle("Portfolio Churn Rate: 31.74% | Monthly Revenue Lost: $205,777",
             fontsize=16, fontweight='bold', color=ACCENT_CYAN, y=1.02)
plt.tight_layout()
plt.savefig('Visualizations/02_churn_distribution.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 03: REVENUE BY SUBSCRIPTION PLAN (ACTIVE VS LOST)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

plan_rev = df.groupby(['Subscription_Plan', 'Churn_Status'])['Monthly_Charges'].sum().unstack()
plan_order = ['Basic', 'Standard', 'Premium', 'Enterprise']
plan_rev = plan_rev.loc[plan_order]

x = np.arange(len(plan_order))
width = 0.35

rects1 = ax.bar(x - width/2, plan_rev['No'], width, label='Active MRR', color=ACCENT_CYAN, edgecolor=BORDER_COLOR)
rects2 = ax.bar(x + width/2, plan_rev['Yes'], width, label='Lost MRR (Churned)', color=COLOR_CHURN, edgecolor=BORDER_COLOR)

ax.set_ylabel('Monthly Recurring Revenue ($)', fontsize=12, color=TEXT_WHITE)
ax.set_title('Monthly Recurring Revenue by Subscription Plan: Active vs Lost', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.set_xticks(x)
ax.set_xticklabels(plan_order, fontsize=11, color=TEXT_WHITE)
ax.legend(facecolor=PANEL_DARK, edgecolor=BORDER_COLOR, labelcolor=TEXT_WHITE, fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.25, color=BORDER_COLOR)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'${h:,.0f}', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                color=TEXT_WHITE, fontsize=9, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'${h:,.0f}', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                color=COLOR_CHURN, fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('Visualizations/03_revenue_by_subscription_plan.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 04: CHURN RATE BY CONTRACT TYPE
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

contract_stats = df.groupby('Contract_Type').agg(
    total=('CustomerID', 'count'),
    churned=('Churn_Status', lambda s: (s == 'Yes').sum())
).reset_index()
contract_stats['churn_rate'] = (contract_stats['churned'] / contract_stats['total'] * 100).round(1)
contract_stats = contract_stats.sort_values('churn_rate', ascending=True)

bars = ax.barh(contract_stats['Contract_Type'], contract_stats['churn_rate'],
               color=[COLOR_RETAIN, COLOR_WARN, COLOR_CHURN], edgecolor=BORDER_COLOR, height=0.55)

ax.set_xlabel('Churn Rate (%)', fontsize=12, color=TEXT_WHITE)
ax.set_title('Customer Churn Rate by Contract Type (Month-to-Month Flight Risk)', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.grid(axis='x', linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=11)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}%",
            va='center', color=TEXT_WHITE, fontweight='bold', fontsize=12)

ax.set_xlim(0, 75)
plt.tight_layout()
plt.savefig('Visualizations/04_churn_by_contract_type.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 05: CHURN BY PAYMENT METHOD
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

pay_stats = df.groupby('Payment_Method').agg(
    total=('CustomerID', 'count'),
    churned=('Churn_Status', lambda s: (s == 'Yes').sum())
).reset_index()
pay_stats['churn_rate'] = (pay_stats['churned'] / pay_stats['total'] * 100).round(1)
pay_stats = pay_stats.sort_values('churn_rate', ascending=False)

bars = ax.bar(pay_stats['Payment_Method'], pay_stats['churn_rate'],
              color=[COLOR_CHURN if r > 40 else ACCENT_PURPLE for r in pay_stats['churn_rate']],
              edgecolor=BORDER_COLOR, width=0.5)

ax.set_ylabel('Churn Rate (%)', fontsize=12, color=TEXT_WHITE)
ax.set_title('Customer Churn Rate by Payment Method (Electronic Check Friction)', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=10)
plt.xticks(rotation=15, ha='right')

for bar in bars:
    h = bar.get_height()
    ax.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                color=TEXT_WHITE, fontsize=11, fontweight='bold')

ax.set_ylim(0, 65)
plt.tight_layout()
plt.savefig('Visualizations/05_churn_by_payment_method.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 06: TENURE COHORT VS CHURN CLIFF
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

tenure_stats = df.groupby('Tenure_Cohort', observed=False).agg(
    total=('CustomerID', 'count'),
    churned=('Churn_Status', lambda s: (s == 'Yes').sum())
).reset_index()
tenure_stats['churn_rate'] = (tenure_stats['churned'] / tenure_stats['total'] * 100).round(1)

ax.plot(tenure_stats['Tenure_Cohort'], tenure_stats['churn_rate'],
        marker='o', markersize=10, linewidth=3, color=COLOR_CHURN, label='Cohort Churn Rate (%)')
ax.fill_between(range(len(tenure_stats)), tenure_stats['churn_rate'], color=COLOR_CHURN, alpha=0.15)

for i, txt in enumerate(tenure_stats['churn_rate']):
    ax.annotate(f"{txt:.1f}%\n({tenure_stats['churned'][i]:,} exits)",
                (i, txt), textcoords="offset points", xytext=(0, 12), ha='center',
                color=TEXT_WHITE, fontweight='bold', fontsize=10)

ax.set_ylabel('Churn Rate (%)', fontsize=12, color=TEXT_WHITE)
ax.set_title('The Onboarding Cliff: Customer Churn Rate Collapses After Year 1', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.grid(True, linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=10)
ax.set_ylim(0, 85)

plt.tight_layout()
plt.savefig('Visualizations/06_tenure_vs_churn_curve.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 07: SUPPORT TICKETS VS CHURN RATE
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

ticket_stats = df.groupby('Support_Tickets').agg(
    total=('CustomerID', 'count'),
    churned=('Churn_Status', lambda s: (s == 'Yes').sum())
).reset_index()
ticket_stats['churn_rate'] = (ticket_stats['churned'] / ticket_stats['total'] * 100).round(1)

colors_grad = [COLOR_RETAIN if r < 30 else (COLOR_WARN if r < 50 else COLOR_CHURN) for r in ticket_stats['churn_rate']]
bars = ax.bar(ticket_stats['Support_Tickets'], ticket_stats['churn_rate'], color=colors_grad, edgecolor=BORDER_COLOR, width=0.6)

ax.set_xlabel('Support Tickets Logged', fontsize=12, color=TEXT_WHITE)
ax.set_ylabel('Churn Rate (%)', fontsize=12, color=TEXT_WHITE)
ax.set_title('Customer Dissatisfaction Tipping Point: Support Tickets vs Churn Rate', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=11)

for bar in bars:
    h = bar.get_height()
    ax.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                color=TEXT_WHITE, fontsize=10, fontweight='bold')

ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig('Visualizations/07_support_tickets_vs_churn.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 08: MONTHLY REVENUE & SIGNUP COHORT TREND
# -----------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(13, 6), facecolor=BG_DARK)
ax1.set_facecolor(PANEL_DARK)

df['Signup_Month'] = pd.to_datetime(df['Signup_Date']).dt.to_period('M')
monthly_cohort = df[df['Signup_Month'] >= '2024-01'].groupby('Signup_Month').agg(
    new_cust=('CustomerID', 'count'),
    new_billing=('Monthly_Charges', 'sum')
).reset_index()
monthly_cohort['Signup_Month_Str'] = monthly_cohort['Signup_Month'].astype(str)

x = np.arange(len(monthly_cohort))
ax1.bar(x, monthly_cohort['new_cust'], color=ACCENT_CYAN, alpha=0.75, width=0.55, label='New Customer Signups')
ax1.set_ylabel('New Customer Signups', fontsize=12, color=ACCENT_CYAN)
ax1.tick_params(axis='y', labelcolor=ACCENT_CYAN)

ax2 = ax1.twinx()
ax2.plot(x, monthly_cohort['new_billing'], color=COLOR_WARN, marker='s', linewidth=2.5, label='Cohort Contracted Billing ($)')
ax2.set_ylabel('Contracted Monthly Billing ($)', fontsize=12, color=COLOR_WARN)
ax2.tick_params(axis='y', labelcolor=COLOR_WARN)

ax1.set_xticks(x[::2])
ax1.set_xticklabels(monthly_cohort['Signup_Month_Str'][::2], rotation=35, ha='right', color=TEXT_WHITE)
ax1.set_title('Acquisition Momentum: Monthly Signups & Invoiced Revenue Trend (2024-2026)', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax1.grid(axis='x', linestyle='--', alpha=0.2, color=BORDER_COLOR)

plt.tight_layout()
plt.savefig('Visualizations/08_monthly_revenue_trend.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 09: CORRELATION HEATMAP
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

df_corr = df[['Tenure_Months', 'Monthly_Charges', 'Total_Charges', 'Support_Tickets', 'Usage_Hours', 'Age']].copy()
df_corr['Churn_Numeric'] = (df['Churn_Status'] == 'Yes').astype(int)
df_corr['Month_to_Month'] = (df['Contract_Type'] == 'Month-to-Month').astype(int)
df_corr['Electronic_Check'] = (df['Payment_Method'] == 'Electronic Check').astype(int)

corr_matrix = df_corr.corr()

cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.6, vmax=0.6,
            linewidths=0.5, linecolor=PANEL_DARK, ax=ax, cbar_kws={'label': 'Pearson Correlation'})
ax.set_title('Feature Correlation Matrix with Customer Churn', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.tick_params(colors=TEXT_WHITE, labelsize=10)
plt.xticks(rotation=30, ha='right')

plt.tight_layout()
plt.savefig('Visualizations/09_correlation_matrix.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 10: CUSTOMER SEGMENTATION CLUSTERS (K-MEANS)
# -----------------------------------------------------------------------------
from sklearn.cluster import KMeans

seg_features = df[['Monthly_Charges', 'Usage_Hours', 'Tenure_Months']].copy()
scaler = StandardScaler()
seg_scaled = scaler.fit_transform(seg_features)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Segment_Cluster'] = kmeans.fit_predict(seg_scaled)

segment_names = {
    0: 'Tier 1: High-Spender Heavy Streamers',
    1: 'Tier 2: Established Loyalists',
    2: 'Tier 3: Budget Disengaged Newbies',
    3: 'Tier 4: Moderate Standard Users'
}
df['Segment_Name'] = df['Segment_Cluster'].map(segment_names)

fig, ax = plt.subplots(figsize=(11, 6.5), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

cluster_colors = [ACCENT_PURPLE, COLOR_RETAIN, COLOR_CHURN, ACCENT_CYAN]
for i in range(4):
    subset = df[df['Segment_Cluster'] == i]
    ax.scatter(subset['Monthly_Charges'], subset['Usage_Hours'],
               c=cluster_colors[i], label=segment_names[i], alpha=0.6, s=35, edgecolors='none')

ax.set_xlabel('Monthly Charges ($)', fontsize=12, color=TEXT_WHITE)
ax.set_ylabel('Platform Usage Hours (hrs/mo)', fontsize=12, color=TEXT_WHITE)
ax.set_title('Behavioral Customer Segmentation (K-Means Clustering)', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.legend(facecolor=PANEL_DARK, edgecolor=BORDER_COLOR, labelcolor=TEXT_WHITE, fontsize=10, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=10)

plt.tight_layout()
plt.savefig('Visualizations/10_customer_segmentation_clusters.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# MACHINE LEARNING PIPELINE: TRAIN MODELS FOR CHARTS 11, 12, 13
# -----------------------------------------------------------------------------
ml_df = df.copy()
# Encode features
ml_df['Is_Churn'] = (ml_df['Churn_Status'] == 'Yes').astype(int)
ml_df['Is_MonthToMonth'] = (ml_df['Contract_Type'] == 'Month-to-Month').astype(int)
ml_df['Is_TwoYear'] = (ml_df['Contract_Type'] == 'Two Year').astype(int)
ml_df['Is_ElectronicCheck'] = (ml_df['Payment_Method'] == 'Electronic Check').astype(int)
ml_df['Is_FiberOptic'] = (ml_df['Internet_Service'] == 'Fiber Optic').astype(int)
ml_df['Has_Discount'] = (ml_df['Discount_Applied'] == 'Yes').astype(int)

features = ['Age', 'Tenure_Months', 'Monthly_Charges', 'Total_Charges', 'Support_Tickets',
            'Usage_Hours', 'Is_MonthToMonth', 'Is_TwoYear', 'Is_ElectronicCheck', 'Is_FiberOptic', 'Has_Discount']

X = ml_df[features]
y = ml_df['Is_Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

scaler_ml = StandardScaler()
X_train_scaled = scaler_ml.fit_transform(X_train)
X_test_scaled = scaler_ml.transform(X_test)

# Model 1: Logistic Regression
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_scaled, y_train)
lr_probs = lr_model.predict_proba(X_test_scaled)[:, 1]
lr_preds = lr_model.predict(X_test_scaled)

# Model 2: Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
rf_model.fit(X_train, y_train)
rf_probs = rf_model.predict_proba(X_test)[:, 1]
rf_preds = rf_model.predict(X_test)

lr_auc = roc_auc_score(y_test, lr_probs)
rf_auc = roc_auc_score(y_test, rf_probs)

# -----------------------------------------------------------------------------
# CHART 11: ROC-AUC CURVES
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_probs)
fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_probs)

ax.plot(fpr_rf, tpr_rf, color=ACCENT_CYAN, linewidth=3, label=f'Random Forest (ROC-AUC = {rf_auc:.3f})')
ax.plot(fpr_lr, tpr_lr, color=ACCENT_PURPLE, linewidth=2.5, linestyle='--', label=f'Logistic Regression (ROC-AUC = {lr_auc:.3f})')
ax.plot([0, 1], [0, 1], color=TEXT_MUTED, linestyle=':', label='Random Benchmark (AUC = 0.500)')

ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=12, color=TEXT_WHITE)
ax.set_ylabel('True Positive Rate (Recall / Sensitivity)', fontsize=12, color=TEXT_WHITE)
ax.set_title('Predictive Churn Modeling: ROC-AUC Performance Comparison', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.legend(facecolor=PANEL_DARK, edgecolor=BORDER_COLOR, labelcolor=TEXT_WHITE, fontsize=11, loc='lower right')
ax.grid(True, linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=10)

plt.tight_layout()
plt.savefig('Visualizations/11_ml_roc_auc_curves.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 12: CONFUSION MATRIX (RANDOM FOREST)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6.5), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

cm = confusion_matrix(y_test, rf_preds)
cm_labels = ['Active (Retained)', 'Churned']

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
            xticklabels=cm_labels, yticklabels=cm_labels,
            annot_kws={'size': 14, 'weight': 'bold'})

ax.set_xlabel('Predicted Label', fontsize=12, color=TEXT_WHITE, labelpad=10)
ax.set_ylabel('Actual Ground Truth', fontsize=12, color=TEXT_WHITE, labelpad=10)
ax.set_title(f'Random Forest Confusion Matrix (Holdout Test Set N={len(y_test):,})',
             fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.tick_params(colors=TEXT_WHITE, labelsize=11)

plt.tight_layout()
plt.savefig('Visualizations/12_ml_confusion_matrix.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 13: FEATURE IMPORTANCE
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

feat_imp = pd.Series(rf_model.feature_importances_, index=features).sort_values(ascending=True)

friendly_names = {
    'Is_MonthToMonth': 'Contract: Month-to-Month',
    'Tenure_Months': 'Customer Tenure (Months)',
    'Support_Tickets': 'Support Tickets Logged',
    'Usage_Hours': 'Platform Usage Hours',
    'Total_Charges': 'Cumulative Total Charges',
    'Monthly_Charges': 'Monthly Recurring Charges',
    'Is_ElectronicCheck': 'Payment: Electronic Check',
    'Age': 'Customer Age',
    'Is_TwoYear': 'Contract: Two Year',
    'Is_FiberOptic': 'Service: Fiber Optic',
    'Has_Discount': 'Discount Promo Applied'
}
feat_imp.index = [friendly_names.get(f, f) for f in feat_imp.index]

bars = ax.barh(feat_imp.index, feat_imp.values, color=ACCENT_CYAN, edgecolor=BORDER_COLOR, height=0.6)
ax.set_xlabel('Relative Gini Importance Score', fontsize=12, color=TEXT_WHITE)
ax.set_title('Top Drivers of Customer Churn (Random Forest Feature Importance)', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.grid(axis='x', linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=10)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.005, bar.get_y() + bar.get_height()/2, f"{w*100:.1f}%",
            va='center', color=TEXT_WHITE, fontweight='bold', fontsize=10)

ax.set_xlim(0, max(feat_imp.values) * 1.18)
plt.tight_layout()
plt.savefig('Visualizations/13_ml_feature_importance.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# -----------------------------------------------------------------------------
# CHART 14: REVENUE AT RISK MATRIX
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5), facecolor=BG_DARK)
ax.set_facecolor(PANEL_DARK)

active_df = df[df['Churn_Status'] == 'No']
risk_summary = active_df.groupby('Risk_Tier', observed=False).agg(
    customer_count=('CustomerID', 'count'),
    mrr_at_risk=('Monthly_Charges', 'sum')
).reset_index()

bars = ax.bar(risk_summary['Risk_Tier'], risk_summary['mrr_at_risk'],
              color=[COLOR_RETAIN, COLOR_WARN, '#FB7185', COLOR_CHURN],
              edgecolor=BORDER_COLOR, width=0.55)

ax.set_ylabel('Active Monthly Revenue ($)', fontsize=12, color=TEXT_WHITE)
ax.set_title('Active Monthly Recurring Revenue at Risk by Customer Risk Tier', fontsize=14, fontweight='bold', color=TEXT_WHITE, pad=15)
ax.grid(axis='y', linestyle='--', alpha=0.25, color=BORDER_COLOR)
ax.tick_params(colors=TEXT_WHITE, labelsize=11)

for bar in bars:
    h = bar.get_height()
    ax.annotate(f"${h:,.0f}", xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                color=TEXT_WHITE, fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('Visualizations/14_revenue_at_risk_matrix.png', dpi=300, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

# Export high risk accounts for targeted retention
active_df_with_risk = active_df[active_df['Risk_Tier'].isin(['High Risk', 'Critical Risk'])].copy()
active_df_with_risk = active_df_with_risk.sort_values('Monthly_Charges', ascending=False)
active_df_with_risk.to_csv('dataset/high_risk_customers_to_contact.csv', index=False)
print(f"Generated 14 high-resolution charts in 'Visualizations/'")
print(f"Identified {len(active_df_with_risk):,} high-risk active accounts exported to 'dataset/high_risk_customers_to_contact.csv'")
