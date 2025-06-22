# plot.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load latency data
df = pd.read_csv("latency_log.csv")

# Set style
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

# Create boxplot
sns.boxplot(x="Endpoint", y="Latency_ms", data=df, palette="Set2")

# Add title and labels
plt.title("Latency Distribution per Endpoint", fontsize=14)
plt.xlabel("API Endpoint", fontsize=12)
plt.ylabel("Latency (ms)", fontsize=12)

# Save the plot
plt.savefig("latency_plot.png")
print("✅ latency_plot.png saved.")


# Choose which CSV to visualize
csv_file = "concurrent_latency_log.csv"  # or "latency_log.csv"

df = pd.read_csv(csv_file)

sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))

sns.boxplot(x="Endpoint", y="Latency_ms", data=df, palette="pastel")

plt.title("Latency Distribution (Concurrent Requests)" if "concurrent" in csv_file else "Latency Distribution", fontsize=14)
plt.xlabel("API Endpoint", fontsize=12)
plt.ylabel("Latency (ms)", fontsize=12)
plt.savefig("latency_plot_concurrent.png")
print("✅ Plot saved as latency_plot_concurrent.png")

