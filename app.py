%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Healthcare RCM Analytics Dashboard", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e1e4e8; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # In a real app, this would be: pd.read_csv('medical_cost_personal_datasets.csv')
    # Using a subset of the project data structure for the demo
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# --- SIDEBAR / FILTERS ---
st.sidebar.header("Dashboard Filters")
region_filter = st.sidebar.multiselect("Select Region:", options=df['region'].unique(), default=df['region'].unique())
smoker_filter = st.sidebar.radio("Smoker Status:", options=['All', 'yes', 'no'], index=0)

# Apply filters
filtered_df = df[df['region'].isin(region_filter)]
if smoker_filter != 'All':
    filtered_df = filtered_df[filtered_df['smoker'] == smoker_filter]

# --- HEADER ---
st.title("🏥 Healthcare Revenue Cycle Management (RCM) Audit")
st.markdown("**Objective:** Identifying revenue drivers and cost leakage through demographic and behavioral analysis.")

# --- KEY METRICS (KPIs) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Patients", f"{len(filtered_df):,}")
with col2:
    st.metric("Avg. Charges", f"${filtered_df['charges'].mean():,.2f}")
with col3:
    st.metric("Total Revenue", f"${filtered_df['charges'].sum()/1e6:.2f}M")
with col4:
    st.metric("Avg. BMI", f"{filtered_df['bmi'].mean():.1f}")

st.divider()

# --- VISUALIZATIONS ---
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Revenue Distribution by Region")
    fig_region = px.sunburst(filtered_df, path=['region', 'smoker'], values='charges', 
                             color='charges', color_continuous_scale='Viridis')
    st.plotly_chart(fig_region, use_container_width=True)

with right_column:
    st.subheader("BMI vs. Medical Charges")
    fig_scatter = px.scatter(filtered_df, x="bmi", y="charges", color="smoker",
                             hover_data=['age'], trendline="ols",
                             title="Correlation: BMI & Charges (by Smoker Status)")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- DETAILED ANALYSIS ---
st.subheader("Age-Based Revenue Cohorts")
df['age_bracket'] = (df['age'] // 10) * 10
age_cohorts = filtered_df.groupby('age_bracket')['charges'].mean().reset_index()
fig_age = px.bar(age_cohorts, x='age_bracket', y='charges', 
                 labels={'charges': 'Avg Revenue ($)', 'age_bracket': 'Age Group'},
                 color='charges', color_continuous_scale='Blues')
st.plotly_chart(fig_age, use_container_width=True)

# --- FOOTER ---
st.info("💡 **RCM Insight:** Smokers with a BMI over 30 represent the highest financial risk category for insurance providers.")
st.markdown("--- ")
st.caption("Support this project: Contributions help keep healthcare analytics tools free and open source.")
