Steps to run

1. Create a virtual environment
```bash
python3 -m venv venv    
source venv/bin/activate
```

2. Install the dependencies
```bash
pip install -r requirements.txt
```

3. Run jupyter notebook
```bash
jupyter notebook lang_agent.ipynb
```

MAC OS
brew install graphviz
export LDFLAGS="-L/opt/homebrew/lib"
export CFLAGS="-I/opt/homebrew/include"
export CPPFLAGS="-I/opt/homebrew/include"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig"



If you’re building a chain of agents to decide the load-balancing algorithm, each agent could perform a specific role in the decision-making process:

Agent Roles
	1.	Log Analyzer Agent:
	•	Reads logs from NGINX.
	•	Extracts key metrics like latency, error rates, and throughput.
	2.	Performance Predictor Agent:
	•	Uses historical data and trends to predict backend performance.
	•	Evaluates whether EWMA or Round-Robin is more effective based on current conditions.
	3.	Judge Agent:
	•	Evaluates recommendations from other agents and makes the final decision on which algorithm to use.
	4.	Action Executor Agent:
	•	Updates the load balancer configuration to apply the chosen algorithm.



2.	Agent Chain Design:
•	Log Analyzer Agent: Continuously monitors and interprets logs to extract performance metrics like latency, response time, and request count.
•	Resource Evaluator Agent: Analyzes system and node-level metrics (e.g., CPU, memory, energy consumption).
•	Judge Agent: Makes decisions based on inputs from the log analyzer and resource evaluator, selecting the optimal algorithm.
•	Feedback Loop Agent: Validates the chosen strategy’s impact on resource and power consumption, feeding data back for continuous learning.