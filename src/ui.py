# src/ui.py
import streamlit as st
import requests
import json

st.title("Customer Churn Prediction")
st.write("Enter customer details to predict if they will churn.")

# Create input fields for the user - UPDATED
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=50.0)
total_charges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=1000.0)
senior_citizen = st.selectbox("Senior Citizen?", ["No", "Yes"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
partner = st.selectbox("Has Partner?", ["Yes", "No"])
dependents = st.selectbox("Has Dependents?", ["Yes", "No"])
phone_service = st.selectbox("Has Phone Service?", ["Yes", "No"])
paperless_billing = st.selectbox("Has Paperless Billing?", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female"])
multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])


if st.button("Predict Churn"):
    # Convert user-friendly inputs to the one-hot encoded format for the API - UPDATED
    api_input = {
        "tenure": tenure, "MonthlyCharges": monthly_charges, "TotalCharges": total_charges,
        "SeniorCitizen": 1 if senior_citizen == "Yes" else 0, # <--- GÜNCELLENDİ
        "Partner": 1 if partner == "Yes" else 0,
        "Dependents": 1 if dependents == "Yes" else 0,
        "PhoneService": 1 if phone_service == "Yes" else 0,
        "PaperlessBilling": 1 if paperless_billing == "Yes" else 0,
        "gender_Male": 1 if gender == "Male" else 0,
        "InternetService_Fiber_optic": 0, "InternetService_No": 0, # <--- GÜNCELLENDİ
        "MultipleLines_No_phone_service": 0, "MultipleLines_Yes": 0,
        "OnlineSecurity_No_internet_service": 0, "OnlineSecurity_Yes": 0,
        "OnlineBackup_No_internet_service": 0, "OnlineBackup_Yes": 0,
        "DeviceProtection_No_internet_service": 0, "DeviceProtection_Yes": 0,
        "TechSupport_No_internet_service": 0, "TechSupport_Yes": 0,
        "StreamingTV_No_internet_service": 0, "StreamingTV_Yes": 0,
        "StreamingMovies_No_internet_service": 0, "StreamingMovies_Yes": 0,
        "Contract_One_year": 0, "Contract_Two_year": 0,
        "PaymentMethod_Credit_card_automatic": 0,
        "PaymentMethod_Electronic_check": 0,
        "PaymentMethod_Mailed_check": 0
    }

    # Set the correct one-hot encoded fields to 1 based on selection - UPDATED
    if internet_service == "Fiber optic": api_input["InternetService_Fiber_optic"] = 1
    elif internet_service == "No": api_input["InternetService_No"] = 1

    if multiple_lines == "Yes": api_input["MultipleLines_Yes"] = 1
    elif multiple_lines == "No phone service": api_input["MultipleLines_No_phone_service"] = 1
    
    if online_security == "Yes": api_input["OnlineSecurity_Yes"] = 1
    elif online_security == "No internet service": api_input["OnlineSecurity_No_internet_service"] = 1

    if online_backup == "Yes": api_input["OnlineBackup_Yes"] = 1
    elif online_backup == "No internet service": api_input["OnlineBackup_No_internet_service"] = 1
    
    if device_protection == "Yes": api_input["DeviceProtection_Yes"] = 1
    elif device_protection == "No internet service": api_input["DeviceProtection_No_internet_service"] = 1
    
    if tech_support == "Yes": api_input["TechSupport_Yes"] = 1
    elif tech_support == "No internet service": api_input["TechSupport_No_internet_service"] = 1

    if streaming_tv == "Yes": api_input["StreamingTV_Yes"] = 1
    elif streaming_tv == "No internet service": api_input["StreamingTV_No_internet_service"] = 1
    
    if streaming_movies == "Yes": api_input["StreamingMovies_Yes"] = 1
    elif streaming_movies == "No internet service": api_input["StreamingMovies_No_internet_service"] = 1

    if contract == "One year": api_input["Contract_One_year"] = 1
    elif contract == "Two year": api_input["Contract_Two_year"] = 1

    if payment_method == "Electronic check": api_input["PaymentMethod_Electronic_check"] = 1
    elif payment_method == "Mailed check": api_input["PaymentMethod_Mailed_check"] = 1
    elif payment_method == "Credit card (automatic)": api_input["PaymentMethod_Credit_card_automatic"] = 1

    # Send a request to the FastAPI
    api_url = "http://127.0.0.1:8000/predict"
    try:
        response = requests.post(api_url, data=json.dumps(api_input))
        response.raise_for_status() 
        
        result = response.json()
        prediction_label = result['prediction_label']

        if prediction_label == "Churn":
            st.error("Prediction: Customer will CHURN")
        else:
            st.success("Prediction: Customer will NOT CHURN")

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the API. Make sure it is running. Error: {e}")