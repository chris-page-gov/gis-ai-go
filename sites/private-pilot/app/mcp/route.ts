import { env, waitUntil } from 'cloudflare:workers';
import { dispatchSitesNativeMcp } from '../../server/sites-pilot-runtime.mjs';

export const dynamic = 'force-dynamic';

// This exact mount shares the reviewed provider, allowance and receipt contract.
// Identity is supplied by Sites; no test token is admitted on the native route.
export function POST(request: Request) { return dispatchSitesNativeMcp(request, env, waitUntil); }
export function GET(request: Request) { return dispatchSitesNativeMcp(request, env, waitUntil); }
export function DELETE(request: Request) { return dispatchSitesNativeMcp(request, env, waitUntil); }
