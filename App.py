import streamlit as st

# Define tax slabs and rates for the new regime
NEW_TAX_SLABS = [
    (400000, 0.05),  # 4L - 8L @ 5%
    (400000, 0.10),  # 8L - 12L @ 10%
    (400000, 0.15),  # 12L - 16L @ 15%
    (400000, 0.20),  # 16L - 20L @ 20%
    (400000, 0.25),  # 20L - 24L @ 25%
    (float('inf'), 0.30)  # Above 24L @ 30%
]

# Define tax slabs for the old regime (based on standard deductions & exemptions)
OLD_TAX_SLABS = [
    (250000, 0.05),  # ₹2.5L - ₹5L @ 5%
    (250000, 0.10),  # ₹5L - ₹7.5L @ 10%
    (250000, 0.15),  # ₹7.5L - ₹10L @ 15%
    (250000, 0.20),  # ₹10L - ₹12.5L @ 20%
    (250000, 0.25),  # ₹12.5L - ₹15L @ 25%
    (float('inf'), 0.30)  # Above ₹15L @ 30%
]

# Function to calculate tax (New Regime)
def calculate_new_tax(income):
    standard_deduction = 75000
    taxable_income = max(0, income - standard_deduction)

    if taxable_income <= 1200000:
        return 0, 0, []  # No tax up to ₹12,00,000 after deduction

    tax = 0
    remaining_income = taxable_income
    start_limit = 0
    tax_breakup = []

    for slab, rate in NEW_TAX_SLABS:
        if remaining_income > 0:
            slab_tax = min(slab, remaining_income) * rate
            tax += slab_tax
            tax_breakup.append((start_limit, start_limit + min(slab, remaining_income), rate * 100, slab_tax))
            remaining_income -= min(slab, remaining_income)
        start_limit += slab

    # Marginal relief
    if taxable_income > 1200000:
        excess_income = taxable_income - 1200000
        max_additional_tax = excess_income
        tax = min(tax, max_additional_tax)

    # Add 4% Cess
    cess = tax * 0.04
    total_tax = tax + cess

    return round(total_tax), round(cess), tax_breakup

# Function to calculate tax (Old Regime)
def calculate_old_tax(income):
    taxable_income = max(0, income - 50000)  # ₹50,000 standard deduction in Old Regime

    if taxable_income <= 250000:
        return 0, 0, []  # No tax up to ₹2.5L

    tax = 0
    remaining_income = taxable_income
    start_limit = 0
    tax_breakup = []

    for slab, rate in OLD_TAX_SLABS:
        if remaining_income > 0:
            slab_tax = min(slab, remaining_income) * rate
            tax += slab_tax
            tax_breakup.append((start_limit, start_limit + min(slab, remaining_income), rate * 100, slab_tax))
            remaining_income -= min(slab, remaining_income)
        start_limit += slab

    # Add 4% Cess
    cess = tax * 0.04
    total_tax = tax + cess

    return round(total_tax), round(cess), tax_breakup

# Streamlit UI
st.title("💰 Bank-err's Income Tax Calculator for FY 2025-26")

# Tabs for New & Old Regime
tab1, tab2 = st.tabs(["New Tax Regime", "Old Tax Regime"])

with tab1:
    st.write("### **As per New Tax Regime**")
    st.write("### **Marginal income relief applied**")

    # Bigger, colorful input field
    income = st.number_input(
        "Enter your Annual Income (in ₹)",
        min_value=0,
        step=1000,
        format="%d",
    )

    # Calculate Tax (New Regime)
    if st.button("Calculate Tax (New Regime)"):
        total_tax, cess, tax_breakup = calculate_new_tax(income)
        st.success(f"🧾 Your total tax: ₹{total_tax}")

        # Show tax breakup
        if st.checkbox("Show Tax & Cess Breakup"):
            st.write("### **Tax Breakdown (New Regime):**")
            for start, end, rate, slab_tax in tax_breakup:
                st.write(f"✔ **₹{start} - ₹{end} @ {rate}%** = ₹{slab_tax}")
            st.write(f"### **Cess (4%) = ₹{cess}**")

with tab2:
    st.write("### **As per Old Tax Regime**")
    st.write("### **Includes Standard Deduction & Slabs from IT Dept.**")

    # Bigger, colorful input field
    income_old = st.number_input(
        "Enter your Annual Income (in ₹) for Old Regime",
        min_value=0,
        step=1000,
        format="%d",
    )

    # Calculate Tax (Old Regime)
    if st.button("Calculate Tax (Old Regime)"):
        total_tax_old, cess_old, tax_breakup_old = calculate_old_tax(income_old)
        st.success(f"🧾 Your total tax (Old Regime): ₹{total_tax_old}")

        # Show tax breakup
        if st.checkbox("Show Tax & Cess Breakup (Old Regime)"):
            st.write("### **Tax Breakdown (Old Regime):**")
            for start, end, rate, slab_tax in tax_breakup_old:
                st.write(f"✔ **₹{start} - ₹{end} @ {rate}%** = ₹{slab_tax}")
            st.write(f"### **Cess (4%) = ₹{cess_old}**")

# Footer with cyan-colored text
st.markdown(
    '<p style="color:cyan; font-size:16px; font-weight:bold; text-align:center;">Created by - Paramjeet Singh Gusain</p>',
    unsafe_allow_html=True
)
