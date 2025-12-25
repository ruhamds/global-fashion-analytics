# Global Fashion Retail Analytics & Churn Prediction

End-to-end analytics and machine learning project on a global fashion retail dataset  
(6.28M transactions, 1.64M customers, $1.62B revenue, 35 stores across multiple countries).

## Project Goals
Answer three core business questions:
1. **How is the business performing?** (Revenue, returns, customer value, geography, products)
2. **What drives profitability and loss?** (Returns, discounts, seasonality, store performance)
3. **Which customers are likely to churn, and what is the financial impact?**

## Dataset Overview
| Entity          | Records     |
|-----------------|-------------|
| Customers       | 1,643,306   |
| Products        | 14,950      |
| Transactions    | 6,284,272   |
| Stores          | 35          |
| Employees       | 403         |
| Discount Campaigns | 204      |
| Date Range      | Jan 2023 – Feb 2025 |
| Total Revenue   | $1.62B      |

## Project Phases

### Phase 1: Data Ingestion & Cleaning
- Chunked loading of 6M+ rows
- Schema validation, duplicate removal, missing value handling
- Financial reconciliation across sources
- Result: Clean, trusted dataset ready for analysis

### Phase 2: Business Intelligence
**Key Metrics**
- Gross Revenue: $807.8M
- Returns: $45.3M (5.61% return rate)
- Net Revenue: $762.5M

**Key Insights**
- China dominates revenue and customer lifetime value
- Feminine & Masculine categories drive sales and returns
- Strong Q4 seasonality (Black Friday + holidays)
- Peak activity on weekends and afternoons
- Discount campaigns effective but ROI decreases with overuse

### Phase 3: Customer Churn Prediction
**Churn Definition**: >180 days since last purchase  
**Results**
- Churn Rate: 46.8%
- Customers at Risk: 594,291
- Revenue at Risk: $227M

**Best Model**: Gradient Boosting (AUC 0.84, F1 0.76)

**Top Churn Drivers (SHAP)**
1. Days as customer (tenure) — strongest protector
2. Discount dependency
3. Order frequency & basket stability
4. Spend velocity

**Retention Simulation**
- Targeted campaign on high-risk customers
- Projected Net ROI: +$4.46M

## Tech Stack
- Python (pandas, scikit-learn, SHAP)
- SQL Server (validation)
- Matplotlib / Seaborn
- Jupyter / Google Colab
- Git & GitHub

## Repository Structure

├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_business_metrics.ipynb
│   └── 03_churn_modeling.ipynb
├── reports/
│   └── Global_Fashion_End_to_End_Analytics_Report.docx
├── scripts/
├── data/                # (ignored via .gitignore)
└── README.md