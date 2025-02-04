import streamlit as st

# Define tax slabs and rates
TAX_SLABS = [
    (400000, 0.05),  # 4L - 8L @ 5%
    (400000, 0.10),  # 8L - 12L @ 10%
    (400000, 0.15),  # 12L - 16L @ 15%
    (400000, 0.20),  # 16L - 20L @ 20%
    (400000, 0.25),  # 20L - 24L @ 25%
    (float('inf'), 0.30)  # Above 24L @ 30%
]

# Function to calculate tax and provide breakup
def calculate_tax(income):
    standard_deduction = 75000
    taxable_income = max(0, income - standard_deduction)

    if taxable_income <= 1200000:
        return 0, 0, []  # No tax up to ₹12,00,000 after deduction

    # Slab-wise tax calculation
    tax = 0
    remaining_income = taxable_income
    start_limit = 0
    tax_breakup = []

    for slab, rate in TAX_SLABS:
        if remaining_income > 0:
            slab_tax = min(slab, remaining_income) * rate
            tax += slab_tax
            tax_breakup.append((start_limit, start_limit + min(slab, remaining_income), rate * 100, slab_tax))
            remaining_income -= min(slab, remaining_income)
        start_limit += slab

    # Marginal relief (if applicable)
    if taxable_income > 1200000:
        excess_income = taxable_income - 1200000
        max_additional_tax = excess_income  # Maximum additional tax allowed for relief
        tax = min(tax, max_additional_tax)

    # Add 4% Cess
    cess = tax * 0.04
    total_tax = tax + cess

    return round(total_tax), round(cess), tax_breakup

# Streamlit UI
st.title("💰 Bank-err's Income Tax Calculator for FY 2025-26")
st.write("### **As per new tax regime**")
st.write("### **Marginal income relief applied**")

# Custom styling for input field
st.markdown(
    """
    <style>
    div[data-baseweb="input"] {
        width: 400px !important;
        border: 2px solid #ff6347;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px;
        background-color: #f8f9fa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Bigger, colorful income input field
income = st.number_input(
    "Enter your Annual Income (in ₹)",
    min_value=0,
    step=1000,
    format="%d",
)

# Calculate Tax
if st.button("Calculate Tax"):
    total_tax, cess, tax_breakup = calculate_tax(income)
    st.success(f"🧾 Your total tax: ₹{total_tax}")

    # Show tax breakup if requested
    if st.checkbox("Show Tax & Cess Breakup"):
        st.write("### **Tax Breakdown:**")
        for start, end, rate, slab_tax in tax_breakup:
            st.write(f"✔ **₹{start} - ₹{end} @ {rate}%** = ₹{slab_tax}")

        st.write(f"### **Cess (4%) = ₹{cess}**")

# Footer with cyan-colored text
st.markdown(
    '<p style="color:cyan; font-size:16px; font-weight:bold; text-align:center;">Created by - Paramjeet Singh Gusain</p>',
    unsafe_allow_html=True
)
