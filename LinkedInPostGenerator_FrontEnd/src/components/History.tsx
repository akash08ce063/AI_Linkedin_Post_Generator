import React from 'react';
import { GenerationHistory } from '../types';
import { PostCard } from './PostCard';
import { Clock, Link, FileText, MessageSquare } from 'lucide-react';

interface HistoryProps {
  history: GenerationHistory[];
}

export function History({ history }: HistoryProps) {
  if (history.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-zinc-500">
        No generation history yet
      </div>
    );
  }

  return (
    <div className="space-y-6 overflow-auto">
      {history.map((item, index) => {
        const TypeIcon = item.input.type === 'links' 
          ? Link 
          : item.input.type === 'topic' 
            ? FileText 
            : MessageSquare;

        return (
          <div key={index} className="p-4 bg-zinc-900 rounded-lg border border-zinc-800 hover:border-zinc-700 transition-all">
            <div className="flex items-center gap-3 mb-3">
              <TypeIcon className="w-4 h-4 text-zinc-400" />
              <span className="text-zinc-300 font-medium truncate">
                {item.input.value.split('\n')[0]}
              </span>
            </div>
            <div className="flex items-center gap-2 text-sm text-zinc-500">
              <Clock className="w-3 h-3" />
              <span>{new Date(item.timestamp).toLocaleString()}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}