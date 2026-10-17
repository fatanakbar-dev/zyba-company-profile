#!/usr/bin/env python3
"""Deploy zyba-demo worker (akun Cloudflare kedua) via Cloudflare API.

Reads the credential through the secure surrogate helper — never handles the raw key.
Deploys ~/workspace/zyba-worker/src/worker.js (single module, no bindings).
"""
import json
import os
import sys
import urllib.request

for _p in ("/opt/hatch/workflow-skills/custom-connector-setup/bin",
           "/opt/muse/skills/custom-connector-setup/templates/skill/bin"):
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
        break
from dynamic_credentials import add_surrogate_to_request, read_json_response

BASE = "https://api.cloudflare.com/client/v4"
ACCOUNT = "4b0e4354ed20d4fdc8773f73a0438b8a"
SCRIPT = "zyba-demo"
WORKER_JS = "/home/hatch/workspace/zyba-worker/src/worker.js"

with open(WORKER_JS, "rb") as f:
    script_bytes = f.read()

metadata = {
    "main_module": "worker.js",
    "compatibility_date": "2026-01-01",
}

boundary = "----zybadeploy1234"
parts = []
parts.append(
    f"--{boundary}\r\nContent-Disposition: form-data; "
    f'name="metadata"\r\nContent-Type: application/json\r\n\r\n'
    f"{json.dumps(metadata)}\r\n".encode())
parts.append(
    f"--{boundary}\r\nContent-Disposition: form-data; "
    f'name="worker.js"; filename="worker.js"\r\n'
    f"Content-Type: application/javascript+module\r\n\r\n".encode()
    + script_bytes + b"\r\n")
parts.append(f"--{boundary}--\r\n".encode())
body = b"".join(parts)

req = urllib.request.Request(
    f"{BASE}/accounts/{ACCOUNT}/workers/scripts/{SCRIPT}",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="PUT",
)
add_surrogate_to_request(req, "custom.cloudflare-ahliwebmurah",
                         allowed_hosts=["api.cloudflare.com"])
with urllib.request.urlopen(req, timeout=120) as resp:
    payload = read_json_response(resp)

result = payload.get("result") or {}
print(json.dumps({"success": payload.get("success"),
                  "errors": payload.get("errors"),
                  "script_id": result.get("id")}, indent=2))
if not payload.get("success"):
    sys.exit(1)
print("DEPLOYED OK")
