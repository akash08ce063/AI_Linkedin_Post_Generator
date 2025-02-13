const API_URL = 'http://localhost:8000';

export async function generatePosts(type: 'links' | 'topic' | 'content', value: string): Promise<Post[]> {
  try {
    const response = await fetch(`${API_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ type, value }),
    });

    if (!response.ok) {
      throw new Error('Failed to generate posts');
    }

    const data: ApiResponse = await response.json();
    return data.posts;
  } catch (error) {
    console.error('Error generating posts:', error);
    throw error;
  }
}