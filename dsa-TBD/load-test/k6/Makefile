# Define variables
K6_CMD = k6 run
RESULT_DIR = results
RESULT_FORMAT = json
SCRIPTS_DIR = distributions

# Ensure results directory exists
init:
	mkdir -p $(RESULT_DIR)

# Run each k6 script and save results
run-normal:
	$(K6_CMD) --out json=$(RESULT_DIR)/normal_results.json $(SCRIPTS_DIR)/normal.js

run-poisson:
	$(K6_CMD) --out json=$(RESULT_DIR)/poisson_results.json $(SCRIPTS_DIR)/poisson.js

run-triangular:
	$(K6_CMD) --out json=$(RESULT_DIR)/triangular_results.json $(SCRIPTS_DIR)/triangular.js

# Analyze results with Python script
analyze:
	python analyze_results.py

# Run all scripts and analyze results
all: init run-normal run-poisson run-triangular analyze
