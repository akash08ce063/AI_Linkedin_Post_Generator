import React, { useState } from 'react';
import { Link, FileText, MessageSquare, AlertCircle } from 'lucide-react';

interface GenerationFormProps {
  onGenerate: (type: 'links' | 'topic' | 'content', value: string) => Promise<void>;
  isLoading: boolean;
}

export function GenerationForm({ onGenerate, isLoading }: GenerationFormProps) {
  const [activeTab, setActiveTab] = useState<'links' | 'topic' | 'content'>('links');
  const [input, setInput] = useState('');
  const [error, setError] = useState<string | null>(null);

  const validateUrls = (text: string): boolean => {
    const urls = text.split('\n').filter(line => line.trim());
    const urlPattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
    
    return urls.every(url => urlPattern.test(url.trim()));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!input.trim()) {
      setError('Please enter some content');
      return;
    }

    if (activeTab === 'links' && !validateUrls(input)) {
      setError('Please enter valid URLs (one per line)');
      return;
    }

    try {
      await onGenerate(activeTab, input.trim());
      setInput('');
    } catch (error) {
      setError('Failed to generate posts. Please try again.');
    }
  };

  return (
    <div className="w-full bg-zinc-900 rounded-lg p-4 md:p-6 border border-zinc-800">
      <div className="flex flex-wrap gap-2 md:gap-4 mb-4">
        <button
          onClick={() => {
            setActiveTab('links');
            setError(null);
          }}
          className={`flex items-center gap-2 px-3 md:px-4 py-2 rounded-md transition-colors ${
            activeTab === 'links' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
          }`}
        >
          <Link className="w-4 h-4" />
          <span className="text-sm md:text-base">From Links</span>
        </button>
        <button
          onClick={() => {
            setActiveTab('topic');
            setError(null);
          }}
          className={`flex items-center gap-2 px-3 md:px-4 py-2 rounded-md transition-colors ${
            activeTab === 'topic' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span className="text-sm md:text-base">From Topic</span>
        </button>
        <button
          onClick={() => {
            setActiveTab('content');
            setError(null);
          }}
          className={`flex items-center gap-2 px-3 md:px-4 py-2 rounded-md transition-colors ${
            activeTab === 'content' ? 'bg-zinc-800 text-white' : 'text-zinc-400 hover:text-white'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span className="text-sm md:text-base">From Content</span>
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
              setError(null);
            }}
            placeholder={
              activeTab === 'links'
                ? 'Paste your URLs here (one per line)...'
                : activeTab === 'topic'
                ? 'Enter your topic...'
                : 'Enter your content ideas...'
            }
            className="w-full h-32 bg-zinc-800 text-white rounded-md p-3 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {error && (
            <div className="flex items-center gap-2 mt-2 text-red-400 text-sm">
              <AlertCircle className="w-4 h-4" />
              <span>{error}</span>
            </div>
          )}
        </div>
        <button
          type="submit"
          disabled={isLoading}
          className={`w-full flex items-center justify-center gap-2 py-2 rounded-md transition-colors ${
            isLoading
              ? 'bg-blue-800 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'
          } text-white`}
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Generating...
            </>
          ) : (
            'Generate Posts'
          )}
        </button>
      </form>
    </div>
  );
}