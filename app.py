import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt

# --- 1. CONFIGURATION & PAGE SETUP ---
st.set_page_config(page_title="Healthcare RCM Dashboard", layout="wide")

# --- 2. DATA LOADING & PREPROCESSING (Synthetic) ---
@st.cache_data
def load_data():
    # Creating a synthetic dataset for demonstration
    np.random.seed(42)
    data = {
        'age': np.random.randint(18, 65, 500),
        'bmi': np.random.uniform(18, 40, 500),
        'children': np.random.randint(0, 5, 500),
        'smoker': np.random.choice(['yes', 'no'], 500, p=[0.2, 0.8]),
        'region': np.random.choice(['southwest', 'southeast', 'northwest', 'northeast'], 500),
        'charges': np.random.uniform(5000, 50000, 500)
    }
    df = pd.DataFrame(data)
    # Logic: Smokers have higher charges in this synthetic model
    df.loc[df['smoker'] == 'yes', 'charges'] *= 2.5
    return df

df = load_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df['region'].unique(), default=df['region'].unique())
selected_smoker = st.sidebar.radio("Smoker Status", options=['All', 'yes', 'no'])

# Filter logic
filtered_df = df[df['region'].isin(selected_region)]
if selected_smoker != 'All':
    filtered_df = filtered_df[filtered_df['smoker'] == selected_smoker]

# --- 4. KPI METRICS ---
st.title("🏥 Healthcare Revenue Cycle Management")
st.markdown("Analyzing medical costs, demographics, and risk factors.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Revenue", f"${filtered_df['charges'].sum():,.2f}")
with col2:
    st.metric("Avg. Charge per Patient", f"${filtered_df['charges'].mean():,.2f}")
with col3:
    st.metric("Patient Count", len(filtered_df))

# --- 5. VISUALIZATION & INSIGHTS ---
st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("Charges vs. BMI by Smoker Status")
    fig1 = px.scatter(filtered_df, x="bmi", y="charges", color="smoker", 
                      trendline="ols", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Revenue Distribution by Region")
    fig2 = px.box(filtered_df, x="region", y="charges", color="region", points="all")
    st.plotly_chart(fig2, use_container_width=True)

# --- 6. RAW DATA TABLE ---
with st.expander("View Filtered Raw Data"):
    st.dataframe(filtered_df.sort_values('charges', ascending=False))

# --- README FRIENDLY FOOTER ---
st.markdown("---")
st.caption("Deployment Tip: Ensure 'requirements.txt' includes: streamlit, pandas, numpy, plotly, and statsmodels.")
