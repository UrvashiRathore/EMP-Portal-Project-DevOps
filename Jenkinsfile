def img

pipeline
{

    environment
    {

        registry = "UrvashiRathore/EMP-Portal-Project-DevOps"

        registryCredential = 'DOCKERHUB'

        githubCredential = 'Github-Creds'

        dockerImage = ' '

        
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

 
	stage('SonarQube Analysis')
{
         steps{
          script{
            withSonarQubeEnv('sonarqube'){
               
		sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=sonarqube_jenkins -Dsonar.source=."

            }
        }
    }
}
	    stage('SonarQube Quality Gates')
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

