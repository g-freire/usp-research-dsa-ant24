- Install
- helm upgrade --install kibana elastic/kibana --namespace logging -f values.yaml


1. Watch all containers come up.
  $ kubectl get pods --namespace=logging -l release=kibana -w
2. Retrieve the elastic user's password.
  $ kubectl get secrets --namespace=logging elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
3. Retrieve the kibana service account token.
  $ kubectl get secrets --namespace=logging kibana-kibana-es-token -ojsonpath='{.data.token}' | base64 -d


- clean up

helm uninstall kibana elastic/kibana --namespace logging

kubectl delete serviceaccount pre-install-kibana-kibana -n logging
kubectl delete configmap kibana-kibana-helm-scripts -n logging
kubectl delete role pre-install-kibana-kibana -n logging
kubectl delete rolebinding pre-install-kibana-kibana -n logging
kubectl delete job pre-install-kibana-kibana -n logging