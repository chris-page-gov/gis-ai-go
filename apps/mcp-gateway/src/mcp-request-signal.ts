import { AsyncLocalStorage } from "node:async_hooks";

const MCP_HTTP_DATA_QUERY_SIGNAL = new AsyncLocalStorage<AbortSignal>();

export interface DataQueryRequestSignal {
  readonly signal: AbortSignal;
  /** Remove combination listeners when the application has settled. */
  readonly close: () => void;
}

/**
 * Preserve the caller-controlled HTTP signal for one data.query dispatch while
 * the pinned SDK owns an independent response lifecycle.
 */
export function withMcpHttpDataQuerySignal<T>(
  signal: AbortSignal,
  dispatch: () => Promise<T>,
): Promise<T> {
  return MCP_HTTP_DATA_QUERY_SIGNAL.run(signal, dispatch);
}

/**
 * Combine the original HTTP caller signal with SDK/JSON-RPC cancellation.
 * STDIO has no HTTP store and therefore retains the raw SDK signal.
 */
export function dataQueryRequestSignal(
  sdkSignal: AbortSignal,
): DataQueryRequestSignal {
  const httpSignal = MCP_HTTP_DATA_QUERY_SIGNAL.getStore();
  if (httpSignal === undefined || httpSignal === sdkSignal) {
    return Object.freeze({ signal: sdkSignal, close: () => undefined });
  }

  const controller = new AbortController();
  let closed = false;
  const close = (): void => {
    if (closed) return;
    closed = true;
    httpSignal.removeEventListener("abort", onHttpAbort);
    sdkSignal.removeEventListener("abort", onSdkAbort);
  };
  const abortFrom = (source: AbortSignal): void => {
    if (!controller.signal.aborted) controller.abort(source.reason);
    close();
  };
  const onHttpAbort = (): void => abortFrom(httpSignal);
  const onSdkAbort = (): void => abortFrom(sdkSignal);
  httpSignal.addEventListener("abort", onHttpAbort, { once: true });
  sdkSignal.addEventListener("abort", onSdkAbort, { once: true });
  if (httpSignal.aborted) abortFrom(httpSignal);
  else if (sdkSignal.aborted) abortFrom(sdkSignal);
  return Object.freeze({ signal: controller.signal, close });
}
