@Library("jenkins_library@master") 
import com.infolytx.*

pipeline {
    agent {
        label 'docker'
    }

    environment {
        SLACK_CHANNEL = "avicenna-alerts"
        REPO_SLUG = "avc_hcc_backend"
        AWS_PROFILE = "awsTestAccount"
    }

    parameters {
        choice (
            choices: ['dev', 'test'], 
            description: 'Select Deployment Environment', 
            name: 'DEPLOY_TO'
        )
    }

    stages {
        stage('Slack Notification') {
           steps {
                script {
                    slackUtils.notifyStart()
                    slackUtils.slackNotify("${env.SLACK_CHANNEL}", "Build Started For ${DEPLOY_TO} Environment")
                }
            }
        }

        stage('Git Clone') {
            steps {
                script {
                    gitUtils.gitClone("git@bitbucket.org:infolytxinc/${env.REPO_SLUG}.git" , "dev")
                }
            }
        }

        stage("CI") {
            steps {
                script {
                    bitbucketUtils.checkLastBuildPassed("${env.REPO_SLUG}")
                }
            }
        }

        stage('Docker image Build') {
            steps { 
            	sh """
            		docker build -t avicenna_hcc_backend_"$DEPLOY_TO":latest .
            	"""
            }
        }

        stage("Pushing Docker Image to ECR") {
            steps {
                script {
                    LOGIN = sh(returnStdout: true, script: "aws --profile ${AWS_PROFILE} ecr get-login --no-include-email --region us-west-2").trim()
                    sh "${LOGIN}"
                    sh "docker tag avicenna_hcc_backend_${DEPLOY_TO}:latest 145587374684.dkr.ecr.us-west-2.amazonaws.com/avicenna_hcc_backend_${DEPLOY_TO}:latest"
                    sh "docker push 145587374684.dkr.ecr.us-west-2.amazonaws.com/avicenna_hcc_backend_${DEPLOY_TO}:latest"
                }
            }
        }

        stage('Docker container creation') {
            steps { 
            	script {        
                	echo "Running Docker Container for $DEPLOY_TO "
                	if (DEPLOY_TO == "dev"){
                		port=9000
                	}
                	else if (DEPLOY_TO == "test"){
                		port=9555
                	}
                }
                sh """
            		if [ ! -z  "\$(docker ps -a -q -f name=avicenna_hcc_backend_"$DEPLOY_TO")" ];then
            		  echo "Found running container"
            		  docker container stop avicenna_hcc_backend_"$DEPLOY_TO"
            		  docker container rm avicenna_hcc_backend_"$DEPLOY_TO"
            		  docker run -d --name avicenna_hcc_backend_"$DEPLOY_TO" --restart always -p $port:8080 avicenna_hcc_backend_"$DEPLOY_TO":latest
            		else
            		  docker run -d --name avicenna_hcc_backend_"$DEPLOY_TO" --restart always -p $port:8080 avicenna_hcc_backend_"$DEPLOY_TO":latest
            		fi
            	"""
            }
        }
    }

    post {
        success {
            script {
                slackUtils.notifySuccess()
            }
        }
        failure {
            script {
                slackUtils.notifyFailure([
                        email: "project-avicenna@infolytx.com"
                ])
            }
        }
        aborted {
            script {
                slackUtils.notifyAbort()
            }
        }
    }	
}