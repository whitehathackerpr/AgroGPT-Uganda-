import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import os
from typing import Dict, List, Tuple
import json

class DiseaseClassifier:
    def __init__(self, model_path: str, config_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_path)
        self.config = self._load_config(config_path)
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])

    def _load_model(self, model_path: str) -> nn.Module:
        """Load the pre-trained model"""
        model = models.resnet50(pretrained=True)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 1000)  # Adjust based on number of classes
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model = model.to(self.device)
        model.eval()
        return model

    def _load_config(self, config_path: str) -> Dict:
        """Load the configuration file with disease mappings"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """Preprocess the input image"""
        image = Image.open(image_path).convert('RGB')
        return self.transform(image).unsqueeze(0).to(self.device)

    def predict(self, image_path: str) -> Tuple[str, float]:
        """Predict the disease from the image"""
        with torch.no_grad():
            image_tensor = self.preprocess_image(image_path)
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            disease_id = predicted.item()
            confidence_score = confidence.item()
            
            disease_name = self.config.get(str(disease_id), "Unknown Disease")
            
            return disease_name, confidence_score

    def get_disease_info(self, disease_name: str) -> Dict:
        """Get detailed information about the disease"""
        return self.config.get("disease_info", {}).get(disease_name, {})

class DiseaseClassifierFactory:
    @staticmethod
    def create_classifier() -> DiseaseClassifier:
        model_path = os.getenv("DISEASE_MODEL_PATH", "./ml/models/disease_classifier.pth")
        config_path = os.getenv("DISEASE_CONFIG_PATH", "./ml/config/disease_config.json")
        return DiseaseClassifier(model_path, config_path) 