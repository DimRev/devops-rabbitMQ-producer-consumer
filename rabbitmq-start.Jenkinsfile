/* groovylint-disable CompileStatic, Indentation */
def podExists = false
def producerDeploymentExists = false
def consumerDeploymentExists = false

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Existing RabbitMQ Pod') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    script {
                        // Check if any pod matches the helm-rabbitmq-application- pattern
                        def cmd = "echo \$WSL_PASS | sudo -S -u \$WSL_USER kubectl get pods | grep 'helm-rabbitmq-application-'"
                        def podCheck = sh(script: cmd, returnStatus: true)
                        if (podCheck == 0) {
                            echo "Existing helm-rabbitmq-application pod found. Skipping RabbitMQ install."
                            podExists = true
                        } else {
                            echo "No existing helm-rabbitmq-application pod found."
                        }
                    }
                }
            }
        }

        stage('Install RabbitMQ') {
            when {
                expression { !podExists }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    sh '''
                      echo $WSL_PASS | sudo -S -u $WSL_USER helm install rabbitmq-app ./helm-rabbitmq-application
                    '''
                }
            }
        }

        stage('Wait for RabbitMQ Pod to be ready') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                        sh '''
                          echo "Waiting for helm-rabbitmq-application pod to be ready..."
                          until echo $WSL_PASS | sudo -S -u $WSL_USER kubectl get pods | grep -q "helm-rabbitmq-application-.*1/1"; do
                            echo "Current pod status:"
                            echo $WSL_PASS | sudo -S -u $WSL_USER kubectl get pods
                            sleep 1
                          done
                        '''
                    }
                }
            }
        }

        stage('Check Existing Producer Deployment') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    script {
                        def cmd = "echo \$WSL_PASS | sudo -S -u \$WSL_USER kubectl get deployment | grep 'helm-producer-application'"
                        def prodCheck = sh(script: cmd, returnStatus: true)
                        if (prodCheck == 0) {
                            echo "Existing helm-producer-application deployment found. Skipping Producer install."
                            producerDeploymentExists = true
                        } else {
                            echo "No existing helm-producer-application deployment found."
                        }
                    }
                }
            }
        }

        stage('Install Producer') {
            when {
                expression { !producerDeploymentExists }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    sh '''
                      echo $WSL_PASS | sudo -S -u $WSL_USER helm install rabbitmq-producer ./helm-producer-application
                    '''
                }
            }
        }

        stage('Wait for Producer Deployment to be ready') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                        sh '''
                          echo "Waiting for rabbitmq-producer deployment to have ready pods..."
                          until echo $WSL_PASS | sudo -S -u $WSL_USER kubectl get deployment | grep 'helm-producer-application' | grep -qE '[[:space:]][1-9][0-9]*/'; do
                            echo "Current deployment status:"
                            echo $WSL_PASS | sudo -S -u $WSL_USER kubectl get deployment
                            sleep 1
                          done
                        '''
                    }
                }
            }
        }

        stage('Check Existing Consumer Deployment') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    script {
                        def cmd = "echo \$WSL_PASS | sudo -S -u \$WSL_USER kubectl get deployment | grep 'helm-consumer-application-'"
                        def consCheck = sh(script: cmd, returnStatus: true)
                        if (consCheck == 0) {
                            echo "Existing helm-consumer-application deployment found. Skipping Consumer install."
                            consumerDeploymentExists = true
                        } else {
                            echo "No existing helm-consumer-application deployment found."
                        }
                    }
                }
            }
        }

        stage('Install Consumer') {
            when {
                expression { !consumerDeploymentExists }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    sh '''
                      echo $WSL_PASS | sudo -S -u $WSL_USER helm install rabbitmq-consumer ./helm-consumer-application
                    '''
                }
            }
        }

        stage('Wait for Consumer Deployment to be ready') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                        sh '''
                          echo "Waiting for rabbitmq-consumer deployment to have ready pods..."
                          until echo $WSL_PASS | sudo -S -u $WSL_USER kubectl get deployment | grep 'helm-consumer-application' | grep -qE '[[:space:]][1-9][0-9]*/'; do
                            echo "Current deployment status:"
                            echo $WSL_PASS | sudo -S -u $WSL_USER kubectl get deployment
                            sleep 1
                          done
                        '''
                    }
                }
            }
        }
    }
}
