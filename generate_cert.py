from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from datetime import datetime, timedelta
from uuid import uuid4
from os.path import isfile
import os
import subprocess
import socket
import sys



print("⚡️ Generating certificate...")

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()
builder = x509.CertificateBuilder().subject_name(x509.Name([
    x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, "DZ"),
    x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, "ORAN"),
    x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, "ORAN"),
    x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, "GalaxyOne"),
    x509.NameAttribute(x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME, "G1"),
    x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "GalaxyOne CA"),
    x509.NameAttribute(x509.oid.NameOID.EMAIL_ADDRESS, "info@galaxy.one"),
])).issuer_name(x509.Name([
    x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, "DZ"),
    x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, "ORAN"),
    x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, "ORAN"),
    x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, "GalaxyOne"),
    x509.NameAttribute(x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME, "G1"),
    x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "GalaxyOne CA"),
    x509.NameAttribute(x509.oid.NameOID.EMAIL_ADDRESS, "info@galaxy.one"),
])).not_valid_before(datetime.today() - timedelta(days=1))\
    .not_valid_after(datetime.today() + timedelta(days=365 * 2))\
    .serial_number(int(uuid4()))\
    .public_key(public_key)\
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)

certificate = builder.sign(
    private_key=private_key,
    algorithm=hashes.SHA256(),
    backend=default_backend()
)

print("⚡️ Writing fah_server_private_key.der...")
with open("fah_server_private_key.der", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

print("⚡️ Writing cacert.der...")
with open("cacert.der", "wb") as f:
    f.write(certificate.public_bytes(
        encoding=serialization.Encoding.DER
    ))

result = subprocess.run(
    ["openssl rsa -inform der -in fah_server_private_key.der -outform pem -out cacertKey.pem"], 
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = subprocess.run(
    ["openssl x509 -inform der -in cacert.der -signkey cacertKey.pem -days 730 -outform der -out fah_ca.der"],
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
result = subprocess.run(
    ["openssl x509 -inform der -in cacert.der -signkey cacertKey.pem -days 730 -outform pem -out cacert.pem"],
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
os.remove('cacertKey.pem')
os.remove('cacert.der')
os.rename('cacert.pem', '35aa2e12.0')
print("⚡️ Next step: copy 35aa2e12.0 to /etc/security/cacerts/")
