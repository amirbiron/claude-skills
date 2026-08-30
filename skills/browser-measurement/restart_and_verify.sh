#!/usr/bin/env bash
# Restart a local test server and PROVE it serves what is on disk.
#
# Why this exists: a dev server that keeps serving stale code returns
# measurements that look perfectly fine and mean nothing. Three failure
# modes, all observed:
#   1. Flask caches templates when debug=False, so editing a template
#      while the server is live never reaches the browser.
#   2. The new server dies silently on "Address already in use" and the
#      old one keeps serving. The only visible output is "[1]+ Done".
#   3. `ss -ltnp` does not always expose the PID mapping, so a kill based
#      on it finds nothing and silently does nothing.
#
# Usage:
#   restart_and_verify.sh PORT START_CMD FILE MARKER [PROBE_PATH]
#
#   PORT       port the server listens on
#   START_CMD  full command to start the server (quoted)
#   FILE       the file you just edited
#   MARKER     a unique string from FILE that must appear in the response
#   PROBE_PATH path to request, default "/"
#
# Exits non-zero, loudly, if the served page does not contain MARKER.
set -u

PORT="${1:?port}"
START_CMD="${2:?start command}"
FILE="${3:?edited file}"
MARKER="${4:?marker string from the edited file}"
PROBE_PATH="${5:-/}"
URL="http://127.0.0.1:${PORT}${PROBE_PATH}"

grep -qF -- "$MARKER" "$FILE" || {
  echo "FAIL: marker is not in $FILE - nothing to verify against"; exit 1; }

# lsof, not `ss -ltnp`: ss may omit the PID mapping entirely.
for p in $(lsof -ti ":$PORT" 2>/dev/null); do kill "$p" 2>/dev/null; done
for _ in $(seq 1 15); do [ -z "$(lsof -ti ":$PORT" 2>/dev/null)" ] && break; sleep 1; done
for p in $(lsof -ti ":$PORT" 2>/dev/null); do kill -9 "$p" 2>/dev/null; done
sleep 1
[ -n "$(lsof -ti ":$PORT" 2>/dev/null)" ] && { echo "FAIL: port $PORT still held"; exit 1; }

# setsid so the server survives this shell, and </dev/null so it never
# blocks on stdin.
setsid nohup bash -c "$START_CMD" > /tmp/restart_and_verify.log 2>&1 < /dev/null &

for _ in $(seq 1 60); do
  curl -sf -o /dev/null --max-time 3 "$URL" && break
  sleep 1
done
[ -z "$(lsof -ti ":$PORT" 2>/dev/null)" ] && {
  echo "FAIL: server did not come up"; tail -5 /tmp/restart_and_verify.log; exit 1; }

if curl -s -L --max-time 15 "$URL" | grep -qF -- "$MARKER"; then
  echo "OK: served content matches disk"
else
  echo "FAIL: served content does NOT match disk - stale template cache."
  echo "      Any measurement taken now would be invalid."
  exit 1
fi