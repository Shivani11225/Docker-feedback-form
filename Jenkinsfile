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
                sh "docker buil -t my-app ."
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

post {
        failure {
              script{
                  emailext from: "kumarishivani00142@gmail.com",
                  to: "kumarishivani00142@gmail.com",
                  body: "Shivani your latest Build is failed",
                  subject: "Build failed"
              }
        }
    
    success{
            script{
                  emailext from: "mskrishivani11@gmail.com",
                  to: "mskrishivani11@gmail.com",
                  body: "Shivani your latest Build is success",
                  subject: "Build success"
              }
        }
        
        aborted{
            script{
                  emailext from: "mskrishivani11@gmail.com",
                  to: "mskrishivani11@gmail.com",
                  body: "Shivani, your latest Build is aborted",
                  subject: "Build aborted"
              }
        }
    }
}
