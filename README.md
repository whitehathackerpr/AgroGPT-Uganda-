# AgroGPT Uganda

An AI-powered agricultural assistant for Ugandan farmers, providing disease diagnosis, weather forecasts, market prices, and farming recommendations.

## Features

- 🌱 Crop Disease Diagnosis using Computer Vision
- 🌦️ Weather Forecasting with Agricultural Metrics
- 💰 Market Price Analysis and Predictions
- 📅 Smart Planting Calendar
- 🌍 Multi-language Support (English, Luganda, Runyankole, Acholi)
- 📱 USSD Interface for Feature Phones

## Tech Stack

- Backend: FastAPI, Python
- ML: PyTorch, scikit-learn
- Mobile: React Native
- Frontend: React.js
- Database: PostgreSQL

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AgroGPT-Uganda.git
   cd AgroGPT-Uganda
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```

6. Download ML models:
   ```bash
   python scripts/download_models.py
   ```

7. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

8. Start the frontend (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

9. Start the mobile app (in a new terminal):
   ```bash
   cd mobile
   npm install
   npm start
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Weather data provided by WeatherAPI
- Market price data sourced from Uganda Bureau of Statistics
- Disease classification model trained on [AgriVision dataset](https://www.kaggle.com/datasets/emmarex/plant-disease-detection-dataset) 