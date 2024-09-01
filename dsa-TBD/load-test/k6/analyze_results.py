import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

results = "results/poisson_results.json"

def parse_json_file(filepath):
    metrics = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                try:
                    metrics.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    return metrics

def normalize_metrics(metrics):
    # Normalize metrics data into a DataFrame
    normalized_data = []
    for metric in metrics:
        try:
            if metric.get('type') == 'Point':
                data = metric.get('data', {})
                # Extract values and handle missing 'name' with default
                normalized_data.append({
                    'metric': metric.get('metric'),
                    'name': data.get('name', metric.get('metric', 'unknown')),  # Use metric as default
                    'value': data.get('value'),
                    'time': data.get('time'),
                    'tags': data.get('tags', {})
                })
        except KeyError as e:
            print(f"KeyError: {e} in metric: {metric}")
    df = pd.DataFrame(normalized_data)
    
    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    
    # Convert value to numeric, coercing errors
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    return df

# Load and normalize data
metrics = parse_json_file(results)
df = normalize_metrics(metrics)

# Extract the base name from the results file for the title
base_name = results.split('/')[-1].split('.')[0]

# Print DataFrame head to debug
print("DataFrame head after processing:")
print(df.head())

# Ensure data is not empty and contains valid values
if not df.empty and df['value'].notna().any():
    # Define colors for each plot
    colors = {
        'http_req_duration': 'blue',
        'http_reqs': 'green',
        'http_req_blocked': 'red',
        'http_req_connecting': 'purple',
        'http_req_tls_handshaking': 'orange',
        'http_req_sending': 'brown'
    }
    
    # Create a single figure with subplots
    fig, axes = plt.subplots(nrows=6, ncols=1, figsize=(12, 18), sharex=True)
    # fig.suptitle(f'Metrics from {base_name}', fontsize=16, y=0.93)
    
    # Plot HTTP request duration
    sns.lineplot(data=df[df['name'] == 'http_req_duration'], x='time', y='value', marker='o', color=colors['http_req_duration'], ax=axes[0])
    axes[0].set_title('HTTP Request Duration')
    axes[0].set_ylabel('Duration (ms)')
    axes[0].grid(True)
    axes[0].set_xlim(df['time'].min(), df['time'].max())  # Set x-axis limits to cover the full range
    axes[0].tick_params(axis='x', rotation=45)

    # Plot HTTP requests count
    sns.lineplot(data=df[df['name'] == 'http_reqs'], x='time', y='value', marker='o', color=colors['http_reqs'], ax=axes[1])
    axes[1].set_title('HTTP Requests Count')
    axes[1].set_ylabel('Requests Count')
    axes[1].grid(True)
    axes[1].set_xlim(df['time'].min(), df['time'].max())  # Set x-axis limits to cover the full range
    axes[1].tick_params(axis='x', rotation=45)

    # Plot HTTP request blocked
    sns.lineplot(data=df[df['name'] == 'http_req_blocked'], x='time', y='value', marker='o', color=colors['http_req_blocked'], ax=axes[2])
    axes[2].set_title('HTTP Request Blocked Duration')
    axes[2].set_ylabel('Blocked Duration (ms)')
    axes[2].grid(True)
    axes[2].set_xlim(df['time'].min(), df['time'].max())  # Set x-axis limits to cover the full range
    axes[2].tick_params(axis='x', rotation=45)

    # Plot HTTP request connecting
    sns.lineplot(data=df[df['name'] == 'http_req_connecting'], x='time', y='value', marker='o', color=colors['http_req_connecting'], ax=axes[3])
    axes[3].set_title('HTTP Request Connecting Duration')
    axes[3].set_ylabel('Connecting Duration (ms)')
    axes[3].grid(True)
    axes[3].set_xlim(df['time'].min(), df['time'].max())  # Set x-axis limits to cover the full range
    axes[3].tick_params(axis='x', rotation=45)

    # Plot HTTP request TLS handshaking
    sns.lineplot(data=df[df['name'] == 'http_req_tls_handshaking'], x='time', y='value', marker='o', color=colors['http_req_tls_handshaking'], ax=axes[4])
    axes[4].set_title('HTTP Request TLS Handshaking Duration')
    axes[4].set_ylabel('TLS Handshaking Duration (ms)')
    axes[4].grid(True)
    axes[4].set_xlim(df['time'].min(), df['time'].max())  # Set x-axis limits to cover the full range
    axes[4].tick_params(axis='x', rotation=45)

    # Plot HTTP request sending
    sns.lineplot(data=df[df['name'] == 'http_req_sending'], x='time', y='value', marker='o', color=colors['http_req_sending'], ax=axes[5])
    axes[5].set_title('HTTP Request Sending Duration')
    axes[5].set_ylabel('Sending Duration (ms)')
    axes[5].grid(True)
    axes[5].set_xlim(df['time'].min(), df['time'].max())  # Set x-axis limits to cover the full range
    axes[5].tick_params(axis='x', rotation=45)

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for the suptitle
    
    # Save as PDF and PNG
    # plt.savefig(f'results/{base_name}_metrics.pdf', format='pdf')
    plt.savefig(f'results/{base_name}_metrics.png', format='png')
    
    plt.show()

else:
    print("No valid data available for plotting.")
