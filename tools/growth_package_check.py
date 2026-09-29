"""Offline distribution smoke check; never logs in or contacts game servers."""
import http.client
import json
import threading


def main():
    import grpc
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
    from tools.growth_login_local import LoginServer
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    cipher = key.public_key().encrypt(b'OFFLINE-CHECK', padding.PKCS1v15())
    assert key.decrypt(cipher, padding.PKCS1v15()) == b'OFFLINE-CHECK'
    channel = grpc.secure_channel('127.0.0.1:1', grpc.ssl_channel_credentials())
    channel.close()  # Creating a channel without RPCs does not connect.
    server = LoginServer()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        connection = http.client.HTTPConnection(server.authority, timeout=3)
        connection.request('GET', '/status')
        response = connection.getresponse()
        state = json.loads(response.read())
        assert response.status == 200 and state['sdkConfigured'] is False
        connection.close()
        connection = http.client.HTTPConnection(server.authority, timeout=3)
        connection.request('GET', '/', headers={'Host': 'invalid.example'})
        response = connection.getresponse()
        assert response.status == 403
        response.read()
        connection.close()
        print(json.dumps({'offlineSelfTest': 'passed', 'rsa': True, 'grpcNativeImport': True,
                          'loopback': True, 'wrongHostRefused': True,
                          'realAccountUsed': False}))
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
