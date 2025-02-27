pipeline {
    agent any

    stages {
        stage('Checkout') {
      steps {
        // Clone the repository using the job's configured SCM
        checkout scm
      }
        }
        stage('Build Docker Image') {
      steps {
        // Change directory to the consumer folder and build the image
        dir('devops-pjct-producer-consumer/consumer') {
          sh '''
                        VERSION=$(cat version)
                        echo "Building docker image version $VERSION..."
                        docker build . \
                          -t dimrev/devops-pjct-consumer:$VERSION \
                          -t dimrev/devops-pjct-consumer:latest
                    '''
        }
      }
        }
        stage('Push Docker Image') {
      steps {
        // Use Docker Hub credentials and perform login before pushing
        withCredentials([usernamePassword(credentialsId: 'dockerhub-user', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
          dir('devops-pjct-producer-consumer/consumer') {
            sh '''
              VERSION=$(cat version)
              echo "Logging into Docker Hub..."
              docker login -u "$DOCKER_HUB_USER" -p "$DOCKER_HUB_PASSWORD"
              echo "Pushing docker image version $VERSION..."
              docker push dimrev/devops-pjct-consumer:$VERSION
              docker push dimrev/devops-pjct-consumer:latest
          '''
          }
        }
      }
        }
    }
}
