import streamlit as st
import pandas as pd
import os

def load_css(file_name):
    """Loads a CSS file and injects it into the Streamlit app."""
    # Check if the file path is absolute or relative
    if not os.path.isabs(file_name):
         # Assuming utils.py is in the root directory
         file_name = os.path.join(os.path.dirname(__file__), file_name)

    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {file_name}")

@st.cache_data
def load_data(file_path="mtn_customer_churn.csv"):
    """Loads and preprocesses the churn data."""
    if not os.path.exists(file_path):
        # Try looking one level up if in pages directory
        file_path = os.path.join("..", file_path)
        if not os.path.exists(file_path):
            return None
    
    df = pd.read_csv(file_path)
    
    # Data Cleaning / Preprocessing
    # Ensure numeric columns are actually numeric
    numerical_cols = ['total_revenue', 'customer_tenure_in_months', 'data_usage']
    for col in numerical_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Normalize text
    if 'customer_churn_status' in df.columns:
        df['customer_churn_status'] = df['customer_churn_status'].astype(str).str.strip().str.title()
    
    # Fill missing numeric values with median (simple imputation) to avoid errors
    df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())

    return df
