/* groovylint-disable CompileStatic, Indentation */
pipeline {
    agent any

    stages {
        stage('Checkout') {
          steps {
            checkout scm
          }
        }
        stage('Build Docker Image') {
          steps {
            dir('devops-pjct-producer-consumer/producer') {
              sh '''
VERSION=$(cat version)
echo "Building docker image version $VERSION..."
docker build . \
  -t dimrev/devops-pjct-producer:$VERSION \
  -t dimrev/devops-pjct-producer:latest
'''
            }
          }
        }
        stage('Push Docker Image') {
          steps {
            withCredentials([usernamePassword(credentialsId: 'dockerhub-user',
              usernameVariable: 'DOCKER_HUB_USER',
              passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
          dir('devops-pjct-producer-consumer/producer') {
            sh '''
VERSION=$(cat version)
echo "Logging into Docker Hub..."
docker login -u "$DOCKER_HUB_USER" -p "$DOCKER_HUB_PASSWORD"
echo "Pushing docker image version $VERSION..."
docker push dimrev/devops-pjct-producer:$VERSION
docker push dimrev/devops-pjct-producer:latest
'''
              }
            }
          }
        }
    }

    post {
        always {
          sh 'docker logout'
        }
    }
}
