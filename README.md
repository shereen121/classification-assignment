 Bean Classifier Pro

An advanced web application for classifying dry bean types using machine learning. This application uses a Stacking Classifier model trained on the Dry Bean Dataset to accurately identify 7 different types of beans based on their morphological features.

![Bean Classifier](https://img.shields.io/badge/Accuracy-92.68%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey)


- **Model Type**: Stacking Classifier
- **Base Estimators**: LogisticRegression + SVC
- **Final Estimator**: LogisticRegression
- **Accuracy**: 92.68%
- **Features**: 16 morphological features
- **Bean Classes**: 7 types


 Features

- **Single Bean Analysis**: Classify individual beans using 16 morphological features
- **Batch Processing**: Classify multiple beans at once using JSON format
- **Real-time Results**: Instant classification with probability scores
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Interactive UI**: User-friendly interface with tooltips and sample data



The classifier uses 16 morphological features:





## 📈 Performance
Cross-validation Accuracy: 92.68%

Model Architecture: Stacking Classifier

Preprocessing: log1p transformation + StandardScaler

Training Data: Dry Bean Dataset
