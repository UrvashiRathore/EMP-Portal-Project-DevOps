def img

pipeline
{

    environment
    {

        registry = "UrvashiRathore/EMP-Portal-Project-DevOps"

        registryCredential = 'DOCKERHUB'

        githubCredential = 'Github-Creds'

        dockerImage = ' '
	scannerHome = tool 'sonarqube_jenkins'

        
    }

   agent any

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
	stage('Static code analysis')
	    {
		    steps{
			    script{
				    sh 'find . -name \\*.py | xargs pylint .f parseable | tee pylint.log'
				    recordIssues(
					    tool: pyLint(pattern: 'pylint.log'),
					    unstableTotalHigh: 100
					    )
			    }
		    }
	    }

 

	    stage('SonarQube Analysis') {
            steps {
		script{
                // Configure SonarQube Scanner
		def scannerHome = tool "sonarqube_jenkins";

                withSonarQubeEnv('sonarqube') {
                 
                  // sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=cicd_proj -Dsonar.sources=. -Dsonar.token=sqp_e36a867c5f2155d3db6cc38a06093d5f3d59b76f"
			sh"/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/sonarqube_jenkins/bin/sonar-scanner -Dsonar.projectKey=cicd_proj -Dsonar.sources=. -Dsonar.login=sqp_e36a867c5f2155d3db6cc38a06093d5f3d59b76f -X"

                }
		}
            }
        }
	    stage('SonarQube Quality Gates'){
	    steps {
		    script {
			    withSonarQubeEnv('sonarqube') {
				    timeout(time:1,unit: 'MINUTES') {
					    def qg = waitForQualityGate()
					    if(qg.status != 'OK') {
						error "Pipeline aborted due to quality gate failure: ${qg.status}"
					    }
				    }
			    }
		    }
	    }
    }
	   stage('Clean Up') {
    steps {
        sh returnStatus: true, script: "docker stop \$(docker ps -a | grep \${JOB_NAME} | awk '{print \$1}')"
        sh returnStatus: true, script: "docker rmi \$(docker images | grep \${registry} | awk '{print \$3}') --force"
        sh returnStatus: true, script: "docker rm -f \${JOB_NAME}"
    }
}

									 }							 
			   
	stage('Build Image') {
            steps {
                script {
                    def img = "${registry}:${env.BUILD_ID}"
                    println("${img}")
                    def dockerImage = docker.build(img)
                }
            }
        }
        stage('Push to DockerHub'){
		steps{
			script{
				docker.withREgistry('https://registry.hub.docker.coom', registryCredential) {
					dockerImage.push()
				}
			}
		}
	}
        stage('Deploy to containers'){
		steps{
			sh label: '',script: "docker run -d --name ${JOB_NAME} -P 5002:5000 ${img}"
		}
	}
}
	post{
        always{
            script{
                def buildStatus = currentBuild.currentResult ?: 'UNKNOWN'
                def color = buildStatus== 'SUCCESS' ? 'good' : 'danger'

                slackSend(
                    channel: '#cicd-pipeline',
                    color: color,
                    message: "Build ${env.BUILD_NUMBER} ${buildStatus}: STAGE=${env.STAGE_NAME}",
                    teamDomain: 'project-d5t8181',
                    tokenCredentialId: 's8'
                )
            }
        }
    }


