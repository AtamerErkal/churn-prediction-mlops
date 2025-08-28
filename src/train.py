# src/train.py
import yaml
import pandas as pd
import argparse
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_model(config_path):
    """
    Trains the model and logs everything to MLflow.
    """
    # Load configuration
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Start an MLflow experiment
    mlflow.set_experiment("Customer Churn Prediction")
    with mlflow.start_run() as run: # Get the run object
        print("MLflow run started.")

        # Log parameters to MLflow
        mlflow.log_params(config['training']['model_params'])
        mlflow.log_param("test_size", config['training']['test_size'])
        mlflow.log_param("random_state", config['training']['random_state'])

        print("1. Loading processed data...")
        df = pd.read_csv(config['data']['processed_path'])

        # Separate features and target
        X = df.drop(config['data']['target_col'], axis=1)
        y = df[config['data']['target_col']]

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=config['training']['test_size'],
            random_state=config['training']['random_state']
        )

        print("2. Training the model...")
        model = LogisticRegression(**config['training']['model_params'])
        model.fit(X_train, y_train)

        print("3. Evaluating model performance...")
        y_pred = model.predict(X_test)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 Score: {f1}")

        # Log metrics to MLflow
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        print("4. Saving the model to MLflow...")
        # Log the model to MLflow
        mlflow.sklearn.log_model(model, config['training']['model_name'])
        print("Model saved successfully.")
        
        # Print the run ID to make it easy to find
        print(f"MLflow Run ID: {run.info.run_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="params.yaml", help="Path to the configuration file")
    args = parser.parse_args()
    train_model(config_path=args.config)