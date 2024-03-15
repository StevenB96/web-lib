# Configmap
kubectl delete -f ./k8s/configmap/mysql-db-configmap.yaml
kubectl delete -f ./k8s/configmap/web-lib-configmap.yaml
# Secret
kubectl delete -f ./k8s/secret/mysql-db-secret.yaml
kubectl delete -f ./k8s/secret/web-lib-secret.yaml
# Deployment
kubectl delete -f ./k8s/deployment/mysql-db-deployment.yaml
kubectl delete -f ./k8s/deployment/web-lib-deployment.yaml
# Service
kubectl delete -f ./k8s/service/mysql-db-service.yaml
kubectl delete -f ./k8s/service/web-lib-service.yaml