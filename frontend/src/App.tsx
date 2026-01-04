import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [gameStarted, setGameStarted] = useState(false)
  const [secretWord, setSecretWord] = useState<string>('')
  const [aiGuess, setAiGuess] = useState<string>('')
  const [isDrawing, setIsDrawing] = useState(false)

  const canvasRef = useRef<HTMLCanvasElement>(null)
  const ctxRef = useRef<CanvasRenderingContext2D | null>(null)

  const words = ['cat', 'dog', 'house', 'tree', 'car', 'sun', 'moon', 'star', 'bird', 'fish']

  const startGame = () => {
    const randomWord = words[Math.floor(Math.random() * words.length)]
    setSecretWord(randomWord)
    setAiGuess('')
    setGameStarted(true)
  }

  useEffect(() => {
    if (gameStarted && canvasRef.current) {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      if (ctx) {
        ctx.strokeStyle = '#000000'
        ctx.lineWidth = 3
        ctx.lineCap = 'round'
        ctxRef.current = ctx
        
        // Set canvas size
        canvas.width = canvas.offsetWidth
        canvas.height = canvas.offsetHeight
      }
    }
  }, [gameStarted])

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    setIsDrawing(true)
    const canvas = canvasRef.current
    const ctx = ctxRef.current
    if (!canvas || !ctx) return
    
    const rect = canvas.getBoundingClientRect()
    const x = 'touches' in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left
    const y = 'touches' in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top
    
    ctx.beginPath()
    ctx.moveTo(x, y)
  }
  
  const draw = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return
    const canvas = canvasRef.current
    const ctx = ctxRef.current
    if (!canvas || !ctx) return
    
    const rect = canvas.getBoundingClientRect()
    const x = 'touches' in e ? e.touches[0].clientX - rect.left : e.clientX - rect.left
    const y = 'touches' in e ? e.touches[0].clientY - rect.top : e.clientY - rect.top
    
    ctx.lineTo(x, y)
    ctx.stroke()
  }
  
  const stopDrawing = () => {
    setIsDrawing(false)
  }

  return (
    <div className="app-container">
    {!gameStarted ? (
      <div className="home-screen">
        <div className="home-content">
          <h1 className="home-title">Sketch Sense</h1>
          <p className="home-description">
            Draw a secret word on the canvas and let AI guess what you're drawing. 
            Score points based on speed, accuracy, and how well the AI understands your sketch!
          </p>
          <button 
            className="start-button" 
            onClick={startGame}
          >
            Start Drawing
          </button>
        </div>
      </div>
    ) : (
      <div className="game-screen">
  <div className="game-header">
    <div className="word-display">
      <h2>Draw: <span className="secret-word">{secretWord}</span></h2>
    </div>
    <div className="ai-guess-display">
      <p>{aiGuess ? `Is it a ${aiGuess}?` : 'AI is thinking...'}</p>
    </div>
  </div>
  
  <div className="canvas-container">
    <canvas
      ref={canvasRef}
      className="drawing-canvas"
      onMouseDown={startDrawing}
      onMouseMove={draw}
      onMouseUp={stopDrawing}
      onMouseLeave={stopDrawing}
      onTouchStart={startDrawing}
      onTouchMove={draw}
      onTouchEnd={stopDrawing}
    />
  </div>
  
  <div className="game-controls">
    <button onClick={() => setGameStarted(false)}>Back to Home</button>
    <button onClick={() => {
      // Clear canvas
      const canvas = canvasRef.current
      const ctx = ctxRef.current
      if (canvas && ctx) {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
      }
    }}>Clear</button>
    <button onClick={() => {
      // Submit drawing for AI analysis (to be implemented)
      // For now, just simulate an AI guess
      setAiGuess('cat')
    }}>Submit</button>
  </div>
  </div>
    )}
  </div>
  )
}

export default App
