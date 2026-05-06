import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

# --- PAGE CONFIG ---
st.set_page_config(page_title="Healthcare RCM Dashboard", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # In a real app, replace this with: pd.read_csv('medical_cost_personal_datasets.csv')
    # For this demo, we assume the file is in the same directory
    try:
        df = pd.read_csv('medical_cost_personal_datasets.csv')
    except:
        # Fallback for demonstration if file isn't uploaded to GitHub yet
        st.error("Dataset file not found. Please ensure 'medical_cost_personal_datasets.csv' is in your repo.")
        return pd.DataFrame()
    
    # Preprocessing
    df['bmi_category'] = pd.cut(df['bmi'], 
                                bins=[0, 18.5, 24.9, 29.9, 100], 
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    return df

df = load_data()

if not df.empty:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Dashboard Filters")
    region = st.sidebar.multiselect("Select Region", options=df['region'].unique(), default=df['region'].unique())
    smoker = st.sidebar.radio("Smoker Status", options=['All', 'yes', 'no'])
    
    # Filter Data
    filtered_df = df[df['region'].isin(region)]
    if smoker != 'All':
        filtered_df = filtered_df[filtered_df['smoker'] == smoker]

    # --- MAIN CONTENT ---
    st.title("🏥 Healthcare Revenue Cycle Management (RCM) Analysis")
    st.markdown("Explore medical cost drivers and patient demographics interactiveley.")

    # --- KPI METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Patients", len(filtered_df))
    col2.metric("Avg. Medical Charge", f"${filtered_df['charges'].mean():,.2f}")
    col3.metric("Total Revenue", f"${filtered_df['charges'].sum():,.0f}")
    col4.metric("Avg. BMI", f"{filtered_df['bmi'].mean():.2f}")

    # --- VISUALIZATIONS ---
    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Charges by Smoker Status")
        fig_box = px.box(filtered_df, x="smoker", y="charges", color="smoker", 
                         color_discrete_map={'yes': '#E74C3C', 'no': '#2ECC71'})
        st.plotly_chart(fig_box, use_container_width=True)

    with c2:
        st.subheader("BMI vs. Charges (Regression View)")
        fig_scatter = px.scatter(filtered_df, x="bmi", y="charges", color="smoker", 
                                 trendline="ols", opacity=0.5)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()
    
    # Row 2
    c3, c4 = st.columns([1, 2])
    
    with c3:
        st.subheader("Revenue by BMI Category")
        bmi_revenue = filtered_df.groupby('bmi_category')['charges'].sum().reset_index()
        fig_pie = px.pie(bmi_revenue, values='charges', names='bmi_category', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c4:
        st.subheader("Age-Based Revenue Trends")
        filtered_df['age_bracket'] = (filtered_df['age'] // 10) * 10
        age_analysis = filtered_df.groupby('age_bracket')['charges'].mean().reset_index()
        fig_bar = px.bar(age_analysis, x='age_bracket', y='charges', 
                         labels={'age_bracket': 'Age Group', 'charges': 'Avg Charge ($)'},
                         color='charges', color_continuous_scale='Viridis')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- DATA TABLE ---
    with st.expander("View Raw Filtered Data"):
        st.dataframe(filtered_df)

    st.sidebar.markdown("---")
    st.sidebar.info("Created for RCM Business Intelligence Analysis")
