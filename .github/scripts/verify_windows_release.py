"""Read-only Windows release acceptance; prints only bounded, non-player results."""
import hashlib
import http.client
import json
import os
from pathlib import Path
import platform
import queue
import re
import subprocess
import sys
import threading
import time

REGIONS = ('global-hmt', 'global-en', 'global-kr')
EXPECTED_SHA256 = '75fbb5eec1ac9adc752c7738acb01e97e6d654e109903b82f05025c05e2c70a0'


def require(value, code):
    if not value:
        raise RuntimeError(code)


def main():
    proc = None
    credentials = {}
    results = []
    phase = 'preflight'
    try:
        root = Path(sys.argv[1]).resolve()
        archive = Path(sys.argv[2]).resolve()
        require(sys.platform == 'win32', 'native_windows_required')
        require(hashlib.sha256(archive.read_bytes()).hexdigest() == EXPECTED_SHA256, 'archive_digest_mismatch')
        require((root / 'sdk.bhk.xml').is_file() and not (root / 'sdk.xml').exists(), 'bundled_sdk_required')
        require((root / 'Start.cmd').is_file() and (root / 'runtime/python.exe').is_file(), 'portable_launcher_required')
        credentials = json.loads(os.environ.pop('GROWTH_WINDOWS_PROBE_JSON'))
        require(set(credentials) == {'account', 'password'}, 'invalid_probe_credentials')
        require(all(isinstance(v, str) and v for v in credentials.values()), 'invalid_probe_credentials')
        for value in credentials.values():
            # GitHub runner consumes this control command and masks subsequent output.
            escaped = value.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
            print('::add-mask::' + escaped, flush=True)
        phase = 'launch'
        # Exercise the shipped command launcher unchanged. Suppress only desktop browser opening.
        env = {**os.environ, 'BROWSER': 'cmd.exe /c exit 0 %s'}
        proc = subprocess.Popen(['cmd.exe', '/d', '/c', 'Start.cmd'], cwd=root, env=env,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True)
        ready_lines = queue.Queue()
        threading.Thread(target=lambda: [ready_lines.put(line) for line in proc.stdout], daemon=True).start()
        deadline = time.monotonic() + 30
        origin = None
        while time.monotonic() < deadline:
            try:
                line = ready_lines.get(timeout=1).strip()
            except queue.Empty:
                require(proc.poll() is None, 'launcher_exited')
                continue
            if re.fullmatch(r'Local login ready: http://127\.0\.0\.1:\d+', line):
                origin = line.removeprefix('Local login ready: ')
                break
        require(origin is not None, 'launcher_timeout')

        def request(method, path, body=None, nonce=None):
            connection = http.client.HTTPConnection(origin.removeprefix('http://'), timeout=12)
            headers = {}
            if body is not None:
                headers = {'Origin': origin, 'Content-Type': 'application/json', 'X-Local-Nonce': nonce}
            try:
                connection.request(method, path, json.dumps(body) if body is not None else None, headers)
                response = connection.getresponse()
                return response.status, response.read(), dict(response.getheaders())
            finally:
                connection.close()

        phase = 'bundled_configuration'
        code, page, headers = request('GET', '/')
        require(code == 200 and all(region.encode() in page for region in REGIONS), 'three_region_page_missing')
        nonce = re.search(r"'nonce-([^']+)'", headers['Content-Security-Policy']).group(1)
        code, data, _ = request('GET', '/status')
        require(code == 200 and json.loads(data)['sdkConfigured'] is True, 'sdk_not_auto_loaded')
        # Deliberately never call /configure and never pass --sdk-resources.
        print(json.dumps({'nativeWindows': True, 'windowsVersion': platform.version(),
                          'launcher': 'Start.cmd', 'bundledSdkAutoLoaded': True,
                          'manualConfigurationUsed': False, 'archiveSha256': EXPECTED_SHA256}), flush=True)
        for region in REGIONS:
            phase = region
            code, _, _ = request('POST', '/export', {**credentials, 'serverId': region}, nonce)
            require(code == 202, 'export_request_rejected')
            deadline = time.monotonic() + 75
            while time.monotonic() < deadline:
                code, data, _ = request('GET', '/status')
                require(code == 200, 'status_unavailable')
                state = json.loads(data)
                if state['stage'] in ('complete', 'failed'):
                    break
                time.sleep(.5)
            else:
                raise RuntimeError('read_timeout')
            if state['stage'] != 'complete':
                # Never print remote messages, account identifiers, or arbitrary exception text.
                known_reasons = ('credentials_rejected', 'rate_limited', 'verification_required',
                                 'account_not_found', 'no_role_for_server', 'maintenance')
                reason = state.get('reason')
                print(json.dumps({'serverId': region, 'result': 'failed',
                                  'reason': reason if reason in known_reasons else 'read_failed'}), flush=True)
                raise RuntimeError('region_read_failed')
            code, data, headers = request('GET', '/download')
            require(code == 200 and headers['Content-Type'].startswith('application/json'), 'download_failed')
            snapshot = json.loads(data)
            require(snapshot['format'] == 'ournotes-growth-snapshot', 'invalid_snapshot_format')
            require(snapshot['source']['serverId'] == region, 'wrong_region_export')
            version = snapshot['source']['clientVersion']
            require(isinstance(version, str) and re.fullmatch(r'\d+\.\d+\.\d+', version), 'invalid_client_version')
            require(all(k in snapshot['growth'] for k in ('memberCards', 'supportCards', 'bandItems', 'characterRanks', 'tgw')), 'missing_growth_fields')
            require(all(value.encode() not in data for value in credentials.values()), 'credentials_in_export')
            require(snapshot['growth']['memberCards'] and snapshot['growth']['supportCards'], 'empty_probe_export')
            result = {'serverId': region, 'result': 'passed', 'clientVersion': version,
                      'readComplete': True, 'jsonDownloadValid': True, 'correctRegion': True,
                      'credentialsAbsent': True}
            results.append(result)
            print(json.dumps(result), flush=True)
            del snapshot, data, state
        require(len(results) == 3, 'incomplete_regions')
        print(json.dumps({'windowsThreeRegionAcceptance': 'passed', 'snapshotsPersisted': False}), flush=True)
        return 0
    except Exception:
        print(json.dumps({'windowsThreeRegionAcceptance': 'failed', 'phase': phase,
                          'snapshotsPersisted': False}), flush=True)
        return 1
    finally:
        credentials.clear()
        if proc is not None:
            subprocess.run(['taskkill.exe', '/F', '/T', '/PID', str(proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == '__main__':
    raise SystemExit(main())
