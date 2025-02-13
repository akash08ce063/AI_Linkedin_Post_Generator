import React from 'react';
import { Post } from '../types';
import { Share2, Star, Zap, Brain } from 'lucide-react';

interface PostCardProps {
  post: Post;
}

export function PostCard({ post }: PostCardProps) {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(post.content);
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-400';
    if (score >= 6) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="bg-zinc-900 rounded-lg border border-zinc-800 overflow-hidden hover:border-zinc-700 transition-all">
      <div className="p-4 md:p-6 space-y-4">
        <div className="prose prose-invert max-w-none">
          <p className="text-zinc-300 whitespace-pre-wrap text-sm leading-relaxed">{post.content}</p>
        </div>
      </div>
      
      <div className="border-t border-zinc-800 bg-zinc-900/50 p-4">
        <div className="grid grid-cols-3 gap-2 md:gap-4 mb-4">
          <div className="text-center">
            <div className="flex items-center justify-center mb-1">
              <Brain className="w-4 h-4 text-blue-400" />
            </div>
            <div className={`text-base md:text-lg font-semibold ${getScoreColor(post.scores.clarity_score)}`}>
              {post.scores.clarity_score.toFixed(1)}
            </div>
            <div className="text-xs text-zinc-500">Clarity</div>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center mb-1">
              <Zap className="w-4 h-4 text-yellow-400" />
            </div>
            <div className={`text-base md:text-lg font-semibold ${getScoreColor(post.scores.engagement_potential_score)}`}>
              {post.scores.engagement_potential_score.toFixed(1)}
            </div>
            <div className="text-xs text-zinc-500">Engagement</div>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center mb-1">
              <Star className="w-4 h-4 text-purple-400" />
            </div>
            <div className={`text-base md:text-lg font-semibold ${getScoreColor(post.scores.overall_impact_score)}`}>
              {post.scores.overall_impact_score.toFixed(1)}
            </div>
            <div className="text-xs text-zinc-500">Impact</div>
          </div>
        </div>

        <button
          onClick={copyToClipboard}
          className="w-full flex items-center justify-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 py-2 rounded-md transition-colors"
        >
          <Share2 className="w-4 h-4" />
          Copy to Clipboard
        </button>
      </div>
    </div>
  );
}