import socket
import dns.resolver
import sys

def check_dns(hostname):
    print(f"\nChecking DNS resolution for {hostname}...")
    try:
        answers = dns.resolver.resolve(hostname, 'A')
        print(f"DNS resolution successful. IP addresses:")
        for rdata in answers:
            print(f"  {rdata}")
        return True
    except Exception as e:
        print(f"DNS resolution failed: {e}")
        return False

def check_connection(hostname, port):
    print(f"\nTesting TCP connection to {hostname}:{port}...")
    try:
        sock = socket.create_connection((hostname, port), timeout=5)
        print(f"Successfully connected to {hostname}:{port}")
        sock.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

# Test both standard and pooler hostnames
hosts = [
    ("db.jntjglobwzctfrsuurnp.supabase.co", 5432),
    ("db.jntjglobwzctfrsuurnp.supabase.co", 6543),  # Direct connection port
    ("aws-0-ap-southeast-1.pooler.supabase.com", 5432),
    ("aws-0-ap-southeast-1.pooler.supabase.com", 6543)
]

print("Supabase Connection Diagnostic Tool")
print("==================================")

for hostname, port in hosts:
    if check_dns(hostname):
        check_connection(hostname, port)