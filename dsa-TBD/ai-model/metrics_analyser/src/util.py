import subprocess

# Function to get ingress details using `kubectl describe ingress`
def get_ingress_details(ingress_name, namespace):
    try:
        result = subprocess.run(
            ["kubectl", "describe", "ingress", ingress_name, "-n", namespace],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error fetching ingress details: {e.stderr.strip()}"

# Function to parse ingress details
def parse_ingress_details(raw_output):
    details = {
        "Name": None,
        "Namespace": None,
        "Host": None,
        "Load Balancer Type": None,
    }

    for line in raw_output.splitlines():
        line = line.strip()
        if line.startswith("Name:"):
            details["Name"] = line.split(":", 1)[1].strip()
        elif line.startswith("Namespace:"):
            details["Namespace"] = line.split(":", 1)[1].strip()
        elif "Host" in line and "Path" in line:  # Start of rules section
            details["Host"] = line.split(" ")[0].strip()
        elif "nginx.ingress.kubernetes.io/load-balance" in line:
            details["Load Balancer Type"] = line.split(":", 1)[1].strip()
    
    return details