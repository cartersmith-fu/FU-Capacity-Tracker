
from scapy.all import sniff, Dot11ProbeReq
import time, hashlib, sqlite3, csv, os

# --- SETTINGS ---
SALT = "change_this_salt"      # any secret string; keep private
DEDUPE_SECONDS = 300           # 5 min window per device
DB_FILE = "agg_counts.db"
CSV_FILE = "hourly_counts.csv"

# --- SETUP ---
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS seen(
  hash TEXT PRIMARY KEY,
  last_seen INTEGER
)
""")
conn.commit()

def hash_mac(mac):
    return hashlib.sha256((mac + SALT).encode()).hexdigest()

def mark_seen(mac):
    h = hash_mac(mac)
    ts = int(time.time())
    c.execute("SELECT last_seen FROM seen WHERE hash=?", (h,))
    row = c.fetchone()
    if row is None:
        c.execute("INSERT INTO seen(hash,last_seen) VALUES(?,?)", (h, ts))
        conn.commit()
        return True
    elif ts - row[0] > DEDUPE_SECONDS:
        c.execute("UPDATE seen SET last_seen=? WHERE hash=?", (ts, h))
        conn.commit()
        return True
    else:
        return False

def handle(pkt):
    if pkt.haslayer(Dot11ProbeReq):
        mac = pkt.addr2
        if mac:
            mark_seen(mac)

def write_hourly_count():
    # find how many unique devices seen in the last hour
    now = int(time.time())
    one_hour_ago = now - 3600
    c.execute("SELECT COUNT(*) FROM seen WHERE last_seen > ?", (one_hour_ago,))
    count = c.fetchone()[0]

    hour_str = time.strftime("%Y-%m-%d %H:00:00", time.localtime(now))
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "unique_devices"])
        writer.writerow([hour_str, count])

    print(f"[{hour_str}] Hourly unique devices: {count}")

if __name__ == "__main__":
    start_time = time.time()
    print("Sniffing started... (Ctrl+C to stop)")
    try:
        while True:
            sniff(iface="wlan0mon", prn=handle, store=False, timeout=60)
            # Every hour, dump count
            if time.time() - start_time >= 3600:
                write_hourly_count()
                start_time = time.time()
    except KeyboardInterrupt:
        print("\nStopping and writing final hourly count...")
        write_hourly_count()
        conn.close()
