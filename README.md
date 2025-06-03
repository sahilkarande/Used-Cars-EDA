# ✅ EDA Report: Used Cars Dataset

🔗 **Live Dashboard:** [usedcardataset.streamlit.app](https://usedcardataset.streamlit.app/)

---

## 📌 Objective

This Exploratory Data Analysis (EDA) project focuses on a dataset of used car listings to:

- Understand key factors influencing used car prices.
- Identify patterns in mileage, engine power, fuel type, transmission, and ownership history.
- Prepare the dataset for future predictive modeling or business insights.

---

## 📊 Dataset Overview

The dataset contains both numerical and categorical features related to used cars:

- **Numerical Features**: `Price`, `Mileage`, `Power`, `Engine`, `Kilometers_Driven`
- **Categorical Features**: `Fuel_Type`, `Transmission`, `Owner_Type`, `Location`, `Year`
- **Target Variable**: `Price`

---

## 🛠️ Tools & Technologies Used

- **Language**: Python  
- **Libraries**: `pandas`, `numpy`, `seaborn`, `matplotlib`, `plotly`, `streamlit`

---

## 📈 Dashboard Features

The deployed Streamlit dashboard includes:

- 🔎 Interactive filters (Location, Fuel Type, Transmission, Price, etc.)
- 📊 Visual insights:
  - Price distribution by bins
  - Mileage and engine size distribution
  - Fuel type and transmission breakdown
  - Price trends over the years
  - Correlation matrix of numerical features
- 🚘 Most and least expensive cars display
- 🧮 Summary statistics and dataset preview

Explore the live dashboard here: 👉 [https://usedcardataset.streamlit.app](https://usedcardataset.streamlit.app)

---

## 🛠 How to Run Locally

1. Clone the repository and place the cleaned dataset (`used_cars_cleaned.csv`) in the root directory.
2. Save the script as `streamlit_app.py`.
3. In your terminal, run:

   ```bash
   streamlit run streamlit_app.py
