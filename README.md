# MTN Customer Churn Analysis

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![SQLite](https://img.shields.io/badge/SQLite-3.41-orange?logo=sqlite&logoColor=white)](https://www.sqlite.org/) 
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/) 
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25-red?logo=streamlit&logoColor=white)](https://streamlit.io/)

## Project Overview
This project analyzes **customer churn for MTN Nigeria**, identifying key factors driving customer attrition and providing actionable insights for retention strategies. The analysis combines **descriptive, diagnostic, and predictive analytics** to quantify churn, understand its drivers, and proactively prevent revenue loss.

A **Machine Learning predictive model** is implemented to flag at-risk customers, enabling MTN to act **before churn occurs**.

---

## Key Metrics

| Metric | Value |
|--------|-------|
| **Total Customer Base** | 974 |
| **Overall Churn Rate** | 29.16% |
| **Total Revenue** | ₦199,348,200.00 |
| **Lost Revenue Due to Churn** | ₦58,000,200.00 (29.09%) |

---

## Top Insights

### 1. Top 3 Reasons for Churn

| Reason | Number of Customers |
|--------|-------------------|
| High Call Tariffs | 54 |
| Better Offers from Competitors | 52 |
| Poor Network | 45 |

### 2. Top 3 Plans with Highest Churn Rate (%)

| Subscription Plan | Churn Rate |
|------------------|------------|
| 200GB Monthly Broadband Plan | 45.2% |
| 3.2GB 2-Day Plan | 42.9% |
| 65GB Monthly Plan | 36.5% |

### 3. Revenue Impact
- Churned customers account for **29.09% of total revenue lost**, highlighting the importance of retention strategies.

---

## Strategic Recommendations

### 🟢 Immediate Actions (0-30 Days)
- **Price Adjustments for High-Value Plans**: Review pricing for the *200GB Broadband Plan* and *65GB Monthly Plan*. Consider adding "bonus data" or loyalty discounts to increase perceived value.
- **Competitor Win-Back Campaign**: Launch targeted SMS/Email campaigns offering "Competitor Match" discounts for at-risk customers identified by the predictive model.

### 🟡 Medium-Term Initiatives (1-3 Months)
- **Network Infrastructure Audit**: Prioritize upgrades in regions reporting the highest "Poor Network" feedback.
- **Tariff Restructuring**: Audit and adjust call tariffs to remain competitive in the market.

### 🔴 Long-Term Strategy (3-6 Months)
- **Proactive Retention Program**: Operationalize the predictive model to flag high-risk customers before churn and automatically trigger retention offers.

---

## Tools & Technologies
- **Python**: Data cleaning, preprocessing, analysis, and predictive modeling  
- **SQLite**: Database storage for customer data  
- **Pandas & NumPy**: Data manipulation and calculations  
- **Scikit-learn**: Logistic regression for churn prediction  
- **Jupyter Notebook / Streamlit**: Dashboard-ready insights and reporting.

Dashboard link: https://mtnchurncustomer-iqeikcji4qxpvxqmqkgnml.streamlit.app/



