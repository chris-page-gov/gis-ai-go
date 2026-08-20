import {
  createServer,
  type IncomingMessage,
  type Server,
  type ServerResponse,
} from "node:http";

import type { CatalogueSnapshot } from "./catalogue-snapshot.js";
import { createGatewayHttpHandler } from "./http-app.js";

const MAX_URL_LENGTH = 4_096;

function writeResponse(response: ServerResponse, result: Response): Promise<void> {
  response.statusCode = result.status;
  result.headers.forEach((value, name) => response.setHeader(name, value));
  return result.arrayBuffer().then((body) => {
    response.setHeader("content-length", body.byteLength);
    response.end(Buffer.from(body));
  });
}

function requestUrl(request: IncomingMessage): URL | undefined {
  const host = request.headers.host;
  const target = request.url;
  if (
    host === undefined ||
    target === undefined ||
    target.length > MAX_URL_LENGTH ||
    !target.startsWith("/") ||
    target.startsWith("//") ||
    target.includes("\\") ||
    target.includes("#")
  ) {
    return undefined;
  }
  try {
    return new URL(target, `http://${host}`);
  } catch {
    return undefined;
  }
}

function applicationHeaders(request: IncomingMessage): Headers {
  const headers = new Headers();
  for (const name of ["host", "origin", "accept", "x-request-id"] as const) {
    const value = request.headers[name];
    if (typeof value === "string") headers.set(name, value);
  }
  return headers;
}

function headerOccurrences(request: IncomingMessage, expectedName: string): number {
  let count = 0;
  for (let index = 0; index < request.rawHeaders.length; index += 2) {
    if (request.rawHeaders[index]?.toLowerCase() === expectedName) count += 1;
  }
  return count;
}

function rejectRequest(response: ServerResponse): void {
  response.writeHead(400, {
    "cache-control": "no-store",
    "content-length": "0",
    "x-content-type-options": "nosniff",
  });
  response.end();
}

/** Create the bounded Node adapter without binding a network interface. */
export function createGatewayNodeServer(snapshot: CatalogueSnapshot): Server {
  const handle = createGatewayHttpHandler({ snapshot });
  const server = createServer(
    {
      headersTimeout: 5_000,
      keepAliveTimeout: 5_000,
      maxHeaderSize: 16_384,
      rejectNonStandardBodyWrites: true,
      requestTimeout: 5_000,
      requireHostHeader: true,
    },
    (request, response) => {
      const url = requestUrl(request);
      if (
        url === undefined ||
        headerOccurrences(request, "host") !== 1 ||
        request.headers["transfer-encoding"] !== undefined ||
        request.headers["content-length"] !== undefined
      ) {
        rejectRequest(response);
        return;
      }
      const fetchRequest = new Request(url, {
        method: request.method ?? "GET",
        headers: applicationHeaders(request),
      });
      void handle(fetchRequest)
        .then((result) => writeResponse(response, result))
        .catch(() => {
          if (!response.headersSent) {
            response.writeHead(500, {
              "cache-control": "no-store",
              "content-length": "0",
              "x-content-type-options": "nosniff",
            });
          }
          response.end();
        });
    },
  );
  server.maxHeadersCount = 64;
  server.maxRequestsPerSocket = 100;
  server.setTimeout(5_000, (socket) => socket.destroy());
  return server;
}
