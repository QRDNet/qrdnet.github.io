import base64
from cryptography.hazmat.primitives.asymmetric import ed25519

private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

print("PRIVATE KEY (Secret):", base64.b64encode(private_key.private_bytes_raw()).decode())
print("PUBLIC KEY:", base64.b64encode(public_key.public_bytes_raw()).decode())