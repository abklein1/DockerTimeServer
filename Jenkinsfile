pipeline {
    agent {
        docker {
            image 'maven:3.8.7-eclipse-temurin-17'
            args '-v /root/.m2:/root/.m2'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'cd ./TimeServer/'
                sh 'mvn -f TimeServer/pom.xml -B -DskipTests clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn -f TimeServer/pom.xml test'
            }
        }
        stage('Push to SCM') {
            steps {
                script{
                    sshagent (credentials: ['f86e8604-aebb-4564-bd96-adf56e453913']) {
                        sh '''
                            git config --global user.name "abklein1"
                            git config --global user.email "akendo21@gmail.com"
                            git commit -am "Jenkins pushing jar to remote"
                            git push origin main
                        '''
                    }

                }

            }
        }
    }
}
