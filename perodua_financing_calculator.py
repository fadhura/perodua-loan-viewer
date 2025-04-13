
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fadhu Perodua Financing Calculator", layout="centered")
st.markdown("""
<style>
    .block-container {
        max-width: 430px;
        margin: auto;
        padding: 1rem;
    }
    .stApp {
        font-size: 16px;
    }
    .info-card {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
    }
    .info-label {
        font-weight: bold;
        display: block;
        margin-bottom: 2px;
    }
    .float-button {
        position: fixed;
        bottom: 24px;
        right: 24px;
        background-color: #5e60ce;
        color: white;
        padding: 12px 16px;
        border-radius: 50px;
        font-size: 16px;
        text-align: center;
        z-index: 9999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        cursor: pointer;
    }
    .float-button:hover {
        background-color: #3f429d;
    }
</style>

<script>
    function scrollToTop() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    }
</script>

<div class="float-button" onclick="scrollToTop()">⬆️ Top</div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .block-container {
            max-width: 430px;
            margin: auto;
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

car_data = {
    "Axia": {"E": 23100, "G": 40190, "X": 41630, "SE": 45740, "AV": 51390},
    "Bezza": {"G": 38170, "X": 45820, "AV": 51920},
    "Myvi": {"G": 50360, "X": 52860, "H": 56970, "AV": 62110},
    "Ativa": {"X": 64800, "H": 70220, "AV": 75720},
    "Alza": {"X": 64710, "H": 70380, "AV": 78070},
    "Aruz": {"X": 75600, "AV": 80700}
}

interest_rates_dict = {
    "Axia": 3.3, "Bezza": 3.3, "Myvi": 3.3, "Ativa": 2.7, "Alza": 2.7, "Aruz": 2.7
}
loan_tenures = [9, 7, 5]

st.title("🚗 Fadhu Perodua Financing Calculator")

st.sidebar.header("Select Car Details")
selected_car = st.sidebar.selectbox("Car Model", list(car_data.keys()))
selected_model = st.sidebar.selectbox("Variants", list(car_data[selected_car].keys()))
selected_tenure = st.sidebar.selectbox("Loan Tenure (Years)", loan_tenures)
custom_deposit = st.sidebar.number_input("💸 Custom Deposit (RM)", min_value=0, value=0, step=500)

rebate = 0
rebate_display = ""
if selected_car in ["Ativa", "Aruz"]:
    rebate_option = st.sidebar.selectbox("Rebate Option", ["None", "RM 1,000", "RM 3,500"])
    if rebate_option != "None":
        rebate = int(rebate_option.replace("RM ", "").replace(",", ""))
        rebate_display = rebate_option
else:
    st.sidebar.selectbox("Rebate Option", ["Not applicable for this model"], disabled=True)

def calculate_monthly_payment(loan_amount, interest_rate, tenure_years):
    monthly_rate = interest_rate / 100 / 12
    payments = tenure_years * 12
    return loan_amount * monthly_rate * (1 + monthly_rate) ** payments / ((1 + monthly_rate) ** payments - 1)

otr_base_price = car_data[selected_car][selected_model]
otr_price = otr_base_price - rebate
deposit_10_percent = otr_price * 0.10

loan_full = otr_price
loan_10_percent = otr_price - deposit_10_percent
loan_custom = otr_price - custom_deposit
interest = interest_rates_dict[selected_car]

monthly_full = calculate_monthly_payment(loan_full, interest, selected_tenure)
monthly_10_percent = calculate_monthly_payment(loan_10_percent, interest, selected_tenure)
monthly_custom = calculate_monthly_payment(loan_custom, interest, selected_tenure)

st.markdown("### 💰 Financing Breakdown")
st.markdown(f"""<div class="info-card"><span class="info-label">OTR Price</span>RM {otr_base_price:,.2f}""", unsafe_allow_html=True) RM {otr_base_price:,.2f}")
if rebate > 0:
    st.markdown(f"**Rebate Applied**: {rebate_display}")
st.markdown(f"**10% Deposit**: RM {deposit_10_percent:,.2f}")
st.markdown(f"**Monthly Payment (Full Loan)**: RM {monthly_full:,.2f}")
st.markdown(f"**Monthly Payment (10% Deposit)**: RM {monthly_10_percent:,.2f}")
st.markdown(f"**Monthly Payment (Custom Deposit RM {custom_deposit:,.0f})**: RM {monthly_custom:,.2f}")
st.markdown(f"**Loan Tenure**: {selected_tenure} years")
st.markdown(f"**Interest Rate**: {interest}%")

summary_data = []
for variant, base_price in car_data[selected_car].items():
    price = base_price - rebate if variant == selected_model else base_price
    depo = price * 0.10
    monthly_all = calculate_monthly_payment(price, interest, selected_tenure)
    monthly_depo = calculate_monthly_payment(price - depo, interest, selected_tenure)
    summary_data.append({
        "Variant": f"{selected_car} {variant}",
        "OTR": f"RM {price:,.2f}",
        "10% Deposit": f"RM {depo:,.2f}",
        "Full Loan Monthly": f"RM {monthly_all:,.2f}",
        "10% Deposit Monthly": f"RM {monthly_depo:,.2f}"
    })

st.markdown("### 📊 Variant Summary")
st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

st.markdown("📸 You may take a screenshot or copy the table for sharing.")
st.markdown("*📝 Calculations are based on DC Auto Pricelist, latest update April 2025.*")
