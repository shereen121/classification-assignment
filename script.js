// Load model information when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadModelInfo();
    setupEventListeners();
});

async function loadModelInfo() {
    try {
        const response = await fetch('/model_info');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error loading model info:', data.error);
            return;
        }
        
        console.log('Model loaded:', data.model_type);
        console.log('Features expected:', data.features_expected);
        
    } catch (error) {
        console.error('Error loading model info:', error);
    }
}

function setupEventListeners() {
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        predict();
    });
}

async function predict() {
    try {
        const featureInputs = document.querySelectorAll('#feature-inputs input');
        const features = Array.from(featureInputs).map(input => parseFloat(input.value));
        
        // Validate inputs
        if (features.some(isNaN)) {
            showError('Please enter valid numbers for all features');
            return;
        }
        
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(features)
        });
        
        const result = await response.json();
        
        if (result.error) {
            showError(result.error);
        } else {
            displayResult(result);
        }
        
    } catch (error) {
        console.error('Prediction error:', error);
        showError('Error making prediction: ' + error.message);
    }
}

async function batchPredict() {
    try {
        const batchInput = document.getElementById('batch-input').value;
        
        if (!batchInput.trim()) {
            showError('Please enter data for batch prediction');
            return;
        }
        
        const instances = JSON.parse(batchInput);
        
        // Validate batch input
        if (!Array.isArray(instances) || !instances.every(Array.isArray)) {
            showError('Invalid batch format. Please use array of arrays format.');
            return;
        }
        
        const response = await fetch('/batch_predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ instances })
        });
        
        const result = await response.json();
        
        if (result.error) {
            showError(result.error);
        } else {
            displayBatchResult(result);
        }
        
    } catch (error) {
        console.error('Batch prediction error:', error);
        showError('Error in batch prediction: ' + error.message);
    }
}

function displayResult(result) {
    const resultsContainer = document.getElementById('results-container');
    
    let resultHTML = `
        <div class="prediction-result" style="border-left-color: ${result.color};">
            <div class="result-header">
                <div class="bean-type">${result.bean_type}</div>
                <div class="confidence-badge">${result.confidence.toFixed(1)}% Confidence</div>
            </div>
            
            <div class="bean-details">
                <div class="scientific-name">${result.scientific_name}</div>
                <p>${result.description}</p>
            </div>
    `;
    
    if (result.probabilities) {
        resultHTML += `
            <div class="probability-chart">
                <h4>Classification Probabilities:</h4>
        `;
        
        // Sort probabilities by value
        const sortedProbs = Object.entries(result.probabilities)
            .sort(([,a], [,b]) => b - a);
        
        sortedProbs.forEach(([beanType, probability]) => {
            const isTop = beanType === result.bean_type;
            const barColor = isTop ? result.color : '#3498db';
            
            resultHTML += `
                <div class="probability-item" style="border-left-color: ${barColor};">
                    <span>${beanType}</span>
                    <div class="probability-bar">
                        <div class="probability-fill" style="width: ${probability}%; background: ${barColor};">
                            ${probability >= 10 ? probability.toFixed(1) + '%' : ''}
                        </div>
                    </div>
                    <span>${probability.toFixed(1)}%</span>
                </div>
            `;
        });
        
        resultHTML += `</div>`;
    }
    
    resultHTML += `</div>`;
    resultsContainer.innerHTML = resultHTML;
}

function displayBatchResult(result) {
    const resultsContainer = document.getElementById('results-container');
    
    let resultHTML = `
        <div class="success-message">
            ✅ Successfully classified ${result.predictions.length} beans
        </div>
        <div class="batch-results">
    `;
    
    result.predictions.forEach(prediction => {
        resultHTML += `
            <div class="batch-result-item" style="border-left-color: ${prediction.color};">
                <div class="batch-bean-color" style="background-color: ${prediction.color};"></div>
                <div>
                    <strong>Bean ${prediction.instance}: ${prediction.bean_type}</strong>
                    <div style="font-size: 0.9rem; color: #666;">
                        ${prediction.scientific_name} - ${prediction.description}
                    </div>
                </div>
            </div>
        `;
    });
    
    resultHTML += `</div>`;
    resultsContainer.innerHTML = resultHTML;
}

function showError(message) {
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = `
        <div class="error-message">
            ❌ ${message}
        </div>
    `;
}

function loadSampleData() {
    // Sample data from the Dry Bean dataset (average values)
    const sampleData = [
        42000, 750, 300, 180, 1.67, 0.85, 43000, 231, 
        0.75, 0.98, 0.85, 0.92, 0.45, 0.65, 0.35, 0.55
    ];
    
    const featureInputs = document.querySelectorAll('#feature-inputs input');
    featureInputs.forEach((input, index) => {
        if (sampleData[index] !== undefined) {
            input.value = sampleData[index];
        }
    });
    
    // Show success message
    const resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = `
        <div class="success-message">
            ✅ Sample data loaded! Click "Classify Bean" to see the prediction.
        </div>
    `;
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl + Enter for prediction
    if (e.ctrlKey && e.key === 'Enter') {
        predict();
    }
    // Ctrl + Shift + L for sample data
    if (e.ctrlKey && e.shiftKey && e.key === 'L') {
        loadSampleData();
    }
});