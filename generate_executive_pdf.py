"""
Customer Churn & Revenue Intelligence - Native PDF Executive Report Compiler
Generates 'Reports/Business_Insights.pdf' using matplotlib's PdfPages.
File: Reports/generate_executive_pdf.py
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.image as mpimg
import os

pdf_path = 'Reports/Business_Insights.pdf'

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

with PdfPages(pdf_path) as pdf:
    # -------------------------------------------------------------------------
    # PAGE 1: EXECUTIVE BRIEFING, SCORECARD & INSIGHTS 1-5
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.27, 11.69), facecolor=BG_DARK) # Standard A4
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.axis('off')

    # Header Banner
    banner = FancyBboxPatch((0.05, 0.90), 0.90, 0.08, facecolor=PANEL_DARK, edgecolor=BORDER_COLOR,
                            boxstyle="round,pad=0.01", transform=ax.transAxes)
    ax.add_patch(banner)
    accent_strip = Rectangle((0.05, 0.90), 0.012, 0.08, facecolor=ACCENT_CYAN, edgecolor='none', transform=ax.transAxes)
    ax.add_patch(accent_strip)

    ax.text(0.08, 0.95, "CUSTOMER CHURN & REVENUE INTELLIGENCE", color=TEXT_WHITE,
            fontsize=15, fontweight='bold', transform=ax.transAxes)
    ax.text(0.08, 0.925, "Executive Business Insights & Strategic Monetization Report",
            color=ACCENT_CYAN, fontsize=10, fontweight='semibold', transform=ax.transAxes)
    ax.text(0.08, 0.908, "Scope: 8,500 Accounts | \\$18.74M Historical Invoiced | \\$470.5K MRR | Date: January 2026",
            color=TEXT_MUTED, fontsize=8, transform=ax.transAxes)

    # KPI Scorecard Cards (4 cards)
    cards = [
        ("ACTIVE CUSTOMERS", "5,802", "68.26% Retention", COLOR_RETAIN),
        ("OVERALL CHURN", "31.74%", "2,698 Accounts Lost", COLOR_CHURN),
        ("ACTIVE MRR", "\\$470,499", "\\$5.65M Annual Run-Rate", ACCENT_PURPLE),
        ("MONTHLY REVENUE LOST", "\\$205,777", "\\$2.47M Annual Churn Bleed", COLOR_CHURN),
    ]
    for i, (title, val, sub, col) in enumerate(cards):
        x = 0.05 + i * 0.23
        y = 0.81
        c_patch = FancyBboxPatch((x, y), 0.21, 0.07, facecolor=PANEL_DARK, edgecolor=BORDER_COLOR,
                                 boxstyle="round,pad=0.008", transform=ax.transAxes)
        ax.add_patch(c_patch)
        t_bar = Rectangle((x, y + 0.065), 0.21, 0.005, facecolor=col, edgecolor='none', transform=ax.transAxes)
        ax.add_patch(t_bar)
        ax.text(x + 0.015, y + 0.048, title, color=TEXT_MUTED, fontsize=6.5, fontweight='bold', transform=ax.transAxes)
        ax.text(x + 0.015, y + 0.022, val, color=TEXT_WHITE, fontsize=12, fontweight='bold', transform=ax.transAxes)
        ax.text(x + 0.015, y + 0.007, sub, color=TEXT_MUTED, fontsize=6.5, transform=ax.transAxes)

    # Executive Summary Paragraph
    ax.text(0.05, 0.775, "EXECUTIVE SUMMARY", color=ACCENT_CYAN, fontsize=11, fontweight='bold', transform=ax.transAxes)
    summary_text = (
        "This analytics investigation profiles 8,500 subscriber accounts across 18 behavioral and financial dimensions.\n"
        "The company is currently losing \\$205,776.91 every month (\\$2.47M ARR) to customer churn. Over 94% of this loss\n"
        "is concentrated in Month-to-Month contracts, with payment friction and customer support escalation acting as primary catalysts."
    )
    ax.text(0.05, 0.725, summary_text, color=TEXT_WHITE, fontsize=8.5, linespacing=1.4, transform=ax.transAxes)

    # Top Insights 1 to 5
    ax.text(0.05, 0.695, "TOP 5 ANALYTICAL FINDINGS", color=ACCENT_CYAN, fontsize=11, fontweight='bold', transform=ax.transAxes)
    
    insights_p1 = [
        ("1. Month-to-Month Contract Vulnerability (The Primary Churn Driver)",
         "Month-to-Month customers churn at 40.7% vs 11.1% for 1-Year and 3.2% for 2-Year contracts.\n"
         "This cohort accounts for 94.8% of all churn (2,558 accounts) and \\$196,712/mo (\\$2.36M ARR) in lost revenue.",
         COLOR_CHURN),
        ("2. Electronic Check Payment Friction (42.4% of Total Lost Revenue)",
         "Month-to-Month users paying via Electronic Check suffer an 84.85% churn rate (1,131 churned accounts),\n"
         "bleeding \\$87,348.18/mo (\\$1.05M ARR). Lack of automatic renewal forces monthly friction and cancellation.",
         COLOR_CHURN),
        ("3. The Critical 0–6 Month Onboarding Cliff (47.2% of All Exits)",
         "Attrition is heavily front-loaded: 71.37% of customers in Months 0–6 churn (1,274 exits).\n"
         "Beyond 24 months, churn drops below 12%, and beyond 48 months collapses to 3.57%. Early onboarding is decisive.",
         COLOR_WARN),
        ("4. Support Ticket Escalation Tipping Point (Operational Friction)",
         "Churn escalates from 25.68% (0 tickets) to 40.52% (3 tickets) and 80%+ (5+ tickets).\n"
         "Unresolved technical tickets represent \\$58,410 in monthly lost MRR. First-contact resolution is critical.",
         COLOR_WARN),
        ("5. Revenue Concentration & Deciles (Pareto 80/20 Rule)",
         "The top 20% of subscribers generate 51.29% of total lifetime revenue (\\$9.61M of \\$18.74M total).\n"
         "Protecting high-decile accounts through dedicated white-glove retention programs is vital to balance sheet stability.",
         ACCENT_PURPLE),
    ]

    y_pos = 0.655
    for title, desc, col in insights_p1:
        box = FancyBboxPatch((0.05, y_pos - 0.055), 0.90, 0.065, facecolor=PANEL_DARK, edgecolor=BORDER_COLOR,
                             boxstyle="round,pad=0.006", transform=ax.transAxes)
        ax.add_patch(box)
        strip = Rectangle((0.05, y_pos - 0.055), 0.008, 0.065, facecolor=col, edgecolor='none', transform=ax.transAxes)
        ax.add_patch(strip)
        ax.text(0.07, y_pos - 0.008, title, color=TEXT_WHITE, fontsize=8.5, fontweight='bold', transform=ax.transAxes)
        ax.text(0.07, y_pos - 0.045, desc, color=TEXT_MUTED, fontsize=7.5, linespacing=1.3, transform=ax.transAxes)
        y_pos -= 0.075

    # Embed Chart 01 (Executive KPI Summary) at bottom of Page 1
    if os.path.exists('Visualizations/01_executive_kpi_summary.png'):
        img = mpimg.imread('Visualizations/01_executive_kpi_summary.png')
        ax_img = fig.add_axes([0.05, 0.04, 0.90, 0.23])
        ax_img.imshow(img)
        ax_img.axis('off')

    pdf.savefig(fig, facecolor=BG_DARK)
    plt.close()

    # -------------------------------------------------------------------------
    # PAGE 2: INSIGHTS 6-10, RECOMMENDATIONS & FINANCIAL MODEL
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.27, 11.69), facecolor=BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.axis('off')

    # Top Banner
    ax.text(0.05, 0.95, "PART II: ADVANCED INSIGHTS, RETENTION PLAYBOOK & ROI", color=TEXT_WHITE,
            fontsize=13, fontweight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.93, "Operational interventions, machine learning risk tiers, and revenue sensitivity model",
            color=ACCENT_CYAN, fontsize=8.5, transform=ax.transAxes)

    # Insights 6 to 10
    ax.text(0.05, 0.90, "ANALYTICAL FINDINGS 6 TO 10", color=ACCENT_CYAN, fontsize=10, fontweight='bold', transform=ax.transAxes)
    insights_p2 = [
        ("6. Primary Churn Reasons", "Competitor pricing (31.3% / \\$75.6K lost MRR), Poor support (23.9% / \\$46.8K lost), Competitor speed (16.3%)."),
        ("7. Tier Vulnerability", "Standard (\\$83.2K/mo lost) and Premium (\\$76.5K/mo lost) account for 77.6% of lost recurring revenue."),
        ("8. Platform Disengagement", "Customers with <20 usage hrs/mo churn at 48.76% vs 23.2% for 120+ hrs/mo users. Engagement decay precedes churn by 45 days."),
        ("9. Geographic Hotspots", "Texas metros (Dallas: 33.79%, San Antonio: 33.72%, Austin: 32.85%) experience highest churn due to local fiber price wars."),
        ("10. ML Risk Scoring Tiers", "647 active accounts hold >50% churn risk representing \\$52,210.16 MRR (\\$626.5K ARR) in immediate jeopardy today.")
    ]
    y_p2 = 0.865
    for title, desc in insights_p2:
        ax.text(0.05, y_p2, f"• {title}:", color=TEXT_WHITE, fontsize=8, fontweight='bold', transform=ax.transAxes)
        ax.text(0.30, y_p2, desc, color=TEXT_MUTED, fontsize=7.5, transform=ax.transAxes)
        y_p2 -= 0.025

    # 5 Strategic Recommendations Table
    ax.text(0.05, 0.725, "5 STRATEGIC ACTIONABLE RECOMMENDATIONS", color=ACCENT_CYAN, fontsize=10, fontweight='bold', transform=ax.transAxes)

    recs = [
        ("1. Payment & Contract Conversion", "Offer \\$10/mo credit for 6 mos to convert Electronic Check users to auto-pay credit card and annual contracts.", "+\\$21,800 / mo (\\$261.6K ARR)"),
        ("2. Overhaul First 90 Days Onboarding", "Deploy automated onboarding workflows, usage alerts, and dedicated setup calls for Standard/Premium.", "+\\$33,600 / mo (\\$403.2K ARR)"),
        ("3. Support Ticket Circuit Breaker", "Automated escalation to Senior Engineering and assignment of Retention Specialist on 2nd support ticket.", "+\\$17,500 / mo (\\$210.0K ARR)"),
        ("4. ML Proactive Retention Outreach", "Target the 647 flagged high-risk accounts using high_risk_customers_to_contact.csv with customized incentives.", "+\\$20,884 / mo (\\$250.6K ARR)"),
        ("5. Competitive Price-Match Incentive", "Empower frontline care agents with pre-approved 15% discount for 12-month re-commitment on competitor offers.", "+\\$26,440 / mo (\\$317.3K ARR)")
    ]

    y_rec = 0.685
    for title, act, roi in recs:
        r_box = FancyBboxPatch((0.05, y_rec - 0.038), 0.90, 0.048, facecolor=PANEL_DARK, edgecolor=BORDER_COLOR,
                               boxstyle="round,pad=0.005", transform=ax.transAxes)
        ax.add_patch(r_box)
        ax.text(0.065, y_rec, title, color=ACCENT_CYAN, fontsize=8, fontweight='bold', transform=ax.transAxes)
        ax.text(0.065, y_rec - 0.022, act, color=TEXT_MUTED, fontsize=7, transform=ax.transAxes)
        ax.text(0.74, y_rec - 0.012, roi, color=COLOR_RETAIN, fontsize=7.5, fontweight='bold', transform=ax.transAxes)
        y_rec -= 0.058

    # Financial Sensitivity Table
    ax.text(0.05, 0.385, "FINANCIAL RECOVERY SENSITIVITY MODEL", color=ACCENT_CYAN, fontsize=10, fontweight='bold', transform=ax.transAxes)
    sens_headers = ["Scenario", "Churn Rate", "Accounts Preserved", "Monthly MRR Saved", "Annual ARR Saved"]
    sens_rows = [
        ["Current Baseline", "31.74%", "5,802 Active", "\\$0.00", "\\$0.00"],
        ["Conservative Target (-2%)", "29.74%", "+170 Accounts", "+\\$13,785 / mo", "+\\$165,424 / yr"],
        ["Strategic Milestone (-5%)", "26.74%", "+425 Accounts", "+\\$34,463 / mo", "+\\$413,559 / yr"],
        ["Transformational (-10%)", "21.74%", "+850 Accounts", "+\\$68,927 / mo", "+\\$827,118 / yr"]
    ]
    # Draw simple table
    t_y = 0.355
    col_x = [0.05, 0.28, 0.44, 0.63, 0.81]
    for ci, h in enumerate(sens_headers):
        ax.text(col_x[ci], t_y, h, color=TEXT_WHITE, fontsize=7.5, fontweight='bold', transform=ax.transAxes)
    line1 = Rectangle((0.05, t_y - 0.006), 0.90, 0.002, facecolor=ACCENT_CYAN, edgecolor='none', transform=ax.transAxes)
    ax.add_patch(line1)

    t_y -= 0.025
    for row in sens_rows:
        is_highlight = "Strategic Milestone" in row[0]
        row_color = COLOR_RETAIN if is_highlight else TEXT_MUTED
        weight = 'bold' if is_highlight else 'normal'
        for ci, cell in enumerate(row):
            ax.text(col_x[ci], t_y, cell, color=row_color, fontsize=7.2, fontweight=weight, transform=ax.transAxes)
        t_y -= 0.022

    # Embed Chart 03 (Revenue by Subscription Plan) at bottom of Page 2
    if os.path.exists('Visualizations/03_revenue_by_subscription_plan.png'):
        img2 = mpimg.imread('Visualizations/03_revenue_by_subscription_plan.png')
        ax_img2 = fig.add_axes([0.05, 0.04, 0.90, 0.21])
        ax_img2.imshow(img2)
        ax_img2.axis('off')

    pdf.savefig(fig, facecolor=BG_DARK)
    plt.close()

print(f"Executive PDF report generated successfully: {pdf_path}")
size_kb = os.path.getsize(pdf_path) / 1024
print(f"File Size: {size_kb:.1f} KB")
