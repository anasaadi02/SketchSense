# SketchSense

An AI-powered drawing recognition game where players draw a secret word on a canvas and the AI attempts to guess what they're drawing. Score points based on speed, accuracy, and how well the AI understands your sketch!

## 🎮 Game Flow

1. Player is given a secret word
2. Player draws it on a canvas (mouse / touch)
3. Drawing is sent to an AI model (live or after submit)
4. AI guesses the word (or gives progressive guesses)
5. Score based on speed / accuracy / number of hints

## ✨ Features

- **Interactive Drawing Canvas**: Draw with mouse or touch support
- **Real-time AI Predictions**: Get AI guesses while you draw (debounced)
- **Beautiful UI**: Modern, aesthetic home screen and game interface
- **FastAPI Backend**: Fast, async API with automatic documentation
- **TypeScript Frontend**: Type-safe React application with Vite

## 🛠️ Tech Stack

### Frontend
- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **CSS3** - Styling

### Backend
- **FastAPI** - Modern Python web framework
- **TensorFlow** - Machine learning framework
- **Pillow** - Image processing
- **NumPy** - Numerical operations
- **Uvicorn** - ASGI server

## 📁 Project Structure

```
SketchSense/
├── frontend/              # React + TypeScript frontend
│   ├── src/
│   │   ├── App.tsx       # Main application component
│   │   ├── App.css       # Application styles
│   │   ├── services/
│   │   │   └── api.ts    # API service for backend communication
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
│
├── backend/               # FastAPI backend
│   ├── app.py            # FastAPI application
│   ├── model_service.py  # ML model service
│   ├── requirements.txt   # Python dependencies
│   └── models/           
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (3.9 or higher)
- **pip** (Python package manager)

### Installation

#### 1. Clone the repository
```bash
git clone <repository-url>
cd SketchSense
```

#### 2. Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

#### 3. Setup Frontend

```bash
cd frontend
npm install
```

### Running the Application

#### Start Backend Server

```bash
cd backend
uvicorn app:app --reload --port 5000
```

The API will be available at:
- **API**: http://localhost:5000
- **Interactive Docs**: http://localhost:5000/docs
- **Alternative Docs**: http://localhost:5000/redoc

#### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at http://localhost:5173 (or another port if 5173 is busy)

## 📡 API Endpoints

### `GET /health`
Check API health and model status.

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### `POST /predict`
Predict what the drawing represents.

**Request Body:**
```json
{
  "image": "data:image/png;base64,iVBORw0KGgo..."
}
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "word": "cat",
      "confidence": 0.95
    },
    ...
  ],
  "top_guess": {
    "word": "cat",
    "confidence": 0.95
  }
}
```

## 🎯 Current Status

- ✅ Frontend UI (home screen and game screen)
- ✅ Canvas drawing functionality
- ✅ Backend API setup
- ✅ Frontend-backend integration
- ✅ Real-time predictions (debounced)
- ⏳ **Model Training/Integration** (in progress - needs trained model file)

## 📝 Notes

- The backend currently expects a trained model at `backend/models/drawing_model.h5`
- You'll need to either:
  - Download a pre-trained QuickDraw model
  - Train your own model using the QuickDraw dataset
  - Use a mock model for testing (see backend code)

## 🔮 Future Enhancements

- [ ] Scoring system (speed, accuracy, hints)
- [ ] Multiple difficulty levels
- [ ] Word categories
- [ ] Leaderboard
- [ ] Multiplayer mode
- [ ] Improved AI model with better accuracy
- [ ] Progressive hints system
- [ ] Drawing history/replay

## 📄 License

[Add your license here]

## 👥 Contributors

[Add contributors here]
