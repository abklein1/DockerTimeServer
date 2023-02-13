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
                sh 'git config --global user.name "jenkins"'
                sh 'git config --global user.email ""'
                sh 'git commit -am "Jenkins pushing jar to remote"'
                sh 'git push origin main'
            }
        }
    }
}
