import { env, waitUntil } from 'cloudflare:workers';
import { dispatchSitesPilot } from '../../../server/sites-pilot-runtime.mjs';

export const dynamic = 'force-dynamic';

// Identity, origin, methods and request bounds belong to the reviewed runtime.
export function POST(request: Request) { return dispatchSitesPilot(request, env, waitUntil); }
export function GET(request: Request) { return dispatchSitesPilot(request, env, waitUntil); }
export function DELETE(request: Request) { return dispatchSitesPilot(request, env, waitUntil); }
