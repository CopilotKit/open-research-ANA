import {
    CopilotRuntime,
    OpenAIAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    LangGraphAgent,
} from '@copilotkit/runtime';
import OpenAI from 'openai';
import { NextRequest } from 'next/server';

// Validate required environment variables
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const LANGSMITH_API_KEY = process.env.LANGSMITH_API_KEY;
const DEPLOYMENT = process.env.DEPLOYMENT;
const LOCAL_DEPLOYMENT_URL = process.env.LOCAL_DEPLOYMENT_URL;
const DEPLOYMENT_URL = process.env.DEPLOYMENT_URL;

if (!OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY environment variable is required');
}

if (!LANGSMITH_API_KEY) {
    throw new Error('LANGSMITH_API_KEY environment variable is required');
}

// Validate and sanitize deployment URL
const deploymentUrl = DEPLOYMENT === 'local' ? LOCAL_DEPLOYMENT_URL : DEPLOYMENT_URL;

if (!deploymentUrl) {
    throw new Error('Deployment URL is not configured. Set LOCAL_DEPLOYMENT_URL or DEPLOYMENT_URL');
}

// Allowlist valid deployment URL patterns to prevent SSRF
const isValidUrl = (url: string): boolean => {
    try {
        const parsed = new URL(url);
        // Only allow http/https protocols
        if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
            return false;
        }
        // For local development, allow localhost and 127.0.0.1
        if (DEPLOYMENT === 'local') {
            return parsed.hostname === 'localhost' || parsed.hostname === '127.0.0.1';
        }
        // For production, only allow trusted domains
        // Add your trusted domain patterns here
        return true; // In production, implement strict domain validation
    } catch {
        return false;
    }
};

if (!isValidUrl(deploymentUrl)) {
    throw new Error('Invalid deployment URL. Must be a valid http/https URL');
}

const openai = new OpenAI({ apiKey: OPENAI_API_KEY });
const serviceAdapter = new OpenAIAdapter({ openai });

// New AG-UI compatible configuration
const runtime = new CopilotRuntime({
    agents: {
        'agent': new LangGraphAgent({
            deploymentUrl: deploymentUrl,
            langsmithApiKey: LANGSMITH_API_KEY,
            graphId: 'agent', // Must match the graphId in agent/langgraph.json
        }),
    }
});

export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
        runtime,
        serviceAdapter,
        endpoint: '/api/copilotkit',
    });

    return handleRequest(req);
};