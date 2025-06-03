import streamlit as st
import pandas as pd
import numpy as np

# Page setup
st.set_page_config(page_title="Used Cars EDA Dashboard", layout="wide")
st.title("🚗 Used Cars Price Analysis Dashboard")
st.markdown("""
### ✅ EDA Report: Used Cars Dataset

This exploratory analysis focuses on understanding key factors affecting used car prices, such as mileage, power, and ownership history.  
It also provides insights through interactive visualizations and filters, aiding predictive modeling and decision-making.
""")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("used_cars_cleaned.csv")

    # Convert Price from lakhs to rupees
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce') * 1e5

    # Clean & transform
    df['Mileage'] = pd.to_numeric(df['Mileage'].astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
    df['Engine'] = pd.to_numeric(df['Engine'].astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
    df['Power'] = pd.to_numeric(df['Power'].astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
    df['New_Price'] = df['New_Price'].astype(str).str.replace('Lakh', '', regex=False).str.strip()
    df['New_Price'] = pd.to_numeric(df['New_Price'], errors='coerce') * 1e5
    df['Brand'] = df['Name'].astype(str).str.split().str[0]

    # Fill missing values
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Price Range slider
min_price = int(df['Price'].min())
max_price = int(df['Price'].max())
price_range = st.sidebar.slider(
    "Select Price Range (₹)", 
    min_value=min_price, 
    max_value=max_price, 
    value=(min_price, max_price), 
    step=100000
)

# Mileage Range slider
min_mileage = int(df['Mileage'].min())
max_mileage = int(df['Mileage'].max())
mileage_range = st.sidebar.slider(
    "Select Mileage Range (kmpl)", 
    min_value=min_mileage, 
    max_value=max_mileage, 
    value=(min_mileage, max_mileage),
    step=1
)

# Engine Size Range slider
min_engine = int(df['Engine'].min())
max_engine = int(df['Engine'].max())
engine_range = st.sidebar.slider(
    "Select Engine Size Range (CC)", 
    min_value=min_engine, 
    max_value=max_engine, 
    value=(min_engine, max_engine),
    step=50
)

# Power Range slider
min_power = int(df['Power'].min())
max_power = int(df['Power'].max())
power_range = st.sidebar.slider(
    "Select Power Range (bhp)", 
    min_value=min_power, 
    max_value=max_power, 
    value=(min_power, max_power),
    step=1
)

# Year Range slider
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider(
    "Select Year Range", 
    min_value=min_year, 
    max_value=max_year, 
    value=(min_year, max_year),
    step=1
)

# Categorical filters
locations = st.sidebar.multiselect("Select Location(s)", sorted(df['Location'].unique()), default=None)
fuel_types = st.sidebar.multiselect("Select Fuel Type(s)", sorted(df['Fuel_Type'].unique()), default=None)
transmissions = st.sidebar.multiselect("Select Transmission(s)", sorted(df['Transmission'].unique()), default=None)
owner_types = st.sidebar.multiselect("Select Owner Type(s)", sorted(df['Owner_Type'].unique()), default=None)

# Apply filters
filtered_df = df[
    (df['Price'] >= price_range[0]) & (df['Price'] <= price_range[1]) &
    (df['Mileage'] >= mileage_range[0]) & (df['Mileage'] <= mileage_range[1]) &
    (df['Engine'] >= engine_range[0]) & (df['Engine'] <= engine_range[1]) &
    (df['Power'] >= power_range[0]) & (df['Power'] <= power_range[1]) &
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
]

if locations:
    filtered_df = filtered_df[filtered_df['Location'].isin(locations)]
if fuel_types:
    filtered_df = filtered_df[filtered_df['Fuel_Type'].isin(fuel_types)]
if transmissions:
    filtered_df = filtered_df[filtered_df['Transmission'].isin(transmissions)]
if owner_types:
    filtered_df = filtered_df[filtered_df['Owner_Type'].isin(owner_types)]

# Dataset Summary
st.subheader("📊 Dataset Overview")
st.dataframe(filtered_df.head(10), use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Total Cars", len(filtered_df))
col2.metric("Avg Price (₹)", f"{filtered_df['Price'].mean():,.0f}")
col3.metric("Avg Mileage (kmpl)", f"{filtered_df['Mileage'].mean():.2f}")

# --- Visualizations ---
st.markdown("---")
st.subheader("📈 Distribution Analysis")

st.markdown("**1. Price Distribution**")
st.bar_chart(filtered_df['Price'].value_counts().sort_index(ascending=True))


st.markdown("**2. Mileage Distribution**")
st.line_chart(filtered_df['Mileage'].value_counts().sort_index())

st.markdown("**3. Engine Size Distribution**")
st.bar_chart(filtered_df['Engine'].value_counts().sort_index())

st.markdown("---")
st.subheader("🧭 Category-Based Insights")

st.markdown("**4. Car Count by Fuel Type**")
st.bar_chart(filtered_df['Fuel_Type'].value_counts())

st.markdown("**5. Cars by Transmission**")
st.bar_chart(filtered_df['Transmission'].value_counts())

st.markdown("**6. Cars by Owner Type**")
st.bar_chart(filtered_df['Owner_Type'].value_counts())

# Yearly Price Trend
st.markdown("---")
st.subheader("📅 Average Price Over the Years")
year_trend = filtered_df.groupby("Year")["Price"].mean()
st.line_chart(year_trend)

# Price Comparison by Location
st.markdown("**7. Price by Location**")
location_price = filtered_df.groupby("Location")["Price"].mean().sort_values()
st.bar_chart(location_price)

# Correlation table
st.markdown("---")
st.subheader("📊 Correlation Table (Numerical Features)")
corr_matrix = filtered_df[['Price', 'Mileage', 'Power', 'Engine', 'Kilometers_Driven']].corr()
st.dataframe(corr_matrix.style.background_gradient(cmap='YlGnBu'), use_container_width=True)

# Price by Owner Type
st.markdown("**8. Avg Price by Owner Type**")
owner_price = filtered_df.groupby("Owner_Type")["Price"].mean()
st.bar_chart(owner_price)

st.markdown("---")
st.subheader("🔍 Most & Least Expensive Cars")


st.markdown("### 💸 Most Expensive Car(s)")
most_expensive = filtered_df[filtered_df['Price'] == filtered_df['Price'].max()]
st.dataframe(most_expensive, use_container_width=True)

st.markdown("### 💰 Least Expensive Car(s)")
least_expensive = filtered_df[filtered_df['Price'] == filtered_df['Price'].min()]
st.dataframe(least_expensive, use_container_width=True)

# Mileage vs Year with Price gradient (simplified)
st.markdown("---")
st.subheader("🚘 Mileage vs Year (colored by price range)")
df_copy = filtered_df.copy()
df_copy['Price_Category'] = pd.qcut(df_copy['Price'], q=3, labels=["Low", "Mid", "High"])
st.scatter_chart(df_copy, x='Year', y='Mileage', color='Price_Category')

# Footer
st.markdown("---")
st.markdown("📌 _Created with ❤️ by Sahil Karande | Streamlit 1.45.0 Compatible_")
