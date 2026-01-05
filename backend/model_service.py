import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

class DrawingModel:
    def __init__(self, model_path='models/drawing_model.h5'):
        self.model = None
        self.model_path = model_path
        self.word_list = ['cat', 'dog', 'house', 'tree', 'car', 'sun', 'moon', 'star', 'bird', 'fish']  # Your word list (345 words for QuickDraw)
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"Model loaded from {self.model_path}")
            # Load word list
            self.load_word_list()
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def load_word_list(self):
        """Load the list of words the model can predict"""
        # You can load from a file or define here
        self.word_list = ['cat', 'dog', 'house', 'tree', 'car', ...]  # 345 words
    
    def preprocess_image(self, image_data):
        """
        Preprocess image for model input
        Args:
            image_data: Base64 encoded image string
        Returns:
            Preprocessed numpy array
        """
        # Convert base64 to PIL Image
        if isinstance(image_data, str):
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            image = image_data
        
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Resize to model input size (e.g., 28x28 or 224x224)
        target_size = 28  # Adjust based on your model
        image = image.resize((target_size, target_size))
        
        # Convert to numpy array and normalize
        img_array = np.array(image) / 255.0
        
        # Reshape for model input: (1, height, width, channels)
        img_array = img_array.reshape(1, target_size, target_size, 1)
        
        return img_array
    
    def predict(self, image_data, top_k=5):
        """
        Predict what the drawing is
        Args:
            image_data: Base64 encoded image string
            top_k: Number of top predictions to return
        Returns:
            List of dicts with 'word' and 'confidence'
        """
        if self.model is None:
            raise Exception("Model not loaded")
        
        # Preprocess
        preprocessed = self.preprocess_image(image_data)
        
        # Predict
        predictions = self.model.predict(preprocessed, verbose=0)
        
        # Get top predictions
        top_indices = np.argsort(predictions[0])[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'word': self.word_list[idx] if idx < len(self.word_list) else 'unknown',
                'confidence': float(predictions[0][idx])
            })
        
        return results