import streamlit as st
import json
from langchain_openai import ChatOpenAI
from src.nginx_prometheus_metrics_collector import PrometheusMetrics

def render_analysis_tab(openai_api_key):
    st.write("Analyze NGINX ingress metrics and get recommendations on load balancing.")
    
    metrics_collector = PrometheusMetrics()

    if st.button("Collect and Analyze Metrics"):
        with st.spinner("Collecting metrics from Prometheus..."):
            try:
                metrics_data = metrics_collector.collect_metrics()
                existing_summary = metrics_data["compact"]
                st.success("Metrics collected successfully.")

                prompt = f"""
                Analyze the following NGINX ingress metrics:

                Metrics Summary:
                {json.dumps(existing_summary, indent=2)}

                Based on the patterns over the last 5m, 15m, 30m, and 1h, recommend if the load balancing algorithm should be changed. Provide reasons for your recommendation.
                """

                llm = ChatOpenAI(
                    model="gpt-4o",
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                    api_key=openai_api_key,
                )

                messages = [
                    (
                        "system",
                        """ Analyze the following NGINX ingress metrics and recommend if the load balancing algorithm should be changed. 
                            Provide clear reasons for your recommendation based on the metrics patterns."""
                    ),
                    ("human", prompt),
                ]

                with st.spinner("Analyzing..."):
                    try:
                        output = llm.invoke(messages)
                        st.success("Analysis complete.")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Analysis Results")
                            st.write(output.content)
                        
                        with col2:
                            st.subheader("Metrics Summary")
                            st.json(existing_summary)

                    except Exception as e:
                        st.error(f"Error during analysis: {e}")

            except Exception as e:
                st.error(f"Error collecting metrics: {e}")