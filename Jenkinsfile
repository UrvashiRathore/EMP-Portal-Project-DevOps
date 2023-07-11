def img
def username = "urvashirathoree"
def password = "sakurv3099"
pipeline {
    agent any

    environment {
        registry = "urvashirathore/emp-portal-project-devops"
        registryCredential = 'DOCKERHUB'
        githubCredential = 'Github-Creds'
        dockerImage = ''
        scannerHome = tool 'sonarqube_jenkins'
    }

    stages {
        stage('Checkout project') {
            steps {
                git branch: 'dev',
                    credentialsId: githubCredential,
                    url: 'https://github.com/UrvashiRathore/EMP-Portal-Project-DevOps.git'
            }
        }

        stage('Installing packages') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Static code analysis') {
            steps {
                script {
                    sh 'find . -name \\*.py | xargs pylint --output-format=parseable | tee pylint.log'
                    recordIssues(
                        tool: pyLint(pattern: 'pylint.log'),
                        unstableTotalHigh: 100
                    )
                }
            }
        }

       // stage('SonarQube Analysis') {
         //   steps {
           //     script {
             //       def scannerHome = tool 'sonarqube_jenkins'

               //     withSonarQubeEnv('sonarqube') {
                 //       sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=cicd_proj -Dsonar.sources=. -Dsonar.login=sqp_e36a867c5f2155d3db6cc38a06093d5f3d59b76f -X"
                   // }
                //}
            //}
        //}

       // stage('SonarQube Quality Gates') {
         //   steps {
           //     script {
             //       withSonarQubeEnv('sonarqube') {
               //         timeout(time: 1, unit: 'MINUTES') {
                 //           def qg = waitForQualityGate()
                   //         if (qg.status != 'OK') {
                     //           error "Pipeline aborted due to quality gate failure: ${qg.status}"
                       //     }
                        //}
                    //}
                //}
            //}
        //}

        stage('Clean Up') {
            steps {
                sh returnStatus: true, script: "docker stop \$(docker ps -a | grep \${JOB_NAME} | awk '{print \$1}')"
                sh returnStatus: true, script: "docker rmi \$(docker images | grep \${registry} | awk '{print \$3}') --force"
                sh returnStatus: true, script: "docker rm -f \${JOB_NAME}"
            }
        }

       // stage('Build Image') {
         //   steps {
           //     script {
             //       img = "${registry}:${env.BUILD_ID}"
               //     println("${img}")
                 //   dockerImage = docker.build(img)
                // }
            // }
        // }

        //stage('Push to DockerHub') {
          //  steps {
            //    script {
              //      docker.withRegistry('https://registry.hub.docker.com', registryCredential) {
                //        dockerImage.push()
                  //  }
                // }
            // }
        // }

        // stage('Deploy to containers') {
           // steps {
             //   sh script: "docker run -d --name \${JOB_NAME} -P 5002:5000 \${img}"
           // }
       // }
        stage('Build image') {
            steps {
                sh 'docker build -t flask-app .'
            }
        }
        stage('Push To Dockerhub') {
            steps {
             //   sh "docker tag 246638f09d31 shantanu2001/flask_application"
                sh "docker login -u ${username} -p ${password}"
                sh "docker push urvashirathoree/emp-portal-project-devops
"
            }
        }
       stage('Deploy to containers') {
            steps {
                sh "docker login -u ${username} -p ${password}"
                sh "docker run -it -p 5000:5000 -d flask-app"
            }
        }



    }

    post {
        always {
            script {
                def buildStatus = currentBuild.currentResult ?: 'UNKNOWN'
                def color = buildStatus == 'SUCCESS' ? 'good' : 'danger'

                slackSend(
                    channel: '#cicd-pipeline',
                    color: color,
                    message: "Build ${env.BUILD_NUMBER} ${build Status}: STAGE=${env.STAGE_NAME}",
                    teamDomain: 'project-d5t8181',
                    tokenCredentialId: 's8'
                )
            }
        }
    }

}
