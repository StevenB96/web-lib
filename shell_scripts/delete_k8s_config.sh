# Configmap
kubectl delete -f ./k8s/configmap/mysql-db-configmap.yaml -n web-lib-project
kubectl delete -f ./k8s/configmap/web-lib-configmap.yaml -n web-lib-project
# Secret
kubectl delete -f ./k8s/secret/mysql-db-secret.yaml -n web-lib-project
kubectl delete -f ./k8s/secret/web-lib-secret.yaml -n web-lib-project
# Service
kubectl delete -f ./k8s/service/mysql-db-service.yaml -n web-lib-project
kubectl delete -f ./k8s/service/web-lib-service.yaml -n web-lib-project
# Deployment
kubectl delete -f ./k8s/deployment/mysql-db-deployment.yaml -n web-lib-project
kubectl delete -f ./k8s/deployment/web-lib-deployment.yaml -n web-lib-project
# Namespace
kubectl delete -f ./k8s/namespace/web-lib-project.yaml