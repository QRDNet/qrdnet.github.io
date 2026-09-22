import sys, json, uuid, datetime, base64
from cryptography.hazmat.primitives.asymmetric import ed25519

def issue_badge(user_name, user_email, cert_type, qrdnet_id, private_key_b64):
    priv_bytes = base64.b64decode(private_key_b64)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
    
    issued_date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    credential = {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.1.json"
        ],
        "id": f"urn:uuid:{uuid.uuid4()}",
        "type": ["VerifiableCredential", "OpenBadgeCredential"],
        "issuer": {
            "id": "https://qrdnet.github.io/registry/issuer.json",
            "type": "Profile",
            "name": "QRDNet Network"
        },
        "issuanceDate": issued_date,
        "credentialSubject": {
            "id": f"mailto:{user_email}",
            "type": "AchievementSubject",
            "name": user_name,
            "qrdnetId": qrdnet_id,
            "achievement": f"https://qrdnet.github.io/achievements/{cert_type}.json"
        }
    }
    
    # Create a digital signature for the data
    data_to_sign = json.dumps(credential, sort_keys=True).encode('utf-8')
    signature = private_key.sign(data_to_sign)
    
    credential["proof"] = {
        "type": "Ed25519Signature2020",
        "created": issued_date,
        "verificationMethod": "https://qrdnet.github.io/keys/public_key.json",
        "proofPurpose": "assertionMethod",
        "proofValue": base64.b64encode(signature).decode('utf-8')
    }
    
    output_filename = f"registry/credentials/{qrdnet_id}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(credential, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Parameters: Name, Email, Type, QRDNet ID, Private Key
    issue_badge(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])