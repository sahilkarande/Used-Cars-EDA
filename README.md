# 🚗 Used Cars Price Analysis Dashboard

🔗 **Live Dashboard:** [usedcardataset.streamlit.app](https://usedcardataset.streamlit.app/)
https://github.com/sahilkarande/Used-Cars-EDA/blob/main/Used%20Cars%20Price%20Analysis.png

![Used Cars Analysis](https://github.com/sahilkarande/Used-Cars-EDA/blob/main/Used%20Cars%20Price%20Analysis.png)


---

## 📌 Objective

This Exploratory Data Analysis (EDA) project explores a used cars dataset to:

- Understand key factors influencing used car prices.
- Identify trends in mileage, engine size, fuel type, transmission, and ownership.
- Derive actionable insights for consumers, sellers, or dealerships.
- Prepare the dataset for future predictive modeling or business applications.

---

## 📊 Dataset Overview

The dataset contains both **numerical** and **categorical** attributes of used car listings:

- **Numerical Features**: `Price`, `Mileage`, `Power`, `Engine`, `Kilometers_Driven`
- **Categorical Features**: `Brand`, `Fuel_Type`, `Transmission`, `Owner_Type`, `Location`, `Year`
- **Target Variable**: `Price`

---

## 💡 Key Performance Indicators

| KPI                          | Value         |
|-----------------------------|---------------|
| 📦 **Total Listings**       | 7244          |
| 💰 **Avg. Price (₹)**       | ₹883,329      |
| ⛽ **Avg. Mileage (kmpl)**   | 18.12         |
| 🔧 **Avg. Power (bhp)**      | 112.25        |
| 🛢️ **Most Common Fuel**     | Diesel        |
| 🏷️ **Top Brand**            | Maruti        |

---

## 🧠 Insights Derived

- 💸 **Price varies significantly** based on location and brand; luxury brands dominate higher price brackets.
- ⛽ **Diesel cars are slightly costlier**, but their mileage advantage is not always significant.
- ⚙️ **Automatic transmissions** are more expensive and mostly appear in newer models.
- 🚦 **First-owner cars** are valued higher and are usually more recent.
- 📈 **Positive correlation** exists between `Engine`, `Power`, and `Price`.

---

## 📈 Dashboard Features

The interactive Streamlit dashboard includes:

- 🔎 **Dynamic Filters**: Location, Fuel Type, Transmission, Owner Type, Brand, Price Range, etc.
- 📊 **Visual Analytics**:
  - Distribution plots for price, mileage, and power
  - Brand-wise price comparisons
  - Fuel and transmission breakdown
  - Year-wise trends in car prices
  - Correlation heatmap for numerical features
- 🚘 **Highlights**: Most and least expensive cars
- 🧮 **Quick Stats**: Summary cards and KPIs
- 🧾 **Data Preview**: Interactive dataframe viewer

Explore the live version 👉 [https://usedcardataset.streamlit.app](https://usedcardataset.streamlit.app)

---

## 🛠️ Tools & Technologies

- **Language**: Python  
- **Libraries**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `streamlit`
- **Deployment**: Streamlit Cloud

---

## 🧪 How to Run Locally

1. Clone this repository and place the cleaned dataset (`used_cars_cleaned.csv`) in the root folder.
2. Save the dashboard script as `streamlit_app.py`.
3. Run the app using:

   ```bash
   streamlit run streamlit_app.py
