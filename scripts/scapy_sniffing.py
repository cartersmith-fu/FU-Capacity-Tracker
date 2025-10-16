import socket
import csv
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP

# Open CSV file in append mode
csv_file = open('network_activity.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)

# Write header if file is empty
if csv_file.tell() == 0:
    csv_writer.writerow(['Timestamp', 'Source IP', 'Destination IP', 'Hostname', 'Protocol', 'Port'])

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Try reverse DNS lookup
        try:
            hostname = socket.gethostbyaddr(ip_dst)[0]
        except:
            hostname = "Unknown"

        protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else "Other"
        port = ""

        if TCP in packet:
            port = packet[TCP].dport
        elif UDP in packet:
            port = packet[UDP].dport

        # Write to CSV
        csv_writer.writerow([timestamp, ip_src, ip_dst, hostname, protocol, port])
        csv_file.flush()  # Ensure data is written immediately

        print(f"Source: {ip_src} -> Destination: {ip_dst} ({hostname}) | {protocol} Port: {port}")

try:
    sniff(prn=packet_callback, store=0)
except KeyboardInterrupt:
    print("\nStopping capture...")
finally:
    csv_file.close()