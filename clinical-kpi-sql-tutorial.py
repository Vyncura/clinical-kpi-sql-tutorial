%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from scipy import stats

# --- CONFIGURATION ---
st.set_page_config(page_title="Healthcare RCM Dashboard", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # In a real app, this would be a path to your CSV or a database connection
    # For this demo, we assume the dataset is in the same directory
    try:
        df = pd.read_csv('medical_cost_personal_datasets.csv')
    except:
        # Fallback for demo purposes if file is missing locally
        st.error("Dataset not found. Please ensure 'medical_cost_personal_datasets.csv' is in the root directory.")
        return pd.DataFrame()
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
region_filter = st.sidebar.multiselect("Select Region", options=df['region'].unique(), default=df['region'].unique())
smoker_filter = st.sidebar.radio("Smoker Status", options=['All', 'yes', 'no'], index=0)

# Filter Logic
filtered_df = df[df['region'].isin(region_filter)]
if smoker_filter != 'All':
    filtered_df = filtered_df[filtered_df['smoker'] == smoker_filter]

# --- HEADER ---
st.title("🏥 Healthcare Revenue Cycle Management (RCM) Audit")
st.markdown("""
Bridging healthcare billing data with automated analytics to identify revenue leakage and cost drivers. 
This dashboard analyzes patient demographics and smoking status to optimize risk-adjusted pricing.
""")

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Patients", len(filtered_df))
with col2:
    st.metric("Avg. Charges", f"${filtered_df['charges'].mean():,.2f}")
with col3:
    st.metric("Max Charge", f"${filtered_df['charges'].max():,.0f}")
with col4:
    st.metric("Avg BMI", f"{filtered_df['bmi'].mean():.2f}")

# --- VISUALIZATIONS ---
st.divider()

left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Revenue by Age Cohort")
    # Replicating Query 5 logic
    df_age = filtered_df.copy()
    df_age['age_bracket'] = (df_age['age'] // 10) * 10
    age_cohorts = df_age.groupby('age_bracket')['charges'].mean().reset_index()
    fig_age = px.bar(age_cohorts, x='age_bracket', y='charges', 
                     title="Average Ticket Size by Age Bracket",
                     labels={'charges': 'Avg Revenue ($)', 'age_bracket': 'Age group'},
                     color='charges', color_continuous_scale='Viridis')
    st.plotly_chart(fig_age, use_container_width=True)

with right_chart:
    st.subheader("BMI vs Charges Interaction")
    fig_bmi = px.scatter(filtered_df, x='bmi', y='charges', color='smoker', 
                         trendline="ols", title="BMI Impact on Revenue (by Smoker Status)",
                         labels={'bmi': 'Body Mass Index', 'charges': 'Charges ($)'},
                         opacity=0.6)
    st.plotly_chart(fig_bmi, use_container_width=True)

# --- STATISTICAL INSIGHTS ---
st.divider()
st.subheader("📊 Statistical Audit")

smoker_charges = df[df['smoker'] == 'yes']['charges']
non_smoker_charges = df[df['smoker'] == 'no']['charges']
t_stat, p_val = stats.ttest_ind(smoker_charges, non_smoker_charges, equal_var=False)

stat_col1, stat_col2 = st.columns([1, 2])
with stat_col1:
    st.write("**Independent T-Test (Smoker vs Non-Smoker)**")
    st.write(f"T-Statistic: `{t_stat:.4f}`")
    st.write(f"P-Value: `{p_val:.4e}`")
    if p_val < 0.05:
        st.success("Difference is Statistically Significant")
    else:
        st.warning("Difference is Not Statistically Significant")

with stat_col2:
    st.info("**Insight:** Smoker status is the primary driver of high-cost claims. While BMI has a weak linear correlation overall, its impact is exponentially higher in the smoking population, as seen in the interaction plot above.")

# --- DATA TABLE ---
with st.expander("View Raw Audit Data"):
    st.dataframe(filtered_df, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("Support this project: Contributions help keep healthcare tools free and online 24/7. Built with Streamlit, Plotly, and SciPy.")
"
