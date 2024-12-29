k create ns usp-dev
k apply -f api.yml -n usp-dev
k apply -f database.yml -n usp-dev



sudo kubectl port-forward svc/ingress-nginx-controller -n ingress-nginx 80:80
curl -v -H "Host: iot-api.local" http://localhost:80/
http://iot-api.local/

/etc/hosts is Configured
127.0.0.1 iot-api.local