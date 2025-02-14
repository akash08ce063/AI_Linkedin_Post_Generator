import React, { useState } from 'react';
import { GenerationForm } from './components/GenerationForm';
import { History } from './components/History';
import { GenerationHistory } from './types';
import { Sparkles, PanelLeftClose, PanelLeft } from 'lucide-react';
import { generatePosts } from './api';
import { PostCard } from './components/PostCard';

function App() {
  const [history, setHistory] = useState<GenerationHistory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedHistory, setSelectedHistory] = useState<GenerationHistory | null>(null);
  const [isHistoryOpen, setIsHistoryOpen] = useState(true);

  const handleGenerate = async (type: 'links' | 'topic' | 'content', value: string) => {
    setIsLoading(true);
    try {
      const posts = await generatePosts(type, value);
      const newHistory: GenerationHistory = {
        input: { type, value },
        posts,
        timestamp: new Date().toISOString()
      };
      setHistory(prev => [newHistory, ...prev]);
      setSelectedHistory(newHistory);
    } catch (error) {
      console.error('Failed to generate posts:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="h-screen flex flex-col">
        <header className="flex-none p-4 border-b border-zinc-800">
          <div className="max-w-7xl mx-auto w-full">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-8 h-8 text-blue-500" />
                <h1 className="text-2xl font-bold">LinkedIn Post Generator</h1>
              </div>
              <button
                onClick={() => setIsHistoryOpen(!isHistoryOpen)}
                className="p-2 hover:bg-zinc-800 rounded-md transition-colors md:hidden"
              >
                {isHistoryOpen ? <PanelLeftClose className="w-5 h-5" /> : <PanelLeft className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-hidden">
          <div className="h-full flex">
            {/* Left Panel - History */}
            <div
              className={`${
                isHistoryOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
              } fixed md:relative z-20 w-80 h-[calc(100vh-73px)] flex-none border-r border-zinc-800 bg-black transition-transform duration-300 ease-in-out`}
            >
              <div className="flex items-center justify-between p-4 border-b border-zinc-800">
                <h2 className="text-lg font-semibold">Generation History</h2>
                <button
                  onClick={() => setIsHistoryOpen(false)}
                  className="p-2 hover:bg-zinc-800 rounded-md transition-colors md:hidden"
                >
                  <PanelLeftClose className="w-5 h-5" />
                </button>
              </div>
              <div className="p-4 h-[calc(100%-65px)] overflow-auto">
                <History history={history} />
              </div>
            </div>

            {/* Overlay */}
            {isHistoryOpen && (
              <div
                className="fixed inset-0 bg-black bg-opacity-50 z-10 md:hidden"
                onClick={() => setIsHistoryOpen(false)}
              />
            )}

            {/* Main Content */}
            <div className="flex-1 overflow-auto w-full">
              <div className="max-w-3xl mx-auto p-4 md:p-6 space-y-6 md:space-y-8">
                <div className="text-center mb-6 md:mb-8">
                  <p className="text-zinc-400 max-w-2xl mx-auto">
                    Generate engaging LinkedIn posts from links, topics, or your own content ideas.
                    Our AI will create multiple variations with engagement scores to help you pick the best one.
                  </p>
                </div>

                <GenerationForm onGenerate={handleGenerate} isLoading={isLoading} />

                {selectedHistory && (
                  <div className="space-y-6">
                    <h2 className="text-xl font-semibold">Generated Posts</h2>
                    <div className="grid grid-cols-1 gap-6">
                      {selectedHistory.posts.map((post, index) => (
                        <PostCard key={index} post={post} />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;