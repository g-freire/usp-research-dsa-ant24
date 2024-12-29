### Install Ingress

- helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace -f values.yml

- helm uninstall ingress-nginx --namespace ingress-nginx 