import os
import sys
from pathlib import Path
import requests
import torch
import joblib
import json
from tqdm import tqdm

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Create necessary directories
MODEL_DIR = Path("backend/app/ml/models")
CONFIG_DIR = Path("backend/app/config")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url: str, destination: Path, description: str):
    """Download a file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=description,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

def download_models():
    """Download pre-trained models and configurations"""
    try:
        # Download disease classifier model
        disease_model_path = MODEL_DIR / "disease_classifier.pth"
        if not disease_model_path.exists():
            print("Downloading disease classifier model...")
            # TODO: Replace with actual model download URL
            # download_file(MODEL_URL, disease_model_path, "Disease Classifier")
            
            # For now, create a dummy model
            model = torch.nn.Sequential(
                torch.nn.Conv2d(3, 64, 3),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 5)
            )
            torch.save(model.state_dict(), disease_model_path)
            print("Created dummy disease classifier model")

        # Download weather predictor model
        weather_model_path = MODEL_DIR / "weather_predictor.joblib"
        if not weather_model_path.exists():
            print("Creating weather predictor model...")
            # Create a dummy weather prediction model
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            joblib.dump(model, weather_model_path)
            print("Created dummy weather predictor model")

        print("All models downloaded successfully!")
        return True

    except Exception as e:
        print(f"Error downloading models: {str(e)}")
        return False

if __name__ == "__main__":
    download_models() 