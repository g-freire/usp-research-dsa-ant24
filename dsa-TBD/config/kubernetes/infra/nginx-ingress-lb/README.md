### Install Ingress

- helm show values ingress-nginx/ingress-nginx | less

- helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace -f values.yml

- helm uninstall ingress-nginx --namespace ingress-nginx 

- helm get values ingress-nginx --namespace ingress-nginx

- sudo kubectl port-forward svc/ingress-nginx-controller -n ingress-nginx 80:80
- curl -v -H "Host: iot-api.local" http://localhost:80/
- http://iot-api.local/

- /etc/hosts is Configured
- 127.0.0.1 iot-api.local

kubectl get svc -n ingress-nginx

ServiceMonitor

- kubectl apply -f ingress-nginx-servicemonitor.yaml

- kubectl get servicemonitor -n monitoring

- kubectl get endpoints -n monitoring

- kubectl get endpoints -n ingress-nginx


helm show values ingress-nginx/ingress-nginx | tee >(pbcopy) | less



curl -G 'http://localhost:58685/api/v1/query' --data-urlencode 'query=nginx_ingress_controller_requests[5m]'