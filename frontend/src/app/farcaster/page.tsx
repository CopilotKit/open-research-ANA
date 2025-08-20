'use client';

import { useState } from 'react';

export default function FarcasterPage() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const send = async () => {
    setLoading(true);
    const res = await fetch('/api/farcaster', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    setResponse(data.response);
    setLoading(false);
  };

  return (
    <div className="p-4 space-y-4">
      <input
        className="border p-2 w-full"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask the Farcaster agent"
      />
      <button
        className="px-4 py-2 bg-blue-600 text-white"
        onClick={send}
        disabled={loading}
      >
        {loading ? 'Sending...' : 'Send'}
      </button>
      {response && <p className="whitespace-pre-wrap">{response}</p>}
    </div>
  );
}
