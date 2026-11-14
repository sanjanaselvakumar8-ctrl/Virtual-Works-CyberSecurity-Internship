
import socket

# Get system details
host = input("Enter IP address or hostname: ")
port = int(input("Enter port number: "))

# Create socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)

try:
    s.connect((host, port))
    print(f"Port {port} is OPEN on {host}")

except:
    print(f"Port {port} is CLOSED or not accessible on {host}")

finally:
    s.close()
