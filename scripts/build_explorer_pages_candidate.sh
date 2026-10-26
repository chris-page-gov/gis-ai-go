#!/usr/bin/env bash
# Build once, then verify and exercise the exact public Explorer candidate.
set -euo pipefail

if [[ "$#" != 1 ]]; then
  echo 'Usage: bash scripts/build_explorer_pages_candidate.sh EXPLORER_CHECKOUT' >&2
  exit 2
fi

publication_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
explorer_checkout="$(cd "$1" && pwd -P)"
cd "$publication_root"

source_commit="$(git rev-parse HEAD)"
if [[ ! "$source_commit" =~ ^[0-9a-f]{40}$ ]] || \
   [[ -n "${GITHUB_SHA:-}" && "$source_commit" != "$GITHUB_SHA" ]]; then
  echo 'The candidate must use the exact checked-out source commit.' >&2
  exit 1
fi
explorer_commit="$(node -p "JSON.parse(require('node:fs').readFileSync('config/explorer-publication.json','utf8')).sourceCommit")"
captured_at="$(node -p "JSON.parse(require('node:fs').readFileSync('config/explorer-publication.json','utf8')).capturedAt")"
context_base="$(node -p "JSON.parse(require('node:fs').readFileSync('config/explorer-publication.json','utf8')).contextPublicationBase")"
if [[ ! "$explorer_commit" =~ ^[0-9a-f]{40}$ ]] || \
   [[ "$(git -C "$explorer_checkout" rev-parse HEAD)" != "$explorer_commit" ]]; then
  echo 'The Explorer checkout does not match the reviewed source pin.' >&2
  exit 1
fi
if [[ ! "$captured_at" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$ ]] || \
   [[ "$context_base" != 'https://chris-page-gov.github.io/gis-ai-go/gis/explorer/context/' ]]; then
  echo 'The reviewed capture scope or canonical context prefix is invalid.' >&2
  exit 1
fi
observed_uv_version="$(uv --version)"
observed_uv_version="${observed_uv_version#uv }"
observed_uv_version="${observed_uv_version%% *}"
if [[ "$observed_uv_version" != '0.12.2' ]]; then
  echo 'The candidate requires the governed uv 0.12.2 toolchain.' >&2
  exit 1
fi

candidate_root="$publication_root/artifacts/explorer-pages-candidate"
if [[ -L "$publication_root/artifacts" ]] || \
   [[ -e "$candidate_root" || -L "$candidate_root" ]] || \
   [[ -e "$publication_root/artifacts/pages" || -L "$publication_root/artifacts/pages" ]]; then
  echo 'Retain earlier candidates and use a clean checkout for a new build.' >&2
  exit 1
fi
mkdir -p "$candidate_root/projection"

# The two repositories retain their own locked package managers and Python roots.
(
  cd "$explorer_checkout/apps/okf-explorer"
  corepack pnpm install --frozen-lockfile
  corepack pnpm check
  corepack pnpm build:determinism
)
(
  cd "$explorer_checkout"
  uv python install
  uv sync --locked
  uv run --locked python scripts/build_site.py
)
pnpm run build:explorer
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/build.py \
  --output "$candidate_root/projection/bundle" --revision "$source_commit"
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/context_projection.py \
  --search-index "$candidate_root/projection/bundle/search-index.json" \
  --bundle "$candidate_root/projection/bundle/okf-bundle.json" \
  --output "$candidate_root/projection/context" \
  --publication-base "$context_base" --captured-at "$captured_at" --all-records
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/explorer_projection.py \
  --search-index "$candidate_root/projection/bundle/search-index.json" \
  --bundle "$candidate_root/projection/bundle/okf-bundle.json" \
  --context-directory "$candidate_root/projection/context" \
  --output "$candidate_root/projection/explorer" --captured-at "$captured_at"

product_version="$(tr -d '\n' < VERSION)"
node scripts/build_explorer_pages.mjs \
  --explorer-checkout "$explorer_checkout" \
  --projection-root "$candidate_root/projection" \
  --legacy-dist "$publication_root/apps/public-explorer/dist" \
  --output "$candidate_root/dist" \
  --source-commit "$source_commit" --version "$product_version"
uv run --locked --cache-dir .uv-cache python scripts/package_explorer_pages.py \
  --dist "$candidate_root/dist" --output-dir artifacts/pages \
  --source-commit "$source_commit" --repository chris-page-gov/gis-ai-go \
  --version "$product_version" --base-path /gis-ai-go/
uv run --locked --cache-dir .uv-cache python scripts/verify_pages_archive.py \
  --archive artifacts/pages/artifact.tar --checksum artifacts/pages/artifact.tar.sha256 \
  --receipt artifacts/pages/archive-receipt.json --expected-source-commit "$source_commit" \
  --expected-repository chris-page-gov/gis-ai-go --expected-version "$product_version" \
  --expected-base-path /gis-ai-go/

archive_sha256="$(node -p "JSON.parse(require('node:fs').readFileSync('artifacts/pages/archive-receipt.json','utf8')).archive.sha256")"
okf_root="$(node -p "JSON.parse(require('node:fs').readFileSync('artifacts/pages/archive-receipt.json','utf8')).okfContentRootSha256")"
payload_root="$(node -p "JSON.parse(require('node:fs').readFileSync('artifacts/pages/archive-receipt.json','utf8')).payloadRootSha256")"
checksums_sha256="$(node -p "JSON.parse(require('node:fs').readFileSync('artifacts/pages/archive-receipt.json','utf8')).publication.checksumsSha256")"
mkdir "$candidate_root/staged"
uv run --locked --cache-dir .uv-cache python scripts/stage_pages_payload.py \
  --archive artifacts/pages/artifact.tar --checksum artifacts/pages/artifact.tar.sha256 \
  --receipt artifacts/pages/archive-receipt.json \
  --output-dir "$candidate_root/staged/gis-ai-go" \
  --expected-source-commit "$source_commit" --expected-repository chris-page-gov/gis-ai-go \
  --expected-version "$product_version" --expected-base-path /gis-ai-go/ \
  --expected-archive-sha256 "$archive_sha256"

# Local transport exercises the canonical-prefix payload without changing its bytes.
# The browser harness labels its explicit canonical-origin mirror as local evidence.
candidate_server_pid=''
cleanup_candidate_server() {
  if [[ -n "$candidate_server_pid" ]]; then
    kill "$candidate_server_pid" 2>/dev/null || true
    wait "$candidate_server_pid" 2>/dev/null || true
  fi
}
trap cleanup_candidate_server EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
uv run --locked --cache-dir .uv-cache python -m http.server 8131 --bind 127.0.0.1 \
  --directory "$candidate_root/staged" > "$candidate_root/server.log" 2>&1 &
candidate_server_pid="$!"
candidate_ready=false
for attempt in {1..50}; do
  if ! kill -0 "$candidate_server_pid" 2>/dev/null; then
    echo 'The bounded candidate server stopped before acceptance.' >&2
    exit 1
  fi
  if curl --fail --silent --max-time 1 \
      http://127.0.0.1:8131/gis-ai-go/publication/manifest.json > /dev/null; then
    candidate_ready=true
    break
  fi
  sleep 0.2
done
if [[ "$candidate_ready" != true ]]; then
  echo 'The bounded candidate server did not become ready.' >&2
  exit 1
fi
CI="${CI:-true}" \
PUBLIC_BASE_URL=http://127.0.0.1:8131/gis-ai-go/ \
EXPECTED_SOURCE_COMMIT="$source_commit" EXPECTED_VERSION="$product_version" \
EXPECTED_ARCHIVE_SHA256="$archive_sha256" EXPECTED_OKF_CONTENT_ROOT="$okf_root" \
EXPECTED_PAYLOAD_ROOT="$payload_root" EXPECTED_PUBLIC_CHECKSUMS_SHA256="$checksums_sha256" \
  pnpm --filter @gis-ai-go/public-explorer run test:explorer-public

# Acceptance reads only the staged archive. Reverify the original before retention.
uv run --locked --cache-dir .uv-cache python scripts/verify_pages_archive.py \
  --archive artifacts/pages/artifact.tar --checksum artifacts/pages/artifact.tar.sha256 \
  --receipt artifacts/pages/archive-receipt.json --expected-source-commit "$source_commit" \
  --expected-repository chris-page-gov/gis-ai-go --expected-version "$product_version" \
  --expected-base-path /gis-ai-go/ --expected-archive-sha256 "$archive_sha256"
