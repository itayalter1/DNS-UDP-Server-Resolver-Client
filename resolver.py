import socket
import sys
import time


# Function to delete old entries from the cache that have exceeded the specified time threshold
def deleteOldRows(the_list, time_is_old):
    current_time = time.time()  
    items_to_delete = [item for item in the_list if current_time - item['time'] > time_is_old]
    for item in items_to_delete:
        the_list.remove(item)  


# Function to handle checking for NS (Name Server) records and making recursive queries
def checkNS(the_list, data_1, parent_ip_fun, parent_port_fun):
    string_result = 'non-existent domain'  
    data2 = 'non-existent domain'
    # Create a new UDP socket
    send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    send.settimeout(5)  

    # Filter the list to get all NS (Name Server) records
    filter_dicts_ns = [dicts for dicts in the_list if dicts['type'] == 'NS']
    for dicts in filter_dicts_ns:
        if data_1.endswith(dicts['domain']):  
            data2 = dicts['answer']  

    # If no matching NS record is found, query the parent server
    if data2 == 'non-existent domain':
        try:
            send.sendto(data_1.encode('utf-8'), (parent_ip_fun, parent_port_fun))  
            data2, addr2 = send.recvfrom(1024)  
            data2 = data2.decode('utf-8')  
        except socket.timeout:  
            send.close()  #
            return string_result  

    # Process the response from the parent or NS server
    while True:
        if data2 != 'non-existent domain':  
            items = data2.split(',')
            # Create a dictionary with the parsed data
            new_dicts = {  
                'domain': items[0],
                'ip': items[1],
                'type': items[2],
                'answer': items[0] + ',' + items[1] + "," + items[2],  
                'time': time.time()  # Record the current time for caching purposes
            }
            # Add the new entry to the cache
            the_list.append(new_dicts)  

            # If the response is an NS type, query the new NS server for a result
            if new_dicts['type'] == "NS":
                parent_ip_local = new_dicts['ip'].split(':')[0] 
                parent_port_local = int(new_dicts['ip'].split(':')[1])  
                try:
                    # Send query to the new NS server
                    send.sendto(data_1.encode('utf-8'), (parent_ip_local, parent_port_local))  
                    data2, addr2 = send.recvfrom(1024)  
                    data2 = data2.decode('utf-8')  
                # If the new NS server does not respond
                except socket.timeout:  
                    send.close() 
                    return 'non-existent domain'  

            else:
                # If it's not an NS record, return the found answer
                string_result = new_dicts['answer']  
                break  
        else:
            # If no valid response was found, return 'non-existent domain'
            string_result = 'non-existent domain'  
            break  

    # Close the socket after processing and return thr result
    send.close()  
    return string_result  

# Main script logic starts here
# Check that the correct number of arguments were provided
if len(sys.argv) != 5:  
    sys.exit(1)  

my_port = int(sys.argv[1])  
parent_ip = sys.argv[2]  
parent_port = int(sys.argv[3])  
cache_time = int(sys.argv[4])  

# Initialize an empty list to store DNS records in memory
list_of_dicts = [] 

# Create a UDP socket to listen for incoming requests
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', my_port))  

# Infinite loop to listen for and process incoming DNS requests
while True:
    data, addr = s.recvfrom(1024)  
    data = data.decode('utf-8')  

    # Clear expired cache entries before processing the request
    deleteOldRows(list_of_dicts, cache_time)

    # Search the cache for a matching domain record
    filter_dicts = [dicts for dicts in list_of_dicts if dicts['domain'] == data]

    # If no matching domain is found in the cache, perform a recursive query
    if not filter_dicts:
        result = checkNS(list_of_dicts, data, parent_ip, parent_port)

    else:
        result = filter_dicts[0]['answer']  

    # Send the result (either a valid answer or 'non-existent domain') back to the client
    s.sendto(result.encode('utf-8'), addr)
