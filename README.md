Predictive Maintenance System for Industrial Robotic Arms

📌 Project Overview

Unplanned equipment failures in large manufacturing facilities can result in significant downtime costs (≈ $10,000/hour).
This project implements an end-to-end predictive maintenance system that forecasts equipment failure risk 24 hours in advance using time-series sensor data from industrial robotic arms.

The system is designed to:
:- Detect early signs of degradation
:-Enable proactive, scheduled maintenance
:-Reduce unplanned downtime
:-Provide explainable predictions engineers can trust

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
* To capture this, the following features are engineered:

:- Lag Features

   Previous sensor values (t-1, t-2)

:- Rolling Window Statistics

   Rolling means over short and medium windows

   All transformations are grouped by Sensor_ID to prevent cross-machine leakage
