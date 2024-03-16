# Configmap
kubectl apply -f ./k8s/configmap/mysql-db-configmap.yaml
kubectl apply -f ./k8s/configmap/web-lib-configmap.yaml
# Secret
kubectl apply -f ./k8s/secret/mysql-db-secret.yaml
kubectl apply -f ./k8s/secret/web-lib-secret.yaml
# Service
kubectl apply -f ./k8s/service/mysql-db-service.yaml
kubectl apply -f ./k8s/service/web-lib-service.yaml
# Deployment
kubectl apply -f ./k8s/deployment/mysql-db-deployment.yaml
kubectl apply -f ./k8s/deployment/web-lib-deployment.yaml
