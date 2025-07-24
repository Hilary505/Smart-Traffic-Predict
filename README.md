# Predicting Short-Term Traffic Flow Congestion On Urban Motorway Networks

## 🚦 Project Overview
A real-time system for predicting vehicle traffic congestion on urban motorways using live traffic camera images and machine learning. The model classifies congestion into low, medium, or high, helping city planners and drivers make informed decisions. The system is designed for extensibility and real-world deployment.

**ICP Integration:** This project includes a Motoko canister deployed on the Internet Computer Protocol (ICP) for decentralized, transparent, and scalable backend logic. See below for details.

---

## 🏗️ Architecture Overview
- **Frontend:** Flask web app with Jinja templates for user interaction and visualization.
- **Backend:** Python (Flask) REST API for image upload, prediction, and region-based queries.
- **ML Model:** TensorFlow model for congestion classification (low/medium/high).
- **Deployment:** Supports Docker, AWS EKS, and GCP App Engine.

![Architecture Diagram](miscellanous/Architecture%20of%20real-time%20prediction.png)

---

## 🎥 Pitch Deck & Demo Video
- [Pitch Deck (Google Slides)](https://docs.google.com/presentation/d/1ecyTVmE2eLL8S8tCIGs8JBKw0EEAsHAqw2U0Yq0A_Ns/edit?usp=sharing)

---

## 🚀 Features
- Real-time traffic image ingestion and prediction
- Region-based search and filtering
- User-friendly web interface
- REST API for integration
- Dockerized for easy deployment
- Supports deployment to AWS EKS and GCP App Engine
- Automated tests for core modules
- ICP  for decentralised users

---

## 🛠️ Hackathon Work
- Built and integrated real-time prediction API
- Added region-based search and dropdown UI
- Dockerized the application
- Added deployment scripts for AWS EKS and GCP
- Improved documentation and setup instructions
- Added/updated tests in `/tests/`


## Installation

### 1. Clone and Setup
```bash
git clone https://github.com/Hilary505/Smart-Traffic-Predict.git
cd Smart-Traffic-Predict
virtualenv venv
source venv/bin/activate
```

### 2. Set Environment Variables

### 🔑 NSW API Key Setup

This project requires an NSW API key for live traffic data.  

### How to Get an API Key
1. Visit the [NSW Open Data Portal](https://opendata.transport.nsw.gov.au/) and register for a free API key.
2. Once you have your key, set it as an environment variable:
   ```bash
   export NSW_API_KEY=your_api_key_here
   ```

### 3. Run Locally
```bash
python run.py
```

### 4. Test Prediction
```bash
python run.py test_image/Aut10_010.jpg
# Output: high congestion (score = 0.70454)
```

### 5. Run Tests
```bash
PYTHONPATH=. pytest tests/
```

---

## 🐳 Docker Deployment
```bash
docker build -t smart-traffic:latest .
docker run --rm -p 80:5000 smart-traffic:latest
# Open http://localhost:80 in your browser
```

---

## ☁️ Cloud Deployment
### AWS EKS
```bash
kubectl apply -f aws_eks/deployment.yaml
# Access via http://localhost:8080/api/v1/namespaces/default/services/smart-traffic-service/proxy
```

### GCP App Engine
```bash
gcloud app deploy
```

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
---

## 🟦 ICP/dfx.json & Motoko Canister

### Why ICP?
The Internet Computer Protocol (ICP) provides a decentralized, tamper-proof, and scalable backend for smart traffic prediction. By deploying a Motoko canister, the project demonstrates how traffic data and logic can be made transparent, secure, and interoperable with other decentralized services.

### Prerequisites
- [DFINITY SDK (dfx)](https://internetcomputer.org/docs/current/developer-docs/quickstart/hello10mins)

#### install dfx

```bash
$ sh -ci "$(curl -fsSL https://sdk.dfinity.org/install.sh)"

```

```bash
$ source ~/.profile
```

```bash
$ dfx --version
```

### Deploying the Canister
1. Start the local replica:
```bash
  $ dfx start --background
   ```
2. Deploy the canister:
```bash
  $ dfx deploy
   ```
3. Call the canister:
```bash
$ dfx canister call hello greet '("Hackathon Judge")'
   # Returns: "Hello, Hackathon Judge! Welcome to Smart Traffic Predict."
```