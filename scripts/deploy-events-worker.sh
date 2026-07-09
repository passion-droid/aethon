#!/usr/bin/env bash
# Deploy the AETHON events worker (scripts/cf-worker-events.js) via the Cloudflare API.
# Idempotent: creates the KV namespace, uploads the worker with the binding, upserts the
# route aethon.house/e* — safe to re-run. Needs env: CLOUDFLARE_API_TOKEN, CF_ACCOUNT_TAG.
# Token permissions used: Workers KV Storage:Edit, Workers Scripts:Edit, Zone:Read,
# Workers Routes:Edit (zone aethon.house). Each step names the permission it needs on failure.
set -euo pipefail

API="https://api.cloudflare.com/client/v4"
ACCT="${CF_ACCOUNT_TAG:?CF_ACCOUNT_TAG not set}"
: "${CLOUDFLARE_API_TOKEN:?CLOUDFLARE_API_TOKEN not set}"
AUTH=(-H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}")
ZONE_NAME="aethon.house"
SCRIPT_NAME="aethon-events"
NS_TITLE="aethon_events"
WORKER_FILE="scripts/cf-worker-events.js"

say() { echo "== $*"; }
fail() { echo "!! $*" >&2; exit 1; }

# ---- 1 · KV namespace: find or create -------------------------------------------------
say "KV namespace '${NS_TITLE}'"
NS_LIST=$(curl -sS "${AUTH[@]}" "${API}/accounts/${ACCT}/storage/kv/namespaces?per_page=100")
echo "${NS_LIST}" | jq -e '.success' >/dev/null || fail "cannot list KV namespaces (need: Workers KV Storage:Read/Edit) — $(echo "${NS_LIST}" | jq -c '.errors')"
NS_ID=$(echo "${NS_LIST}" | jq -r --arg t "${NS_TITLE}" '.result[] | select(.title==$t) | .id' | head -1)
if [ -z "${NS_ID}" ]; then
  CREATED=$(curl -sS -X POST "${AUTH[@]}" -H 'Content-Type: application/json' \
    -d "{\"title\":\"${NS_TITLE}\"}" "${API}/accounts/${ACCT}/storage/kv/namespaces")
  echo "${CREATED}" | jq -e '.success' >/dev/null || fail "cannot create KV namespace (need: Workers KV Storage:Edit) — $(echo "${CREATED}" | jq -c '.errors')"
  NS_ID=$(echo "${CREATED}" | jq -r '.result.id')
  say "created namespace ${NS_ID}"
else
  say "found namespace ${NS_ID}"
fi

# ---- 2 · upload the worker with the KV binding ----------------------------------------
# NB: the Workers API resolves modules by the multipart part's FILENAME, not the field
# name — without ;filename=worker.js the upload fails with 10021 'No such module'.
say "upload worker '${SCRIPT_NAME}'"
METADATA=$(jq -nc --arg ns "${NS_ID}" '{
  main_module: "worker.js",
  compatibility_date: "2026-01-01",
  bindings: [ { type: "kv_namespace", name: "EVENTS", namespace_id: $ns } ]
}')
UPLOAD=$(curl -sS -X PUT "${AUTH[@]}" \
  -F "metadata=${METADATA};type=application/json" \
  -F "worker.js=@${WORKER_FILE};type=application/javascript+module;filename=worker.js" \
  "${API}/accounts/${ACCT}/workers/scripts/${SCRIPT_NAME}")
echo "${UPLOAD}" | jq -e '.success' >/dev/null || fail "worker upload failed (need: Workers Scripts:Edit) — $(echo "${UPLOAD}" | jq -c '.errors')"
say "worker uploaded"

# ---- 3 · zone id -----------------------------------------------------------------------
say "zone lookup ${ZONE_NAME}"
ZONES=$(curl -sS "${AUTH[@]}" "${API}/zones?name=${ZONE_NAME}")
echo "${ZONES}" | jq -e '.success' >/dev/null || fail "cannot read zones (need: Zone:Read) — $(echo "${ZONES}" | jq -c '.errors')"
ZONE_ID=$(echo "${ZONES}" | jq -r '.result[0].id // empty')
[ -n "${ZONE_ID}" ] || fail "zone ${ZONE_NAME} not visible to this token (need: Zone:Read on the zone)"
say "zone ${ZONE_ID}"

# ---- 4 · route upsert: aethon.house/e* -> worker ---------------------------------------
say "route ${ZONE_NAME}/e*"
ROUTES=$(curl -sS "${AUTH[@]}" "${API}/zones/${ZONE_ID}/workers/routes")
echo "${ROUTES}" | jq -e '.success' >/dev/null || fail "cannot list worker routes (need: Workers Routes:Edit) — $(echo "${ROUTES}" | jq -c '.errors')"
ROUTE_ID=$(echo "${ROUTES}" | jq -r --arg p "${ZONE_NAME}/e*" '.result[] | select(.pattern==$p) | .id' | head -1)
BODY=$(jq -nc --arg p "${ZONE_NAME}/e*" --arg s "${SCRIPT_NAME}" '{pattern:$p, script:$s}')
if [ -z "${ROUTE_ID}" ]; then
  R=$(curl -sS -X POST "${AUTH[@]}" -H 'Content-Type: application/json' -d "${BODY}" "${API}/zones/${ZONE_ID}/workers/routes")
else
  R=$(curl -sS -X PUT  "${AUTH[@]}" -H 'Content-Type: application/json' -d "${BODY}" "${API}/zones/${ZONE_ID}/workers/routes/${ROUTE_ID}")
fi
echo "${R}" | jq -e '.success' >/dev/null || fail "route upsert failed (need: Workers Routes:Edit) — $(echo "${R}" | jq -c '.errors')"
say "route active"

# ---- 5 · verify ------------------------------------------------------------------------
say "verify: beacon through the live route"
CODE=$(curl -sS -o /dev/null -w '%{http_code}' "https://${ZONE_NAME}/e?n=afterglow" -H 'User-Agent: Mozilla/5.0 (deploy-verify)') || CODE="curl-error"
echo "   live /e?n=afterglow -> HTTP ${CODE} (204 = counted; 403 would be bot protection challenging curl — real browsers pass)"
TODAY=$(date -u +%F)
VAL=$(curl -sS "${AUTH[@]}" "${API}/accounts/${ACCT}/storage/kv/namespaces/${NS_ID}/values/afterglow:${TODAY}" || true)
echo "   KV afterglow:${TODAY} = ${VAL:-<empty>}"
say "done — namespace ${NS_ID}, script ${SCRIPT_NAME}, route ${ZONE_NAME}/e*"
