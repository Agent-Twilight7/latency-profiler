# profiler.py
import requests
import time
import csv

BASE_URL = "http://127.0.0.1:5000/"
endpoints = ["market_data", "order_submission", "trade_ack"]
results = []

REPEAT = 20  # number of times each endpoint will be hit

for _ in range(REPEAT):
    for endpoint in endpoints:
        full_url = BASE_URL + endpoint
        start = time.monotonic_ns()
        try:
            response = requests.get(full_url)
            end = time.monotonic_ns()
            latency_ms = (end - start) / 1e6  # convert to milliseconds
            results.append([endpoint, latency_ms])
            print(f"{endpoint} → {latency_ms:.3f} ms")
        except Exception as e:
            print(f"Error hitting {endpoint}: {e}")

# Write to CSV
with open("latency_log.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Endpoint", "Latency_ms"])
    writer.writerows(results)

print("✅ Latency results written to latency_log.csv")
