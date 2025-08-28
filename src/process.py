# src/process.py
import yaml
import pandas as pd
import argparse

def process_data(config_path):
    """
    ETL script to process the raw data.
    """
    with open(config_path) as f:
        config = yaml.safe_load(f)

    print("1. Loading data...")
    df = pd.read_csv(config['data']['raw_path'])

    print("2. Cleaning and transforming data...")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    df.drop(columns=config['processing']['drop_cols'], inplace=True)

    for col in config['processing']['binary_cols']:
        df[col] = df[col].apply(lambda x: 1 if x == 'Yes' else 0)
    
    df[config['data']['target_col']] = df[config['data']['target_col']].apply(lambda x: 1 if x == 'Yes' else 0)

    df = pd.get_dummies(df, columns=config['processing']['categorical_cols'], drop_first=True)

    df.columns = df.columns.str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    print("3. Saving processed data...")
    processed_path = config['data']['processed_path']
    df.to_csv(processed_path, index=False)
    print(f"Processed data saved successfully to '{processed_path}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="params.yaml", help="Path to the configuration file")
    args = parser.parse_args()
    process_data(config_path=args.config)