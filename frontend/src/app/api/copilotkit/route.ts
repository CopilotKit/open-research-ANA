import {
    CopilotRuntime,
    OpenAIAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    LangGraphAgent,
} from '@copilotkit/runtime';
import OpenAI from 'openai';
import { NextRequest } from 'next/server';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const serviceAdapter = new OpenAIAdapter({ openai });
const deploymentUrl = process.env.DEPLOYMENT === 'local' ? process.env.LOCAL_DEPLOYMENT_URL : process.env.DEPLOYMENT_URL;

// New AG-UI compatible configuration
const runtime = new CopilotRuntime({
    agents: {
        'agent': new LangGraphAgent({
            deploymentUrl: deploymentUrl!,
            langsmithApiKey: process.env.LANGSMITH_API_KEY,
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