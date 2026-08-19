export function isRequestFromConfiguredOrigin(requestUrl: string, baseURL: string): boolean {
  return new URL(requestUrl).origin === new URL(baseURL).origin;
}
