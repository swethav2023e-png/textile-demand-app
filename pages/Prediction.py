import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("🤖 Demand Prediction")

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

if st.button("🚀 Predict"):
    data = np.array([[value, pfco, total, year, month, day, lag_1]])
    prediction = model.predict(data)[0]

    st.success(f"📈 Predicted Demand: {round(prediction,2)} Kgs")

    if prediction > lag_1:
        st.success("📊 Increase Production")
    else:
        st.warning("📉 Reduce Production")