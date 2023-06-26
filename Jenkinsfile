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
	    stage('Testing with pytest')
	    {
		    steps{
			    script{
				    withPythonEnv('python3')
				    {
					    sh 'pip install pytest'
					    sh 'pip install flask_sqlalchemy'
					    sh 'pytest test_app.py'
				    }
			    }
		    }
	    }
    }
}
