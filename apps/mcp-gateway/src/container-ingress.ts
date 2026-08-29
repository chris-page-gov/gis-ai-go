import {
  DEFAULT_ALLOWED_HOSTS,
  DEFAULT_ALLOWED_ORIGINS,
} from "./http-app.js";
import {
  DEFAULT_MCP_ALLOWED_HOSTS,
  DEFAULT_MCP_ALLOWED_HOSTNAMES,
  DEFAULT_MCP_ALLOWED_ORIGINS,
  type GovernedCandidateNodeServerOptions,
} from "./http-server.js";
import { parsePublicHttpsOrigin } from "./public-origin.js";

export const GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE =
  "GIS_AI_GO_PUBLIC_HTTPS_ORIGIN" as const;

export type GatewayContainerIngressOptions = Pick<
  GovernedCandidateNodeServerOptions,
  | "directAllowedHosts"
  | "directAllowedOrigins"
  | "mcpAllowedHosts"
  | "mcpAllowedHostnames"
  | "mcpAllowedOrigins"
  | "openApiServerOrigin"
>;

/**
 * Select either the fixed loopback boundary or one canonical public HTTPS origin.
 *
 * TLS remains an independently verified ingress responsibility. Forwarded headers
 * are not consulted here or by the gateway, so they cannot widen this allowlist.
 */
export function gatewayContainerIngressOptions(
  environment: Readonly<Record<string, string | undefined>>,
): GatewayContainerIngressOptions {
  const rawOrigin = environment[GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE];
  if (rawOrigin === undefined) {
    return Object.freeze({
      directAllowedHosts: DEFAULT_ALLOWED_HOSTS,
      directAllowedOrigins: DEFAULT_ALLOWED_ORIGINS,
      mcpAllowedHosts: DEFAULT_MCP_ALLOWED_HOSTS,
      mcpAllowedHostnames: DEFAULT_MCP_ALLOWED_HOSTNAMES,
      mcpAllowedOrigins: DEFAULT_MCP_ALLOWED_ORIGINS,
    });
  }
  const publicOrigin = parsePublicHttpsOrigin(rawOrigin);
  return Object.freeze({
    directAllowedHosts: Object.freeze([
      publicOrigin.hostname,
      `${publicOrigin.hostname}:443`,
    ]),
    directAllowedOrigins: Object.freeze([publicOrigin.origin]),
    mcpAllowedHosts: Object.freeze([
      publicOrigin.hostname,
      `${publicOrigin.hostname}:443`,
    ]),
    mcpAllowedHostnames: Object.freeze([publicOrigin.hostname]),
    mcpAllowedOrigins: Object.freeze([publicOrigin.origin]),
    openApiServerOrigin: publicOrigin.origin,
  });
}

/** Use the same admitted authority for the image's internal health request. */
export function gatewayContainerHealthHeaders(
  environment: Readonly<Record<string, string | undefined>>,
): Readonly<Record<string, string>> {
  const rawOrigin = environment[GATEWAY_CONTAINER_PUBLIC_HTTPS_ORIGIN_VARIABLE];
  if (rawOrigin === undefined) return Object.freeze({ accept: "application/json" });
  const publicOrigin = parsePublicHttpsOrigin(rawOrigin);
  return Object.freeze({
    accept: "application/json",
    host: publicOrigin.hostname,
  });
}
