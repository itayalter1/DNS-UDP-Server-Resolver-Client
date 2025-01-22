import socket
import sys

# Check if the correct number of parameters is passed (port and file name)
if len(sys.argv) != 3:
    sys.exit(1)

my_port = int(sys.argv[1])  # Get the port number from command line arguments
file_name = sys.argv[2]  # Get the file name from command line arguments

# Try to open the file and read its contents
try:
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]  
except FileNotFoundError:
    # If the file is not found, print an error message and exit
    print(f"file don't exist {sys.argv[2]}")
    sys.exit(1)
except Exception as e:
    # If there's another problem with opening the file, print the error and exit
    print(f"problem with {e}")
    sys.exit(1)

# Create a list of dictionaries, each containing domain-related data from the file
list_of_dicts = []
for line in lines:
    items = line.split(',')  
    dicts = {
        'domain': items[0],  
        'ip': items[1],  
        'type': items[2],  
        'answer': items[0] + ',' + items[1] + "," + items[2]  
    }
    # Add the dictionary to the list
    list_of_dicts.append(dicts)  

# Create a UDP socket for communication with specified port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', my_port))

while True:
    # Listen for incoming data from clients
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')  

    # Search for a matching domain in the list of dictionaries
    filter_dicts = [dicts for dicts in list_of_dicts if dicts['domain'] == data]
    result = ''
    
    if not filter_dicts:
        # If no matching domain is found, check for NS records
        result = 'non-existent domain'
        filter_dicts_ns = [dicts for dicts in list_of_dicts if dicts['type'] == 'NS']
        for dicts in filter_dicts_ns:
            # Check if the data ends with an NS domain and set the result to the corresponding answer
            if data.endswith(dicts['domain']):
                result = dicts['answer']
                break
    else:
        # If a matching domain is found, return its answer
        result = filter_dicts[0]['answer']

    # Send the result (either the IP address or 'non-existent domain') back to the client
    s.sendto(result.encode('utf-8'), addr)
