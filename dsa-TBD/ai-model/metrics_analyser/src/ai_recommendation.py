import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    st.error("OpenAI API Key is not set. Please set the `OPENAI_API_KEY` environment variable.")
    st.stop()

import json
try:
    with open("nginx_metrics_compact.json", "r") as compact_file:
        existing_summary = json.load(compact_file)
except FileNotFoundError:
    raise FileNotFoundError("nginx_metrics_compact.json not found")


# LLM prompt
prompt = f"""
Analyze the following NGINX ingress metrics:

Metrics Summary:
{json.dumps(existing_summary, indent=2)}

Based on the patterns over the last 5m, 1h, 3h, 6h, 12h, 1d, 3d, and 7d, recommend if the load balancing algorithm should be changed. Provide reasons for your recommendation.
"""

from langchain_openai import ChatOpenAI

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
output = llm.invoke(messages)

print(output.content)

