# concurrent_profiler.py
import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://127.0.0.1:5000/"
endpoints = ["market_data", "order_submission", "trade_ack"]
THREADS = 10         # Number of concurrent requests
REQUESTS_PER_EP = 20  # Total requests per endpoint

results = []

def hit_endpoint(endpoint):
    full_url = BASE_URL + endpoint
    start = time.monotonic_ns()
    try:
        response = requests.get(full_url)
        end = time.monotonic_ns()
        latency_ms = (end - start) / 1e6
        return (endpoint, latency_ms)
    except Exception as e:
        return (endpoint, -1)

with ThreadPoolExecutor(max_workers=THREADS) as executor:
    futures = []

    for ep in endpoints:
        for _ in range(REQUESTS_PER_EP):
            futures.append(executor.submit(hit_endpoint, ep))

    for future in as_completed(futures):
        endpoint, latency = future.result()
        results.append([endpoint, latency])
        print(f"{endpoint} → {latency:.3f} ms")

# Write to CSV
with open("concurrent_latency_log.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Endpoint", "Latency_ms"])
    writer.writerows(results)

print("✅ Concurrent latency log saved to concurrent_latency_log.csv")
