# 🚀 Network Traffic Analysis using Machine Learning

A full-stack real-time Network Intrusion Detection and Traffic Analysis System built using **React, Flask, Socket.IO, Python, and Machine Learning**.

The project continuously generates and monitors network traffic, analyzes packets using machine learning models, detects anomalies and cyber attacks, and visualizes the results on an interactive Security Operations Center (SOC) dashboard.

The system combines machine learning-based anomaly detection techniques with a modern React dashboard to provide live traffic monitoring, attack classification, and network analytics.

---

# 📌 Features

* Real-time network traffic monitoring
* Machine learning based anomaly detection
* Supervised and unsupervised learning models
* Live WebSocket communication using Socket.IO
* Interactive SOC dashboard
* Attack classification (Known / Unknown)
* Live packet monitoring table
* Packets-per-second visualization
* Attack distribution pie chart
* Animated attack alert popups
* Model confidence and accuracy visualization
* Modular frontend and backend architecture

---

# 🏗️ Tech Stack

## Frontend

* React
* Vite
* Chart.js
* Recharts
* Socket.IO Client
* Framer Motion
* Tailwind CSS
* Radix UI

## Backend

* Flask
* Flask-SocketIO
* Flask-CORS

## Machine Learning

* Scikit-learn
* Random Forest
* XGBoost
* Isolation Forest
* Pandas
* NumPy
* Joblib

---

# 📂 Project Structure

```
NetworkTrafficAnalysis/

│
├── backend/
│   ├── server.py
│   ├── app.py
│   ├── ml/
│   ├── models/
│   │      ├── supervised/
│   │      └── unsupervised/
│   ├── routes/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │      ├── components/
│   │      ├── context/
│   │      ├── services/
│   │      ├── hooks/
│   │      ├── styles/
│   │      ├── App.jsx
│   │      └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── src/
│   └── datasets/
│         └── CICIDS2017_final.csv
│
└── README.md
```

---

# ⚙️ System Architecture

```
                CICIDS2017 Dataset
                        │
                        ▼
              Data Cleaning & Encoding
                        │
                        ▼
            Feature Engineering Pipeline
                        │
                        ▼
      StandardScaler + LabelEncoder
                        │
                        ▼
      RandomForest / XGBoost Training
                        │
                        ▼
      Isolation Forest Training
                        │
                        ▼
          Saved ML Models (.pkl)
                        │
                        ▼
              Flask Backend Server
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
 REST API Endpoints              Socket.IO Server
        │                               │
        └───────────────┬───────────────┘
                        ▼
               React Dashboard
                        │
                        ▼
       Real-time Visualization & Alerts
```

---

# 🧠 Machine Learning Pipeline

The project uses both supervised and unsupervised learning approaches.

## Supervised Learning

* Random Forest Classifier
* XGBoost Classifier

Workflow:

```
Dataset

↓

Data Cleaning

↓

Feature Selection

↓

Scaling

↓

Label Encoding

↓

Train-Test Split

↓

Random Forest Training

↓

XGBoost Training

↓

Model Serialization (.pkl)
```

Saved artifacts:

* rf_model.pkl
* xgb_model.pkl
* scaler.pkl
* label_encoder.pkl

---

## Unsupervised Learning

Isolation Forest is trained for anomaly detection.

Workflow:

```
Dataset

↓

Remove unwanted columns

↓

Categorical Encoding

↓

Isolation Forest Training

↓

Save Model

↓

Save Feature Columns
```

Saved artifacts:

* isolation_forest.pkl
* iso_features_columns.pkl

---

# 🔄 End-to-End Workflow

## Step 1

Dataset is loaded.

```
CICIDS2017_final.csv
```

↓

## Step 2

Data preprocessing

* Remove missing values
* Remove infinity values
* Encode labels
* Scale numerical features

↓

## Step 3

Machine learning models are trained.

↓

## Step 4

Models are saved using Joblib.

↓

## Step 5

Backend starts.

```
python server.py
```

↓

## Step 6

Traffic generator continuously creates packets.

Example:

```
Source IP

Destination IP

Attack Type

Confidence

Prediction

Model

Accuracy
```

↓

## Step 7

Traffic is stored in memory.

↓

## Step 8

Socket.IO broadcasts packets to all connected clients.

↓

## Step 9

React frontend receives packets instantly.

↓

## Step 10

Dashboard updates automatically.

* Charts
* Tables
* Alerts
* Statistics
* Attack distribution

without page refresh.

---

# 🌐 REST API

## GET /

Returns backend status.

```
GET /

Response

{
    "message":"Network Traffic Analysis Backend Running"
}
```

---

## GET /traffic

Returns latest traffic packets.

```
GET /traffic
```

---

## POST /predict_attack

Predict attack from packet details.

Request:

```
{
    "src_ip":"192.168.1.10",
    "dst_ip":"10.0.0.5"
}
```

Response:

```
{
    "timestamp":"2026-06-12 14:20:18",
    "source_ip":"192.168.1.10",
    "destination_ip":"10.0.0.5",
    "attack_name":"DDoS",
    "attack_category":"Known",
    "prediction":1,
    "confidence":0.95,
    "model":"RandomForest",
    "accuracy":0.97
}
```

---

# 📊 Dashboard Components

* Live Traffic Dashboard
* Packets Per Second Chart
* Attack Distribution Pie Chart
* Live Packet Table
* Alert Popup Notifications
* Accuracy Gauge
* Model Status Panel
* Security Operations Center Sidebar
* Header Navigation

---

# ⚡ Real-Time Communication

The frontend connects to the backend using Socket.IO.

```
Backend

↓

Socket.IO Emit

↓

React Socket Context

↓

Dashboard Components

↓

Live UI Update
```

No page refresh is required.

---

# ▶️ Installation

## Clone repository

```
git clone https://github.com/yourusername/NetworkTrafficAnalysis.git
```

```
cd NetworkTrafficAnalysis
```

---

## Backend setup

Create virtual environment

```
python -m venv venv
```

Activate

### Windows

```
venv\Scripts\activate
```

### Linux / macOS

```
source venv/bin/activate
```

Install dependencies

```
pip install -r backend/requirements.txt
```

Run backend

```
cd backend

python server.py
```

---

## Frontend setup

```
cd frontend

npm install

npm run dev
```

Frontend starts at

```
http://localhost:5173
```

Backend runs on

```
http://localhost:5000
```

---

# 🖼️ Screenshots

Add project screenshots here.

```
screenshots/

dashboard.png

alerts.png

live_table.png

traffic_chart.png

attack_distribution.png
```

---

# 🔮 Future Enhancements

* Live packet capture using Scapy
* PCAP file analysis
* Kafka-based streaming pipeline
* Elasticsearch integration
* Kibana dashboards
* JWT authentication
* Docker deployment
* Kubernetes support
* Model retraining pipeline
* Explainable AI for attack predictions
* Cloud deployment

---

# 👨‍💻 Learning Outcomes

This project demonstrates:

* Full-stack development
* REST API development
* Real-time systems using WebSockets
* Machine learning integration
* Data preprocessing
* Model training and serialization
* Interactive dashboard design
* Network traffic visualization
* End-to-end ML application deployment workflow

---

Author

Bhaavan Dhanishya Vemula

B.Tech Computer Science Engineering

Machine Learning | Full Stack Development | Cyber Security

# 📜 License

This project is intended for educational and research purposes.
