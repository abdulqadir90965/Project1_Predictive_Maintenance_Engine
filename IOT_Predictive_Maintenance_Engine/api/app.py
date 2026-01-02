from flask import Flask, request, jsonify
import joblib
import pandas as pd
import shap

app = Flask(__name__)

# Load model and feature names
model = joblib.load("../model/failure_prediction_model.pkl")
feature_names = joblib.load("../model/feature_names.pkl")


#model = joblib.load("failure_prediction_model.pkl")
#feature_names = joblib.load("feature_names.pkl")

explainer = shap.TreeExplainer(model)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Model service is running"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Predictive Maintenance Model API",
        "endpoints": {
            "/health": "Check service status",
            "/predict": "POST sensor data for failure prediction"
        }
    })



@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Read input JSON
        data = request.get_json()
        input_df = pd.DataFrame([data])

        # Ensure ALL training features exist
        for col in feature_names:
            if col not in input_df.columns:
                input_df[col] = 0.0

        # Reorder columns to match training
        input_df = input_df[feature_names]

        # Prediction
        failure_prob = model.predict_proba(input_df)[0][1]

        # SHAP explanation
        shap_values = explainer.shap_values(input_df)[1][0]

        top_features = sorted(
            zip(feature_names, shap_values),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]

        return jsonify({
            "failure_probability": round(float(failure_prob), 4),

            "top_risk_factors": [
                {
                    "feature": f,
                    "effect": "increases risk" if v > 0 else "reduces risk",
                    "impact_score": round(float(abs(v)), 4)
                }
                for f, v in top_features
            ]

            
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
