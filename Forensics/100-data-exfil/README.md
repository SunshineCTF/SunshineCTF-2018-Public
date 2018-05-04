# [Forensics - 100] Data Exfil
Network Forensics Challenge.
The goal of this challenge is extract files that's contained within DNS traffic.  
## Distributables
1. `DataExfil.zip`: Download and unzip the file to get to the challenge materials. 
## [How it works]
The `DataExfil.zip` contains a snapshot of web related network traffic. The file being "stolen" was broken into chunks (in hex), that would fit into a DNS query, and sent to a modified DNS server that would respond to any query. 

## [How to solve]
### Method 1
1. open the pcap with wireshark. 
2. From the statistics page you can view a resolved address to `cozybear.group` at `52.175.216.124` with what appears to be a large hex string in the subdomain. 
3. Filtering for the suspected suspect ip address `ip.addr == 54.175.216.124`
4. We can do a regex to extract the hex character before "cozybear.group" - `[0-9a-f]+.cozybear.group`
    - `tshark -r pcap.pcap -n -T fields -e dns.qry.name | grep -E [0-9a-f]+.cozybear.group | cut -d '.' -f1 | uniq` 
5. You can observe that the queries are repeated, with the same data so you can ignore the extra queries. After you filter out, and reassemble the Hex values you get.
    - ```504b030414000000000030be774c973a10791e0000001e0000000a0000007365637265742e74787473756e7b7730775f495f646e735f7333335f7930755f316e5f683372337d504b0102140014000000000030be774c973a10791e0000001e0000000a00000000000000010020000000000000007365637265742e747874504b0506000000000100010038000000460000000000```
6. From here you can decode the hex to ascii using python, cyberchef, or your tool of choice. In the example below
 we use python.
    - ```"504b030414000000000030be774c973a10791e0000001e0000000a0000007365637265742e74787473756e7b7730775f495f646e735f7333335f7930755f316e5f683372337d504b0102140014000000000030be774c973a10791e0000001e0000000a00000000000000010020000000000000007365637265742e747874504b0506000000000100010038000000460000000000".decode('hex')```
- Output 
    - ``` 'PK\x03\x04\x14\x00\x00\x00\x00\x000\xbewL\x97:\x10y\x1e\x00\x00\x00\x1e\x00\x00\x00\n\x00\x00\x00secret.txtsun{w0w_I_dns_s33_y0u_1n_h3r3}PK\x01\x02\x14\x00\x14\x00\x00\x00\x00\x000\xbewL\x97:\x10y\x1e\x00\x00\x00\x1e\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x01\x00 \x00\x00\x00\x00\x00\x00\x00secret.txtPK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x008\x00\x00\x00F\x00\x00\x00\x00\x00'```

7. the flag `sun{w0w_I_dns_s33_y0u_1n_h3r3}`
