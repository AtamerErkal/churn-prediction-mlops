# src/api.py
import pandas as pd
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel

# Define the input data schema using Pydantic
# These features must match the columns of the training data AFTER processing
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Partner: int
    Dependents: int
    PhoneService: int
    PaperlessBilling: int
    gender_Male: int
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
# IMPORTANT: Replace <RUN_ID> with the actual Run ID from your MLflow experiment
RUN_ID = "fc498cc3966e40ba92d27c107e1dbe67" # Example: "a1b2c3d4e5f6..."
MODEL_NAME = "logistic_regression_model"
logged_model_uri = f'runs:/{RUN_ID}/{MODEL_NAME}'
model = mlflow.pyfunc.load_model(logged_model_uri)
print("Model loaded successfully.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Churn Prediction API"}

@app.post("/predict")
def predict_churn(customer_data: CustomerData):
    """
    Takes customer data as input and returns churn prediction.
    """
    # Convert the Pydantic model to a dictionary
    data_dict = customer_data.dict()

    # Convert the dictionary to a pandas DataFrame
    # The model expects a DataFrame as input
    input_df = pd.DataFrame([data_dict])

    # Make a prediction
    prediction = model.predict(input_df)

    # The output of predict is a numpy array, get the first element
    churn_result = int(prediction[0])

    # Return the result
    return {
        "prediction": churn_result,
        "prediction_label": "Churn" if churn_result == 1 else "No Churn"
    }