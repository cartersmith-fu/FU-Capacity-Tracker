import csv, time, random
from datetime import datetime

def fake_capture():
    """Simulate random device counts for testing."""
    return random.randint(20, 120)

while True:
    count = fake_capture()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("../data/example_data.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([ts, count])

    print(f"{ts}: {count} devices recorded")
    time.sleep(30)  # log every hour
