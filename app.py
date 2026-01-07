import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import matplotlib
matplotlib.use('Agg')  # Set backend to Agg to prevent GUI issues
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the pre-trained model
model = None
try:
    model = load_model('cnn.hdf5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    try:
        # Read and preprocess the image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
            
        # Resize to 28x28 and normalize
        img = cv2.resize(img, (28, 28))
        img = img.astype('float32') / 255.0
        img = img.reshape(1, 28, 28, 1)
        
        # Invert colors for canvas drawings (black on white -> white on black)
        img = 1.0 - img
        
        return img
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accuracy_plot')
def accuracy_plot():
    """Serve the accuracy plot image"""
    return send_from_directory('.', 'accuracy_plot', mimetype='image/png')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess and predict
        processed_img = preprocess_image(filepath)
        if processed_img is None:
            return jsonify({'error': 'Error processing image'}), 400
            
        try:
            # Make prediction
            prediction = model.predict(processed_img)
            predicted_digit = int(np.argmax(prediction[0]))
            confidence = float(np.max(prediction[0]))
            
            # Get all probabilities for chart
            probabilities = [float(p) for p in prediction[0]]
            
            # Save prediction visualization
            plt.figure(figsize=(10, 5))
            
            # Show original image
            plt.subplot(1, 2, 1)
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            plt.imshow(img, cmap='gray')
            plt.title('Uploaded Image')
            plt.axis('off')
            
            # Show prediction probabilities
            plt.subplot(1, 2, 2)
            plt.bar(range(10), prediction[0] * 100, color='skyblue')
            plt.xticks(range(10))
            plt.title('Prediction Probabilities')
            plt.xlabel('Digit')
            plt.ylabel('Confidence (%)')
            
            # Save the plot
            plot_filename = f"prediction_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            plot_path = os.path.join('static', 'predictions', plot_filename)
            os.makedirs(os.path.dirname(plot_path), exist_ok=True)
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()
            
            return jsonify({
                'prediction': predicted_digit,
                'confidence': confidence,
                'probabilities': probabilities,
                'image_url': filepath.replace('\\', '/'),
                'plot_url': plot_path.replace('\\', '/')
            })
            
        except Exception as e:
            print(f"Prediction error details: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Prediction error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/predictions', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    
    # Run the app
    app.run(debug=True, port=5000)
