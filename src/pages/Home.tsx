// import React from 'react';
// import HeroSection from '../components/HeroSection';
// import FeaturesSection from '../components/FeaturesSection';
// import TestimonialsSection from '../components/TestimonialsSection';

// const Home: React.FC = () => {
//   return (
//     <div>
//       <HeroSection />
//       <FeaturesSection />
//       <TestimonialsSection />
//     </div>
//   );
// };

// export default Home;

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
      content:
        'Welcome to Motion Canvas! I can help you create animations and visual effects. What would you like to build today?'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [canvasObjects, setCanvasObjects] = useState<CanvasObject[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const objects: CanvasObject[] = [];
    for (let i = 0; i < 8; i++) {
      objects.push({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: Math.random() * 20 + 10,
        color: `hsl(${Math.random() * 360}, 70%, 60%)`,
        speed: Math.random() * 0.5 + 0.1,
        direction: Math.random() * Math.PI * 2
      });
    }
    setCanvasObjects(objects);
  }, []);

  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      setCanvasObjects(prev =>
        prev.map(obj => ({
          ...obj,
          x: (obj.x + Math.cos(obj.direction) * obj.speed) % 100,
          y: (obj.y + Math.sin(obj.direction) * obj.speed) % 100,
          direction: obj.direction + (Math.random() - 0.5) * 0.1
        }))
      );
    }, 50);

    return () => clearInterval(interval);
  }, [isPlaying]);

  const handleSendMessage = () => {
    if (!inputText.trim()) return;

    const newMessage: Message = {
      id: messages.length + 1,
      type: 'user',
      content: inputText
    };

    setMessages(prev => [...prev, newMessage]);
    setInputText('');

    // Placeholder: actual assistant response should be fetched from API here
  };

  const handleVoiceInput = () => {
    setIsRecording(!isRecording);
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleReset = () => {
    setIsPlaying(false);
    const objects: CanvasObject[] = [];
    for (let i = 0; i < 8; i++) {
      objects.push({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: Math.random() * 20 + 10,
        color: `hsl(${Math.random() * 360}, 70%, 60%)`,
        speed: Math.random() * 0.5 + 0.1,
        direction: Math.random() * Math.PI * 2
      });
    }
    setCanvasObjects(objects);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-900 to-indigo-900 flex">
      {/* Left Panel */}
      <div className="w-1/2 flex flex-col bg-black bg-opacity-20 backdrop-blur-sm border-r border-indigo-700/30">
        <div className="p-6 border-b border-indigo-700/30">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Motion Canvas AI</h1>
              <p className="text-indigo-200 text-sm">Create animations with AI assistance</p>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map(message => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl transition-all duration-300 ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    : 'bg-indigo-800 bg-opacity-50 text-indigo-100 border border-indigo-700/30'
                }`}
              >
                <p className="text-sm">{message.content}</p>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-6 border-t border-indigo-700/30">
          <div className="flex items-center space-x-3 mb-4">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputText}
                onChange={e => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Describe your animation idea..."
                className="w-full px-4 py-3 bg-indigo-900 bg-opacity-50 border border-indigo-700/50 rounded-xl text-white placeholder-indigo-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-300"
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim()}
              className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleVoiceInput}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 transform hover:scale-105 active:scale-95 ${
                isRecording
                  ? 'bg-red-600 hover:bg-red-700 text-white'
                  : 'bg-indigo-800 bg-opacity-50 border border-indigo-700/50 text-indigo-200 hover:bg-indigo-700 hover:bg-opacity-50'
              }`}
            >
              <Mic className="w-4 h-4" />
              <span className="text-sm">Voice</span>
            </button>

            <button
              onClick={handlePlayPause}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all duration-300 transform hover:scale-105 active:scale-95"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              <span className="text-sm">Run</span>
            </button>

            <button
              onClick={handleReset}
              className="flex items-center space-x-2 px-4 py-2 bg-indigo-800 bg-opacity-50 border border-indigo-700/50 text-indigo-200 hover:bg-indigo-700 hover:bg-opacity-50 rounded-lg transition-all duration-300 transform hover:scale-105 active:scale-95"
            >
              <RotateCcw className="w-4 h-4" />
              <span className="text-sm">Reset</span>
            </button>
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-1/2 flex flex-col">
        <div className="p-6 border-b border-indigo-700/30 bg-black bg-opacity-20 backdrop-blur-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg">
                <Palette className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Live Canvas</h2>
                <p className="text-indigo-200 text-sm">Real-time animation preview</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button className="p-2 bg-indigo-800 bg-opacity-50 border border-indigo-700/50 text-indigo-200 hover:bg-indigo-700 hover:bg-opacity-50 rounded-lg transition-all duration-300 transform hover:scale-105 active:scale-95">
                <Settings className="w-5 h-5" />
              </button>
              <button className="p-2 bg-indigo-800 bg-opacity-50 border border-indigo-700/50 text-indigo-200 hover:bg-indigo-700 hover:bg-opacity-50 rounded-lg transition-all duration-300 transform hover:scale-105 active:scale-95">
                <Download className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        <div className="flex-1 relative bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 overflow-hidden">
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-blue-500 rounded-full blur-3xl animate-pulse"></div>
            <div
              className="absolute bottom-1/4 right-1/4 w-24 h-24 bg-purple-500 rounded-full blur-2xl animate-pulse"
              style={{ animationDelay: '1s' }}
            ></div>
            <div
              className="absolute top-1/2 right-1/3 w-20 h-20 bg-pink-500 rounded-full blur-xl animate-pulse"
              style={{ animationDelay: '0.5s' }}
            ></div>
          </div>

          <div className="absolute inset-0 overflow-hidden">
            {canvasObjects.map(obj => (
              <div
                key={obj.id}
                className={`absolute rounded-full shadow-lg transition-all duration-75 ${
                  isPlaying ? 'animate-spin' : ''
                }`}
                style={{
                  left: `${obj.x}%`,
                  top: `${obj.y}%`,
                  width: `${obj.size}px`,
                  height: `${obj.size}px`,
                  backgroundColor: obj.color,
                  boxShadow: `0 0 ${obj.size}px ${obj.color}40`,
                  transform: isPlaying
                    ? `scale(${1 + Math.sin(Date.now() * 0.001 + obj.id) * 0.2})`
                    : 'scale(1)',
                  animationDuration: `${2 + obj.id * 0.2}s`
                }}
              />
            ))}
          </div>

          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center text-white">
              <div className="mb-4 animate-fade-in">
                <Code className="w-16 h-16 mx-auto mb-4 text-indigo-300" />
                <h3 className="text-2xl font-bold mb-2">Motion Canvas</h3>
                <p className="text-indigo-200">Your animations come to life here</p>
              </div>

              {!isPlaying && (
                <div className="mt-6 animate-fade-in" style={{ animationDelay: '0.5s' }}>
                  <button
                    onClick={handlePlayPause}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-full font-medium transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
                  >
                    Start Animation
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="absolute top-4 right-4">
            <div
              className={`flex items-center space-x-2 px-3 py-1 rounded-full ${
                isPlaying ? 'bg-green-600' : 'bg-gray-600'
              } bg-opacity-80 backdrop-blur-sm`}
            >
              <div
                className={`w-2 h-2 rounded-full ${
                  isPlaying ? 'bg-green-300 animate-pulse' : 'bg-gray-300'
                }`}
              ></div>
              <span className="text-white text-sm font-medium">
                {isPlaying ? 'Running' : 'Paused'}
              </span>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in {
          animation: fade-in 0.5s ease-out forwards;
        }
      `}</style>
    </div>
  );
};

export default MotionCanvasChatUI;
