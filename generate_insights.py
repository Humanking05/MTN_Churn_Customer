import pandas as pd
import utils

df = utils.load_data()

if df is not None:
    total_customers = len(df)
    churners = df[df['customer_churn_status'] == 'Yes']
    churn_count = len(churners)
    churn_rate = churn_count / total_customers * 100
    
    total_revenue = df['total_revenue'].sum()
    lost_revenue = churners['total_revenue'].sum()
    revenue_loss_rate = lost_revenue / total_revenue * 100
    
    top_reasons = churners['reasons_for_churn'].value_counts().head(3)
    
    churn_by_plan = df.groupby('subscription_plan')['customer_churn_status'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False).head(3)
    
    print(f"Total Customers: {total_customers}")
    print(f"Churn Rate: {churn_rate:.2f}%")
    print(f"Total Revenue: N{total_revenue:,.2f}")
    print(f"Lost Revenue: N{lost_revenue:,.2f} ({revenue_loss_rate:.2f}%)")
    print("\nTop 3 Churn Reasons:")
    print(top_reasons)
    print("\nHighest Churn Plans:")
    print(churn_by_plan)
else:
    print("Failed to load data")
