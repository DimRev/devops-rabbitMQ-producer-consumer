pipeline {
    agent any

    stages {
        stage('Deploy Consumer') {
            steps {
                script {
                    // 1. Query Docker Hub for the latest version (ignoring the 'latest' tag)
                    def latestVersion = sh(script: '''
                        curl -s "https://hub.docker.com/v2/repositories/dimrev/devops-pjct-consumer/tags?page_size=100" | \
                        jq -r '.results[].name' | grep -E '^v[0-9]+\\.[0-9]+\\.[0-9]+$' | sort -V | tail -n 1
                    ''', returnStdout: true).trim()
                    echo "Latest Docker Hub version: ${latestVersion}"

                    // 2. Change into the helm consumer directory
                    dir('helm-consumer-application') {
                        // Read the current tag value from values.yaml (assumes a line like "tag: v0.0.3")
                        def currentTag = sh(script: "grep 'tag:' values.yaml | awk '{print \$2}'", returnStdout: true).trim()
                        echo "Current tag in values.yaml: ${currentTag}"

                        // 3. Compare and update files if needed
                        if (currentTag == latestVersion) {
                            echo "No update needed. The tag is already ${latestVersion}."
                        } else {
                            echo "Updating tag from ${currentTag} to ${latestVersion}..."
                            // Update values.yaml tag
                            sh "sed -i 's/tag: .*/tag: ${latestVersion}/' values.yaml"

                            // Remove the 'v' prefix for Chart.yaml appVersion (e.g. v0.0.4 -> 0.0.4)
                            def newAppVersion = latestVersion.replaceFirst(/^v/, '')
                            sh "sed -i 's/appVersion: .*/appVersion: \"${newAppVersion}\"/' Chart.yaml"

                            echo "Updated values.yaml and Chart.yaml with new version ${latestVersion} (${newAppVersion})."
                        }
                    }

                    // 4. Run Helm upgrade
                    sh "helm upgrade rabbitmq-consumer ./helm-consumer-application"
                }
            }
        }
    }
}
