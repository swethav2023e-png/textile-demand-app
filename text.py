import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Load dataset
df = pd.read_csv("Textile_sales_data.csv")

# Preprocess
df['DATE'] = pd.to_datetime(df['DATE'], format='mixed', dayfirst=True)
df['year'] = df['DATE'].dt.year
df['month'] = df['DATE'].dt.month

# Page config
st.set_page_config(page_title="Textile Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;'>📊 Textile Demand Analytics Dashboard</h1>", unsafe_allow_html=True)

# ============================================
# 🎛️ FILTER SECTION
# ============================================

st.sidebar.header("🔍 Filters")

selected_pfco = st.sidebar.multiselect(
    "Select PFco_Code",
    options=df['PFco_Code'].unique(),
    default=df['PFco_Code'].unique()[:5]
)

selected_month = st.sidebar.slider("Select Month", 1, 12, (1, 12))

# Apply filters
filtered_df = df[
    (df['PFco_Code'].isin(selected_pfco)) &
    (df['month'] >= selected_month[0]) &
    (df['month'] <= selected_month[1])
]

# ============================================
# 📊 KPI CARDS
# ============================================

st.subheader("📊 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Total Demand", round(filtered_df['QUANTITIES_Kgs'].sum(), 2))
col2.metric("Average Demand", round(filtered_df['QUANTITIES_Kgs'].mean(), 2))
col3.metric("Max Demand", round(filtered_df['QUANTITIES_Kgs'].max(), 2))

# ============================================
# 📊 CHARTS
# ============================================

col1, col2 = st.columns(2)

# Monthly Trend
with col1:
    st.write("### 📈 Monthly Demand Trend")
    monthly = filtered_df.groupby('month')['QUANTITIES_Kgs'].mean()

    fig1, ax1 = plt.subplots()
    ax1.plot(monthly.index, monthly.values, marker='o')
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Demand")
    st.pyplot(fig1)

# Top PFco_Code
with col2:
    st.write("### 🏆 Top Performing PFco_Code")
    top_pfco = filtered_df.groupby('PFco_Code')['QUANTITIES_Kgs'].sum().sort_values(ascending=False).head(5)

    fig2, ax2 = plt.subplots()
    ax2.bar(top_pfco.index.astype(str), top_pfco.values)
    st.pyplot(fig2)

import streamlit as st

st.set_page_config(page_title="Textile ML App", layout="wide")

st.title("📊 Textile Demand Forecasting System")

st.write("""
Welcome to the Textile Demand Forecasting System.

Use the sidebar to navigate:
- 📊 Dashboard → View analytics
- 🤖 Prediction → Predict demand
""")

# ============================================
# 🤖 PREDICTION SECTION
# ============================================

st.subheader("🤖 Demand Prediction")

col1, col2 = st.columns(2)

with col1:
    value = st.number_input("VALUE", 0.0)
    pfco = st.number_input("PFco_Code", 0)

with col2:
    total = st.number_input("Total_values", 0.0)
    month = st.slider("Month", 1, 12)

year = st.slider("Year", 2020, 2030)
day = st.slider("Day", 1, 31)
lag_1 = st.number_input("Previous Demand", 0.0)

if st.button("🚀 Predict Demand"):
    
    data = np.array([[value, pfco, total, year, month, day, lag_1]])
    prediction = model.predict(data)[0]

    st.success(f"📈 Predicted Demand: {round(prediction,2)} Kgs")

    # Recommendation
    if prediction > lag_1:
        st.success("📊 Demand Increasing → Increase Production")
    elif prediction < lag_1:
        st.warning("📉 Demand Decreasing → Reduce Production")
    else:
        st.info("⚖ Demand Stable → Maintain Production")

# Footer
st.markdown("""
---
Developed by Swetha | Industry-Level ML Dashboard 🚀
""")