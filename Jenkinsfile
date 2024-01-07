pipeline {
    agent any
    stages {
        stage("Clean workspace") {
            steps {
                sh "git clean -xdf"
            }
        }
        stage("Run in container") {
            agent {
                dockerfile {
                    reuseNode true
                }
            }
            environment {
                HOME = "${env.WORKSPACE}"
                USERNAME = "jenkins" // getpass.getuser() fix
            }
            stages {
                stage("Install dependencies") {
                    steps {
                        sh "python -m pip install --user .[test]"
                    }
                }
                stage("Run tests") {
                    stages {
                        stage("Run mypy") {
                            steps {
                                sh "python -m mypy it tests"
                            }
                        }
                        stage("Run pylint") {
                            steps {
                                sh "python -m pylint it tests"
                            }
                        }
                        stage("Run pytest") {
                            steps {
                                sh "python -m pytest tests"
                            }
                        }
                    }
                }
            }
        }
        stage("Build and publish") {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://releases.docker.buddaphest.se', 'nexus') {

                        def customImage = docker.build("marwinfaiter/pyplanet:rmt-${BUILD_ID}")

                        customImage.push()
                        customImage.push("rmt")
                    }
                }
            }
        }
    }
    post {
        always {
            sh "docker system prune -af"
        }
    }
}
