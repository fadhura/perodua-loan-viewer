
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fadhu Perodua Financing Calculator", layout="centered")

car_data = {
    "Axia": {"E": 23100, "G": 40190, "X": 41630, "SE": 45740, "AV": 51390},
    "Bezza": {"G": 38170, "X": 45820, "AV": 51920},
    "Myvi": {"G": 50360, "X": 52860, "H": 56970, "AV": 62110},
    "Ativa": {"X": 64800, "H": 70220, "AV": 75720},
    "Alza": {"X": 64710, "H": 70380, "AV": 78070},
    "Aruz": {"X": 75600, "AV": 80700}
}

car_colors = {
    "Axia": {
        "Granite Grey (S43)": "#505050",
        "Glittering Silver (S28)": "#B0B0B0",
        "Coral Blur (B89)": "#5CA4B6",
        "Ivory White (W09)": "#F9F9F9",
        "Lava Red (R69)": "#B10F2E"
    }
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
selected_car = st.sidebar.selectbox("Car Model", list(car_data.keys()))
selected_model = st.sidebar.selectbox("Variants", list(car_data[selected_car].keys()))
selected_interest = st.sidebar.selectbox("Interest Rate (%)", interest_rates_dict[selected_car])
selected_tenure = st.sidebar.selectbox("Loan Tenure (Years)", loan_tenures)
custom_deposit = st.sidebar.number_input("💸 Custom Deposit (RM)", min_value=0, value=0, step=500)

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

# Color selection
if selected_car in car_colors:
    st.sidebar.markdown("### 🎨 Select Color")
    for color_name, hex_code in car_colors[selected_car].items():
        st.sidebar.markdown(f"<div style='display:flex;align-items:center;gap:10px;'><div style='width:15px;height:15px;border-radius:50%;background:{hex_code};'></div><span>{color_name}</span></div>", unsafe_allow_html=True)

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
loan_custom = otr_price - custom_deposit

monthly_full = calculate_monthly_payment(loan_full, selected_interest, selected_tenure)
monthly_10_percent = calculate_monthly_payment(loan_10_percent, selected_interest, selected_tenure)
monthly_custom = calculate_monthly_payment(loan_custom, selected_interest, selected_tenure)

description = ["OTR Price"]
amounts = [f"RM {otr_base_price:,.2f}"]

if rebate > 0:
    description.append("Rebate Applied")
    amounts.append(f"{rebate_display}")

description += [
    "10% Deposit",
    "Monthly Payment (Full Loan)",
    "Monthly Payment (10% Deposit)",
    f"Monthly Payment (Custom Deposit RM {custom_deposit:,.0f})",
    "Loan Tenure (Years)",
    "Interest Rate (%)"
]
amounts += [
    f"RM {deposit_10_percent:,.2f}",
    f"RM {monthly_full:,.2f}",
    f"RM {monthly_10_percent:,.2f}",
    f"RM {monthly_custom:,.2f}",
    f"{selected_tenure}",
    f"{selected_interest}"
]

df = pd.DataFrame({"Description": description, "Amount": amounts})

st.subheader(f"{selected_car} {selected_model} Financing Details")
st.table(df)

st.markdown("*Calculations are based on DC Auto Pricelist, latest update April 2025.*")
