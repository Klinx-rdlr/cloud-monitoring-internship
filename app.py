from flask import Flask, render_template
from prometheus_client import start_http_server, Counter, Gauge
import pandas as pd

app = Flask(__name__)

# 1. Define the Gauges
estimated_total_cost = Gauge('cloud_estimated_total_cost', 'Total calculated cloud cost')
cost_per_service = Gauge('cloud_cost_per_service', 'Cost broken down by service', ['service_name'])
cost_per_request = Gauge('cloud_cost_per_request', 'Current cost efficiency per request')

# 2. Define your Cost Data (from your Day 5 task)
def update_costs():
    data = {
        "Service": ["Compute", "Storage", "Network"],
        "Usage": [120, 500, 80],
        "Cost_per_unit": [0.05, 0.02, 0.01]
    }
    df = pd.DataFrame(data)
    df["Total_Cost"] = df["Usage"] * df["Cost_per_unit"]
    
    # Update Total Cost Gauge
    total = df["Total_Cost"].sum()
    estimated_total_cost.set(total)
    
    # Update Per-Service Gauges using Labels
    for index, row in df.iterrows():
        cost_per_service.labels(service_name=row['Service']).set(row['Total_Cost'])

    # Calculate Cost Per Request (Example: Total Cost / Total Requests)
    # We'll set a dummy value for now or use your REQUEST_COUNT value
    cost_per_request.set(total / 1000) # Assuming 1000 requests for the simulation

# Initial run
update_costs()

@app.route("/")
def home():
    update_costs() # Update metrics whenever the page is visited
    return render_template("index.html")

if __name__ == "__main__":
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5000)

