import requests
import json
from datetime import datetime

# Prometheus query function with proper query_range parameters
def query_prometheus(prometheus_url, promql_query, start, end, step):
    params = {
        "query": promql_query,
        "start": start,
        "end": end,
        "step": step,
    }
    response = requests.get(prometheus_url, params=params)
    response.raise_for_status()
    return response.json()

# Prometheus base URL
prometheus_url = "http://localhost:58685/api/v1/query_range"

# Define aggregation periods in seconds
lookback_windows = {
    "5m": 300,             # 5 minutes
    "15m": 900,            # 15 minutes
    "30m": 1800,           # 30 minutes
    "1h": 3600,            # 1 hour
    # "3h": 3600 * 3,        # 3 hours
    # "6h": 3600 * 6,        # 6 hours
    # "12h": 3600 * 12,      # 12 hours
    # "1d": 86400,           # 1 day
    # "3d": 86400 * 3,       # 3 days
    # "7d": 86400 * 7,       # 7 days
}

# Define Prometheus queries for each metric
queries = {
    "request_count": "sum(rate(nginx_ingress_controller_requests[1m]))",
    "response_time_avg": "avg(rate(nginx_ingress_controller_response_duration_seconds_sum[1m]))",
    "response_time_p95": "histogram_quantile(0.95, sum(rate(nginx_ingress_controller_response_duration_seconds_bucket[1m])) by (le))",
    "active_connections": "avg(nginx_ingress_controller_nginx_connections_active)",
    "dropped_connections": "sum(rate(nginx_ingress_controller_nginx_connections_dropped[1m]))",
}

# Aggregate metrics over different lookback windows
aggregated_results = {}
for period, seconds in lookback_windows.items():
    print(f"Aggregating metrics for {period}...")
    end_time = int(datetime.now().timestamp())
    start_time = end_time - seconds
    step = "60s" if seconds <= 3600 else "300s"  # Adjust step for short or long windows
    metrics = {}
    for key, promql_query in queries.items():
        try:
            data = query_prometheus(prometheus_url, promql_query, start_time, end_time, step)
            metrics[key] = data["data"]["result"]
        except requests.exceptions.RequestException as e:
            print(f"Error querying {key} for {period}: {e}")
    aggregated_results[period] = metrics

# Summarize and export data
summary = {
    period: {
        metric: [
            {
                "labels": result["metric"],
                "values": result["values"],
            }
            for result in results
        ]
        for metric, results in metrics.items()
    }
    for period, metrics in aggregated_results.items()
}

# Save results as JSON
with open("nginx_metrics.json", "w") as json_file:
    json.dump(summary, json_file, indent=2)

# Save results as TXT
with open("nginx_metrics.txt", "w") as txt_file:
    txt_file.write(json.dumps(summary, indent=2))

# Compact the summary for LLM prompt
compact_summary = {
    period: {
        metric: {
            "summary": f"{metric} data aggregated over {period}",
            "example_values": [
                {"timestamp": value[0], "value": value[1]} for result in results for value in result["values"][:2]
            ],  # Show first 2 data points
        }
        for metric, results in metrics.items()
    }
    for period, metrics in aggregated_results.items()
}

# Save the compact summary
with open("nginx_metrics_compact.json", "w") as compact_file:
    json.dump(compact_summary, compact_file, indent=2)

# LLM prompt
prompt = f"""
Analyze the following NGINX ingress metrics:

Metrics Summary:
{json.dumps(compact_summary, indent=2)}

Based on the patterns over the last 5m, 1h, 3h, 6h, 12h, 1d, 3d, and 7d, recommend if the load balancing algorithm should be changed. Provide reasons for your recommendation.
"""






