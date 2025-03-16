import React, { useState, useRef, useEffect } from 'react';
import { Play, Pause, Download, RefreshCw } from 'lucide-react';

const MusicGenerator = ({ description }) => {
  const [audioSrc, setAudioSrc] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(null);

  useEffect(() => {
    if (description && description.trim()) {
      generateMusic();
    }
  });

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => {
      setCurrentTime(audio.currentTime);
      setDuration(audio.duration);
    };

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', () => {
      setDuration(audio.duration);
    });

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateTime);
    };
  }, [audioSrc]);

  const generateMusic = async () => {
    if (!description || !description.trim()) {
      setError('Please provide a description for the music');
      return;
    }

    try {
      setIsLoading(true);
      setError('');
      setAudioSrc('');
      
      const response = await fetch('http://127.0.0.1:5000/generate-music', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ des: description }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate music');
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      const audioData = `data:audio/wav;base64,${data.audio_data_base64}`;
      setAudioSrc(audioData);
    } catch (err) {
      setError(`Error: ${err.message}`);
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePlayPause = () => {
    if (!audioRef.current) return;
    
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    
    setIsPlaying(!isPlaying);
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const downloadAudio = () => {
    if (!audioSrc) return;
    
    const a = document.createElement('a');
    a.href = audioSrc;
    a.download = 'generated-music.wav';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const formatTime = (time) => {
    if (isNaN(time)) return '00:00';
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  const handleProgressChange = (e) => {
    const newTime = e.target.value;
    setCurrentTime(newTime);
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
    }
  };

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      {isLoading ? (
        <div className="flex items-center justify-center p-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-700"></div>
          <span className="ml-3 text-gray-600">Generating music...</span>
        </div>
      ) : audioSrc ? (
        <div className="flex flex-col">
          <audio 
            ref={audioRef} 
            src={audioSrc} 
            onEnded={handleAudioEnded}
            className="hidden"
          />
          
          <div className="flex items-center space-x-2 mb-2">
            <button
              onClick={togglePlayPause}
              className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
            >
              {isPlaying ? (
                <Pause className="w-6 h-6 text-gray-800" />
              ) : (
                <Play className="w-6 h-6 text-gray-800" />
              )}
            </button>
            
            <div className="flex-1 flex items-center space-x-2">
              <span className="text-xs text-gray-500 w-10">{formatTime(currentTime)}</span>
              <input
                type="range"
                min="0"
                max={duration || 0}
                value={currentTime}
                onChange={handleProgressChange}
                className="flex-1 h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
              <span className="text-xs text-gray-500 w-10">{formatTime(duration)}</span>
            </div>
            
            <button
              onClick={downloadAudio}
              className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors"
              title="Download audio"
            >
              <Download className="w-5 h-5 text-gray-700" />
            </button>
          </div>
          
          <div className="h-10 bg-gray-50 rounded-md overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-gray-200 to-green-100" 
              style={{ width: `${(currentTime / duration) * 100 || 0}%`, transition: 'width 0.1s linear' }}
            ></div>
          </div>
        </div>
      ) : (
        <div className="flex justify-center p-3">
          <button
            onClick={generateMusic}
            disabled={isLoading || !description}
            className={`flex items-center px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors ${
              isLoading || !description ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            Generate Accompaniment
            <RefreshCw className="w-4 h-4 ml-2" />
          </button>
        </div>
      )}
      
      {error && (
        <div className="mt-2 p-2 bg-red-50 text-red-500 rounded text-sm">
          {error}
        </div>
      )}
    </div>
  );
};

export default MusicGenerator;
