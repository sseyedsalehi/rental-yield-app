# minor change
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rental Yield Calculator", layout="wide")

st.title("🏡 Rental Yield Calculator")
st.write("Upload a CSV file with columns: `Suburb`, `Price`, and `Weekly_Rent`. Or use sample data below.")

# Upload CSV
uploaded_file = st.file_uploader("Upload your property data (.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded — using sample data below 👇")
    sample_data = {
        'Suburb': ['Hawthorn', 'Richmond', 'Brunswick', 'Footscray', 'Southbank'],
        'Price': [850000, 790000, 710000, 670000, 910000],
        'Weekly_Rent': [650, 630, 600, 580, 700]
    }
    df = pd.DataFrame(sample_data)

# Clean and prepare data
df.dropna(inplace=True)
df['Annual_Rent'] = df['Weekly_Rent'] * 52

# Sidebar: Adjustable costs
st.sidebar.header("Cost Assumptions")
vacancy_rate = st.sidebar.slider("Vacancy Rate (%)", 0.0, 10.0, 2.0) / 100
property_tax = st.sidebar.slider("Property Tax (%)", 0.0, 5.0, 1.0) / 100
maintenance = st.sidebar.slider("Maintenance (% of price)", 0.0, 5.0, 1.0) / 100
insurance = st.sidebar.slider("Insurance (% of price)", 0.0, 3.0, 0.5) / 100
include_strata = st.sidebar.checkbox("Include Strata Fees", value=False)
strata_annual = st.sidebar.number_input("Annual Strata ($)", value=2500.0) if include_strata else 0

# Calculations
df['Vacancy_Loss'] = df['Annual_Rent'] * vacancy_rate
df['Property_Tax'] = df['Price'] * property_tax
df['Maintenance_Cost'] = df['Price'] * maintenance
df['Insurance_Cost'] = df['Price'] * insurance
df['Strata_Fees'] = strata_annual

df['Net_Annual_Income'] = df['Annual_Rent'] - (
    df['Vacancy_Loss'] +
    df['Property_Tax'] +
    df['Maintenance_Cost'] +
    df['Insurance_Cost'] +
    df['Strata_Fees']
)

df['Gross_Yield'] = (df['Annual_Rent'] / df['Price']) * 100
df['Net_Yield'] = (df['Net_Annual_Income'] / df['Price']) * 100

# Display
st.subheader("📊 Rental Yield Summary")
st.dataframe(df[['Suburb', 'Price', 'Weekly_Rent', 'Gross_Yield', 'Net_Yield']].round(2))

# Bar Chart
st.subheader("📈 Net Yield by Suburb")
fig, ax = plt.subplots()
ax.bar(df['Suburb'], df['Net_Yield'], color='skyblue')
ax.set_ylabel("Net Rental Yield (%)")
st.pyplot(fig)

# Export
st.subheader("📁 Download Results")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)
st.download_button("Download CSV", csv, "rental_yield_results.csv", "text/csv")
