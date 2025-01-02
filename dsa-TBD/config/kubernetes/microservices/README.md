k create ns usp-dev

k apply -f iot-api/ -n usp-dev

Check lb status when
kubectl describe ingress iot-app-ingress -n usp-dev

Check logs

kubectl logs -n ingress-nginx \
  -l app.kubernetes.io/component=controller \
  -c controller \
  --follow