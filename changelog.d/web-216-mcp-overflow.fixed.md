- Cancel both Fetch body branches on overflow without waiting for a stalled
  producer, so the existing MCP wrapper returns its bounded `413` response.
