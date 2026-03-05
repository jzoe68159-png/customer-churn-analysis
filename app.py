import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Load data and model
@st.cache_data
def load_data():
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    # Clean as before
    df = df[df['TotalCharges'].str.strip() != ''].copy()
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    return df

@st.cache_resource
def load_model():
    model = joblib.load('churn_model.pkl')
    columns = joblib.load('model_columns.pkl')
    return model, columns

df = load_data()
model, model_columns = load_model()


# Helper function for prediction
def prepare_input(tenure, monthly_charges, contract, internet, payment, paperless):
    input_dict = {col: [0] for col in model_columns}
    input_dict['tenure'] = tenure
    input_dict['MonthlyCharges'] = monthly_charges
    input_dict['TotalCharges'] = tenure * monthly_charges
    input_dict['SeniorCitizen'] = 0

    if contract == 'One year':
        input_dict['Contract_One year'] = 1
    elif contract == 'Two year':
        input_dict['Contract_Two year'] = 1

    if internet == 'Fiber optic':
        input_dict['InternetService_Fiber optic'] = 1
    elif internet == 'No':
        input_dict['InternetService_No'] = 1

    if payment == 'Credit card (automatic)':
        input_dict['PaymentMethod_Credit card (automatic)'] = 1
    elif payment == 'Electronic check':
        input_dict['PaymentMethod_Electronic check'] = 1
    elif payment == 'Mailed check':
        input_dict['PaymentMethod_Mailed check'] = 1

    if paperless == 'Yes':
        input_dict['PaperlessBilling_Yes'] = 1

    return pd.DataFrame(input_dict)[model_columns]

# Streamlit UI
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")
st.title("📊 Customer Churn Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")

# Create filter widgets
contract_filter = st.sidebar.multiselect(
    "Select Contract Type(s)",
    options=df['Contract'].unique(),
    default=df['Contract'].unique()
)

internet_filter = st.sidebar.multiselect(
    "Select Internet Service(s)",
    options=df['InternetService'].unique(),
    default=df['InternetService'].unique()
)

# Apply filters to create a filtered dataframe
filtered_df = df[
    (df['Contract'].isin(contract_filter)) &
    (df['InternetService'].isin(internet_filter))
]
# Create tabs
tab1, tab2 = st.tabs(["📈 Overview", "🔮 Predict Churn"])

with tab1:
    st.header("Overview of Churn Patterns")

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", f"{len(filtered_df):,}")
    with col2:
        st.metric("Churn Rate", f"{filtered_df['Churn'].mean():.1%}")
    with col3:
        st.metric("Avg Monthly Charges", f"${filtered_df['MonthlyCharges'].mean():.2f}")
    with col4:
        st.metric("Avg Tenure", f"{filtered_df['tenure'].mean():.1f} months")

    # Two charts side by side
    col1, col2 = st.columns(2)
    with col1:
        contract_churn = filtered_df.groupby('Contract')['Churn'].mean().reset_index()
        fig1 = px.bar(contract_churn, x='Contract', y='Churn', title='Churn Rate by Contract Type')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        internet_churn = filtered_df.groupby('InternetService')['Churn'].mean().reset_index()
        fig2 = px.bar(internet_churn, x='InternetService', y='Churn', title='Churn Rate by Internet Service')
        st.plotly_chart(fig2, use_container_width=True)

    # High-risk customers table
    st.subheader("High-Risk Customers (Monthly Charges > $80, Tenure < 6 months)")
    high_risk = filtered_df[(filtered_df['MonthlyCharges'] > 80) & (filtered_df['tenure'] < 6)]
    st.dataframe(high_risk[['customerID', 'tenure', 'MonthlyCharges', 'Contract']].head(10),
                 use_container_width=True)

with tab2:
    st.header("Predict Churn for a New Customer")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.0, step=5.0)
            contract = st.selectbox("Contract Type", ['Month-to-month', 'One year', 'Two year'])
        with col2:
            internet = st.selectbox("Internet Service", ['DSL', 'Fiber optic', 'No'])
            payment = st.selectbox("Payment Method",
                                   ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
            paperless = st.selectbox("Paperless Billing", ['Yes', 'No'])

        submitted = st.form_submit_button("Predict")

    if submitted:
        input_df = prepare_input(tenure, monthly_charges, contract, internet, payment, paperless)
        prob = model.predict_proba(input_df)[0][1]
        st.subheader(f"Churn Probability: **{prob:.1%}**")

        if prob >= 0.7:
            st.error("🔴 High risk – immediate offer needed.")
        elif prob >= 0.4:
            st.warning("🟠 Moderate risk – consider promotional offer.")
        else:
            st.success("🟢 Low risk – no immediate action.")