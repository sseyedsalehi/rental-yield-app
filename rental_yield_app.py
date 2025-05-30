#minor change
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Rental Yield Calculator", layout="centered")
st.title("🏠 Rental Yield Calculator")
st.markdown("""
Upload a CSV file with the following columns:
- **Suburb**
- **Price** (e.g., 750000)
- **Weekly_Rent** (e.g., 600)
""")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully")
else:
    st.warning("⚠️ No file uploaded. Using default sample data.")
    sample_file = 'sample_data.csv'
    df = pd.read_csv(sample_file)

# Drop rows with missing data
df.dropna(inplace=True)

# Calculate Annual Rent and Gross Yield
df['Annual_Rent'] = df['Weekly_Rent'] * 52
df['Gross_Yield'] = (df['Annual_Rent'] / df['Price']) * 100

# Assume annual costs as % of annual rent
vacancy_rate = 0.05
maintenance_rate = 0.05
management_rate = 0.05

# Calculate total annual costs and net yield
df['Annual_Cost'] = df['Annual_Rent'] * (vacancy_rate + maintenance_rate + management_rate)
df['Net_Yield'] = ((df['Annual_Rent'] - df['Annual_Cost']) / df['Price']) * 100

# Show results
st.subheader("📊 Rental Yield Table")
st.dataframe(df[['Suburb', 'Price', 'Weekly_Rent', 'Gross_Yield', 'Net_Yield']].sort_values(by='Net_Yield', ascending=False))

# Plot Net Yield Chart
st.subheader("📈 Net Yield by Suburb")
fig, ax = plt.subplots()
ax.bar(df['Suburb'], df['Net_Yield'], color='skyblue')
plt.xticks(rotation=45)
plt.ylabel("Net Yield (%)")
plt.title("Net Rental Yield per Suburb")
st.pyplot(fig)

# Export button
st.subheader("📁 Download Results")
export_file = "rental_yield_results.xlsx"
df.to_excel(export_file, index=False)
with open(export_file, "rb") as f:
    st.download_button(label="📥 Download Excel File", data=f, file_name=export_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
