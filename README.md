# Telecom Customer Churn App

A Flask-based web application for predicting telecom customer churn. This app is tightly integrated with the MLOps pipeline built in the [bda](https://github.com/singhdeepakkumar/bda) repo. It consumes the latest promoted ML model from MLflow and serves real-time churn predictions through a web interface.

---

## Features

- Loads the latest **production** model version from MLflow
- Accepts user input through a form or JSON payload
- Displays predictions with confidence scores
- Built as a Dockerized app and deployed via Kubernetes on a GCP VM
- GitHub self-hosted runner for automated CI/CD

---

## How It Works

### 1. Model Loading

- Downloads the ML model registered under the alias `production` in MLflow
- Uses `mlflow.sklearn.load_model()`

### 2. User Interaction

- **Web Form**: Inputs key customer data fields
- **API Endpoint**: Accepts JSON POST requests for predictions

### 3. Model Prediction

- Returns churn classification and prediction probability

## Deployment

### Docker Image

- Built via GitHub Actions from the latest promoted model
- Pushed to Docker Hub: `deepakkumarsingh/telecomcustomerchurn-app`

### Kubernetes

- Manifests in `k8s/` folder
- `deployment.yml.template` is rendered at runtime using GitHub Actions

### CI/CD

- Triggered by model promotion event from MLOps repo
- Self-hosted GitHub runner on GCP VM handles deployment

---

## Requirements

- Python 3.9
- `mlflow`, `Flask`, `scikit-learn`, etc.
- See `requirements.txt`

---

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Then visit `http://localhost:5000`
