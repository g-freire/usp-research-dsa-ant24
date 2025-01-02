- helm repo add elastic https://helm.elastic.co
- helm repo update
- helm install elasticsearch elastic/elasticsearch -n logging -f values.yaml

1. Watch all cluster members come up.
  $ kubectl get pods --namespace=logging -l app=elasticsearch-master -w
2. Retrieve elastic user's password.
  $ kubectl get secrets --namespace=logging elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
3. Test cluster health using Helm test.
  $ helm --namespace=logging test elasticsearch

- make install

- kubectl port-forward svc/elasticsearch-master 9200
- curl localhost:9200/_cat/indices

- kubectl port-forward svc/kibana-kibana 5601



