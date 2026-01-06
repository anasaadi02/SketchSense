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
│   ├── train_model.py    # Model training script
│   ├── download_data.py  # QuickDraw data downloader
│   ├── requirements.txt  # Python dependencies
│   ├── models/           # Trained model files
│   │   ├── drawing_model.h5
│   │   └── class_names.json
│   └── data/             # Training data (not in git)
│       └── quickdraw/    # QuickDraw dataset files           
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

## 🤖 Training Your Own Model

The project includes scripts to train a custom drawing recognition model using the QuickDraw dataset.

### Step 1: Download Training Data

```bash
cd backend
python download_data.py
```

This downloads the QuickDraw dataset for the categories defined in the script (default: 20 categories including cat, dog, house, tree, car, etc.).

**Note**: The data folder is excluded from git. Downloaded files will be saved to `backend/data/quickdraw/`.

### Step 2: Train the Model

```bash
cd backend
python train_model.py
```

This will:
- Load and preprocess the QuickDraw data
- Create a CNN model architecture
- Train the model with data augmentation
- Save the best model to `backend/models/drawing_model.h5`
- Save class names to `backend/models/class_names.json`

### Training Configuration

You can customize training by editing `train_model.py`:

- **Categories**: Modify `QUICKDRAW_CATEGORIES` in `download_data.py`
- **Samples per class**: Adjust `MAX_SAMPLES_PER_CLASS` (default: 10,000)
- **Epochs**: Change `EPOCHS` (default: 50)
- **Batch size**: Modify `BATCH_SIZE` (default: 32)
- **Learning rate**: Adjust `LEARNING_RATE` (default: 0.001)

### Model Architecture

The model uses a CNN architecture with:
- 3 convolutional blocks with batch normalization
- Dropout layers for regularization
- Dense layers for classification
- Softmax output for multi-class prediction

### Training Tips

- **Start small**: Test with 5-10 categories first
- **Use GPU**: Training is much faster with GPU (TensorFlow will auto-detect)
- **Monitor overfitting**: Watch validation vs training accuracy
- **Adjust hyperparameters**: Experiment with learning rate and batch size

### After Training

Once training completes:
1. The model will be saved to `backend/models/drawing_model.h5`
2. Class names will be saved to `backend/models/class_names.json`
3. Restart the backend server to load the new model
4. The model will automatically be used for predictions

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
- ✅ Model training scripts (download_data.py, train_model.py)
- ⏳ **Model Training** (ready to train - run training scripts)

## 📝 Notes

- **Model Location**: The backend expects a trained model at `backend/models/drawing_model.h5`
- **Training Data**: The `backend/data/` folder is excluded from git (see `.gitignore`)
- **Training Options**:
  - Use the provided training scripts to train your own model (recommended)
  - Download a pre-trained QuickDraw model and place it in `backend/models/`
  - The model service will create a mock model if no trained model is found (for testing only)
- **Class Names**: After training, class names are automatically saved and loaded from `backend/models/class_names.json`

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
