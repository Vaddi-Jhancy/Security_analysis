#!/usr/bin/python3
import socket, ssl, sys, pprint

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <hostname>")
    sys.exit(1)

hostname = sys.argv[1]
port = 443
# cadir = '/etc/ssl/certs'
cadir = './certs'  # for task 2


# Setup the TLS context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(capath=cadir)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
# context.check_hostname = False  # for task 3 hostname as fakegoogle.com

# Create TCP connection
print(f"[+] Connecting to {hostname} on port {port}...")
sock = socket.create_connection((hostname, port))
input("TCP connection established. Press Enter to continue...")

# Wrap with TLS
print("[+] Starting TLS handshake...")
ssock = context.wrap_socket(sock, server_hostname=hostname)
# Handshake done automatically here

# task 1 Printing the server certificate
cert = ssock.getpeercert()
print("\n[+] Server Certificate:")
pprint.pprint(cert)

# task 1 Printing the cipher used between the client and the server
print("\n[+] Cipher used:")
print(ssock.cipher())

input("Handshake complete. Press Enter to close the connection...")

# sending http request # task 4
request = (
    "GET /images/branding/googlelogo/2x/googlelogo_color_272x92dp.png HTTP/1.1\r\n"
    "Host: www.google.com\r\n"
    "Connection: close\r\n\r\n"
).encode('utf-8')

ssock.sendall(request)
print("[+] Sent HTTP GET request. Receiving response...")

# # read the response # task 4_1
# response = ssock.recv(2048)
# while response:
#     pprint.pprint(response.split(b"\r\n"))
#     response = ssock.recv(2048)

# Read and write image data
response = b""
while True:
    data = ssock.recv(4096)
    if not data:
        break
    response += data

# Separate headers and body
header_end = response.find(b'\r\n\r\n')
headers = response[:header_end]
body = response[header_end+4:]

# Save image
with open("google_logo.png", "wb") as f:
    f.write(body)

print("Image saved as google_logo.png")
# Close connection
# ssock.shutdown(socket.SHUT_RDWR)   # commented because in https client we don't need to manually call shut down, just closing is enough
ssock.close()
print("[+] Connection closed.")
