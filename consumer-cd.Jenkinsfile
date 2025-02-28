/* groovylint-disable CompileStatic, Indentation */
pipeline {
    agent any
    stages {
        stage('Check & Upgrade Consumer') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    script {
                        // Query Docker Hub for the latest consumer version (e.g. "v1.2.3")
                        def latestVersion = sh(script: '''
                            curl -s "https://hub.docker.com/v2/repositories/dimrev/devops-pjct-consumer/tags?page_size=100" | \
                            jq -r '.results[].name' | grep -E '^v[0-9]+\\.[0-9]+\\.[0-9]+$' | sort -V | tail -n 1
                        ''', returnStdout: true).trim()
                        echo "Latest Docker Hub Consumer Version: ${latestVersion}"

                        // Remove the leading "v"
                        def latestVersionNum = latestVersion.replaceAll(/^v/, '')

                        // Retrieve the currently deployed consumer version from helm.
                        def currentVersion = sh(script: '''
                            echo $WSL_PASS | sudo -S -u $WSL_USER helm list --filter rabbitmq-consumer | tail -n 1 | awk '{print $NF}'
                        ''', returnStdout: true).trim()
                        echo "Current Consumer Version: ${currentVersion}"

                        // Compare and upgrade if necessary.
                        if (latestVersionNum != currentVersion) {
                            echo "Upgrading Consumer to version ${latestVersionNum}"
                            sh '''
                                echo $WSL_PASS | sudo -S -u $WSL_USER helm upgrade rabbitmq-consumer ./helm-consumer-application
                            '''
                        } else {
                            echo "Consumer is up-to-date with version ${currentVersion}"
                        }
                    }
                }
            }
        }
    }
}
