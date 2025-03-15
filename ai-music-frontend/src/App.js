import React, { useState } from 'react';
import { Sparkles, Copy, FileText, Music } from 'lucide-react';
import jsPDF from 'jspdf';

const LyricsGenerator = () => {
  const [formData, setFormData] = useState({
    music_style: '',
    theme: '',
    emotion: '',
    structure: '',
    length: ''
  });
  const [lyrics, setLyrics] = useState('');
  const [isGenerated, setIsGenerated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const getWordCount = (text) => {
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
  };

  const copyToClipboard = () => {
    if (lyrics) {
      navigator.clipboard.writeText(lyrics)
        .then(() => {
          alert('Lyrics copied to clipboard');
        })
        .catch(err => {
          console.error('Could not copy text: ', err);
        });
    }
  };

  const exportToPDF = () => {
    if (!lyrics) {
      alert('No lyrics to export!');
      return;
    }
  
    const doc = new jsPDF();
    doc.setFont('Helvetica', 'normal');
    doc.setFontSize(12);
  
    // Add title
    doc.text('Generated Lyrics', 10, 10);
  
    // Add lyrics content
    const margin = 10;
    const pageWidth = doc.internal.pageSize.width;
    const textWidth = pageWidth - margin * 2;
    const lines = doc.splitTextToSize(lyrics, textWidth);
    doc.text(lines, margin, 20);
  
    // Save the PDF
    doc.save('lyrics.pdf');
  };

  const generateLyrics = async () => {
    try {
      setIsLoading(true);
      setError('');
      
      // Prepare data for API call
      const apiData = {
        music_style: formData.music_style || 'No specific style',
        theme: formData.theme || 'No specific theme',
        emotion: formData.emotion || 'No specific emotion',
        structure: formData.structure || 'No specific structure',
        length: parseInt(formData.length) || 350
      };

      // Call backend API
      const response = await fetch('http://127.0.0.1:5000/generate-lyrics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiData),
      });

      if (!response.ok) {
        throw new Error('Failed to generate lyrics');
      }

      const data = await response.json();
      setLyrics(data.lyrics);
      setIsGenerated(true);
    } catch (err) {
      setError('Error generating lyrics. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto min-h-screen p-6 mt-28 pb-20">
      <div className="flex flex-col justify-between items-center mb-12">
        <div className="flex items-center gap-3">
          <h1 className="text-5xl font-bold text-gray-800 font-cartoon">AI Lyrics Generator</h1>
          <Music size={40} className="text-gray-800" />
        </div>
        <h3 className="text-1xl font-bold text-gray-400 mt-4">Create your customized lyrics!</h3>
      </div>
      
      <div className="relative">
        <div className="flex justify-between gap-8">
          {/* Input section */}
          <div className={`transition-all duration-1000 ease-in-out ${
            isGenerated ? 'w-1/2' : 'w-3/5 mx-auto'
          }`}>
            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Style</h2>
              <input
                type="text"
                name="music_style"
                value={formData.music_style}
                onChange={handleInputChange}
                placeholder="e.g. Pop, Rock, Country, Hip-Hop, Jazz, R&B"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Theme</h2>
              <input
                type="text"
                name="theme"
                value={formData.theme}
                onChange={handleInputChange}
                placeholder="e.g. Love, Friendship, Journey, Heartbreak, Success"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Emotional Tone</h2>
              <input
                type="text"
                name="emotion"
                value={formData.emotion}
                onChange={handleInputChange}
                placeholder="e.g. Happy, Sad, Hopeful, Angry, Nostalgic, Upbeat"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Structure</h2>
              <input
                type="text"
                name="structure"
                value={formData.structure}
                onChange={handleInputChange}
                placeholder="e.g. Verse-Chorus-Verse, AABA, Includes Bridge"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Length</h2>
              <input
                type="text"
                name="length"
                value={formData.length}
                onChange={handleInputChange}
                placeholder="e.g. 350 (approximate character length)"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>
          </div>

          {/* Generated lyrics area */}
          <div className={`w-3/5 transition-all duration-1000 ease-in-out ${
            isGenerated ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-full hidden'
          }`}>
            <div className="relative">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Your generated lyrics:</h2>
              <textarea
                value={lyrics}
                onChange={(e) => setLyrics(e.target.value)}
                className="w-full p-4 font-bold bg-gray-50 border border-gray-200 rounded-lg text-gray-500 min-h-[470px] resize-y"
              />
              <div className="absolute right-3 bottom-3 text-sm text-gray-400">
                {getWordCount(lyrics)} words
              </div>
              
              <div className="absolute right-2 bottom-[-3rem] flex space-x-3">
                <div className="relative group">
                  <button 
                    onClick={copyToClipboard}
                    className="p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-all duration-300 group-hover:scale-110"
                  >
                    <Copy size={20} className="text-gray-600" />
                  </button>
                  <span className="absolute -top-10 left-1/2 -translate-x-1/2 w-max opacity-0 transition-opacity group-hover:opacity-100 bg-gray-800 text-white text-xs px-2 py-1 rounded pointer-events-none">
                    Copy Text
                  </span>
                </div>
                
                <div className="relative group">
                  <button 
                    onClick={exportToPDF}
                    className="p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-all duration-300 group-hover:scale-110"
                  >
                    <FileText size={20} className="text-gray-600" />
                  </button>
                  <span className="absolute -top-10 left-1/2 -translate-x-1/2 w-max opacity-0 transition-opacity group-hover:opacity-100 bg-gray-800 text-white text-xs px-2 py-1 rounded pointer-events-none">
                    Export to PDF
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Generate button */}
        <div className="absolute left-1/2 -translate-x-1/2 mt-8">
          <button
            onClick={generateLyrics}
            disabled={isLoading}
            className={`flex flex-row justify-center items-center px-8 py-3 bg-[#1DB954] text-white font-large rounded-lg transition-colors hover:bg-[#1ed760] font-sora ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
          >  
            {isLoading ? 'Generating...' : 'Generate Lyrics'}
            {!isLoading && <Sparkles className="w-5 h-5 ml-2" />}
          </button>
        </div>
        
        {/* Error message */}
        {error && (
          <div className="mt-16 text-center text-red-500">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default LyricsGenerator;
