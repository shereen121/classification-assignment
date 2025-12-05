import warnings
import os
from sklearn.exceptions import InconsistentVersionWarning

# Suppress version compatibility warnings
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')
static_dir = os.path.join(current_dir, 'static')
model_dir = os.path.join(current_dir, 'model')

print("🌱 Bean Classifier Pro - Starting...")
print(f"📁 Current directory: {current_dir}")
print(f"📁 Template directory: {template_dir}")
print(f"📁 Static directory: {static_dir}")
print(f"📁 Model directory: {model_dir}")

# Check if required folders exist
print(f"✅ Templates folder exists: {os.path.exists(template_dir)}")
print(f"✅ Static folder exists: {os.path.exists(static_dir)}")
print(f"✅ Model folder exists: {os.path.exists(model_dir)}")

if os.path.exists(template_dir):
    print(f"📄 Templates found: {os.listdir(template_dir)}")

# Create Flask app with explicit absolute paths
app = Flask(__name__, 
            template_folder=template_dir,
            static_folder=static_dir)

# Load your bean classification model and preprocessing objects
MODEL_PATH = os.path.join(model_dir, 'bean_model.joblib')
SCALER_PATH = os.path.join(model_dir, 'scaler.joblib')
LABEL_ENCODER_PATH = os.path.join(model_dir, 'label_encoder.joblib')

# Bean classes from your dataset
BEAN_CLASSES = {
    0: {'name': 'BARBUNYA', 'scientific': 'Phaseolus vulgaris', 'description': 'Turkish kidney bean', 'color': '#8B4513'},
    1: {'name': 'BOMBAY', 'scientific': 'Vigna unguiculata', 'description': 'Black-eyed pea', 'color': '#000000'},
    2: {'name': 'CALI', 'scientific': 'Phaseolus lunatus', 'description': 'Lima bean', 'color': '#F5F5DC'},
    3: {'name': 'DERMASON', 'scientific': 'Phaseolus vulgaris', 'description': 'White kidney bean', 'color': '#FFFFFF'},
    4: {'name': 'HOROZ', 'scientific': 'Phaseolus coccineus', 'description': 'Runner bean', 'color': '#8B0000'},
    5: {'name': 'SEKER', 'scientific': 'Phaseolus vulgaris', 'description': 'Sugar bean', 'color': '#FFD700'},
    6: {'name': 'SIRA', 'scientific': 'Vigna radiata', 'description': 'Mung bean', 'color': '#90EE90'}
}

# Features from your dataset
BEAN_FEATURES = [
    'Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength',
    'AspectRation', 'Eccentricity', 'ConvexArea', 'EquivDiameter',
    'Extent', 'Solidity', 'Roundness', 'Compactness',
    'ShapeFactor1', 'ShapeFactor2', 'ShapeFactor3', 'ShapeFactor4'
]

# Feature descriptions for tooltips
FEATURE_DESCRIPTIONS = {
    'Area': 'Total area of the bean in pixels',
    'Perimeter': 'Total perimeter length of the bean',
    'MajorAxisLength': 'Length of the longest axis',
    'MinorAxisLength': 'Length of the shortest axis',
    'AspectRation': 'Ratio of major to minor axis',
    'Eccentricity': 'Measure of how circular the bean is',
    'ConvexArea': 'Area of the convex hull',
    'EquivDiameter': 'Diameter of a circle with same area',
    'Extent': 'Ratio of pixels in bounding box',
    'Solidity': 'Ratio of pixels in convex hull',
    'Roundness': 'Circularity measure',
    'Compactness': 'Compactness measure',
    'ShapeFactor1': 'Shape factor 1',
    'ShapeFactor2': 'Shape factor 2',
    'ShapeFactor3': 'Shape factor 3',
    'ShapeFactor4': 'Shape factor 4'
}

def load_models():
    """Load the trained model, scaler, and label encoder"""
    try:
        print("🔄 Loading models...")
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        label_encoder = joblib.load(LABEL_ENCODER_PATH)
        print("✅ All models loaded successfully")
        return model, scaler, label_encoder
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return None, None, None

model, scaler, label_encoder = load_models()

def predict_bean(features):
    """Complete prediction pipeline matching your notebook"""
    # Convert to numpy array
    features_array = np.array(features).reshape(1, -1)
    
    # Apply log1p transformation (as in your notebook)
    features_log = np.log1p(features_array)
    
    # Scale the features
    features_scaled = scaler.transform(features_log)
    
    # Make prediction
    prediction = model.predict(features_scaled)
    predicted_class = int(prediction[0])
    
    # Get probabilities
    probabilities = model.predict_proba(features_scaled)[0]
    confidence = max(probabilities) * 100
    
    return predicted_class, probabilities, confidence

@app.route('/')
def home():
    print("🏠 Home route accessed")
    return render_template('index.html', features=BEAN_FEATURES, feature_descriptions=FEATURE_DESCRIPTIONS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Convert to numpy array
        if isinstance(data, dict):
            features = [data[feature] for feature in BEAN_FEATURES]
        elif isinstance(data, list):
            features = data
        else:
            return jsonify({'error': 'Invalid input format'}), 400
        
        # Validate inputs
        if len(features) != len(BEAN_FEATURES):
            return jsonify({'error': f'Expected {len(BEAN_FEATURES)} features, got {len(features)}'}), 400
        
        if any(np.isnan(f) for f in features):
            return jsonify({'error': 'All features must be valid numbers'}), 400
        
        # Make prediction
        predicted_class, probabilities, confidence = predict_bean(features)
        
        # Prepare response
        bean_info = BEAN_CLASSES.get(predicted_class)
        
        response = {
            'prediction': predicted_class,
            'bean_type': bean_info['name'],
            'scientific_name': bean_info['scientific'],
            'description': bean_info['description'],
            'color': bean_info['color'],
            'confidence': confidence
        }
        
        # Add probabilities for all classes
        response['probabilities'] = {
            BEAN_CLASSES[i]['name']: float(prob) * 100 
            for i, prob in enumerate(probabilities)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Endpoint for batch predictions"""
    try:
        data = request.get_json()
        instances = data['instances']
        
        results = []
        for i, features in enumerate(instances):
            predicted_class, probabilities, confidence = predict_bean(features)
            bean_info = BEAN_CLASSES.get(predicted_class)
            
            results.append({
                'instance': i + 1,
                'bean_type': bean_info['name'],
                'scientific_name': bean_info['scientific'],
                'description': bean_info['description'],
                'color': bean_info['color'],
                'confidence': confidence
            })
        
        return jsonify({'predictions': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/model_info')
def model_info():
    """Return information about the model"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    info = {
        'model_type': 'StackingClassifier',
        'architecture': 'LogisticRegression + SVC → LogisticRegression',
        'features_expected': len(BEAN_FEATURES),
        'feature_names': BEAN_FEATURES,
        'bean_classes': BEAN_CLASSES,
        'accuracy': 92.68,
        'preprocessing': ['log1p transformation', 'standard scaling']
    }
    
    return jsonify(info)

if __name__ == '__main__':
    print("\n🚀 Starting Bean Classifier Pro Server...")
    print("📊 Model: StackingClassifier")
    print("🔢 Features: 16 morphological features")
    print("🎯 Accuracy: 92.68%")
    print("🌐 Server running on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)