export interface Post {
  content: string;
  scores: {
    clarity_score: number;
    engagement_potential_score: number;
    overall_impact_score: number;
  };
  timestamp: string;
}

export interface GenerationHistory {
  input: {
    type: 'links' | 'topic' | 'content';
    value: string;
  };
  posts: Post[];
  timestamp: string;
}

export interface ApiResponse {
  posts: Post[];
}