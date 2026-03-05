## Customer Churn Prediction Dashboard

An interactive dashboard that predicts which customers are likely to leave a telecom company. Built with machine learning, this tool helps identify at‑risk customers and reveals the key drivers of churn – so businesses can take action before it's too late. Built with Python and Streamlit.

## Live Demo
**[View the live dashboard here](https://customer-churn-analysis-gr59deseslxbxjdzng9qzq.streamlit.app/)**  
(Click the link – it may take a few seconds to wake up)

## About the Project
I wanted to answer a simple question: *Can we predict which customers are about to leave, and more importantly, why?*  
Using a real‑world dataset of 7,000+ telecom customers, I built a machine learning model that predicts churn with 79% accuracy. The dashboard lets you explore churn patterns, test predictions on new customers, and download lists of high‑risk accounts.

The dataset includes:
- **Customer demographics** (gender, senior citizen status, dependents)
- **Account information** (tenure, contract type, payment method)
- **Services used** (phone, internet, online security, streaming, etc.)
- **Churn label** – whether the customer left within the last month

## Features
- **Sidebar filters** – filter data by contract type and internet service to dynamically update charts.
- **Overview tab** – view key metrics (total customers, churn rate, average charges) and interactive bar charts showing churn by contract type and internet service.
- **High‑risk customer table** – see customers with monthly charges > $80 and tenure < 6 months.
- **Download button** – export the high‑risk list as a CSV file for targeted retention campaigns.
- **Prediction tab** – enter customer details to get an instant churn probability and risk level (low, moderate, high).
- **Model explainability** – the dashboard highlights which features most influence churn (e.g., month‑to‑month contracts, fiber optic service, high monthly charges).

##  Built With
- **Python** – pandas, numpy, scikit‑learn, joblib
- **Streamlit** – interactive web app framework
- **Plotly** – interactive charts
- **SQLite** – for querying the data
- **GitHub** – version control and deployment

##  Screenshots


![Overview](graph1&2__.png)
![Graph](graph1.2_.png)
![Table](table_.png)

##  Key Insights
- **Month‑to‑month contracts** are the strongest predictor of churn (43% churn rate vs. 3% for two‑year contracts).
- **New customers** (tenure < 6 months) are most vulnerable – churn rate drops significantly after the first year.
- **Fiber optic users** churn more than DSL users – possibly due to higher prices or competition.
- **Electronic check payment** is associated with higher churn; automatic payments (credit card, bank transfer) have much lower churn.
- **Price sensitivity** is real – customers who churn pay on average $13 more per month than those who stay.

##  How to Run Locally
1. Clone this repository  
   `git clone https://github.com/jzoe68159-png/customer-churn-analysis.git`
2. Create a virtual environment (optional but recommended)  
   `python -m venv venv`  
   `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies  
   `pip install -r requirements.txt`
4. Run the app  
   `streamlit run app.py`

##  Repository Structure
- `app.py` – main Streamlit dashboard
- `WA_Fn-UseC_-Telco-Customer-Churn.csv` – dataset
- `churn_model.pkl` – trained logistic regression model
- `model_columns.pkl` – feature names for prediction
- `requirements.txt` – Python packages
- `screenshots/` – images for README
- `README.md` – you're reading it!

## Author
Zoe John

Have questions? Feel free to reach out!


