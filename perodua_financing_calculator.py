
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

color_codes = {
    "S28": "#C0C0C0", "S43": "#4B4B4B", "W09": "#FFFFFF", "B89": "#00AEEF", "R69": "#B22222",
    "B81": "#0077BE", "R67": "#8B0000", "B77": "#1E90FF", "R76": "#8B1E3F", "W25": "#F5F5F5",
    "B79": "#0033A0", "R75": "#8B0000", "XJ3": "#DDDDDD", "XJ2": "#660000", "X16": "#2E2E2E", "T35": "#5C4033"
}

variant_colors = {
    "Axia": {"E": ["S43", "W09", "S28"], "G": ["S43", "W09", "S28", "B89", "R69"], "X": ["S43", "W09", "S28", "B89", "R69"],
             "SE": ["S43", "W09", "S28", "B89", "R69"], "AV": ["S43", "W09", "S28", "B89", "R69"]},
    "Bezza": {"G": ["S43", "W09", "S28", "B81", "R67"], "X": ["S43", "W09", "S28", "B81", "R67"], "AV": ["S43", "W09", "S28", "B81", "R67"]},
    "Myvi": {"G": ["W09", "S28", "B77"], "X": ["S43", "W09", "S28", "B77", "R76"], "H": ["S43", "W09", "S28", "B77", "R76"], "AV": ["S43", "W09", "S28", "B77", "R76"]},
    "Ativa": {"X": ["S43", "S28", "W25"], "H": ["S43", "S28", "B79", "W25", "R75"], "AV": ["S43", "S28", "W25", "R75", "XJ3", "XJ2"]},
    "Alza": {"X": ["W09", "S28", "R67", "X16", "T35"], "H": ["W09", "S28", "R67", "X16", "T35"], "AV": ["W09", "S28", "R67", "X16", "T35"]},
    "Aruz": {"X": ["S43", "W09", "S28", "B77", "R67", "X16"], "AV": ["S43", "W09", "S28", "B77", "R67", "X16"]}
}

interest_rates_dict = {
    "Axia": [3.3], "Bezza": [3.3], "Myvi": [3.3], "Ativa": [2.7], "Alza": [2.7], "Aruz": [2.7]
}
loan_tenures = [9, 7, 5]  # Set 9 as default

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
    rebate_display = rebate_option if rebate_option != "None" else ""
    rebate = int(rebate_display.replace("RM ", "").replace(",", "")) if rebate_display else 0
else:
    st.sidebar.selectbox("Rebate Option", ["Not applicable for this model"], disabled=True)

# Color dot with code
if selected_car in variant_colors and selected_model in variant_colors[selected_car]:
    st.sidebar.markdown("### 🎨 Available Colors")
    for code in variant_colors[selected_car][selected_model]:
        color_name = [k for k in color_codes.keys() if k == code]
        hex_color = color_codes.get(code, "#000000")
        st.sidebar.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;'>"
            f"<div style='width:15px;height:15px;border-radius:50%;background:{hex_color};border:1px solid #ccc;'></div>"
            f"<span style='font-size:14px'>{code}</span></div>",
            unsafe_allow_html=True
        )

otr_base_price = car_data[selected_car][selected_model]
otr_price = otr_base_price - rebate
deposit_10_percent = otr_price * 0.10

def calculate_monthly_payment(loan_amount, interest_rate, tenure_years):
    monthly_rate = interest_rate / 100 / 12
    payments = tenure_years * 12
    return loan_amount * monthly_rate * (1 + monthly_rate) ** payments / ((1 + monthly_rate) ** payments - 1)

loan_full = otr_price
loan_10_percent = otr_price - deposit_10_percent
loan_custom = otr_price - custom_deposit

monthly_full = calculate_monthly_payment(loan_full, selected_interest, selected_tenure)
monthly_10_percent = calculate_monthly_payment(loan_10_percent, selected_interest, selected_tenure)
monthly_custom = calculate_monthly_payment(loan_custom, selected_interest, selected_tenure)

# Display in styled layout instead of table
st.subheader(f"{selected_car} {selected_model} Financing Breakdown")
st.markdown(f"**OTR Price**: RM {otr_base_price:,.2f}")
if rebate > 0:
    st.markdown(f"**Rebate Applied**: {rebate_display}")
st.markdown(f"**10% Deposit**: RM {deposit_10_percent:,.2f}")
st.markdown(f"**Monthly Payment (Full Loan)**: RM {monthly_full:,.2f}")
st.markdown(f"**Monthly Payment (10% Deposit)**: RM {monthly_10_percent:,.2f}")
st.markdown(f"**Monthly Payment (Custom Deposit RM {custom_deposit:,.0f})**: RM {monthly_custom:,.2f}")
st.markdown(f"**Loan Tenure**: {selected_tenure} years")
st.markdown(f"**Interest Rate**: {selected_interest}%")

st.markdown("*Calculations are based on DC Auto Pricelist, latest update April 2025.*")
