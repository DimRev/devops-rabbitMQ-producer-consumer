/* groovylint-disable CompileStatic, Indentation */
pipeline {
    agent any
    stages {
        stage('Check & Upgrade Producer') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'wsl-user', usernameVariable: 'WSL_USER', passwordVariable: 'WSL_PASS')]) {
                    script {
                        // Query Docker Hub for the latest producer version (e.g. "v1.2.3")
                        def latestVersion = sh(script: '''
                            curl -s "https://hub.docker.com/v2/repositories/dimrev/devops-pjct-producer/tags?page_size=100" | \
                            jq -r '.results[].name' | grep -E '^v[0-9]+\\.[0-9]+\\.[0-9]+$' | sort -V | tail -n 1
                        ''', returnStdout: true).trim()
                        echo "Latest Docker Hub Producer Version: ${latestVersion}"

                        // Remove the leading "v" to get just the version number.
                        def latestVersionNum = latestVersion.replaceAll(/^v/, '')

                        // Retrieve the currently deployed producer version from helm.
                        def currentVersion = sh(script: '''
                            echo $WSL_PASS | sudo -S -u $WSL_USER helm list --filter rabbitmq-producer | tail -n 1 | awk '{print $NF}'
                        ''', returnStdout: true).trim()
                        echo "Current Producer Version: ${currentVersion}"

                        // If versions differ, run the upgrade.
                        if (latestVersionNum != currentVersion) {
                            echo "Upgrading Producer to version ${latestVersionNum}"
                            sh '''
                                echo $WSL_PASS | sudo -S -u $WSL_USER helm upgrade rabbitmq-producer ./helm-producer-application --set image.tag=${latestVersionNum}
                            '''
                        } else {
                            echo "Producer is up-to-date with version ${currentVersion}"
                        }
                    }
                }
            }
        }
    }
}
