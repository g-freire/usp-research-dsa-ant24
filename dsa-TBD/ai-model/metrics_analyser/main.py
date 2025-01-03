import os
import streamlit as st
from dotenv import load_dotenv
from tabs.ingress_tab import render_ingress_tab
from tabs.analysis_tab import render_analysis_tab

def main():
    # Load environment variables
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        st.error("OpenAI API Key is not set. Please set the `OPENAI_API_KEY` environment variable.")
        st.stop()

    # Set up Streamlit interface
    st.title("ICMC/USP Load Balancer Metrics Analyser")

    # Create tabs
    tab_ingress, tab_analysis = st.tabs(["Ingress Details", "AI Metrics Analysis"])

    # Render tabs
    with tab_ingress:
        render_ingress_tab()

    with tab_analysis:
        render_analysis_tab(OPENAI_API_KEY)

if __name__ == "__main__":
    main()