import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

import utils

# Set Page Config
st.set_page_config(
    page_title="MTN Customer Churn Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
utils.load_css("style.css")

# Load Data
df = utils.load_data()

if df is None:
    st.error("Data file 'mtn_customer_churn.csv' not found. Please ensure the file exists in the directory.")
    st.stop()

# --- Sidebar Filters ---
with st.sidebar:
    st.title("Filters")
    
    # State Filter
    state_options = ["All"] + sorted(df['state'].unique().tolist())
    selected_state = st.selectbox("Select State", state_options)
    
    # Subscription Plan Filter
    plan_options = ["All"] + sorted(df['subscription_plan'].unique().tolist())
    selected_plan = st.selectbox("Select Plan", plan_options)

    # Filter Logic
    df_filtered = df.copy()
    if selected_state != "All":
        df_filtered = df_filtered[df_filtered['state'] == selected_state]
    if selected_plan != "All":
        df_filtered = df_filtered[df_filtered['subscription_plan'] == selected_plan]

# --- Main Content ---

st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h1>📊 MTN Customer Churn Analysis</h1>
        <p style='color: #64748b;'>Insights into customer retention, revenue, and demographics.</p>
    </div>
""", unsafe_allow_html=True)

# --- KPI Section ---
total_customers = len(df_filtered)
churn_count = len(df_filtered[df_filtered['customer_churn_status'] == 'Yes'])
churn_rate = (churn_count / total_customers * 100) if total_customers > 0 else 0
total_revenue = df_filtered['total_revenue'].sum() if 'total_revenue' in df_filtered.columns else 0
avg_satisfaction = df_filtered['satisfaction_rate'].mean() if 'satisfaction_rate' in df_filtered.columns else 0

c1, c2, c3, c4 = st.columns(4)

def kpi_card(col, title, value, prefix="", suffix="", color="default"):
    with col:
        st.markdown(f"""
        <div class="shadcn-card">
            <h3 style="margin: 0; font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">{title}</h3>
            <h2 style="margin: 10px 0 0 0; font-size: 2rem; color: #0f172a;">{prefix}{value}{suffix}</h2>
        </div>
        """, unsafe_allow_html=True)

kpi_card(c1, "Total Customers", f"{total_customers:,}")
kpi_card(c2, "Churn Rate", f"{churn_rate:.1f}", suffix="%")
kpi_card(c3, "Total Revenue", f"{total_revenue/1_000_000:.1f}", prefix="₦", suffix="M")
kpi_card(c4, "Avg Satisfaction", f"{avg_satisfaction:.1f}", suffix="/5")


# --- Row 1: Churn Analysis ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### Reasons for Churn")
    if 'reasons_for_churn' in df_filtered.columns:
        churn_reasons = df_filtered[df_filtered['customer_churn_status'] == 'Yes']['reasons_for_churn'].value_counts().reset_index()
        churn_reasons.columns = ['Reason', 'Count']
        
        fig_reasons = px.bar(
            churn_reasons, 
            x='Count', 
            y='Reason', 
            orientation='h',
            text='Count',
            color='Count',
            color_continuous_scale='Reds'
        )
        fig_reasons.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        st.plotly_chart(fig_reasons, use_container_width=True)
    else:
        st.info("No churn reason data available.")

with col_right:
    st.markdown("### Churn Composition")
    churn_dist = df_filtered['customer_churn_status'].value_counts().reset_index()
    churn_dist.columns = ['Status', 'Count']
    
    fig_donut = px.pie(
        churn_dist, 
        values='Count', 
        names='Status', 
        hole=0.6,
        color='Status',
        color_discrete_map={'Yes': '#ef4444', 'No': '#22c55e'}
    )
    fig_donut.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_donut, use_container_width=True)


# --- Row 2: Revenue & Plans ---
st.markdown("### Revenue by Plan")
if 'subscription_plan' in df_filtered.columns and 'total_revenue' in df_filtered.columns:
    rev_by_plan = df_filtered.groupby('subscription_plan')['total_revenue'].sum().reset_index().sort_values('total_revenue', ascending=False)
    
    fig_rev = px.bar(
        rev_by_plan,
        x='subscription_plan',
        y='total_revenue',
        color='total_revenue',
        color_continuous_scale='Blues'
    )
    fig_rev.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Revenue (₦)"),
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    st.plotly_chart(fig_rev, use_container_width=True)

# --- Row 3: Demographics & Data ---
c_demo_1, c_demo_2 = st.columns(2)

with c_demo_1:
    st.markdown("### Data Usage vs Tenure")
    if 'data_usage' in df_filtered.columns and 'customer_tenure_in_months' in df_filtered.columns:
        fig_scatter = px.scatter(
            df_filtered,
            x='customer_tenure_in_months',
            y='data_usage',
            color='customer_churn_status',
            color_discrete_map={'Yes': '#ef4444', 'No': '#3b82f6'},
            opacity=0.6
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Tenure (Months)"),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Data Usage (GB)"),
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with c_demo_2:
    st.markdown("### Churn by State (Top 10)")
    state_churn = df_filtered[df_filtered['customer_churn_status'] == 'Yes']['state'].value_counts().head(10).reset_index()
    state_churn.columns = ['State', 'Churn Count']
    
    fig_state = px.bar(
        state_churn,
        x='State',
        y='Churn Count',
        color='Churn Count',
        color_continuous_scale='Oranges'
    )
    fig_state.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    st.plotly_chart(fig_state, use_container_width=True)
