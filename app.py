import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Streamlit Page Config
st.set_page_config(
    page_title="Used Cars EDA Dashboard",
    layout="wide",
    page_icon="🚗",
    initial_sidebar_state="expanded"
)

# Custom Styling for dark theme
st.markdown("""
    <style>
        html, body, [class*="css"] {
            color: #f8f9fa;
            background-color: #121212;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(to bottom, #212529, #343a40);
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .metric {
            background-color: #1f1f1f;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 2px 6px rgba(255,255,255,0.05);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Used Cars Price Analysis Dashboard")
st.markdown("""
This interactive dashboard helps analyze the used car market based on various features such as mileage, engine, brand, fuel type, and ownership.  
Utilize the filters to dig deeper into trends and pricing insights.
""")
from streamlit_card import card


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("used_cars_cleaned.csv")
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce') * 1e5
    df['Mileage'] = pd.to_numeric(df['Mileage'].astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
    df['Engine'] = pd.to_numeric(df['Engine'].astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
    df['Power'] = pd.to_numeric(df['Power'].astype(str).str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
    df['New_Price'] = df['New_Price'].astype(str).str.replace('Lakh', '', regex=False).str.strip()
    df['New_Price'] = pd.to_numeric(df['New_Price'], errors='coerce') * 1e5
    df['Brand'] = df['Name'].astype(str).str.split().str[0]
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter the Cars")
with st.sidebar:
    price_range = st.slider("Price (₹)", int(df['Price'].min()), int(df['Price'].max()), (int(df['Price'].min()), int(df['Price'].max())))
    mileage_range = st.slider("Mileage (kmpl)", int(df['Mileage'].min()), int(df['Mileage'].max()), (int(df['Mileage'].min()), int(df['Mileage'].max())))
    engine_range = st.slider("Engine (CC)", int(df['Engine'].min()), int(df['Engine'].max()), (int(df['Engine'].min()), int(df['Engine'].max())))
    power_range = st.slider("Power (bhp)", int(df['Power'].min()), int(df['Power'].max()), (int(df['Power'].min()), int(df['Power'].max())))
    year_range = st.slider("Year", int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))
    locations = st.multiselect("Location", sorted(df['Location'].unique()))
    fuels = st.multiselect("Fuel Type", sorted(df['Fuel_Type'].unique()))
    transmissions = st.multiselect("Transmission", sorted(df['Transmission'].unique()))
    owners = st.multiselect("Owner Type", sorted(df['Owner_Type'].unique()))

# Apply Filters
filtered = df[
    (df['Price'].between(*price_range)) &
    (df['Mileage'].between(*mileage_range)) &
    (df['Engine'].between(*engine_range)) &
    (df['Power'].between(*power_range)) &
    (df['Year'].between(*year_range))
]
if locations: filtered = filtered[filtered['Location'].isin(locations)]
if fuels: filtered = filtered[filtered['Fuel_Type'].isin(fuels)]
if transmissions: filtered = filtered[filtered['Transmission'].isin(transmissions)]
if owners: filtered = filtered[filtered['Owner_Type'].isin(owners)]

st.markdown("---")
st.markdown("### 📊 Key Performance Indicators")

# Define 2 rows of 3 columns
kpi1, kpi2, kpi3 = st.columns(3)
kpi4, kpi5, kpi6 = st.columns(3)

# Style template
def styled_card(icon, title, value, bg_color):
    return f"""
    <div style='
        background-color:{bg_color};
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        color: #333;
        margin: 10px;           
    '>
        <div style='font-size: 1.2rem; margin-bottom: 0.5rem;'>{icon} <b>{title}</b></div>
        <div style='font-size: 2rem; font-weight: bold;'>{value}</div>
    </div>
    """

# Row 1 KPIs
kpi1.markdown(styled_card("📦", "Total Listings", len(filtered), "#e8f5e9"), unsafe_allow_html=True)
kpi2.markdown(styled_card("💰", "Avg. Price (₹)", f"{filtered['Price'].mean():,.0f}", "#e3f2fd"), unsafe_allow_html=True)
kpi3.markdown(styled_card("⛽", "Avg. Mileage (kmpl)", f"{filtered['Mileage'].mean():.2f}", "#fff8e1"), unsafe_allow_html=True)



# Row 2 KPIs
kpi4.markdown(styled_card("🔧", "Avg. Power (bhp)", f"{filtered['Power'].mean():.2f}", "#f1f8e9"), unsafe_allow_html=True)
kpi5.markdown(styled_card("🛢️", "Most Common Fuel", filtered['Fuel_Type'].mode()[0], "#e1f5fe"), unsafe_allow_html=True)
kpi6.markdown(styled_card("🏷️", "Top Brand", filtered['Brand'].mode()[0], "#fff3e0"), unsafe_allow_html=True)


# Insights Section
st.markdown("---")
st.subheader("🧠 Insights Derived")

st.markdown("""
- 💸 **Price varies drastically** by location and brand. Luxury brands dominate the high end.
- ⛽ **Diesel cars are slightly costlier** on average, but not always more efficient.
- ⚙️ **Automatic cars are costlier**, but they're more common in newer models.
- 🚦 **First-owner cars** fetch a better price and appear in newer year ranges.
- 📈 **Positive correlation** exists between Engine CC, Power, and Price.
""")

# Charts
st.markdown("---")
st.subheader("📈 Visual Explorations")

chart1, chart2 = st.columns(2)
with chart1:
    st.markdown("**Price by Fuel Type**")
    fig = px.box(filtered, x='Fuel_Type', y='Price', color='Fuel_Type')
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.markdown("**Price by Transmission**")
    fig = px.box(filtered, x='Transmission', y='Price', color='Transmission')
    st.plotly_chart(fig, use_container_width=True)

# Line Chart: Average Price by Year
st.markdown("**📅 Price Trend Over the Years**")
fig = px.line(
    filtered.groupby("Year")["Price"].mean().reset_index(), 
    x="Year", y="Price", markers=True, 
    title="Average Price by Year"
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Bar Chart: Average Price by Location
st.markdown("**📍 Average Price by Location**")
fig = px.bar(
    filtered.groupby("Location")["Price"].mean().sort_values(ascending=False).reset_index(), 
    x="Location", y="Price", color="Location",
    title="Average Car Price by Location"
)
fig.update_layout(showlegend=False, template="plotly_dark", xaxis_title="Location", yaxis_title="Avg Price (₹)")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Correlation Matrix
# -----------------------------
st.markdown("### 🔗 Feature Correlation Matrix")
corr_matrix = filtered[['Price', 'Mileage', 'Power', 'Engine', 'Kilometers_Driven']].corr()
fig = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    title="Correlation Heatmap"
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Most and Least Expensive Cars
# -----------------------------
st.markdown("### 💸 Most Expensive Car(s)")
most_expensive = filtered[filtered['Price'] == filtered['Price'].max()]
st.dataframe(most_expensive, use_container_width=True)

st.markdown("### 💰 Least Expensive Car(s)")
least_expensive = filtered[filtered['Price'] == filtered['Price'].min()]
st.dataframe(least_expensive, use_container_width=True)

# -----------------------------
# Mileage vs Year colored by Price Category
# -----------------------------
st.markdown("### 🚘 Mileage vs Year (Colored by Price Segment)")
df_copy = filtered.copy()
df_copy['Price_Category'] = pd.qcut(df_copy['Price'], q=3, labels=["Low", "Mid", "High"])
fig = px.scatter(
    df_copy, x='Year', y='Mileage', color='Price_Category',
    title="Mileage vs Year Colored by Price Range",
    labels={"Price_Category": "Price Segment"}
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <sub>📌 Built with ❤️ by <strong>Sahil Karande</strong> | CDAC Mumbai - DBDA | Streamlit v1.45</sub>
</div>
""", unsafe_allow_html=True)
