
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import io
from PIL import Image

st.set_page_config(page_title="Fadhu Perodua Financing Calculator", layout="centered")

car_data = {
    "Axia": {"E": 23100, "G": 40190, "X": 41630, "SE": 45740, "AV": 51390},
    "Bezza": {"G": 38170, "X": 45820, "AV": 51920},
    "Myvi": {"G": 50360, "X": 52860, "H": 56970, "AV": 62110},
    "Ativa": {"X": 64800, "H": 70220, "AV": 75720},
    "Alza": {"X": 64710, "H": 70380, "AV": 78070},
    "Aruz": {"X": 75600, "AV": 80700}
}

interest_rates_dict = {
    "Axia": [3.3],
    "Bezza": [3.3],
    "Myvi": [3.3],
    "Ativa": [2.7],
    "Alza": [2.7],
    "Aruz": [2.7]
}
loan_tenures = [5, 7, 9]

st.title("🚗 Fadhu Perodua Financing Calculator")

st.sidebar.header("Select Car Details")
selected_car = st.sidebar.selectbox("Car Type", list(car_data.keys()))
selected_model = st.sidebar.selectbox("Model", list(car_data[selected_car].keys()))
selected_interest = st.sidebar.selectbox("Interest Rate (%)", interest_rates_dict[selected_car])
selected_tenure = st.sidebar.selectbox("Loan Tenure (Years)", loan_tenures)

rebate = 0
rebate_display = ""
if selected_car in ["Ativa", "Aruz"]:
    rebate_option = st.sidebar.selectbox("Rebate Option", ["None", "RM 1,000", "RM 3,500"])
    if rebate_option == "RM 1,000":
        rebate = 1000
        rebate_display = "RM 1,000"
    elif rebate_option == "RM 3,500":
        rebate = 3500
        rebate_display = "RM 3,500"
    else:
        rebate_display = "None"
else:
    st.sidebar.selectbox("Rebate Option", ["Not applicable for this model"], disabled=True)

otr_base_price = car_data[selected_car][selected_model]
otr_price = otr_base_price - rebate
deposit_10_percent = otr_price * 0.10

def calculate_monthly_payment(loan_amount, interest_rate, tenure_years):
    monthly_rate = interest_rate / 100 / 12
    payments = tenure_years * 12
    if monthly_rate == 0:
        return loan_amount / payments
    return loan_amount * monthly_rate * (1 + monthly_rate) ** payments / ((1 + monthly_rate) ** payments - 1)

loan_full = otr_price
loan_10_percent = otr_price - deposit_10_percent
loan_10k = otr_price - 10000
loan_5k = otr_price - 5000

monthly_full = calculate_monthly_payment(loan_full, selected_interest, selected_tenure)
monthly_10_percent = calculate_monthly_payment(loan_10_percent, selected_interest, selected_tenure)
monthly_10k = calculate_monthly_payment(loan_10k, selected_interest, selected_tenure)
monthly_5k = calculate_monthly_payment(loan_5k, selected_interest, selected_tenure)

description = [
    "OTR Price",
]
amounts = [
    f"RM {otr_base_price:,.2f}",
]

if rebate > 0:
    description.append("Rebate Applied")
    amounts.append(f"{rebate_display}")

description += [
    "10% Deposit",
    "Monthly Payment (Full Loan)",
    "Monthly Payment (10% Deposit)",
    "Monthly Payment (RM 10k Deposit)",
    "Monthly Payment (RM 5k Deposit)",
    "Loan Tenure (Years)",
    "Interest Rate (%)"
]
amounts += [
    f"RM {deposit_10_percent:,.2f}",
    f"RM {monthly_full:,.2f}",
    f"RM {monthly_10_percent:,.2f}",
    f"RM {monthly_10k:,.2f}",
    f"RM {monthly_5k:,.2f}",
    f"{selected_tenure}",
    f"{selected_interest}"
]

df = pd.DataFrame({
    "Description": description,
    "Amount": amounts
})

st.subheader(f"{selected_car} {selected_model} Financing Details")
st.table(df)

fig = ff.create_table(df)
img_bytes = fig.to_image(format="png")
img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
buffer = io.BytesIO()
img.save(buffer, format="JPEG")
buffer.seek(0)

st.download_button(
    label="📸 Download Table as JPG",
    data=buffer,
    file_name=f"{selected_car}_{selected_model}_financing.jpg",
    mime="image/jpeg"
)

st.markdown("*Calculations are based on DC Auto Pricelist, latest update April 2025.*")
