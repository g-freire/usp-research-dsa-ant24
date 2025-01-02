default: test

RELEASE := helm-es-kind
TIMEOUT := 1200s

install:
	helm upgrade --wait --timeout=$(TIMEOUT) --install --values values.yaml $(RELEASE) ../../ -n logging

test: install
	helm test $(RELEASE)

purge:
	helm del $(RELEASE)