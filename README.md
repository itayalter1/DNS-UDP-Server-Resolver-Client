# 🌐 DNS Resolver and Server Implementation

## 🎯 Overview
Simple DNS-like service implementation with domain name to IP resolution, similar to 144 information service. Includes primary DNS server, resolver server, and client components.

## 🛠️ Components
1. **Primary DNS Server** 📝
   - Holds zone.txt with domain-IP mappings
   - Responds to DNS queries
   - Returns "non-existent domain" if not found

2. **Resolver Server** 🔄
   - Mediates between clients and primary servers
   - Caches results for specified duration
   - Queries primary server for unknown domains

3. **Client** 👥
   - Submits domain queries
   - Displays IP addresses or error messages

## 🚀 How to Run

### Clone Poject
```bash
git clone https://github.com/itayalter1/DNS-UDP-Server-Resolver-Client.git
```
```bash
cd DNS-Resolver-and-Server
```

### 1. Primary Server
```bash
python server.py [port] [zoneFile]
# Example:
python server.py 55555 zone.txt
```

### 2. Resolver Server
```bash
python resolver.py [port] [parentIP] [parentPort] [x]
# Example:
python resolver.py 12345 127.0.0.1 55555 60
```

### 3. Client
```bash
python client.py [serverIP] [serverPort]
# Example:
python client.py 127.0.0.1 12345
```

## 📋 Example zone.txt
```
biu.ac.il,1.2.3.4,A
.co.il,1.2.3.5:777,NS
example.com,1.2.3.7,A
```
## 📝 DNS Record Types


### A Record (Address) 🏠
- Maps domain to IPv4
- Example: `biu.ac.il,1.2.3.4,A`
- Direct IP address connection

### NS Record (Name Server) 🔀
- Delegates to another server
- Example: `.co.il,1.2.3.5:777,NS`
- Forwards queries to specified server



## 🔍 Sample Queries
```
Input: il.ac.biu
Output: 1.2.3.4

Input: il.ac.biu.www
Output: non-existent domain
```

## ⚙️ Requirements
- Python 3.x
- No external libraries needed
