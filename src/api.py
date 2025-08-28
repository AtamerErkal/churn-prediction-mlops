# src/api.py
import pandas as pd
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel

try:
    PROCESSED_DATA_PATH = "data/processed/processed_data.csv"
    df_processed = pd.read_csv(PROCESSED_DATA_PATH)
    TRAINING_COLUMNS = df_processed.drop(columns=["Churn"]).columns.tolist()
except FileNotFoundError:
    print(f"Error: Processed data file not found at {PROCESSED_DATA_PATH}")
    TRAINING_COLUMNS = []


# Define the input data schema using Pydantic - UPDATED
class CustomerData(BaseModel):
    SeniorCitizen: int  # <--- YENİ EKLENDİ
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Partner: int
    Dependents: int
    PhoneService: int
    PaperlessBilling: int
    gender_Male: int
    InternetService_Fiber_optic: int
    InternetService_No: int
    MultipleLines_No_phone_service: int
    MultipleLines_Yes: int
    OnlineSecurity_No_internet_service: int
    OnlineSecurity_Yes: int
    OnlineBackup_No_internet_service: int
    OnlineBackup_Yes: int
    DeviceProtection_No_internet_service: int
    DeviceProtection_Yes: int
    TechSupport_No_internet_service: int
    TechSupport_Yes: int
    StreamingTV_No_internet_service: int
    StreamingTV_Yes: int
    StreamingMovies_No_internet_service: int
    StreamingMovies_Yes: int
    Contract_One_year: int
    Contract_Two_year: int
    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int

# Initialize the FastAPI app
app = FastAPI(title="Customer Churn Prediction API", version="1.0")

# Load the trained model from MLflow
RUN_ID = "2e75a1a78ab94393a9bb980e98ca1540"
MODEL_NAME = "logistic_regression_model"
logged_model_uri = f'runs:/{RUN_ID}/{MODEL_NAME}'
model = mlflow.pyfunc.load_model(logged_model_uri)
print("Model loaded successfully.")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Churn Prediction API"}


@app.post("/predict")
def predict_churn(customer_data: CustomerData):
    if not TRAINING_COLUMNS:
         return {"error": "Model training columns not loaded. API is not ready."}
         
    data_dict = customer_data.dict()
    input_df = pd.DataFrame([data_dict])
    
    # Reorder columns to match the training data order
    input_df = input_df[TRAINING_COLUMNS]
    
    prediction = model.predict(input_df)
    churn_result = int(prediction[0])
    
    return {
        "prediction": churn_result,
        "prediction_label": "Churn" if churn_result == 1 else "No Churn"
    }