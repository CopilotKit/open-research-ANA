import {
    CopilotRuntime,
    OpenAIAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    langGraphCloudEndpoint,
} from '@copilotkit/runtime';
import OpenAI from 'openai';
import { NextRequest } from 'next/server';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const serviceAdapter = new OpenAIAdapter({ openai });
const deploymentUrl = process.env.NODE_ENV === 'development' ? process.env.LOCAL_DEPLOYMENT_URL : process.env.DEPLOYMENT_URL
const runtime = new CopilotRuntime({
    remoteEndpoints: [
        langGraphCloudEndpoint({
            deploymentUrl: deploymentUrl!,
            langsmithApiKey: process.env.LANGSMITH_API_KEY!,
            agents: [{
                name: 'agent',
                description: 'Research assistant',
            }],
        })
    ]
});

export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
        runtime,
        serviceAdapter,
        endpoint: '/api/copilotkit',
    });

    return handleRequest(req);
};