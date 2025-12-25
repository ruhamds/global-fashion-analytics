🌍 Global Fashion Retail Analytics & Churn Prediction

End-to-end data analytics and machine learning project on a large-scale global retail dataset (6.28M transactions, $1.62B revenue), transforming raw data into business insights and churn-driven decision making.

📌 Project Overview

This project analyzes a global fashion retail dataset to answer three core business questions:

How is the business performing?
→ Revenue, returns, customer value, stores, countries, products

What drives profitability and loss?
→ Returns, discounts, seasonal trends, employee/store performance

Which customers are at risk of churn, and what is the business impact?
→ Leak-free churn modeling, explainability, and ROI-driven retention strategy

The project is structured into three clear phases, mirroring how analytics is done in real organizations.

🗂️ Dataset Summary
Entity	Records
Customers	1,643,306
Products	14,950
Transactions	6,284,272
Stores	35
Employees	403
Discount Campaigns	204
Date Range	Jan 2023 – Feb 2025
Total Revenue	$1.62B

All data was cleaned, validated, and integrity-checked before analysis.

🧠 Phase 1 — Data Ingestion & Exploratory Analysis
🎯 Objective

Ensure the dataset is clean, reliable, and analytics-ready before drawing conclusions.

Key Work

Chunked ingestion of 6.2M+ rows (beyond Excel limits)

Schema design and validation

Handling missing values (sizes, colors, job titles)

Duplicate detection and removal

Financial reconciliation between raw CSV, SQL, and Python

Key Findings

No missing foreign keys in transactions

Returns embedded as negative line totals

Strong seasonality (Q4 peaks)

Data quality issues identified early (encoding, missing metadata)

✅ Outcome: A trusted foundation for business and ML analysis

📊 Phase 2 — Business Intelligence & Metrics
🎯 Objective

Translate raw transactions into decision-ready business metrics.

Core Metrics

Gross Revenue: $807.8M

Returns (Loss): $45.3M

Net Revenue: $762.5M

Return Rate: 5.61%

Business Insights

China dominates revenue and CLV, far exceeding other countries

Feminine & Masculine categories drive most sales and returns

Returns are consistent across categories, not isolated quality failures

Discount campaigns work, but ROI declines at higher penetration

Q4 (Black Friday + Holidays) is the strongest revenue period

Weekends and afternoon hours show peak customer activity

📈 Outcome: Clear understanding of where money is made, lost, and concentrated

🔁 Phase 3 — Customer Churn Modeling & Business Impact
🎯 Objective

Predict customer churn without data leakage and quantify financial risk.

Churn Definition

One-time buyers = churned

Repeat buyers = active

Churn Snapshot

Churn Rate: 46.8%

Customers at Risk: 594,291

Revenue at Risk: $227M

Modeling

Models tested: Logistic Regression, Random Forest, Gradient Boosting

Best Model: Gradient Boosting

ROC-AUC: 0.84

F1 Score: 0.76

Explainability (SHAP)

Top churn drivers:

Days as customer

Discount dependency

Order frequency & basket stability

Tenure and spend velocity

Business Impact Simulation

Identified 103K high-risk customers

Simulated targeted retention campaign

Projected Net ROI: +$4.46M

💡 Outcome: Churn predictions translated into actionable, revenue-backed decisions

🛠️ Tech Stack

Python (pandas, numpy, scikit-learn, SHAP)

SQL Server (schema design, validation)

Matplotlib / Seaborn

Jupyter / Google Colab

Git & GitHub

Repositary Structure

├── data/
│   ├── raw/
│   └── cleaned/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_business_metrics.ipynb
│   └── 03_churn_modeling.ipynb
├── reports/
│   └── Global_Fashion_End_to_End_Analytics_Report.docx
├── scripts/
├── README.md
