//  store 'servicename': 'latest ami is present or not'
def serviceAmiIdChanged = [: ]
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
    stage('check the ami version') {
      agent {label "${AWS_AGENT_LABEL}"}
      steps {

        script {

          def result = sh(returnStdout: true, script: 'python3 check_ami_version.py')
          println(result);

          for (String jobStatus: result.split(',')) {

            String[] eachjobStatus = jobStatus.split(':');

            if (eachjobStatus.size() > 1) {

              serviceAmiIdChanged[eachjobStatus[0]] = eachjobStatus[1];
            }

          }
        }
      }
    }
    // create the jobs dynamically
    stage('build the QA-service-01') {

      steps {
        sh "aws configure list"

        

      }
    }

    stage('build the QA-service-02') {
      steps {
        echo "hello world"
        

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
