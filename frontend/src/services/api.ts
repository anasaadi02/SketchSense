const API_URL = 'http://localhost:5000'

export interface Prediction {
  word: string
  confidence: number
}

export interface PredictResponse {
  success: boolean
  predictions: Prediction[]
  top_guess: Prediction | null
}

export interface HealthResponse {
  status: string
  model_loaded: boolean
}

export const checkHealth = async (): Promise<HealthResponse> => {
  const response = await fetch(`${API_URL}/health`)
  if (!response.ok) {
    throw new Error('Health check failed')
  }
  return response.json()
}

export const predictDrawing = async (canvas: HTMLCanvasElement): Promise<PredictResponse> => {
  // Convert canvas to base64
  const imageData = canvas.toDataURL('image/png')
  
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      image: imageData
    })
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Prediction failed')
  }
  
  return response.json()
}