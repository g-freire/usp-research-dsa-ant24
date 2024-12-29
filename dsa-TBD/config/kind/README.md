kind create cluster --config kind-cluster-config.yaml 

kind delete cluster --name kind

kubectl cluster-info --context kind-kind

kind get clusters

kind get nodes

kind get kubeconfig --name kind > kubeconfig.yaml

kubectl get pods --all-namespaces

kubectl get pods --namespace default

kubectl get pods --namespace default -o jsonpath="{.items[*].spec.containers[*].image}"
