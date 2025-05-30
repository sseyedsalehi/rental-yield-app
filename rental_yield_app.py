import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Rental Yield Calculator", layout="centered")

st.title("🏠 Rental Yield Calculator")

uploaded_file = st.file_uploader("📁 Upload your property CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df.dropna(inplace=True)
        df['Annual_Rent'] = df['Weekly_Rent'] * 52
        df['Gross_Yield'] = (df['Annual_Rent'] / df['Price']) * 100

        st.markdown("### 🛠️ Cost Assumptions")
        vacancy_rate = st.slider("Vacancy Rate (%)", 0.0, 10.0, 4.0)
        property_tax_rate = st.slider("Annual Property Tax (%)", 0.0, 5.0, 0.5)
        maintenance_rate = st.slider("Annual Maintenance (%)", 0.0, 5.0, 0.5)
        management_fee_rate = st.slider("Property Management Fee (%)", 0.0, 10.0, 5.0)

        st.markdown("### 🧾 Additional Annual Costs")
        insurance_cost = st.number_input("Annual Insurance Cost ($)", min_value=0, value=1200)
        include_strata = st.checkbox("Include Strata Fees?")
        strata_fee = st.number_input("Annual Strata Fee ($)", min_value=0, value=2500) if include_strata else 0

        df['Vacancy_Cost'] = (vacancy_rate / 100) * df['Annual_Rent']
        df['Property_Tax'] = (property_tax_rate / 100) * df['Price']
        df['Maintenance_Cost'] = (maintenance_rate / 100) * df['Price']
        df['Management_Fee'] = (management_fee_rate / 100) * df['Annual_Rent']

        df['Net_Rent'] = (
            df['Annual_Rent']
            - df['Vacancy_Cost']
            - df['Property_Tax']
            - df['Maintenance_Cost']
            - df['Management_Fee']
            - insurance_cost
            - strata_fee
        )

        df['Net_Yield'] = (df['Net_Rent'] / df['Price']) * 100

        st.markdown("### 📊 Yield Overview")
        st.dataframe(df[['Suburb', 'Price', 'Weekly_Rent', 'Gross_Yield', 'Net_Yield']])

        # Bar chart
        st.markdown("### 📈 Net Yield Comparison")
        fig, ax = plt.subplots()
        ax.bar(df['Suburb'], df['Net_Yield'])
        ax.set_ylabel("Net Yield (%)")
        ax.set_title("Net Rental Yield by Suburb")
        st.pyplot(fig)

        # Download
        st.markdown("### 📥 Download Results")
        to_download = df.copy()
        buffer = io.BytesIO()
        to_download.to_excel(buffer, index=False)
        st.download_button(
            label="Download Excel File",
            data=buffer,
            file_name="rental_yield_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")

else:
    st.info("Upload a file with at least Suburb, Price, and Weekly_Rent columns.")
