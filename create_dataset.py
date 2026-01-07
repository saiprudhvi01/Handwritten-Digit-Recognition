import os
import numpy as np
from tensorflow.keras.datasets import mnist
import cv2

# Create dataset directories
def create_directories(base_dir='handwritten_digits'):
    # Create base directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Create subdirectories for each digit (0-9)
    for i in range(10):
        os.makedirs(os.path.join(base_dir, str(i)), exist_ok=True)
    
    return base_dir

# Generate and save sample digits
def generate_dataset(samples_per_digit=100, output_dir='handwritten_digits'):
    # Load MNIST dataset
    (x_train, y_train), (_, _) = mnist.load_data()
    
    # Create directories if they don't exist
    output_dir = create_directories(output_dir)
    
    # Counter for each digit
    digit_count = {i: 0 for i in range(10)}
    
    # Generate and save samples
    for i in range(len(x_train)):
        label = int(y_train[i])
        
        # Only save if we need more samples of this digit
        if digit_count[label] < samples_per_digit:
            # Save the image
            img = x_train[i]
            filename = os.path.join(output_dir, str(label), f'digit_{digit_count[label]}.png')
            cv2.imwrite(filename, img)
            
            # Increment counter
            digit_count[label] += 1
            
            # Check if we have enough samples
            if all(count >= samples_per_digit for count in digit_count.values()):
                break
    
    print(f"Dataset created successfully in '{output_dir}'")
    print("Samples per digit:", samples_per_digit)
    
    # Print summary
    print("\nDataset Summary:")
    total_samples = 0
    for digit in range(10):
        count = len(os.listdir(os.path.join(output_dir, str(digit))))
        print(f"Digit {digit}: {count} samples")
        total_samples += count
    print(f"\nTotal samples: {total_samples}")

if __name__ == "__main__":
    # Generate dataset with 100 samples per digit
    generate_dataset(samples_per_digit=100)
