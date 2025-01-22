import socket
import sys

# Check that the correct number of arguments were provided
if len(sys.argv) != 3:
    sys.exit(1)

server_ip = sys.argv[1]  
server_port = int(sys.argv[2])  

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

while True:
    send = input()
    # Send the message to the server
    s.sendto(send.encode('utf-8'), (server_ip, server_port))  

    # Receive response from the server
    data, addr = s.recvfrom(1024)  
    data = data.decode('utf-8')  

    try:
        # Try to print the part of the response after the comma and before the colon
        print(data.split(',')[1].split(':')[0])
    except IndexError:
        # If the response format is incorrect, just print the whole response
        print(data)
