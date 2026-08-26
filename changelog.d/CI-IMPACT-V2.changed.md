- Upgrade the fail-closed CI impact planner to a shadow-only v2 contract with an
  explicit repository root, a canonical Boolean gateway-image decision and a
  workflow output that defaults to full image assurance on missing or malformed
  candidate result; bind routing coverage to every tracked repository path and every
  tracked gateway build-context input while retaining full assurance for unknown,
  empty, global and protected-main changes. Every existing assurance job still runs.
