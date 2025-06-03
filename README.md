### ✅ EDA Report: Used Cars Dataset

#### 📌 **Objective**

This EDA project focuses on analyzing a dataset of used car listings to:

* Understand key factors affecting used car prices.
* Identify patterns in car attributes like mileage, power, fuel type, and ownership history.
* Prepare the dataset for predictive modeling.

#### 📊 **Dataset Overview**

The dataset includes:

* **Numerical Features**: `Price`, `Mileage`, `Power`, `Engine`, `Kilometers Driven`
* **Categorical Features**: `Fuel Type`, `Transmission`, `Owner Type`, `Location`, `Year`
* **Target Variable**: `Price`

#### 🛠️ **Tools Used**

* **Python Libraries**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`

---

### 📈 Key Visual Insights (from notebook)

I'll now generate a Streamlit dashboard that will include:

1. A data table
2. Summary statistics
3. Interactive filters
4. Visualizations:

   * Histogram of Prices
   * Distribution of Mileage and Power
   * Price vs Year (line or scatter)
   * Box plots by Fuel Type or Owner Type
5. Basic query functionality


### 🛠 How to Run:

1. Save this as `streamlit_app.py`.
2. Make sure you have a cleaned CSV file (`used_cars_cleaned.csv`) in the same directory.
3. Run using:

   ```bash
   streamlit run streamlit_app.py
   ```

If you’d like, I can also help you clean your dataset and generate that CSV file. Just upload the dataset or let me know!

