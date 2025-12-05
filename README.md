# 🌱 Bean Classifier Pro

An advanced web application for classifying dry bean types using machine learning. This application uses a Stacking Classifier model trained on the Dry Bean Dataset to accurately identify 7 different types of beans based on their morphological features.

![Bean Classifier](https://img.shields.io/badge/Accuracy-92.68%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey)

## 📊 Model Overview

- **Model Type**: Stacking Classifier
- **Base Estimators**: LogisticRegression + SVC
- **Final Estimator**: LogisticRegression
- **Accuracy**: 92.68%
- **Features**: 16 morphological features
- **Bean Classes**: 7 types

## 🎯 Supported Bean Types

| Bean Type | Scientific Name | Description |
|-----------|----------------|-------------|
| BARBUNYA | Phaseolus vulgaris | Turkish kidney bean |
| BOMBAY | Vigna unguiculata | Black-eyed pea |
| CALI | Phaseolus lunatus | Lima bean |
| DERMASON | Phaseolus vulgaris | White kidney bean |
| HOROZ | Phaseolus coccineus | Runner bean |
| SEKER | Phaseolus vulgaris | Sugar bean |
| SIRA | Vigna radiata | Mung bean |

## 🚀 Features

- **Single Bean Analysis**: Classify individual beans using 16 morphological features
- **Batch Processing**: Classify multiple beans at once using JSON format
- **Real-time Results**: Instant classification with probability scores
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Interactive UI**: User-friendly interface with tooltips and sample data

## 📁 Project Structure
bean-classifier/
│

├── 📁 model/

│ ├── bean_model.joblib

│ ├── scaler.joblib

│ ├── label_encoder.joblib

│ └── model_info.json

│
├── 📁 static/

│ ├── style.css

│ └── script.js

│
├── 📁 templates/

│ └── index.html

│
├── app.py

├── requirements.txt

└── README.md


## 📊 Model Features
The classifier uses 16 morphological features:

Area - Total area of the bean in pixels

Perimeter - Total perimeter length

MajorAxisLength - Length of the longest axis

MinorAxisLength - Length of the shortest axis

AspectRation - Ratio of major to minor axis

Eccentricity - Measure of circularity

ConvexArea - Area of the convex hull

EquivDiameter - Diameter of equivalent circle

Extent - Ratio of pixels in bounding box

Solidity - Ratio of pixels in convex hull

Roundness - Circularity measure

Compactness - Compactness measure

ShapeFactor1 - Shape factor 1

ShapeFactor2 - Shape factor 2

ShapeFactor3 - Shape factor 3

ShapeFactor4 - Shape factor 4


## 🔧 API Endpoints
GET / - Main web interface

POST /predict - Single bean classification

POST /batch_predict - Multiple bean classification

GET /model_info - Model metadata

## 📈 Performance
Cross-validation Accuracy: 92.68%

Model Architecture: Stacking Classifier

Preprocessing: log1p transformation + StandardScaler

Training Data: Dry Bean Dataset
