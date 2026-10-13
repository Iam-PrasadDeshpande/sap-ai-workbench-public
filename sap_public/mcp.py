"""Minimal read-only MCP client for SAP's two public developer endpoints. Nothing else can be reached.

Enforced here (covered by tests/test_public_isolation.py):
  * only the two fixed https endpoints in contract.ALLOWED_ENDPOINTS - a visitor never supplies a host or URL;
  * no credentials of any kind: this client has no code path that adds an identity header;
  * a tool is callable only if it is allowlisted for that endpoint AND the server advertises readOnlyHint=true;
  * redirects are refused, responses are size-bounded, time is bounded, arguments are size-bounded;
  * everything a server returns is untrusted data: it is parsed, never executed or followed.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request

from .contract import ALLOWED_ENDPOINTS, LIMITS, PROTOCOL_VERSION, USER_AGENT


class McpError(Exception):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise McpError('redirects are not followed')


class PublicMcpClient:
    def __init__(self, endpoint: str, opener=None):
        if endpoint not in ALLOWED_ENDPOINTS:
            raise McpError('endpoint is not on the public allowlist')
        self.endpoint = endpoint
        self.allowed = ALLOWED_ENDPOINTS[endpoint]
        self.opener = opener or urllib.request.build_opener(_NoRedirect())
        self.tools: dict = {}
        self.server_info: dict = {}
        self.session_id = ''
        self._id = 0

    # ---- transport ----------------------------------------------------------------------------------------
    def _post(self, body: dict):
        data = json.dumps(body, separators=(',', ':')).encode()
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
                   'User-Agent': USER_AGENT, 'MCP-Protocol-Version': PROTOCOL_VERSION}
        if self.session_id:
            headers['Mcp-Session-Id'] = self.session_id
        req = urllib.request.Request(self.endpoint, data=data, headers=headers, method='POST')
        started = time.monotonic()
        try:
            with self.opener.open(req, timeout=LIMITS['timeout_seconds']) as r:
                raw = r.read(LIMITS['response_max_bytes'] + 1)
                status, hdrs = r.status, {k.lower(): v for k, v in r.headers.items()}
                if r.geturl() != self.endpoint:
                    raise McpError('unexpected redirect target')
        except urllib.error.HTTPError as exc:
            return exc.code, {}, exc.read(2000), int((time.monotonic() - started) * 1000)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise McpError(f'transport failure: {type(exc).__name__}') from exc
        if len(raw) > LIMITS['response_max_bytes']:
            raise McpError('response exceeds the size limit')
        return status, hdrs, raw, int((time.monotonic() - started) * 1000)

    @staticmethod
    def _parse(raw: bytes, want_id) -> dict:
        text = raw.decode('utf-8', 'replace').strip()
        if not text:
            return {}
        candidates = [text] if text.startswith('{') else []
        candidates += [ln[5:].strip() for ln in text.splitlines() if ln.startswith('data:')]
        for c in candidates:
            try:
                msg = json.loads(c)
            except ValueError:
                continue
            if isinstance(msg, dict) and (want_id is None or msg.get('id') == want_id):
                return msg
        raise McpError('no JSON-RPC response found')

    def _rpc(self, method, params=None):
        self._id += 1
        body = {'jsonrpc': '2.0', 'id': self._id, 'method': method}
        if params is not None:
            body['params'] = params
        status, hdrs, raw, ms = self._post(body)
        if status != 200:
            raise McpError(f'HTTP {status} for {method}')
        if 'mcp-session-id' in hdrs and not self.session_id:
            self.session_id = hdrs['mcp-session-id']
        msg = self._parse(raw, self._id)
        if 'error' in msg:
            raise McpError(f'{method}: server error')
        return msg.get('result', {}), ms, hashlib.sha256(raw).hexdigest()

    # ---- protocol -----------------------------------------------------------------------------------------
    def connect(self) -> dict:
        res, _, _ = self._rpc('initialize', {'protocolVersion': PROTOCOL_VERSION, 'capabilities': {},
                                             'clientInfo': {'name': 'sap-ai-workbench-public', 'version': '0.1'}})
        self.server_info = res.get('serverInfo', {})
        try:
            self._post({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        except McpError:
            pass
        listed, _, _ = self._rpc('tools/list')
        self.tools = {t['name']: t for t in listed.get('tools', []) if isinstance(t, dict) and 'name' in t}
        return {'server': self.server_info, 'callable': sorted(self.callable_tools())}

    def callable_tools(self) -> set:
        return {n for n, t in self.tools.items() if n in self.allowed
                and (t.get('annotations') or {}).get('readOnlyHint') is True}

    def call(self, tool: str, arguments: dict) -> dict:
        if tool not in self.allowed:
            raise McpError('tool is not allowlisted for this endpoint')
        if not self.tools:
            raise McpError('connect() must be called first')
        if tool not in self.callable_tools():
            raise McpError('tool is not advertised as read-only by the server')
        if not isinstance(arguments, dict) or len(json.dumps(arguments).encode()) > LIMITS['argument_max_bytes']:
            raise McpError('arguments must be a small JSON object')
        res, ms, digest = self._rpc('tools/call', {'name': tool, 'arguments': arguments})
        text = '\n'.join(c.get('text', '') for c in res.get('content', []) if isinstance(c, dict))
        return {'tool': tool, 'endpoint': self.endpoint, 'ok': not res.get('isError', False), 'text': text[:20_000],
                'structured': res.get('structuredContent'), 'latency_ms': ms, 'response_sha256': digest}
