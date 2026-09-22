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
#   bash restart_and_verify.sh PORT START_CMD FILE MARKER [PROBE_PATH]
#
#   PORT       port the server listens on
#   START_CMD  full command to start the server (quoted)
#   FILE       the file you just edited
#   MARKER     a unique string from FILE that must appear in the response
#   PROBE_PATH path to request, default "/"
#
# Invoke with an explicit `bash` prefix: the executable bit does not
# reliably survive skill installation.
#
# Exits non-zero, loudly, if the served page does not contain MARKER.
set -u

PORT="${1:?port}"
START_CMD="${2:?start command}"
FILE="${3:?edited file}"
MARKER="${4:?marker string from the edited file}"
PROBE_PATH="${5:-/}"
URL="http://127.0.0.1:${PORT}${PROBE_PATH}"

# `lsof` is required, and its absence must be loud. Without this guard a
# missing lsof yields empty output, which reads exactly like "port is
# free" - the script would start a second server and then report that it
# never came up, while leaving it running.
command -v lsof >/dev/null 2>&1 || {
  echo "FAIL: lsof is required and was not found on PATH."
  echo "      Install it, or replace the port lookups below with an"
  echo "      equivalent that reports LISTEN-state PIDs only."
  exit 1; }

# LISTEN state only. Measured: with a server on :5299 and one client
# connected, `lsof -ti :5299` returned BOTH pids - the listener and the
# client. Since this skill exists to drive a browser against the test
# server, that client is the browser doing the measuring: an unfiltered
# lookup kills it, and also makes a lingering client socket look like
# "port still held" or "server came up".
listeners() { lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null; }

grep -qF -- "$MARKER" "$FILE" || {
  echo "FAIL: marker is not in $FILE - nothing to verify against"; exit 1; }

for p in $(listeners); do kill "$p" 2>/dev/null; done
for _ in $(seq 1 15); do [ -z "$(listeners)" ] && break; sleep 1; done
for p in $(listeners); do kill -9 "$p" 2>/dev/null; done
sleep 1
[ -n "$(listeners)" ] && { echo "FAIL: port $PORT still has a listener"; exit 1; }

# mktemp, not a fixed /tmp path: a fixed name can follow a pre-existing
# symlink, and concurrent runs would overwrite each other's output.
LOG="$(mktemp -t restart_and_verify.XXXXXX)" || {
  echo "FAIL: could not create a log file - is TMPDIR writable?"; exit 1; }

# setsid so the server survives this shell, and </dev/null so it never
# blocks on stdin.
setsid nohup bash -c "$START_CMD" > "$LOG" 2>&1 < /dev/null &

# Wait for the server to ANSWER, not to answer 2xx. `curl -sf` fails on
# every non-2xx, so a probe path behind an auth gate would spin here for
# the full timeout with no diagnostic. "000" means no response at all.
code=000
for _ in $(seq 1 60); do
  code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "$URL")"
  [ -z "$code" ] && code=000
  [ "$code" != "000" ] && break
  sleep 1
done
[ -z "$(listeners)" ] && {
  echo "FAIL: server did not come up (last HTTP code: $code)"
  tail -5 "$LOG"; exit 1; }
[ "$code" = "000" ] && echo "NOTE: port is listening but $URL never answered."

if curl -s -L --max-time 15 "$URL" | grep -qF -- "$MARKER"; then
  echo "OK: served content matches disk"
else
  echo "FAIL: served content does NOT match disk - stale template cache."
  echo "      Any measurement taken now would be invalid."
  echo "      (HTTP code from the readiness probe: $code, log: $LOG)"
  exit 1
fi