# AgroGPT-Uganda

An AI-powered agricultural assistant for Ugandan farmers, providing localized insights and support for farming practices, weather patterns, pest control, and market information.

## Features

- Plant disease diagnosis from images
- Localized planting and harvesting calendars
- Sustainable farming practice recommendations
- Market price tracking and buyer connections
- Multi-language support (English, Luganda, Runyankole, Acholi)
- SMS/USSD interface for farmers without internet access
- Real-time weather data integration
- User profiles for different stakeholders

## Tech Stack

- Backend: Python/FastAPI
- Frontend: React/Next.js
- Mobile: React Native
- Database: PostgreSQL + Redis
- AI/ML: PyTorch
- SMS/USSD: Local telecom integration

## Project Structure

```
agrogpt-uganda/
├── backend/           # FastAPI backend
├── frontend/          # Next.js frontend
├── mobile/           # React Native mobile app
├── ml/               # Machine learning models
├── docs/             # Documentation
└── scripts/          # Utility scripts
```

## Setup Instructions

1. Clone the repository
2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
5. Set up environment variables (see .env.example)
6. Run the development servers:
   ```bash
   # Backend
   cd backend
   uvicorn main:app --reload
   
   # Frontend
   cd frontend
   npm run dev
   ```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 