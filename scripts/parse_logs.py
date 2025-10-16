import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the CSV file (skip header if it exists)
df = pd.read_csv('network_activity.csv', 
                 names=['timestamp', 'src_ip', 'dst_ip', 'hostname', 'protocol', 'port'],
                 skiprows=1,  # Skip the header row
                 low_memory=False)

# Convert timestamp to datetime with explicit format
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Remove any rows where timestamp couldn't be parsed
df = df.dropna(subset=['timestamp'])

# Extract hour from timestamp
df['hour'] = df['timestamp'].dt.floor('H')

# Count packets per hour
hourly_counts = df.groupby('hour').size().reset_index(name='packet_count')

# Create the line graph
plt.figure(figsize=(12, 6))
plt.plot(hourly_counts['hour'], hourly_counts['packet_count'], 
         marker='o', linewidth=2, markersize=6)

plt.xlabel('Time (Hour)', fontsize=12)
plt.ylabel('Number of Packets', fontsize=12)
plt.title('Network Activity Over Time', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# Format x-axis to show time in 12-hour format (e.g., 2pm, 6pm)
from matplotlib.dates import DateFormatter
ax = plt.gca()
ax.xaxis.set_major_formatter(DateFormatter('%-I%p'))  # Use %I%p for Windows
plt.xticks(rotation=45)
plt.tight_layout()

# Display statistics
print(f"Total Packets: {hourly_counts['packet_count'].sum()}")
print(f"Peak Hour: {hourly_counts.loc[hourly_counts['packet_count'].idxmax(), 'hour']}")
print(f"Average Packets per Hour: {hourly_counts['packet_count'].mean():.2f}")

plt.show()