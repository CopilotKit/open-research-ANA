import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.FARCASTER_BACKEND_URL || 'http://localhost:8000/farcaster';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const res = await fetch(BACKEND_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data);
}
