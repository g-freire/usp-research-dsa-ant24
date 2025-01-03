import os
import json
import subprocess
import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    st.error("OpenAI API Key is not set. Please set the `OPENAI_API_KEY` environment variable.")
    st.stop()

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

# Set up Streamlit interface
st.title("Load Balancer Metrics Analyser")
st.write("Analyze NGINX ingress metrics and get recommendations on load balancing.")

# Input for ingress and namespace
# ingress_name = st.text_input("Enter the Ingress Name", value="iot-app-ingress")
# namespace = st.text_input("Enter the Namespace", value="usp-dev")

ingress_name = "iot-app-ingress"
namespace = "usp-dev"

# Add this CSS to create a table-like appearance with background
st.markdown("""
    <style>
    [data-testid="column"] {
        border: 1px solid #e6e6e6;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Automatically fetch ingress details on load
raw_details = get_ingress_details(ingress_name, namespace)
if "Error" in raw_details:
    st.error(raw_details)
else:
    ingress_details = parse_ingress_details(raw_details)
    st.success("Ingress details fetched successfully.")
    
    st.subheader("Ingress Details")
    
    # Create a container for the metrics
    with st.container():
        metrics = {
            "Name": ingress_details['Name'],
            "Namespace": ingress_details['Namespace'],
            "Host": ingress_details['Host'],
            "Load Balancer Type": ingress_details['Load Balancer Type']
        }
        
        if metrics["Load Balancer Type"] and "nginx.ingress.kubernetes.io/load-balance:" in metrics["Load Balancer Type"]:
            metrics["Load Balancer Type"] = metrics["Load Balancer Type"].split(":")[-1].strip()
        
        for label, value in metrics.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**{label}:**")
            with col2:
                st.write(value or "N/A")

# Update the refresh button section to use the same display format
if st.button("Refresh Ingress Details"):
    raw_details = get_ingress_details(ingress_name, namespace)
    if "Error" in raw_details:
        st.error(raw_details)
    else:
        ingress_details = parse_ingress_details(raw_details)
        st.success("Ingress details refreshed successfully.")
        
        st.subheader("Ingress Details")
        
        metrics = {
            "Name": ingress_details['Name'],
            "Namespace": ingress_details['Namespace'],
            "Host": ingress_details['Host'],
            "Load Balancer Type": ingress_details['Load Balancer Type']
        }
        
        if metrics["Load Balancer Type"] and "nginx.ingress.kubernetes.io/load-balance:" in metrics["Load Balancer Type"]:
            metrics["Load Balancer Type"] = metrics["Load Balancer Type"].split(":")[-1].strip()
        
        with st.container():
            for label, value in metrics.items():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(f"**{label}:**")
                with col2:
                    st.write(value or "N/A")

# File path input
file_path = st.text_input(
    "Enter the path to your `nginx_metrics_compact.json` file",
    value="./metrics/nginx_metrics_compact.json",
)

# Automatically analyze metrics when file is loaded
if file_path:
    try:
        with open(file_path, "r") as file:
            existing_summary = json.load(file)
        st.success("Metrics file loaded successfully.")

        # Construct the prompt
        prompt = f"""
        Analyze the following NGINX ingress metrics:

        Metrics Summary:
        {json.dumps(existing_summary, indent=2)}

        Based on the patterns over the last 5m, 1h, 3h, 6h, 12h, 1d, 3d, and 7d, recommend if the load balancing algorithm should be changed. Provide reasons for your recommendation.
        """

        # Set up LLM
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=OPENAI_API_KEY,
        )

        messages = [
            (
                "system",
                """ Analyze the following NGINX ingress metrics and recommend if the load balancing algorithm should be changed. 
                    Provide clear reasons for your recommendation based on the metrics patterns."""
            ),
            ("human", prompt),
        ]

        # Fetch the output automatically
        with st.spinner("Analyzing..."):
            try:
                output = llm.invoke(messages)
                st.success("Analysis complete.")
                st.subheader("Analysis Results")
                st.write(output.content)

                # Show Metrics Summary at the Bottom
                st.subheader("Metrics Summary")
                st.json(existing_summary)

            except Exception as e:
                st.error(f"Error during analysis: {e}")
        # Keep the analyze button for manual refresh
        if st.button("Re-run Analysis"):
            try:
                output = llm.invoke(messages)
                st.success("Analysis complete.")
                st.subheader("Analysis Results") 
                st.write(output.content)

                # Show Metrics Summary at the Bottom
                st.subheader("Metrics Summary")
                st.json(existing_summary)
            except Exception as e:
                st.error(f"Error during analysis: {e}")

    except FileNotFoundError:
        st.error(f"The file at `{file_path}` was not found. Please provide a valid path.")
    except json.JSONDecodeError:
        st.error("The file is not a valid JSON.")
else:
    st.info("Please enter the path to the `nginx_metrics_compact.json` file.")