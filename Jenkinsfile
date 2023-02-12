pipeline {
    agent {
        docker {
            image 'maven:3.8.7-eclipse-temurin-11'
            args '-v /root/.m2:/root/.m2'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'mvn -f ./var/lib/workspace/DockerTimeServer_main/TimeServer/pom.xml -B -DskipTests clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn -f ./var/lib/workspace/DockerTimeServer_main/TimeServer/pom.xml test'
            }
        }
    }
}
