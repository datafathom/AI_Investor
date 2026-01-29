import os
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import argparse

def generate_certs(lan_ip: str, output_dir: str):
    print(f"Generating certificates for LAN IP: {lan_ip}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Generate Private Key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 2. Generate Certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"AI Investor"),
        x509.NameAttribute(NameOID.COMMON_NAME, lan_ip),
    ])

    import ipaddress
    san_list = [x509.DNSName(u"localhost")]
    if lan_ip and lan_ip != "localhost":
        try:
            san_list.append(x509.IPAddress(ipaddress.ip_address(lan_ip)))
        except ValueError:
            san_list.append(x509.DNSName(lan_ip))
            
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # 10 years
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650)
    ).add_extension(
        x509.SubjectAlternativeName(san_list),
        critical=False,
    ).sign(key, hashes.SHA256())

    # 3. Write Private Key
    with open(os.path.join(output_dir, "server.key"), "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # 4. Write Certificate
    with open(os.path.join(output_dir, "server.crt"), "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Certificates generated in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LAN SSL certificates")
    parser.add_argument("--ip", required=True, help="The LAN IP of the box")
    parser.add_argument("--dir", default="infra/certs", help="Output directory")
    args = parser.parse_args()
    generate_certs(args.ip, args.dir)
