import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Used Cars EDA Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("used_cars_data.csv")
    df['Mileage'] = pd.to_numeric(df['Mileage'].str.split().str[0], errors='coerce')
    df['Engine'] = pd.to_numeric(df['Engine'].str.split().str[0], errors='coerce')
    df['Power'] = pd.to_numeric(df['Power'].str.split().str[0], errors='coerce')
    df['New_Price'] = pd.to_numeric(df['New_Price'].str.replace('Lakh', '').str.strip(), errors='coerce') * 100000
    df['Brand'] = df['Name'].str.split().str[0]
    df.fillna(method='ffill', inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filter Options")
locations = st.sidebar.multiselect("Select Locations", options=df['Location'].unique(), default=df['Location'].unique())
fuel_types = st.sidebar.multiselect("Select Fuel Types", options=df['Fuel_Type'].unique(), default=df['Fuel_Type'].unique())
transmissions = st.sidebar.multiselect("Select Transmissions", options=df['Transmission'].unique(), default=df['Transmission'].unique())

df = df[df['Location'].isin(locations) & df['Fuel_Type'].isin(fuel_types) & df['Transmission'].isin(transmissions)]

# Title
st.title("🚗 Used Cars Data Analysis Dashboard")
st.markdown("""
This interactive dashboard helps in understanding used car listings across various cities by visualizing:
- Price variations
- Feature distributions
- Outliers and patterns
- Most and least expensive listings
- Correlations among numeric features
""")

# Overview Section
st.header("📊 Dataset Overview")
st.dataframe(df.head(10))
st.write("Shape of dataset:", df.shape)

# Descriptive Statistics
st.subheader("📈 Summary Statistics")
st.dataframe(df.describe())

# Categorical Distributions
st.subheader("🔧 Categorical Feature Distributions")
cats = ['Fuel_Type', 'Transmission', 'Owner_Type']
cols = st.columns(len(cats))
for i, cat in enumerate(cats):
    with cols[i]:
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.countplot(x=cat, data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

# Histograms and Boxplots
st.subheader("📦 Numerical Feature Distributions")
numerical_cols = ['Price', 'Engine', 'Mileage']
for col in numerical_cols:
    st.markdown(f"#### {col} Distribution")
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        sns.histplot(df[col], bins=30, ax=ax)
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots()
        sns.boxplot(x=df[col], ax=ax)
        st.pyplot(fig)

# Price by Year
st.subheader("📅 Average Price by Year")
yearly_avg = df.groupby('Year')['Price'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=yearly_avg, x='Year', y='Price', marker='o', ax=ax)
st.pyplot(fig)

# Price by Location
st.subheader("📍 Price Distribution by Location")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df, x='Location', y='Price', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Scatterplots
st.subheader("🧮 Price Correlation with Features")
features = ['Mileage', 'Engine', 'Power', 'Kilometers_Driven']
for feat in features:
    st.markdown(f"#### Price vs {feat}")
    fig, ax = plt.subplots()
    sns.scatterplot(x=df[feat], y=df['Price'], ax=ax)
    st.pyplot(fig)

# Multivariate Interaction
st.subheader("🧪 Price by Fuel Type and Transmission")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x='Fuel_Type', y='Price', hue='Transmission', ax=ax)
st.pyplot(fig)

# Outliers
st.subheader("🚨 Outlier Detection")
outlier_cols = ['Price', 'Engine', 'Power']
cols = st.columns(3)
for i, feat in enumerate(outlier_cols):
    with cols[i]:
        fig, ax = plt.subplots()
        sns.boxplot(x=df[feat], ax=ax)
        st.pyplot(fig)

# Most & Least Expensive Cars
st.subheader("💰 Most & Least Expensive Cars")
st.markdown("**Most Expensive:**")
st.write(df[df['Price'] == df['Price'].max()])
st.markdown("**Least Expensive:**")
st.write(df[df['Price'] == df['Price'].min()])

# Owner Type vs Price
st.subheader("🧍 Owner Type vs Average Price")
avg_price_owner = df.groupby('Owner_Type')['Price'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='Owner_Type', y='Price', data=avg_price_owner, order=['First', 'Second', 'Third', 'Fourth & Above'], ax=ax)
st.pyplot(fig)

# Mileage vs Year vs Price
st.subheader("📉 Mileage vs Year (colored by Price)")
fig, ax = plt.subplots()
sns.scatterplot(x='Year', y='Mileage', hue='Price', data=df, ax=ax)
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Data Source: Used Cars Listings")
