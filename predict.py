"""
Predicts a number from an image using a pre-trained CNN model.
"""
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt



def predict(img):
    try:
        # Convert to grayscale if image is color
        if len(img.shape) == 3:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            image = img.copy()
            
        # Resize to 28x28 and normalize
        image = cv2.resize(image, (28, 28))
        image = image.astype('float32')
        image = image.reshape(1, 28, 28, 1)
        image = image / 255.0

        # Display the processed image
        plt.figure(figsize=(4, 4))
        plt.imshow(image.reshape(28, 28), cmap='gray')
        plt.title('Processed Input Image')
        plt.axis('off')
        plt.show()

        # Load the pre-trained model
        model = load_model('cnn.hdf5')
        
        # Make prediction
        prediction = model.predict(image)
        predicted_digit = np.argmax(prediction[0])
        confidence = np.max(prediction[0]) * 100
        
        print(f"\nPredicted Digit: {predicted_digit}")
        print(f"Confidence: {confidence:.2f}%")
        
        # Print all class probabilities
        print("\nClass Probabilities:")
        for i, prob in enumerate(prediction[0]):
            print(f"Digit {i}: {prob*100:.2f}%")
            
        return predicted_digit
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

if __name__ == "__main__":
    # Load and predict the test image
    test_image_path = 'TestNumber.png'
    try:
        img = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Could not load image at {test_image_path}")
        predict(img)
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure the test image 'TestNumber.png' exists in the current directory.")
