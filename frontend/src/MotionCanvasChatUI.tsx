import { useState, useRef, useEffect } from 'react';
import {
  Send,
  Mic,
  Play,
  Pause,
  RotateCcw,
  Download,
  Settings,
  Sparkles,
  Code,
  Palette
} from 'lucide-react';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
}

interface CanvasObject {
  id: number;
  x: number;
  y: number;
  size: number;
  color: string;
  speed: number;
  direction: number;
}

const MotionCanvasChatUI = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'assistant',
      content: 'Welcome to Motion Canvas! I can help you create animations and visual effects. What would you like to build today?'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [canvasObjects, setCanvasObjects] = useState<CanvasObject[]>([]);
  const [showCanvas, setShowCanvas] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize canvas objects
  useEffect(() => {
    const objects: CanvasObject[] = [];
    for (let i = 0; i < 12; i++) {
      objects.push({
        id: i,
        x: Math.random() * 400,
        y: Math.random() * 400,
        size: Math.random() * 30 + 15,
        color: `hsl(${Math.random() * 360}, 70%, 60%)`,
        speed: Math.random() * 2 + 0.5,
        direction: Math.random() * Math.PI * 2
      });
    }
    setCanvasObjects(objects);
  }, []);

  // Canvas animation loop
  useEffect(() => {
    if (!isPlaying || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    const animate = () => {
      if (!isPlaying) return;

      // Clear canvas with gradient background
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      gradient.addColorStop(0, '#0f0f23');
      gradient.addColorStop(0.5, '#1a1a3e');
      gradient.addColorStop(1, '#0f0f23');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update and draw objects
      setCanvasObjects(prev => 
        prev.map(obj => {
          const newX = obj.x + Math.cos(obj.direction) * obj.speed;
          const newY = obj.y + Math.sin(obj.direction) * obj.speed;
          
          // Bounce off edges
          let newDirection = obj.direction;
          if (newX <= 0 || newX >= canvas.width) {
            newDirection = Math.PI - obj.direction;
          }
          if (newY <= 0 || newY >= canvas.height) {
            newDirection = -obj.direction;
          }

          const updatedObj = {
            ...obj,
            x: Math.max(0, Math.min(canvas.width, newX)),
            y: Math.max(0, Math.min(canvas.height, newY)),
            direction: newDirection + (Math.random() - 0.5) * 0.05
          };

          // Draw object with glow effect
          ctx.save();
          ctx.shadowColor = updatedObj.color;
          ctx.shadowBlur = 20;
          ctx.fillStyle = updatedObj.color;
          ctx.beginPath();
          ctx.arc(updatedObj.x, updatedObj.y, updatedObj.size, 0, Math.PI * 2);
          ctx.fill();
          
          // Inner glow
          ctx.shadowBlur = 5;
          ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
          ctx.beginPath();
          ctx.arc(updatedObj.x, updatedObj.y, updatedObj.size * 0.6, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();

          return updatedObj;
        })
      );

      requestAnimationFrame(animate);
    };

    animate();
  }, [isPlaying, canvasObjects.length]);

  const handleSendMessage = () => {
    if (!inputText.trim()) return;
    
    const newMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: inputText
    };
    
    setMessages(prev => [...prev, newMessage]);
    
    // Simulate AI response
    setTimeout(() => {
      const responses = [
        "Great idea! I'll create that animation for you.",
        "Let me generate some moving shapes with those colors.",
        "I'll add some particle effects to make it more dynamic.",
        "That sounds like a fun animation to create!",
        "I'll make the objects dance across the screen."
      ];
      
      const aiResponse: Message = {
        id: messages.length + 2,
        type: 'assistant',
        content: responses[Math.floor(Math.random() * responses.length)]
      };
      
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
    
    setInputText('');
  };

  const handleVoiceInput = () => {
    setIsRecording(!isRecording);
    // Voice input simulation
    if (!isRecording) {
      setTimeout(() => {
        setIsRecording(false);
        setInputText("Create colorful floating particles");
      }, 2000);
    }
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
    if (!showCanvas) setShowCanvas(true);
  };

  const handleReset = () => {
    setIsPlaying(false);
    setShowCanvas(false);
    
    // Reset canvas objects
    const objects: CanvasObject[] = [];
    for (let i = 0; i < 12; i++) {
      objects.push({
        id: i,
        x: Math.random() * 400,
        y: Math.random() * 400,
        size: Math.random() * 30 + 15,
        color: `hsl(${Math.random() * 360}, 70%, 60%)`,
        speed: Math.random() * 2 + 0.5,
        direction: Math.random() * Math.PI * 2
      });
    }
    setCanvasObjects(objects);
  };

  const handleExport = () => {
    if (canvasRef.current) {
      const link = document.createElement('a');
      link.download = 'motion-canvas-frame.png';
      link.href = canvasRef.current.toDataURL();
      link.click();
    }
  };

  return (
    <div className="min-h-screen flex bg-gray-900">
      {/* Left Panel - Chat Interface */}
      <div className="w-1/2 bg-gradient-to-br from-gray-900 to-gray-800 text-white p-6 flex flex-col">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-400" />
            Motion Canvas AI
          </h1>
          <p className="text-gray-400 text-sm">Create animations with AI assistance</p>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
          {messages.map(message => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs px-4 py-2 rounded-2xl ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-700 text-gray-100'
              }`}>
                {message.content}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="space-y-4">
          <div className="flex rounded-xl bg-gray-800 overflow-hidden">
            <input
              type="text"
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && handleSendMessage()}
              className="flex-1 p-3 bg-transparent text-white placeholder-gray-400 focus:outline-none"
              placeholder="Describe your animation idea..."
            />
            <button 
              onClick={handleSendMessage}
              className="px-4 py-3 bg-purple-600 hover:bg-purple-700 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>

          {/* Control Buttons */}
          <div className="flex space-x-2">
            <button 
              onClick={handleVoiceInput}
              className={`p-3 rounded-lg transition-all ${
                isRecording 
                  ? 'bg-red-600 hover:bg-red-700 animate-pulse' 
                  : 'bg-red-500 hover:bg-red-600'
              }`}
            >
              <Mic className="w-5 h-5" />
            </button>
            <button 
              onClick={handlePlayPause}
              className={`p-3 rounded-lg transition-all ${
                isPlaying 
                  ? 'bg-orange-600 hover:bg-orange-700' 
                  : 'bg-green-600 hover:bg-green-700'
              }`}
            >
              {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
            </button>
            <button 
              onClick={handleReset}
              className="p-3 bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors"
            >
              <RotateCcw className="w-5 h-5" />
            </button>
            <button 
              onClick={handleExport}
              className="p-3 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors"
            >
              <Download className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Right Panel - Canvas */}
      <div className="w-1/2 relative bg-gradient-to-br from-gray-800 to-gray-900">
        {showCanvas ? (
          <div className="w-full h-full relative">
            <canvas
              ref={canvasRef}
              className="w-full h-full"
              style={{ background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%)' }}
            />
            
            {/* Canvas Overlay Controls */}
            <div className="absolute top-4 left-4 flex space-x-2">
              <div className="bg-black bg-opacity-50 px-3 py-1 rounded-full text-white text-sm">
                {isPlaying ? 'Playing' : 'Paused'}
              </div>
              <div className="bg-black bg-opacity-50 px-3 py-1 rounded-full text-white text-sm">
                {canvasObjects.length} objects
              </div>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-white">
            <div className="text-center">
              <Play className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <h2 className="text-xl font-semibold mb-2">Ready to Create</h2>
              <p className="text-gray-400">Press Play to start your animation</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MotionCanvasChatUI;