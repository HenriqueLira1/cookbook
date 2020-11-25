#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Setting up DOCKER_TAG variable
readonly VERSION="${CI_BUILD_REF:0:8}"
readonly DOCKER_TAG="${CI_REGISTRY}/${CI_PROJECT_PATH}:${VERSION}"
readonly TIMEOUT="5m"
echo "Deploying ${DOCKER_TAG} on ${CI_ENVIRONMENT_SLUG}"

# Generating credentials to access EKS.
aws eks update-kubeconfig --name eks-mimic

# Generate secrets
SECRET_NAME="${CI_PROJECT_NAME}-secret"
kubectl delete secret -n "${CI_ENVIRONMENT_SLUG}" "${SECRET_NAME}" --ignore-not-found
kubectl create secret generic -n "${CI_ENVIRONMENT_SLUG}" "${SECRET_NAME}" \
    --from-literal="DB_HOST=${DB_HOST}" \
    --from-literal="DB_NAME=${DB_NAME}" \
    --from-literal="DB_PASSWORD=${DB_PASSWORD}" \
    --from-literal="DB_USER=${DB_USER}" \
    --from-literal="SECRET_KEY=${SECRET_KEY}" \

# Replacing docker tag
sed -i "s;<DOCKER_TAG>;${DOCKER_TAG};g" .k8s/cookbook/base/deployment.yml
sed -i "s;<DOCKER_TAG>;${DOCKER_TAG};g" .k8s/consumer/base/deployment.yml

kubectl apply -k ".k8s/cookbook/overlays/${CI_ENVIRONMENT_SLUG}"
kubectl apply -k ".k8s/consumer/overlays/${CI_ENVIRONMENT_SLUG}"

echo "Waiting deployment to rollout"
kubectl -n "${CI_ENVIRONMENT_SLUG}" rollout status --timeout=$TIMEOUT deploy/cookbook
kubectl -n "${CI_ENVIRONMENT_SLUG}" rollout status --timeout=$TIMEOUT deploy/cookbook-consumer
