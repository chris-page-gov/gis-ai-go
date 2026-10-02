import { createSitesPilotCapacity, createSitesPilotHttpHandler, createSitesPilotStore } from './vendor/sites-pilot/sites-pilot-runtime.mjs';
import manifest from './vendor/sites-pilot/bundle-manifest.json' with { type: 'json' };

const runtimes = new WeakMap();

function configuration(environment) {
  if (environment === null || typeof environment !== 'object') throw new Error('Pilot unavailable');
  const database = environment.DB;
  const origin = environment.SITES_PILOT_ORIGIN;
  const softwareRevision = environment.SITES_PILOT_SOURCE_REVISION;
  const osApiKey = environment.OS_NAMES_API_KEY;
  const testTokenSha256 = environment.SITES_PILOT_TEST_TOKEN_SHA256;
  if (database === null || typeof database !== 'object' || typeof database.prepare !== 'function' ||
      typeof origin !== 'string' || typeof softwareRevision !== 'string' || !/^[0-9a-f]{40}$/.test(softwareRevision) ||
      softwareRevision !== manifest.source_revision || manifest.schema !== 'gis-ai-go.sites-pilot-package.v1' ||
      (osApiKey !== undefined && (typeof osApiKey !== 'string' || !/^[A-Za-z0-9_-]{8,256}$/.test(osApiKey))) ||
      (testTokenSha256 !== undefined && (typeof testTokenSha256 !== 'string' || !/^[0-9a-f]{64}$/.test(testTokenSha256)))) {
    throw new Error('Pilot unavailable');
  }
  const parsed = new URL(origin);
  if (parsed.protocol !== 'https:' || parsed.origin !== origin || parsed.port !== '' ||
      parsed.username !== '' || parsed.password !== '' || parsed.hostname !== parsed.hostname.toLowerCase()) {
    throw new Error('Pilot unavailable');
  }
  return { database, origin, softwareRevision, osApiKey, testTokenSha256 };
}

/** Uses trusted worker bindings only; normal requests never initialise or reset storage. */
async function dispatch(request, environment, waitUntil, path) {
  try {
    if (typeof waitUntil !== 'function') throw new Error('Pilot unavailable');
    const config = configuration(environment);
    const existing = runtimes.get(config.database);
    if (existing && ['origin', 'softwareRevision', 'osApiKey', 'testTokenSha256'].some((name) => existing.config[name] !== config[name])) {
      // Rotating runtime configuration requires a fresh deployment/isolate, not a silent in-place switch.
      throw new Error('Pilot unavailable');
    }
    let entry = existing;
    if (!entry) {
      entry = { config, store: createSitesPilotStore(config.database), capacity: createSitesPilotCapacity(), handlers: new Map() };
      runtimes.set(config.database, entry);
    }
    let handler = entry.handlers.get(path);
    if (!handler) {
      handler = createSitesPilotHttpHandler({
        origin: config.origin, path, softwareRevision: config.softwareRevision,
        store: entry.store, capacity: entry.capacity, fetch: globalThis.fetch.bind(globalThis),
        // cloudflare:workers resolves the current request context when called.
        // Never capture a previous request's ExecutionContext in this shared handler.
        waitUntil,
        ...(config.osApiKey === undefined ? {} : { osApiKey: config.osApiKey }),
        // Native MCP must use Sites' authenticated identity. The historical
        // application test token remains confined to the ordinary pilot route.
        ...(path !== '/pilot/mcp' || config.testTokenSha256 === undefined ? {} : { testTokenSha256: config.testTokenSha256 }),
      });
      entry.handlers.set(path, handler);
    }
    return await handler.fetch(request);
  } catch {
    return Response.json({ error: 'pilot-unavailable' }, { status: 503,
      headers: { 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' } });
  }
}

/** The path is authored here, never inferred from a caller or rewritten. */
export function dispatchSitesPilot(request, environment, waitUntil) {
  return dispatch(request, environment, waitUntil, '/pilot/mcp');
}

/** Native Sites OAuth supplies the trusted identity at the hosting boundary. */
export function dispatchSitesNativeMcp(request, environment, waitUntil) {
  return dispatch(request, environment, waitUntil, '/mcp');
}
