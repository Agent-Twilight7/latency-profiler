# dashboard.py
import streamlit as st
import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup
BASE_URL = "http://127.0.0.1:5000/"
endpoints = ["market_data", "order_submission", "trade_ack"]

# Sidebar config
st.sidebar.title("⚙️ Stress Test Config")
endpoint = st.sidebar.selectbox("Choose Endpoint", endpoints)
num_requests = st.sidebar.slider("Requests", 10, 100, 30)
threads = st.sidebar.slider("Threads", 1, 20, 5)

# Run benchmark function
def run_benchmark(endpoint, num_requests, threads):
    results = []

    def hit():
        url = BASE_URL + endpoint
        start = time.monotonic_ns()
        try:
            r = requests.get(url)
            end = time.monotonic_ns()
            latency = (end - start) / 1e6
            return latency
        except:
            return -1

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(hit) for _ in range(num_requests)]
        for future in as_completed(futures):
            latency = future.result()
            results.append(latency)

    return results

# UI
st.title("🚀 Real-Time Latency Profiler")
st.write("Benchmark REST API latency under load and visualize results instantly.")

if st.button("Start Benchmark"):
    with st.spinner("Benchmarking in progress..."):
        latencies = run_benchmark(endpoint, num_requests, threads)
        df = pd.DataFrame({ "Latency (ms)": latencies })
        avg = df["Latency (ms)"].mean()
        st.success(f"✅ Completed {num_requests} requests on /{endpoint}")
        st.write(f"**Average Latency:** `{avg:.2f} ms`")

        # Plot
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df, ax=ax, color="skyblue")
        st.pyplot(fig)

        # CSV download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, f"{endpoint}_latency.csv", "text/csv")
    