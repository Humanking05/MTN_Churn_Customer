import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add parent dir to path so we can import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score

# --- Config & Setup ---
st.set_page_config(page_title="Predictive Analytics", page_icon="🔮", layout="wide")
utils.load_css("style.css")

st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h1>🔮 Predictive Analytics</h1>
        <p style='color: #64748b;'>Machine Learning model to predict customer churn probability.</p>
    </div>
""", unsafe_allow_html=True)

# --- Load & Preprocess Data ---
df = utils.load_data()

if df is None:
    st.error("Data not found.")
    st.stop()

# Prepare Data for Modeling
@st.cache_resource
def train_model(data):
    # Select Features
    feature_cols = [
        'age', 'gender', 'state', 'customer_tenure_in_months', 
        'subscription_plan', 'data_usage', 'mtn_device', 
        'satisfaction_rate', 'number_of_time_purchased', 'total_revenue'
    ]
    target_col = 'customer_churn_status'
    
    # Filter only available columns
    available_cols = [c for c in feature_cols if c in data.columns]
    model_df = data[available_cols + [target_col]].copy().dropna()
    
    # Encode Categorical Variables
    encoders = {}
    for col in model_df.select_dtypes(include=['object']).columns:
        if col != target_col:
            le = LabelEncoder()
            model_df[col] = le.fit_transform(model_df[col].astype(str))
            encoders[col] = le
            
    # Target Encoding (Yes=1, No=0)
    model_df[target_col] = model_df[target_col].apply(lambda x: 1 if x == 'Yes' else 0)
    
    X = model_df[available_cols]
    y = model_df[target_col]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred)
    }
    
    return model, encoders, metrics, available_cols

with st.spinner("Training predictive model..."):
    model, encoders, metrics, feature_names = train_model(df)

# --- Model Performance Section ---
st.markdown("### Model Performance")
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""
    <div class="shadcn-card">
        <h3 style="color: #64748b; font-size: 0.9rem;">Model Accuracy</h3>
        <h2 style="color: #0f172a; margin-top: 5px;">{metrics['accuracy']:.1%}</h2>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="shadcn-card">
        <h3 style="color: #64748b; font-size: 0.9rem;">F1 Score</h3>
        <h2 style="color: #0f172a; margin-top: 5px;">{metrics['f1']:.2f}</h2>
    </div>
    """, unsafe_allow_html=True)


# --- Feature Importance ---
st.markdown("### Key Drivers of Churn")
importances = pd.DataFrame({
    'Feature': feature_names,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=True)

fig_imp = px.bar(
    importances, 
    x='Importance', 
    y='Feature', 
    orientation='h',
    color='Importance',
    color_continuous_scale='Purples'
)
fig_imp.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    height=400,
    xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
    yaxis=dict(title=None),
    margin=dict(l=0, r=0, t=0, b=0)
)
st.plotly_chart(fig_imp, use_container_width=True)


# --- What-If Analysis Tool ---
st.markdown("---")
st.markdown("### 🛠️ What-If Analysis Tool")
st.info("Adjust the parameters below to predict the churn probability for a hypothetical customer.")

with st.form("prediction_form"):
    c1, c2, c3 = st.columns(3)
    
    inputs = {}
    
    # Helper to create input fields based on type
    for col in feature_names:
        if col in encoders:
            # Categorical: Selectbox
            # Get original classes from encoder
            options = list(encoders[col].classes_)
            with c1 if len(inputs) % 3 == 0 else c2 if len(inputs) % 3 == 1 else c3:
                val = st.selectbox(f"{col.replace('_', ' ').title()}", options)
                inputs[col] = encoders[col].transform([val])[0]
        else:
            # Numerical: Number Input
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            avg_val = float(df[col].mean())
            with c1 if len(inputs) % 3 == 0 else c2 if len(inputs) % 3 == 1 else c3:
                val = st.number_input(f"{col.replace('_', ' ').title()}", min_value=0.0, value=avg_val)
                inputs[col] = val

    submitted = st.form_submit_button("Predict Churn Probability")

if submitted:
    # Create DataFrame for prediction
    input_df = pd.DataFrame([inputs])
    
    # Predict
    prob = model.predict_proba(input_df)[0][1] # Probability of Class 1 (Yes)
    prediction = "Churn Risk" if prob > 0.5 else "Safe"
    
    st.markdown("### Prediction Result")
    
    color = "#ef4444" if prob > 0.5 else "#22c55e"
    
    st.markdown(f"""
    <div style="padding: 20px; border-radius: 8px; background-color: {color}20; border: 1px solid {color};">
        <h3 style="color: {color}; margin: 0;">Probability of Churn: {prob:.1%}</h3>
        <p style="margin-top: 5px; font-weight: 500;">Status: {prediction}</p>
    </div>
    """, unsafe_allow_html=True)
