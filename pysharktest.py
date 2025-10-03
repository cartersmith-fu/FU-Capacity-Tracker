import pyshark
import nest_asyncio
nest_asyncio.apply()

cap = pyshark.LiveCapture(interface='en0')

packets = cap.sniff(timeout=10)  # Capture for 10 seconds
for packet in packets:
    print(packet)
