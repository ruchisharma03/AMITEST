//  store 'region': 'latest ami is present or not'
def serviceAmiIdChanged = [: ]
String cron_string = "0 0 */20 * *" // cron every 20th of the month

pipeline {
  agent none
  parameters {

    string(name: 'AWS_AGENT_LABEL', defaultValue: 'any', description: 'Label of the Agent which has python3 and aws profile configured')
    string(name: 'AGENT_LABEL', defaultValue: 'any', description: 'Label of the Agent on which to execute the JOBS')
    string(name: 'JOBCONFIG_FILE_PATH', defaultValue: 'config/jobconfig.json', description: 'Path of the job config file')
    string(name: 'AWS_SERVICE_CONFIG_FILE', defaultValue: './config/config.json', description: 'Path of the aws service config file')
  }

  stages {
    stage('check the ami version') {
      agent any
      steps {
        sh script:"pip3 install boto3"
        script {

          def result = sh(returnStdout: true, script: 'python3 check_ami_version.py')
        }
        echo "${result}"
      }        
    }
  }

}

post {
  always {
    echo "====++++always++++===="
  }
  success {
    echo "====++++only when successful++++===="
  }
  failure {
    echo "====++++only when failed++++===="
  }
}
