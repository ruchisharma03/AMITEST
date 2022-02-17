//  store 'region': 'latest ami is present or not'
def serviceAmiIdChanged = [: ]
String cron_string = "0 0 */20 * *" // cron every 20th of the month

pipeline {
  agent none
  // triggers {
  //   cron(cron_string)
  // }
  parameters {

    string(name: 'AWS_AGENT_LABEL', defaultValue: 'any', description: 'Label of the Agent which has python3 and aws profile configured')
    string(name: 'AGENT_LABEL', defaultValue: 'any', description: 'Label of the Agent on which to execute the JOBS')
    string(name: 'JOBCONFIG_FILE_PATH', defaultValue: 'config/jobconfig.json', description: 'Path of the job config file')
    string(name: 'AWS_SERVICE_CONFIG_FILE', defaultValue: './config/config.json', description: 'Path of the aws service config file')
    string(name: 'JOB_NAMES', description: 'List of jobs separated by commas in build sequence')
  }

  stages {
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
    stage('build the QA services if the latest ami id is present') {

      agent {label "${AGENT_LABEL}"}

      steps {

        script {

          String[] jobList = params.JOB_NAMES.split(',');
          println(jobList[0])
          if (jobList.size() > 0) {

            for (String eachJob: jobList) {
              println(serviceAmiIdChanged)
              if (serviceAmiIdChanged["${eachJob}"] == 'True') {
                try {
                  stage("QA-${eachJob}") {

                    build job: "${eachJob}"
                    // emailext body: "${eachJob} succeeded", recipientProviders: [buildUser()], subject: "JOB ${eachJob} SUCCESS", to: ''

                  }
                } catch (Exception e) {

                  echo "${eachJob} failed"
                  // emailext body: "${eachJob} failed", recipientProviders: [buildUser()], subject: "JOB ${eachJob} FAILED", to: ''
                  throw e;

                }

              }

            }

          }

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
