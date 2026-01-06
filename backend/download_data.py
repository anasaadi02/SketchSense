import os
import requests
from tqdm import tqdm
import json

# QuickDraw categories (you can modify this list)
QUICKDRAW_CATEGORIES = [
    'cat', 'dog', 'house', 'tree', 'car', 'sun', 'moon', 'star', 
    'bird', 'fish', 'apple', 'banana', 'airplane', 'bicycle', 
    'book', 'clock', 'cloud', 'flower', 'heart', 'key'
]

def download_quickdraw_data(categories, output_dir='data/quickdraw', max_samples=10000):
    """
    Download QuickDraw dataset
    Args:
        categories: List of category names
        output_dir: Directory to save data
        max_samples: Maximum samples per category
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for category in tqdm(categories, desc="Downloading categories"):
        url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{category}.npy"
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            file_path = os.path.join(output_dir, f"{category}.npy")
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded {category}")
            
        except Exception as e:
            print(f"Error downloading {category}: {e}")
    
    print(f"Download complete! Files saved to {output_dir}")

if __name__ == "__main__":
    download_quickdraw_data(QUICKDRAW_CATEGORIES, max_samples=10000)