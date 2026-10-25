pipeline {
    agent any

    stages {
        stage('Code') {
            steps {
                git url: "https://github.com/Shivani11225/Docker-feedback-form.git"
            }
        }
        stage('Build') {
            steps {
                sh "docker build -t my-app ."
            }
        }
         stage('Test') {
            steps {
                echo 'will test it!'
            }
        }
        stage('Docker push') {
            steps {
                withCredentials([usernamePassword(credentialsId:"dockerhubcred",
                passwordVariable: "dockerHubPass",
                usernameVariable: "dockerHubUser"
                )]){
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                    sh "docker image tag my-app ${env.dockerHubUser}/my-app:latest"
                    sh "docker push ${env.dockerHubUser}/my-app:latest"
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker compose up --build'
            }
        }
    }
}
