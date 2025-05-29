import os
from flask import Flask, request, jsonify, render_template
from mlflow import mlflow
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load model from MLflow
#MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
#MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME", "DecisionTreeTelecomCustomerChurnModel")
# Load model
MODEL_PATH = "app_model"
model = mlflow.sklearn.load_model(MODEL_PATH)

#mlflow.set_tracking_uri("https://dagshub.com/singhdeepakkumar/my-bda-repo.mlflow")
#model = mlflow.sklearn.load_model(f"models:/DecisionTreeTelecomCustomerChurnModel/5")

sample_input = {
    "Gender": "Female",
    "Age": 30,
    "Married": "Yes",
    "Number of Dependents": 1,
    "Number of Referrals": 0,
    "Tenure in Months": 12,
    "Offer": "None",
    "Phone Service": "Yes",
    "Avg Monthly Long Distance Charges": 0.0,
    "Multiple Lines": "No",
    "Internet Service": "DSL",
    "Internet Type": "Fiber Optic",
    "Avg Monthly GB Download": 20.0,
    "Online Security": "No",
    "Online Backup": "No",
    "Device Protection Plan": "No",
    "Premium Tech Support": "No",
    "Streaming TV": "No",
    "Streaming Movies": "No",
    "Streaming Music": "No",
    "Unlimited Data": "Yes",
    "Contract": "Month-to-month",
    "Paperless Billing": "Yes",
    "Payment Method": "Credit Card",
    "Monthly Charge": 70.0,
    "Total Charges": 840.0,
    "Total Refunds": 0.0,
    "Total Extra Data Charges": 0.0,
    "Total Long Distance Charges": 10.0,
    "Total Revenue": 850.0
}



@app.route('/', methods=["GET"])
def form():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    input_data = build_input_from_user(
    request.form.get("Gender"),
    int(request.form.get("Age")),
    request.form.get("Married"))
    
    df = pd.DataFrame([input_data])
    df = preprocess_input(df)
    prediction = model.predict(df)[0]
    return jsonify({"prediction": int(prediction)})

def build_input_from_user(gender, age, married):
    input_data = sample_input.copy()
    input_data["Gender"] = gender
    input_data["Age"] = age
    input_data["Married"] = married
    return input_data

def preprocess_input(df):    
    df['Avg Monthly GB Download'] = df['Avg Monthly GB Download'].fillna(0.0)
    df['Avg Monthly Long Distance Charges'] = df['Avg Monthly Long Distance Charges'].fillna(0.0)
    df['Offer'] = df['Offer'].fillna('No Offer')    

    for col in df.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    return df


# Read version from file
version_path = os.path.join(MODEL_PATH, "model_version.txt")
model_version = "unknown"
if os.path.exists(version_path):
    with open(version_path, "r") as f:
        model_version = f.read().strip()

@app.route("/version", methods=["GET"])
def health_check():
    return jsonify({
        "message": "Churn Prediction API is live",
        "model_version": model_version
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
