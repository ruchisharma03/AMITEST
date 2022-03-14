//  store 'servicename': 'latest ami is present or not'
def isJobRunning = true;
String cron_string = "0 0 */20 * *" // cron every 20th of the month

pipeline {
  agent none
  triggers {
    cron(cron_string)
  }
  parameters {

    string(name: 'AWS_AGENT_LABEL', defaultValue: 'any', description: 'Label of the Agent which has python3 and aws profile configured')
    string(name: 'AWS_SERVICE_CONFIG_FILE', defaultValue: './config/config.json', description: 'Path of the aws service config file')
  }

  stages {
    //  check for the ami version and if the ami is different , then go to the next stage.
   
    // create the jobs dynamically
    stage('build the QA-service-01') {

      steps {


        build job: "kodak/kodak-user-test"
       
        script{
          isJobRunning = false;
        }

      }
    }

    stage('build the QA-service-02') {
      steps {

        script{

           while(!isJobRunning){

              isJobRunning = true;
              build job: "conversations-submission/content-origin-registry/10-dev-code-build"

           }
            isJobRunning = false;
        }
       

      }
    }
  }
  post {
    always {
      echo "====++++always++++===="
    }
    success {
      echo "====++++only when successful ++++===="
    }
    failure {
      echo "====++++only when failed++++===="
    }
  }

}
