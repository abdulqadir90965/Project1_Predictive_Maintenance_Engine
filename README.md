Predictive Maintenance System for Industrial Robotic Arms

📌 Project Overview

Unplanned equipment failures in large manufacturing facilities can result in significant downtime costs (≈ $10,000/hour).
This project implements an end-to-end predictive maintenance system that forecasts equipment failure risk 24 hours in advance using time-series sensor data from industrial robotic arms.

The system is designed to:
* Detect early signs of degradation
* Enable proactive, scheduled maintenance
* Reduce unplanned downtime
* Provide explainable predictions engineers can trust

🏭 Use Case Context

* Environment: Large-scale manufacturing facility
* Assets: ~500 critical robotic arms
* Sensors:
    Vibration (m/s²)
    Temperature (°C)
* Prediction Target: Binary classification — failure within next 24 hours
* Key Challenge: Failures are rare events (<1%), making class imbalance and data leakage major concerns

🧠 Solution Approach
1. Data Ingestion & Cleaning

* Supports ingestion of one or multiple CSV sensor log files
* Converts timestamps into proper datetime format
* Handles missing sensor values using time-based interpolation, preserving temporal continuity
  
2. Feature Engineering (Core Component)

* Failures are driven by temporal trends, not single readings.
  
2.1. To capture this, the following features are engineered:

* Lag Features

   Previous sensor values (t-1, t-2)

* Rolling Window Statistics

   Rolling means over short and medium windows

All transformations are grouped by Sensor_ID to prevent cross-machine leakage

3. Failure Labeling

* Since real maintenance logs were not available, a proxy failure label was created:

* A machine is flagged as at-risk if vibration or temperature exceeds the 90th percentile

⚠️ Note: In production, failure labels should be derived from actual maintenance and breakdown records.

4. Train–Test Split Strategy

* Uses a time-based split (80% past data for training, 20% future data for testing)

* Prevents data leakage

* Accurately simulates real-world deployment conditions

🤖 Modeling Strategy

A layered modeling approach was used:

1. Baseline Model :-
   
Logistic Regression

* Interpretable

* Serves as a performance benchmark

* Uses class weighting to address imbalance

2. Advanced Models :-

Random Forest

* Captures non-linear sensor interactions

* Robust to noisy industrial data

XGBoost

* High-performance gradient boosting model

* Handles severe class imbalance using scale_pos_weight

Hyperparameter tuning is performed using RandomizedSearchCV with ROC-AUC as the primary metric.


