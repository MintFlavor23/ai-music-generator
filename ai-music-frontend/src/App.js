import React, { useState } from 'react';
import { Sparkles, Copy, FileText, Music } from 'lucide-react';

const LyricsGenerator = () => {
  const [summary, setSummary] = useState('');
  const [isGenerated, setIsGenerated] = useState(false);

  const getWordCount = (text) => {
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
  };

  const copyToClipboard = () => {
    if (summary) {
      navigator.clipboard.writeText(summary)
        .then(() => {
          alert('Summary copied to clipboard');
        })
        .catch(err => {
          console.error('Could not copy text: ', err);
        });
    }
  };

  const exportToPDF = () => {
    alert('Exporting to PDF... (This would be implemented with a PDF library)');
  };

  const generateSummary = () => {
    setSummary("The modern olympics games are the world's leading international sporting events. Thousands of athletes from around the world participate in a variety of competitions. More than two hundred teams representing sovereign states and territories participate by default.");
    setIsGenerated(true);
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
          {/* 左侧输入区域 */}
          <div className={`transition-all duration-1000 ease-in-out ${
            isGenerated ? 'w-1/2' : 'w-3/5 mx-auto'
          }`}>
            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Style</h2>
              <input
                type="text"
                placeholder="e.g. Pop, Rock, Country, Hip-Hop, Jazz, R&B"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Theme</h2>
              <input
                type="text"
                placeholder="e.g. Love, Friendship, Journey, Heartbreak, Success"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Emotional Tone</h2>
              <input
                type="text"
                placeholder="e.g. Happy, Sad, Hopeful, Angry, Nostalgic, Upbeat"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Structure</h2>
              <input
                type="text"
                placeholder="e.g. Verse-Chorus-Verse, AABA, Includes Bridge"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>

            <div className="mb-6">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Length</h2>
              <input
                type="text"
                placeholder="e.g. Around 200 words"
                className="w-full p-3 border border-gray-200 rounded-lg text-gray-700 focus:outline-none focus:border-gray-400"
              />
            </div>
          </div>

          {/* 右侧生成区域 */}
          <div className={`w-3/5 transition-all duration-1000 ease-in-out ${
            isGenerated ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-full hidden'
          }`}>
            <div className="relative">
              <h2 className="text-md font-bold text-gray-700 mb-2 font-sora">Modify your lyrics:</h2>
              <textarea
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                className="w-full p-4 font-bold bg-gray-50 border border-gray-200 rounded-lg text-gray-500 min-h-[470px] resize-y"
              />
              <div className="absolute right-3 bottom-3 text-sm text-gray-400">
                {getWordCount(summary)} words
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

        {/* 将按钮移到这里，使用绝对定位 */}
        <div className="absolute left-1/2 -translate-x-1/2 mt-8">
          <button
            onClick={generateSummary}
            className="flex flex-row justify-center items-center px-8 py-3 bg-[#1DB954] text-white font-large rounded-lg transition-colors hover:bg-[#1ed760] font-sora"
          >  
            Generate Lyrics
            <Sparkles className="w-5 h-5 ml-2" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default LyricsGenerator;
