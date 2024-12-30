



helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace


helm upgrade --install grafana grafana/grafana --namespace monitoring --create-namespace -f values.yml



2. Install Prometheus Operator CRDs:
```bash
helmfile -f prometheus-operator-crds.yaml apply
```
or 
```bash
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values prometheus-operator-crds.yaml
```

3. Install Kube Prometheus Stack:
```bash
helmfile -f kube-prometheus-stack.yaml apply
```
or
```bash
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values kube-prometheus-stack.yaml
```

4. Install Grafana:
```bash
helmfile -f grafana.yaml apply
```
or
```bash
helm install grafana grafana/grafana \
  --namespace monitoring \
  --values grafana.yaml
```

kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

helmfile destroy -f grafana.yaml


