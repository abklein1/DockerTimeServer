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
                    sshagent (credentials: ['df8d5eb8-247a-46f8-9145-6b7c7f7cc767']) {
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
